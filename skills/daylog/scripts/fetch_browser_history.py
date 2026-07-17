"""
自动从本地浏览器数据库读取历史记录，无需手动导出 CSV。

支持：Chrome, Edge, Zen Browser, Firefox
原理：直接读取 SQLite 数据库（复制到临时目录避免锁冲突）

用法：
    python fetch_browser_history.py --start 2026-07-01 --end 2026-07-17
    python fetch_browser_history.py --start 2026-07-01 --end 2026-07-17 --browsers chrome edge
    python fetch_browser_history.py --start 2026-07-01 --end 2026-07-17 --out history.json
"""

import argparse
import json
import os
import shutil
import sqlite3
import tempfile
from datetime import datetime, timezone, timedelta
from pathlib import Path

BEIJING_TZ = timezone(timedelta(hours=8))


# ── 浏览器配置 ─────────────────────────────────────────────────────────

def get_user_home():
    return Path.home()


def chrome_profiles():
    """发现 Chrome 所有 profile 的 History 数据库路径"""
    home = get_user_home()
    user_data = home / "AppData" / "Local" / "Google" / "Chrome" / "User Data"
    if not user_data.exists():
        return []
    profiles = []
    for item in user_data.iterdir():
        if item.is_dir() and (item / "History").exists():
            profiles.append(item / "History")
    return profiles


def edge_profiles():
    """发现 Edge 所有 profile 的 History 数据库路径"""
    home = get_user_home()
    user_data = home / "AppData" / "Local" / "Microsoft" / "Edge" / "User Data"
    if not user_data.exists():
        return []
    profiles = []
    for item in user_data.iterdir():
        if item.is_dir() and (item / "History").exists():
            profiles.append(item / "History")
    return profiles


def zen_profiles():
    """发现 Zen Browser 的 places.sqlite 路径"""
    home = get_user_home()
    zen_dir = home / "AppData" / "Roaming" / "zen" / "Profiles"
    if not zen_dir.exists():
        return []
    profiles = []
    for item in zen_dir.iterdir():
        if item.is_dir():
            db = item / "places.sqlite"
            if db.exists():
                profiles.append(db)
    return profiles


def firefox_profiles():
    """发现 Firefox 的 places.sqlite 路径"""
    home = get_user_home()
    ff_dir = home / "AppData" / "Roaming" / "Mozilla" / "Firefox" / "Profiles"
    if not ff_dir.exists():
        return []
    profiles = []
    for item in ff_dir.iterdir():
        if item.is_dir():
            db = item / "places.sqlite"
            if db.exists():
                profiles.append(db)
    return profiles


BROWSER_DETECTORS = {
    "chrome": chrome_profiles,
    "edge": edge_profiles,
    "zen": zen_profiles,
    "firefox": firefox_profiles,
}


# ── Chromium 时间戳转换 ────────────────────────────────────────────────
CHROMIUM_EPOCH = datetime(1601, 1, 1, tzinfo=timezone.utc)


def chromium_ts_to_datetime(ts):
    """Chromium microseconds since 1601-01-01 -> datetime"""
    if ts is None or ts == 0:
        return None
    return CHROMIUM_EPOCH + timedelta(microseconds=ts)


def unix_ts_to_datetime(ts):
    """Unix microseconds -> datetime"""
    if ts is None or ts == 0:
        return None
    return datetime(1970, 1, 1, tzinfo=timezone.utc) + timedelta(microseconds=ts)


# ── 数据库复制（避免锁冲突）────────────────────────────────────────────

def copy_db_to_temp(db_path):
    """复制数据库到临时目录，返回临时文件路径"""
    tmp = tempfile.NamedTemporaryFile(suffix=f"_{db_path.name}", delete=False)
    tmp.close()
    shutil.copy2(str(db_path), tmp.name)
    return Path(tmp.name)


# ── Chromium 系浏览器读取 ─────────────────────────────────────────────

def read_chromium_history(db_path, start_utc, end_utc):
    """读取 Chrome/Edge 的 History 数据库"""
    tmp_db = None
    try:
        tmp_db = copy_db_to_temp(db_path)
        conn = sqlite3.connect(f"file:{tmp_db}?mode=ro", uri=True)
        conn.row_factory = sqlite3.Row

        # Chromium 时间戳范围
        start_chromium = int((start_utc - CHROMIUM_EPOCH).total_seconds() * 1_000_000)
        end_chromium = int((end_utc - CHROMIUM_EPOCH).total_seconds() * 1_000_000)

        rows = conn.execute("""
            SELECT
                visits.visit_time,
                visits.visit_duration,
                urls.url,
                urls.title
            FROM visits
            INNER JOIN urls ON visits.url = urls.id
            WHERE visits.visit_time >= ? AND visits.visit_time < ?
              AND visits.visit_duration > 0
            ORDER BY visits.visit_time
        """, (start_chromium, end_chromium)).fetchall()

        conn.close()

        results = []
        for row in rows:
            ts = chromium_ts_to_datetime(row["visit_time"])
            if ts is None:
                continue
            title = row["title"] or ""
            url = row["url"] or ""
            if not url or not title:
                continue
            results.append({
                "timestamp": ts.isoformat(),
                "url": url,
                "title": title,
                "duration_seconds": (row["visit_duration"] or 0) / 1_000_000,
            })
        return results

    except Exception as e:
        return [{"error": f"Failed to read {db_path}: {e}"}]
    finally:
        if tmp_db and tmp_db.exists():
            try:
                tmp_db.unlink()
            except OSError:
                pass


# ── Firefox/Zen 读取 ──────────────────────────────────────────────────

