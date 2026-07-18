"""
日记素材生成器

将 AI 对话记录索引 + 浏览器活动时间线合并，生成一份日记素材文档。
按日期分段，每天按时间段列出在哪个网站干了什么，详细到标题级别。

用法：
    python generate_diary_material.py --ai-log output\ai-log-index.json --history input\BrowserHistory.csv --out output --start 2026-03-10 --end 2026-03-22
"""

import json
import argparse
import os
import re
from datetime import datetime, timedelta, timezone
from urllib.parse import urlparse
from collections import defaultdict

# 复用 process_history 的逻辑
from process_history import process_history, CATEGORY_EMOJI, DOMAIN_RULES, get_default_outdir

BEIJING_TZ = timezone(timedelta(hours=8))


def format_date_nice(iso_date):
    """'2026-05-26' → '2026.5.26'"""
    parts = iso_date.split("-")
    return f"{int(parts[0])}.{int(parts[1])}.{int(parts[2])}"


# ── 域名 → 中文名映射 ────────────────────────────────────────────────
DOMAIN_CN = {}
for keyword, category, label in DOMAIN_RULES:
    if keyword not in DOMAIN_CN:
        DOMAIN_CN[keyword] = label

# 额外映射（process_history 的 DOMAIN_RULES 里没覆盖到的常见站点）
EXTRA_CN = {
    "qidian.com": "起点中文网",
    "17k.com": "17K小说网",
    "zongheng.com": "纵横中文网",
    "mail.qq.com": "QQ邮箱",
    "wx.mail.qq.com": "QQ邮箱",
    "cloud.tencent.com": "腾讯云",
    "console.cloud.tencent.com": "腾讯云控制台",
    "console.dcloud.net.cn": "DCloud控制台",
    "minimaxi.com": "MiniMax",
    "deepseek.com": "DeepSeek",
    "moonshot.cn": "Kimi",
    "openclaw.ai": "OpenClaw",
    "openclaw.org": "OpenClaw社区",
    "clawd.org.cn": "OpenClaw中文社区",
    "packyapi.com": "PackyAPI",
    "gptacg.top": "GPT ACG中转",
    "openclaudecode.cn": "OpenClaudeCode",
    "ngabbs.com": "NGA",
    "nga.178.com": "NGA",
    "xiaoheihe.cn": "小黑盒",
    "smzdm.com": "什么值得买",
    "bilibili.com": "B站",
    "youtube.com": "YouTube",
    "sspai.com": "少数派",
    "github.com": "GitHub",
    "gitlab.com": "GitLab",
    "juejin.cn": "掘金",
    "csdn.net": "CSDN",
    "zhihu.com": "知乎",
    "xiaohongshu.com": "小红书",
    "weibo.com": "微博",
    "hupu.com": "虎扑",
    "reddit.com": "Reddit",
    "twitter.com": "Twitter",
    "x.com": "Twitter",
    "notion.so": "Notion",
    "notion.site": "Notion",
    "obsidian.md": "Obsidian",
    "figma.com": "Figma",
    "canva.com": "Canva",
    "netlify.com": "Netlify",
    "vercel.com": "Vercel",
    "supabase.com": "Supabase",
    "taobao.com": "淘宝",
    "tmall.com": "天猫",
    "jd.com": "京东",
    "pinduoduo.com": "拼多多",
    "meituan.com": "美团",
    "dianping.com": "大众点评",
    "eleme.cn": "饿了么",
    "amap.com": "高德地图",
    "music.163.com": "网易云音乐",
    "spotify.com": "Spotify",
    "netflix.com": "Netflix",
    "disneyplus.com": "Disney+",
    "google.com": "Google",
    "google.cn": "Google",
    "bing.com": "Bing",
    "baidu.com": "百度",
    "qq.com": "QQ",
    "weixin.qq.com": "微信",
    "feishu.cn": "飞书",
    "larksuite.com": "飞书",
    "youdao.com": "有道",
    "iciba.com": "金山词霸",
    "icloud.com": "iCloud",
    "apple.com": "Apple",
    "microsoft.com": "微软",
    "live.com": "微软",
    "office.com": "Office",
    "1password.com": "1Password",
    "bitwarden.com": "Bitwarden",
    "dashlane.com": "Dashlane",
    "todoist.com": "Todoist",
    "trello.com": "Trello",
    "excalidraw.com": "Excalidraw",
    "mi.com": "小米",
    "miui.com": "MIUI",
    "v2ex.com": "V2EX",
    "hostloc.com": "主机巢",
    "digitalocean.com": "DigitalOcean",
    "aws.amazon.com": "AWS",
    "console.aws.amazon.com": "AWS控制台",
    "anthropic.com": "Anthropic",
    "openai.com": "OpenAI",
    "coze.cn": "Coze",
    "coze.com": "Coze",
    "doubao.com": "豆包",
    "tongyi.com": "通义",
    "tongyi.aliyun.com": "通义千问",
    "bigmodel.cn": "智谱",
    "chatglm.cn": "ChatGLM",
    "360.com": "360",
    "sogo.com": "搜狗",
    "samsung.com": "三星",
    "huawei.com": "华为",
    "vivo.com": "vivo",
    "oppo.com": "OPPO",
    "oneplus.com": "一加",
    "sony.com": "索尼",
    "xiaomiyoupin.com": "小米有品",
    "deeptoai.com": "DeepToAI博客",
    "blog.sagecola.top": "Sage's Echoes",
    "sagecola.top": "Sage's Echoes",
    "unifyllm.com": "UnifyLLM",
    "helpaio.com": "HelpAIO",
    "pypi.org": "PyPI",
    "pypi.python.org": "PyPI",
    "python.org": "Python",
    "js.org": "JS.org",
    "npmjs.com": "npm",
    "npmjs.org": "npm",
    "crates.io": "Crates.io",
    "puppeteer.github.io": "Puppeteer",
    "playwright.dev": "Playwright",
    "developer.mozilla.org": "MDN",
    "w3schools.com": "W3Schools",
    "stackblitz.com": "StackBlitz",
    "codepen.io": "CodePen",
    "codesandbox.io": "CodeSandbox",
    "replit.com": "Replit",
    "glitch.com": "Glitch",
    "itch.io": "itch.io",
    "store.steampowered.com": "Steam",
    "steampowered.com": "Steam",
    "epicgames.com": "Epic Games",
    "gog.com": "GOG",
    "zhihu.com": "知乎",
    "douyin.com": "抖音",
    "ixigua.com": "西瓜视频",
    "toutiao.com": "今日头条",
    "sohu.com": "搜狐",
    "163.com": "网易",
    "sina.com": "新浪",
    "ifeng.com": "凤凰网",
    "caixin.com": "财新",
    "thepaper.cn": "澎湃",
    "36kr.com": "36氪",
    "techcrunch.com": "TechCrunch",
    "theverge.com": "The Verge",
    "arstechnica.com": "Ars Technica",
    "hackernews.com": "Hacker News",
    "news.ycombinator.com": "Hacker News",
    "producthunt.com": "Product Hunt",
    "auxtool.cn": "个税计算器",
    "unicef.cn": "联合国儿童基金会",
    "cgp.unicef.cn": "联合国儿童基金会",
    "openclaw.org": "OpenClaw社区",
    "clawd.org.cn": "OpenClaw中文社区",
    "unifyllm.com": "UnifyLLM",
    "douyin.com": "抖音",
    "ixigua.com": "西瓜视频",
    "acfun.cn": "AcFun",
    "huya.com": "虎牙",
    "douyu.com": "斗鱼",
    "twitch.tv": "Twitch",
    "niconico.com": "Niconico",
    "iqiyi.com": "爱奇艺",
    "youku.com": "优酷",
    "v.qq.com": "腾讯视频",
    "mgtv.com": "芒果TV",
    "play.google.com": "Google Play",
    "apps.apple.com": "App Store",
    "nintendo.com": "Nintendo",
    "playstation.com": "PlayStation",
    "xbox.com": "Xbox",
    "ea.com": "EA",
    "ubisoft.com": "育碧",
    "blizzard.com": "暴雪",
    "riotgames.com": "Riot Games",
    "supercell.com": "Supercell",
    "miHoYo.com": "米哈游",
    "hoYoverse.com": "HoYoverse",
}


