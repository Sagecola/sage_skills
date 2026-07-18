"""
浏览器历史记录清洗+分类脚本

读取浏览器历史记录（CSV 或 fetch_browser_history.py 生成的 JSON），按天生成干净的活动时间线。
输出：每天一个 Markdown 文件，按域名归类，过滤噪音。

用法：
    # 从 CSV 读取（旧方式）
    python process_history.py --input History/BrowserHistory.csv --out output

    # 从 JSON 读取（新方式，配合 fetch_browser_history.py）
    python process_history.py --input browser-history.json --out output

    # 自动获取 + 处理（一步到位）
    python process_history.py --auto --start 2026-07-01 --end 2026-07-17 --out output
"""

import csv
import argparse
import json
import os
import re
from datetime import datetime, timezone, timedelta
from collections import defaultdict
from urllib.parse import urlparse, parse_qs, unquote
from pathlib import Path


# ── 数据源读取 ─────────────────────────────────────────────────────────

def read_csv_history(input_file):
    """读取 BrowserHistory.csv，返回统一格式记录列表"""
    records = []
    with open(input_file, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # 跳过重复表头行
            if "DateTime" in row.get("NavigatedToUrl", ""):
                continue
            records.append({
                "timestamp": row["DateTime"],
                "url": row.get("NavigatedToUrl", ""),
                "title": row.get("PageTitle", ""),
                "browser": row.get("Browser", ""),
            })
    return records


def read_json_history(input_file):
    """读取 fetch_browser_history.py 生成的 JSON，返回统一格式记录列表"""
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    records = []
    for r in data.get("records", []):
        if "error" in r:
            continue
        records.append({
            "timestamp": r["timestamp"],
            "url": r.get("url", ""),
            "title": r.get("title", ""),
            "browser": r.get("browser", ""),
        })
    return records


def auto_fetch_history(start_date, end_date):
    """自动调用 fetch_browser_history.py 获取浏览器历史"""
    script_dir = Path(__file__).parent
    fetch_script = script_dir / "fetch_browser_history.py"
    if not fetch_script.exists():
        print(f"⚠ 找不到 fetch_browser_history.py，跳过自动获取")
        return []

    import subprocess
    import tempfile
    tmp_json = Path(tempfile.mktemp(suffix=".json"))
    try:
        cmd = [
            "python", str(fetch_script),
            "--start", start_date,
            "--end", end_date,
            "--out", str(tmp_json),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode != 0:
            print(f"⚠ fetch_browser_history.py 执行失败: {result.stderr}")
            return []
        if result.stdout:
            print(result.stdout)
        return read_json_history(str(tmp_json))
    except Exception as e:
        print(f"⚠ 自动获取浏览器历史失败: {e}")
        return []
    finally:
        if tmp_json.exists():
            tmp_json.unlink()

# ── 时区 ────────────────────────────────────────────────────────────
BEIJING_TZ = timezone(timedelta(hours=8))


# ── 域名分类规则 ─────────────────────────────────────────────────────
# 格式: (关键词/域名片段, 类别, 中文标签)
DOMAIN_RULES = [
    # 视频
    ("bilibili.com",         "video",    "B站"),
    ("youtube.com",          "video",    "YouTube"),
    ("youtube-nocookie.com", "video",    "YouTube"),
    ("nicovideo.jp",         "video",    "N站"),
    ("v.qq.com",             "video",    "腾讯视频"),
    ("youku.com",            "video",    "优酷"),
    ("iqiyi.com",            "video",    "爱奇艺"),
    ("disneyplus.com",       "video",    "Disney+"),
    ("netflix.com",          "video",    "Netflix"),

    # 社交/论坛
    ("xiaohongshu.com",      "social",   "小红书"),
    ("twitter.com",          "social",   "Twitter/X"),
    ("x.com",                "social",   "Twitter/X"),
    ("weibo.com",            "social",   "微博"),
    ("instagram.com",        "social",   "Instagram"),
    ("reddit.com",           "social",   "Reddit"),
    ("hupu.com",             "social",   "虎扑"),
    ("tieba.baidu.com",      "social",   "贴吧"),
    ("zhihu.com",            "social",   "知乎"),

    # 购物
    ("taobao.com",           "shopping", "淘宝"),
    ("tmall.com",            "shopping", "天猫"),
    ("jd.com",               "shopping", "京东"),
    ("pinduoduo.com",        "shopping", "拼多多"),
    ("amazon.com",           "shopping", "亚马逊"),
    ("suning.com",           "shopping", "苏宁"),

    # 阅读/知识
    ("sspai.com",            "reading",  "少数派"),
    ("wikipedia.org",        "reading",  "维基百科"),
    ("medium.com",           "reading",  "Medium"),
    ("juejin.cn",            "reading",  "掘金"),
    ("csdn.net",             "reading",  "CSDN"),
    ("segmentfault.com",     "reading",  "SegmentFault"),
    ("notion.site",          "reading",  "Notion"),
    ("notion.so",            "reading",  "Notion"),

    # AI/开发工具
    ("github.com",           "dev",      "GitHub"),
    ("gitlab.com",           "dev",      "GitLab"),
    ("stackoverflow.com",    "dev",      "StackOverflow"),
    ("anthropic.com",        "ai",       "Anthropic"),
    ("claude.ai",            "ai",       "Claude"),
    ("chat.openai.com",      "ai",       "ChatGPT"),
    ("chatgpt.com",          "ai",       "ChatGPT"),
    ("gemini.google.com",    "ai",       "Gemini"),
    ("bigmodel.cn",          "ai",       "智谱"),
    ("kimi.moonshot.cn",     "ai",       "Kimi"),
    ("cursor.com",           "ai",       "Cursor"),
    ("cherry-ai.com",        "ai",       "Cherry Studio"),
    ("openai.com",           "ai",       "OpenAI"),

    # 音乐
    ("music.163.com",        "music",    "网易云音乐"),
    ("spotify.com",          "music",    "Spotify"),
    ("music.apple.com",      "music",    "Apple Music"),

    # 地图/出行
    ("amap.com",             "map",      "高德地图"),
    ("maps.google.com",      "map",      "Google Maps"),
    ("dianping.com",         "food",     "大众点评"),
    ("meituan.com",          "food",     "美团"),
    ("eleme.cn",             "food",     "饿了么"),

    # 工具/效率
    ("notion.so",            "tool",     "Notion"),
    ("figma.com",            "tool",     "Figma"),
    ("canva.com",            "tool",     "Canva"),
    ("excalidraw.com",       "tool",     "Excalidraw"),
    ("trello.com",           "tool",     "Trello"),
]


# ── 噪音过滤 ─────────────────────────────────────────────────────────
NOISE_PATTERNS = [
    # 搜索引擎的中间跳转页
    r"google\.com/search\?",
    r"bing\.com/search\?",
    r"baidu\.com/s\?",
    r"google\.cn/search\?",
    # Chrome 内部页面
    r"^chrome://",
    r"^chrome-extension://",
    r"^edge://",
    r"^about:",
    # favicon / 图标请求
    r"/favicon\.",
    r"/favicon.ico",
    # 本地文件认证回调
    r"127\.0\.0\.1.*code=",
    r"localhost.*code=",
    # Bitwarden / 密码管理器弹窗
    r"bitwarden.*popup",
]

NOISE_URL_RE = re.compile("|".join(NOISE_PATTERNS), re.IGNORECASE)

# PageTitle 中的噪音关键词
NOISE_TITLE_KEYWORDS = ["搜索", "Search", "Sign in", "登录", "Authentication"]


# ── 解析与清洗 ────────────────────────────────────────────────────────
def parse_utc_to_beijing(dt_str):
    dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
    return dt.astimezone(BEIJING_TZ)


def classify_domain(url):
    """根据 URL 返回 (类别, 中文标签)，未知返回 (other, 域名)"""
    try:
        parsed = urlparse(url)
        host = parsed.hostname or ""
    except Exception:
        return "other", "其他"

    for keyword, category, label in DOMAIN_RULES:
        if keyword in host:
            return category, label
    return "other", host


def extract_search_query(url):
    """从搜索引擎 URL 中提取搜索词"""
    try:
        parsed = urlparse(url)
        host = parsed.hostname or ""
        params = parse_qs(parsed.query)

        if "bing.com" in host or "google.com" in host or "google.cn" in host:
            return params.get("q", params.get("query", [""]))[0]
        elif "baidu.com" in host:
            return params.get("wd", [""])[0]
    except Exception:
        pass
    return ""


def extract_bilibili_title(title):
    """清理 B站标题：去掉后缀"""
    title = re.sub(r"_哔哩哔哩_bilibili$", "", title)
    title = re.sub(r"- bilibili$", "", title)
    return title.strip()


def is_noise(url, title):
    """判断是否为噪音记录"""
    if NOISE_URL_RE.search(url):
        return True
    # 空标题
    if not title or not title.strip():
        return True
    # 如果标题全是搜索关键词拼接，也算噪音
    if any(kw in title for kw in NOISE_TITLE_KEYWORDS):
        # 但如果 URL 不是搜索页，就保留（比如 "登录 - GitHub"）
        if any(engine in url for engine in ["/search?", "/s?"]):
            return True
    # 文件协议的本地文件
    if url.startswith("file://"):
        return True
    return False


def clean_url(url):
    """清理 URL：去掉追踪参数等"""
    # 去掉 bilibili 的追踪参数
    url = re.sub(r"[?&](spm_id_from|trackid|from|is_video|vd_source)=[^&]*", "", url)
    url = re.sub(r"\?$", "", url)
    return url


def clean_title(title, category):
    """清理页面标题"""
    title = title.strip()
    if category == "video":
        title = extract_bilibili_title(title)
    # 截断过长标题
    if len(title) > 60:
        title = title[:57] + "..."
    return title


def is_generic_title(title):
    """判断标题是否过于笼统（无法传达有效信息）"""
    # 单个英文单词、纯站名等
    generic_patterns = [
        r"^Happy$",           # 博客标题只有"Happy"
        r"^GitHub$",
        r"^General$",
        r"^Pages$",
        r"^Your profile$",
        r"^Your Repositories$",
        r"^Workflows?$",
        r"^Settings$",
        r"^Notifications$",
        r"^Collaborative space$",  # 飞书协作空间
    ]
    return any(re.match(p, title, re.IGNORECASE) for p in generic_patterns)


# ── 主逻辑 ────────────────────────────────────────────────────────────
def process_history(input_file=None, start_date=None, end_date=None, records=None):
    """
    读取浏览器历史（CSV/JSON/自动获取），返回按天分组的清洗后记录。
    结果: { "2026-03-10": [ {datetime, url, title, category, label, search_query, cleaned_url}, ... ] }
    """
    # 读取数据源
    if records is None:
        if input_file is None:
            raise ValueError("必须指定 --input 或 --auto")
        ext = Path(input_file).suffix.lower()
        if ext == ".json":
            records = read_json_history(input_file)
        else:
            records = read_csv_history(input_file)

    daily = defaultdict(list)
    stats = {"total": len(records), "filtered": 0, "kept": 0}

    for row in records:
        dt_str = row["timestamp"]
        url = row.get("url", "")
        title = row.get("title", "")

        dt_beijing = parse_utc_to_beijing(dt_str)
        date_key = dt_beijing.strftime("%Y-%m-%d")

        # 日期过滤
        if start_date and date_key < start_date:
            continue
        if end_date and date_key > end_date:
            continue

        # 噪音过滤
        if is_noise(url, title):
            stats["filtered"] += 1
            continue

        # 分类
        category, label = classify_domain(url)

        # 提取搜索词
        search_query = extract_search_query(url) if category == "other" else ""

        # 清理
        cleaned_url = clean_url(url)
        cleaned_title = clean_title(title, category)

        daily[date_key].append({
            "datetime": dt_beijing,
            "url": cleaned_url,
            "title": cleaned_title,
            "category": category,
            "label": label,
            "search_query": search_query,
            "original_url": url,
        })
        stats["kept"] += 1

    # 每天内部按时间排序
    for date in daily:
        daily[date].sort(key=lambda x: x["datetime"])

        # 去重 + 过滤
        deduped = []
        last_key = None
        for r in daily[date]:
            # 过滤过于笼统的标题
            if is_generic_title(r["title"]):
                continue
            # 去重键：分钟 + 标题前30字
            minute = r["datetime"].strftime("%Y-%m-%d %H:%M")
            title_prefix = r["title"][:30]
            key = (minute, title_prefix)
            if key != last_key:
                deduped.append(r)
                last_key = key
        daily[date] = deduped

    return dict(daily), stats


def format_date_nice(iso_date):
    """'2026-05-26' → '2026.5.26'"""
    parts = iso_date.split("-")
    return f"{int(parts[0])}.{int(parts[1])}.{int(parts[2])}"


# ── 输出格式 ────────────────────────────────────────────────────────────
CATEGORY_ORDER = ["dev", "ai", "reading", "video", "social", "shopping", "music", "food", "map", "tool", "other"]
CATEGORY_EMOJI = {
    "dev": "💻", "ai": "🤖", "reading": "📖", "video": "🎬",
    "social": "💬", "shopping": "🛒", "music": "🎵", "food": "🍜",
    "map": "🗺️", "tool": "🔧", "other": "🌐",
}


def format_daily_markdown(date, records):
    """将一天的记录格式化为 Markdown"""
    lines = []
    lines.append(f"# 浏览活动 - {format_date_nice(date)}\n")
    lines.append(f"共 {len(records)} 条有效记录\n")

    # 按类别分组
    by_category = defaultdict(list)
    for r in records:
        by_category[r["category"]].append(r)

    for cat in CATEGORY_ORDER:
        if cat not in by_category:
            continue
        items = by_category[cat]
        emoji = CATEGORY_EMOJI.get(cat, "📌")
        lines.append(f"\n## {emoji} {items[0]['label']}类活动（{len(items)} 条）\n")

        for r in items:
            time_str = r["datetime"].strftime("%H:%M")
            title = r["title"]
            url = r["url"]

            # 搜索词特殊处理
            if r["search_query"]:
                lines.append(f"- **{time_str}** 🔍 搜索：{r['search_query']}")
            else:
                lines.append(f"- **{time_str}** {title}")

    return "\n".join(lines)


def format_compact_timeline(date, records):
    """紧凑时间线格式（适合合并到日记素材）"""
    lines = [f"## 📅 {format_date_nice(date)} 浏览器时间线\n"]

    current_hour = None
    for r in records:
        hour = r["datetime"].strftime("%H:00")
        if hour != current_hour:
            current_hour = hour
            lines.append(f"\n**{hour}**")

        time_str = r["datetime"].strftime("%H:%M")
        emoji = CATEGORY_EMOJI.get(r["category"], "📌")

        if r["search_query"]:
            lines.append(f"  {time_str} {emoji} 搜索「{r['search_query']}」")
        else:
            title = r["title"]
            lines.append(f"  {time_str} {emoji} {title}")

    return "\n".join(lines)


# ── 默认输出目录 ────────────────────────────────────────────────────────
def get_default_outdir():
    """默认输出到当前工作目录，如果没有权限则回退到桌面"""
    cwd = os.getcwd()
    test_file = os.path.join(cwd, ".write_test")
    try:
        with open(test_file, "w") as f:
            f.write("")
        os.remove(test_file)
        return cwd
    except OSError:
        return os.path.expanduser("~/Desktop")


# ── CLI ────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="浏览器历史记录清洗+分类")
    parser.add_argument("--input", "-i", default=None, help="BrowserHistory.csv 或 browser-history.json 路径")
    parser.add_argument("--auto", "-a", action="store_true", help="自动从浏览器数据库获取历史记录")
    parser.add_argument("--out", "-o", default=None, help="输出目录（默认：当前工作目录）")
    parser.add_argument("--start", "-s", help="起始日期 YYYY-MM-DD")
    parser.add_argument("--end", "-e", help="结束日期 YYYY-MM-DD")
    parser.add_argument("--format", "-f", choices=["full", "compact", "both"], default="both",
                        help="输出格式：full=完整, compact=紧凑时间线, both=两者都输出")
    args = parser.parse_args()

    if not args.input and not args.auto:
        parser.error("必须指定 --input 或 --auto")

    if args.out is None:
        args.out = get_default_outdir()
    os.makedirs(args.out, exist_ok=True)

    if args.auto:
        records = auto_fetch_history(args.start, args.end)
        daily, stats = process_history(start_date=args.start, end_date=args.end, records=records)
    else:
        daily, stats = process_history(args.input, args.start, args.end)

    print(f"总记录: {stats['total']}, 保留: {stats['kept']}, 过滤噪音: {stats['filtered']}")

    if not daily:
        print("没有找到符合条件的记录")
        return

    for date in sorted(daily.keys()):
        records = daily[date]

        if args.format in ("full", "both"):
            full_md = format_daily_markdown(date, records)
            path = os.path.join(args.out, f"history_{date}.md")
            with open(path, "w", encoding="utf-8") as f:
                f.write(full_md)

        if args.format in ("compact", "both"):
            compact_md = format_compact_timeline(date, records)
            path = os.path.join(args.out, f"timeline_{date}.md")
            with open(path, "w", encoding="utf-8") as f:
                f.write(compact_md)

        print(f"  {date}: {len(records)} 条")

    print(f"\n输出目录: {args.out}")


if __name__ == "__main__":
    main()