def read_firefox_history(db_path, start_utc, end_utc):
    """读取 Firefox/Zen 的 places.sqlite"""
    tmp_db = None
    try:
        tmp_db = copy_db_to_temp(db_path)
        conn = sqlite3.connect(f"file:{tmp_db}?mode=ro", uri=True)
        conn.row_factory = sqlite3.Row

        # Firefox 时间戳是 Unix microseconds
        start_unix = int(start_utc.timestamp() * 1_000_000)
        end_unix = int(end_utc.timestamp() * 1_000_000)

        rows = conn.execute("""
            SELECT
                moz_historyvisits.visit_date,
                moz_places.url,
                moz_places.title
            FROM moz_historyvisits
            INNER JOIN moz_places ON moz_historyvisits.place_id = moz_places.id
            WHERE moz_historyvisits.visit_date >= ? AND moz_historyvisits.visit_date < ?
              AND moz_places.url LIKE 'http%'
              AND moz_places.title IS NOT NULL
            ORDER BY moz_historyvisits.visit_date
        """, (start_unix, end_unix)).fetchall()

        conn.close()

        results = []
        for row in rows:
            ts = unix_ts_to_datetime(row["visit_date"])
            if ts is None:
                continue
            title = row["title"] or ""
            url = row["url"] or ""
            if not url or not title:
                continue
            results.append({
                "timestamp": ts.isoformat(),
                "url": url,
                "title": title,
                "duration_seconds": 0,
            })
        return results

    except Exception as e:
        return [{"error": f"Failed to read {db_path}: {e}"}]
    finally:
        if tmp_db and tmp_db.exists():
            try:
                tmp_db.unlink()
            except OSError:
                pass


# ── 主逻辑 ────────────────────────────────────────────────────────────

def fetch_all(browsers=None, start_date=None, end_date=None):
    """从所有指定浏览器获取历史记录"""
    tz = BEIJING_TZ
    start = datetime.fromisoformat(start_date).replace(tzinfo=tz) if start_date else datetime.now(tz).replace(hour=0, minute=0, second=0, microsecond=0)
    end = datetime.fromisoformat(end_date).replace(tzinfo=tz) + timedelta(days=1) if end_date else start + timedelta(days=1)
    start_utc = start.astimezone(timezone.utc)
    end_utc = end.astimezone(timezone.utc)

    if browsers is None:
        browsers = ["chrome", "edge", "zen", "firefox"]

    all_records = []
    browser_stats = {}

    for browser_name in browsers:
        detector = BROWSER_DETECTORS.get(browser_name)
        if not detector:
            continue

        profiles = detector()
        browser_stats[browser_name] = {"profiles_found": len(profiles), "records": 0, "errors": []}

        for db_path in profiles:
            if browser_name in ("chrome", "edge"):
                records = read_chromium_history(db_path, start_utc, end_utc)
            else:
                records = read_firefox_history(db_path, start_utc, end_utc)

            for r in records:
                if "error" in r:
                    browser_stats[browser_name]["errors"].append(r["error"])
                else:
                    r["browser"] = browser_name
                    r["profile"] = str(db_path.parent.name)
                    all_records.append(r)
                    browser_stats[browser_name]["records"] += 1

    # 按时间排序
    all_records.sort(key=lambda x: x["timestamp"])

    return {
        "range": {
            "start": start_date or start.strftime("%Y-%m-%d"),
            "end": end_date or (end - timedelta(days=1)).strftime("%Y-%m-%d"),
            "timezone": "Asia/Shanghai",
        },
        "stats": browser_stats,
        "records": all_records,
    }


# ── CSV 兼容输出 ──────────────────────────────────────────────────────

def to_csv(data, output_path):
    """输出与 BrowserHistory.csv 兼容的格式"""
    import csv
    with open(output_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["DateTime", "NavigatedToUrl", "PageTitle", "Browser", "Profile"])
        writer.writeheader()
        for r in data["records"]:
            # 转换为北京时间字符串
            ts = datetime.fromisoformat(r["timestamp"]).astimezone(BEIJING_TZ)
            writer.writerow({
                "DateTime": ts.strftime("%Y-%m-%d %H:%M:%S"),
                "NavigatedToUrl": r["url"],
                "PageTitle": r["title"],
                "Browser": r.get("browser", ""),
                "Profile": r.get("profile", ""),
            })


def main():
    parser = argparse.ArgumentParser(description="自动从浏览器数据库读取历史记录")
    parser.add_argument("--start", "-s", required=True, help="起始日期 YYYY-MM-DD")
    parser.add_argument("--end", "-e", required=True, help="结束日期 YYYY-MM-DD")
    parser.add_argument("--browsers", "-b", nargs="+", default=["chrome", "edge", "zen", "firefox"],
                        help="要读取的浏览器（默认全部）")
    parser.add_argument("--out", "-o", default=None, help="输出 JSON 路径（默认 browser-history.json）")
    parser.add_argument("--csv", action="store_true", help="同时输出 CSV 兼容格式")
    args = parser.parse_args()

    print(f"正在扫描浏览器历史记录: {args.start} ~ {args.end}")
    print(f"目标浏览器: {', '.join(args.browsers)}")

    data = fetch_all(args.browsers, args.start, args.end)

    # 打印统计
    total = len(data["records"])
    for name, stats in data["stats"].items():
        print(f"  {name}: {stats['profiles_found']} 个 profile, {stats['records']} 条记录")
        for err in stats["errors"]:
            print(f"    ⚠ {err}")
    print(f"总计: {total} 条有效记录")

    # 输出 JSON
    out_path = args.out or "browser-history.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"JSON 输出: {out_path}")

    # 可选 CSV 输出
    if args.csv:
        csv_path = out_path.replace(".json", ".csv")
        to_csv(data, csv_path)
        print(f"CSV 输出: {csv_path}")


if __name__ == "__main__":
    main()