def get_site_name(url):
    """从 URL 提取站点中文名"""
    try:
        parsed = urlparse(url)
        host = parsed.hostname or ""
    except Exception:
        return "其他"

    # IP 地址特殊处理
    if re.match(r"^\d+\.\d+\.\d+\.\d+$", host):
        # 常见 IP 映射（可根据实际情况扩展）
        IP_CN = {
            "183.129.251.138": "飞书协作空间",
        }
        if host in IP_CN:
            return IP_CN[host]
        return f"IP:{host}"

    # 本地服务
    if host in ("127.0.0.1", "localhost"):
        path = parsed.path or ""
        if "feishu" in path or "lark" in path:
            return "飞书协作空间"
        return f"本地服务:{host}"

    # 按长度降序匹配，优先匹配更具体的域名
    for keyword in sorted(DOMAIN_CN.keys(), key=len, reverse=True):
        if keyword in host:
            return DOMAIN_CN[keyword]

    for keyword in sorted(EXTRA_CN.keys(), key=len, reverse=True):
        if keyword in host:
            return EXTRA_CN[keyword]

    # 返回主域名
    parts = host.split(".")
    if len(parts) >= 2:
        return parts[-2]  # github.com → github
    return host or "其他"


def clean_url(url):
    """清理 URL：去掉追踪参数"""
    url = re.sub(r"[?&](spm_id_from|trackid|from|is_video|vd_source|ref)=[^&]*", "", url)
    url = re.sub(r"\?$", "", url)
    return url


def parse_time(t):
    """解析 HH:MM 字符串为分钟数"""
    try:
        h, m = t.split(":")
        return int(h) * 60 + int(m)
    except (ValueError, AttributeError):
        return -1


def load_ai_log_index(path):
    """读取 ai-log-index.json"""
    if not path or not os.path.exists(path):
        return {}

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    daily = defaultdict(list)
    if "sessions" in data:
        for s in data["sessions"]:
            date = s.get("date", "")
            daily[date].append(s)
    elif isinstance(data, dict):
        for date_key, entries in data.items():
            if isinstance(entries, list):
                daily[date_key] = entries
            elif isinstance(entries, dict):
                daily[date_key] = [entries]
    return dict(daily)


# ── 核心：按域名分组 ──────────────────────────────────────────────────
def group_by_site(history_records, ai_records):
    """
    将浏览记录按站点分组，每组内记录不同页面标题。
    AI 记录穿插在对应时间点。
    返回: [ { type, site, start, end, entries: [title, ...], count }, ... ]
    """
    items = []

    # 浏览器记录 → 按站点聚合
    if history_records:
        for rec in history_records:
            time_str = rec["datetime"].strftime("%H:%M")
            site = get_site_name(rec["url"])
            items.append({
                "type": "browser",
                "site": site,
                "time": time_str,
                "title": rec["title"],
                "category": rec["category"],
                "search_query": rec.get("search_query", ""),
            })

    # AI 记录
    if ai_records:
        for rec in ai_records:
            tool = rec.get("tool", "AI")
            first_time = rec.get("first_time", "")
            summary = rec.get("summary", rec.get("summary_lines", ""))
            if isinstance(summary, list):
                summary = "\n".join(summary)
            items.append({
                "type": "ai",
                "site": f"{tool}",
                "time": first_time,
                "title": summary[:200] if summary else f"{tool} 对话",
                "category": "ai",
                "search_query": "",
            })

    # 按时间排序
    items.sort(key=lambda x: x["time"])

    # 合并同一站点的连续记录（间隔 ≤ 8 分钟）
    blocks = []
    current = None

    for item in items:
        is_new_block = True
        if current:
            same_site = (current["site"] == item["site"])
            t1 = parse_time(current["end"])
            t2 = parse_time(item["time"])
            time_close = (t1 >= 0 and t2 >= 0 and (t2 - t1) <= 8)

            if same_site and time_close:
                is_new_block = False

        if is_new_block:
            if current:
                blocks.append(current)
            current = {
                "type": item["type"],
                "site": item["site"],
                "start": item["time"],
                "end": item["time"],
                "entries": [],
                "count": 0,
            }

        current["end"] = item["time"]
        current["count"] += 1

        # 收集有信息量的标题
        title = item["title"]
        if item["search_query"]:
            title = f"搜索「{item['search_query']}」→ {title}"

        # 去重：标题前20字相同的只保留一条
        title_key = title[:20]
        if not any(title_key == e[:20] for e in current["entries"]):
            if len(current["entries"]) < 8:
                current["entries"].append(title)

    if current:
        blocks.append(current)

    return blocks


# ── 输出格式 ──────────────────────────────────────────────────────────
def block_to_text(block, indent=""):
    """将活动块转为可读文本"""
    time_range = block["start"] if block["start"] == block["end"] else f"{block['start']}–{block['end']}"
    site = block["site"]
    entries = block["entries"]
    count = block["count"]

    lines = []
    lines.append(f"**{time_range} | {site}**")

    if block["type"] == "ai":
        # AI 记录：直接展示摘要
        for entry in entries[:2]:
            lines.append(f"  {entry}")
    else:
        # 浏览器记录：列出标题
        if count <= 3 and len(entries) <= 3:
            # 少量记录，逐条列出
            for entry in entries:
                lines.append(f"  - {entry}")
        else:
            # 多条记录，列出标题 + 总数
            for entry in entries[:5]:
                lines.append(f"  - {entry}")
            if count > len(entries):
                lines.append(f"  … 共 {count} 条浏览记录")

    return "\n".join(lines)


def generate_day(date, history_records, ai_records):
    """生成一天的日记素材"""
    blocks = group_by_site(history_records, ai_records)

    lines = []
    lines.append(f"## {format_date_nice(date)}\n")

    if not blocks:
        lines.append("（无数据）\n")
        return "\n".join(lines)

    current_hour = None
    for block in blocks:
        hour = block["start"][:2] + ":00" if block["start"] else "??:00"
        if hour != current_hour:
            current_hour = hour
            lines.append(f"### {hour}")

        lines.append(block_to_text(block))
        lines.append("")

    return "\n".join(lines)


def generate_batch(daily_ai, daily_history, start_date, end_date):
    """批量生成"""
    all_dates = set(daily_ai.keys()) | set(daily_history.keys())
    if start_date:
        all_dates = {d for d in all_dates if d >= start_date}
    if end_date:
        all_dates = {d for d in all_dates if d <= end_date}

    if not all_dates:
        return "# 没有找到任何数据\n", []

    sorted_dates = sorted(all_dates)
    parts = []
    summary = []

    for date in sorted_dates:
        ai = daily_ai.get(date)
        hist = daily_history.get(date)
        day_text = generate_day(date, hist, ai)
        parts.append(day_text)
        summary.append({
            "date": date,
            "ai_count": len(ai) if ai else 0,
            "browser_count": len(hist) if hist else 0,
        })

    return "\n---\n\n".join(parts), summary


def main():
    parser = argparse.ArgumentParser(description="日记素材生成器")
    parser.add_argument("--ai-log", help="ai-log-index.json 路径（可选）")
    parser.add_argument("--history", "-i", required=True, help="BrowserHistory.csv 路径")
    parser.add_argument("--out", "-o", default=None, help="输出目录（默认：当前工作目录）")
    parser.add_argument("--start", "-s", help="起始日期 YYYY-MM-DD")
    parser.add_argument("--end", "-e", help="结束日期 YYYY-MM-DD")
    args = parser.parse_args()

    if args.out is None:
        args.out = get_default_outdir()
    os.makedirs(args.out, exist_ok=True)

    # 1. 处理浏览器历史
    print("处理浏览器历史...")
    daily_history, hist_stats = process_history(args.history, args.start, args.end)
    print(f"  浏览器记录: {hist_stats['kept']} 条（过滤 {hist_stats['filtered']} 条噪音）")

    # 2. 加载 AI 对话记录
    daily_ai = load_ai_log_index(args.ai_log) if args.ai_log else {}
    if daily_ai:
        print(f"  AI 对话记录: {len(daily_ai)} 天")
    else:
        print("  AI 对话记录: 无（仅使用浏览器数据）")

    # 3. 生成素材稿
    print("生成日记素材...")
    material, summary = generate_batch(daily_ai, daily_history, args.start, args.end)

    output_path = os.path.join(args.out, "diary_material.md")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(material)

    total_ai = sum(s["ai_count"] for s in summary)
    total_browser = sum(s["browser_count"] for s in summary)
    print(f"\n生成完成:")
    print(f"  覆盖天数: {len(summary)}")
    print(f"  AI 线索: {total_ai} 条")
    print(f"  浏览器线索: {total_browser} 条")
    print(f"  输出文件: {output_path}")


if __name__ == "__main__":
    main()
