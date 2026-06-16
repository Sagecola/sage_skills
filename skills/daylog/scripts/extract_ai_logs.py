import argparse
import datetime as dt
import json
import os
import sqlite3
from pathlib import Path
from zoneinfo import ZoneInfo


NOISE_MARKERS = [
    "[tool_result]",
    "<local-command-caveat>",
    "<command-name>",
    "<local-command-stdout>",
    "<environment_context>",
    "# AGENTS.md instructions",
    "<system-reminder>",
]


def parse_args():
    parser = argparse.ArgumentParser(description="Extract local AI CLI history into a portable JSON index.")
    parser.add_argument("--start", required=True, help="Start date, inclusive, in YYYY-MM-DD.")
    parser.add_argument("--end", required=True, help="End date, inclusive, in YYYY-MM-DD.")
    parser.add_argument("--timezone", default="Asia/Shanghai", help="Timezone for day grouping. Default: Asia/Shanghai.")
    parser.add_argument("--out", default="ai-log-index.json", help="Output JSON path.")
    parser.add_argument("--source-root", help="Optional copied backup root containing codex/, claude/, opencode/, kimi/.")
    parser.add_argument("--codex-sessions", help="Override Codex sessions directory.")
    parser.add_argument("--claude-projects", help="Override Claude Code projects directory.")
    parser.add_argument("--opencode-db", help="Override opencode SQLite database path.")
    parser.add_argument("--kimi-sessions", help="Override Kimi Code CLI sessions directory.")
    return parser.parse_args()


def local_day_bounds(start_text, end_text, timezone):
    tz = ZoneInfo(timezone)
    start = dt.datetime.fromisoformat(start_text).replace(tzinfo=tz)
    end = dt.datetime.fromisoformat(end_text).replace(tzinfo=tz) + dt.timedelta(days=1)
    return start.astimezone(dt.timezone.utc), end.astimezone(dt.timezone.utc), tz


def parse_time(value):
    if value is None:
        return None
    if isinstance(value, (int, float)):
        if value > 10_000_000_000:
            value = value / 1000
        return dt.datetime.fromtimestamp(value, tz=dt.timezone.utc)
    if isinstance(value, str):
        text = value.replace("Z", "+00:00")
        try:
            parsed = dt.datetime.fromisoformat(text)
            if parsed.tzinfo is None:
                parsed = parsed.replace(tzinfo=dt.timezone.utc)
            return parsed.astimezone(dt.timezone.utc)
        except ValueError:
            return None
    return None


def in_range(value, start_utc, end_utc):
    return value is not None and start_utc <= value < end_utc


def text_from_content(content):
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict):
                if "text" in item:
                    parts.append(str(item["text"]))
                elif item.get("type") == "tool_use":
                    parts.append(f"[tool_use:{item.get('name', '')}]")
                elif item.get("type") == "tool_result":
                    parts.append("[tool_result]")
            else:
                parts.append(str(item))
        return "\n".join(p for p in parts if p)
    if isinstance(content, dict):
        return text_from_content(content.get("content") or content.get("text"))
    return str(content)


def clip(text, limit=1400):
    text = " ".join(str(text).split())
    return text if len(text) <= limit else text[:limit] + "..."


def is_noise(text):
    return any(marker in text for marker in NOISE_MARKERS)


def read_jsonl(path):
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue


def make_record(tool, first_ts, tz, session_id, cwd, path, messages, commands):
    visible_messages = [m for m in messages if m.get("text") and not is_noise(m.get("text", ""))]
    return {
        "tool": tool,
        "date": first_ts.astimezone(tz).date().isoformat(),
        "timestamp": first_ts.isoformat(),
        "session_id": session_id,
        "cwd": cwd,
        "path": str(path),
        "messages": visible_messages,
        "commands": commands[:30],
        "message_count": len(visible_messages),
    }


def parse_codex(root, start_utc, end_utc, tz):
    root = Path(root)
    if not root.exists():
        return []
    records = []
    for path in sorted(root.rglob("*.jsonl")):
        messages = []
        commands = []
        cwd = None
        session_id = path.stem
        first_ts = None
        for obj in read_jsonl(path):
            ts = parse_time(obj.get("timestamp"))
            if ts and first_ts is None:
                first_ts = ts
            typ = obj.get("type")
            payload = obj.get("payload") or {}
            if typ == "session_meta":
                cwd = payload.get("cwd") or cwd
                session_id = payload.get("id") or session_id
                meta_ts = parse_time(payload.get("timestamp"))
                if meta_ts:
                    first_ts = meta_ts
            if typ == "response_item":
                role = payload.get("role")
                if payload.get("type") == "message" and role in {"user", "assistant"}:
                    text = text_from_content(payload.get("content"))
                    if text:
                        messages.append({"role": role, "text": clip(text)})
                if payload.get("type") in {"function_call", "custom_tool_call"}:
                    name = payload.get("name") or payload.get("call_id") or payload.get("type")
                    args = payload.get("arguments") or payload.get("input") or ""
                    commands.append(clip(f"{name}: {args}", 500))
        if in_range(first_ts, start_utc, end_utc):
            records.append(make_record("codex", first_ts, tz, session_id, cwd, path, messages, commands))
    return records


def parse_claude(root, start_utc, end_utc, tz):
    root = Path(root)
    if not root.exists():
        return []
    records = []
    for path in sorted(root.rglob("*.jsonl")):
        lowered = str(path).lower()
        if "\\subagents\\" in lowered or "\\tool-results\\" in lowered:
            continue
        messages = []
        commands = []
        cwd = None
        session_id = path.stem
        first_ts = None
        for obj in read_jsonl(path):
            ts = parse_time(obj.get("timestamp"))
            if ts and first_ts is None:
                first_ts = ts
            cwd = cwd or obj.get("cwd")
            session_id = obj.get("sessionId") or session_id
            typ = obj.get("type")
            if typ in {"user", "assistant"}:
                msg = obj.get("message") or {}
                role = msg.get("role") or typ
                text = text_from_content(msg.get("content") if msg else obj.get("content"))
                if text:
                    messages.append({"role": role, "text": clip(text)})
            elif typ == "system" and obj.get("subtype") == "local_command":
                text = text_from_content(obj.get("content"))
                if text:
                    commands.append(clip(text, 500))
        if in_range(first_ts, start_utc, end_utc):
            records.append(make_record("claude-code", first_ts, tz, session_id, cwd, path, messages, commands))
    return records


def sqlite_tables(conn):
    rows = conn.execute("select name from sqlite_master where type='table' order by name").fetchall()
    return [row[0] for row in rows]


def parse_opencode(db_path, start_utc, end_utc, tz):
    db_path = Path(db_path)
    if not db_path.exists():
        return [], {}
    details = {}
    records = []
    try:
        conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        conn.row_factory = sqlite3.Row
        tables = sqlite_tables(conn)
        for table in tables:
            cols = [row[1] for row in conn.execute(f"pragma table_info({table})").fetchall()]
            count = conn.execute(f"select count(*) from {table}").fetchone()[0]
            details[table] = {"columns": cols, "count": count}
        if "message" not in tables:
            conn.close()
            return [], details
        parts_by_message = {}
        if "part" in tables:
            for row in conn.execute("select * from part").fetchall():
                data = dict(row)
                try:
                    payload = json.loads(data.get("data") or "{}")
                except Exception:
                    payload = {}
                if payload.get("type") == "text" and payload.get("text"):
                    parts_by_message.setdefault(data.get("message_id"), []).append(payload.get("text"))
        session_meta = {}
        if "session" in tables:
            for row in conn.execute("select * from session").fetchall():
                data = dict(row)
                session_meta[str(data.get("id") or "")] = data
        by_session = {}
        for row in conn.execute("select * from message").fetchall():
            data = dict(row)
            try:
                payload = json.loads(data.get("data") or "{}")
            except Exception:
                payload = {}
            ts = parse_time(data.get("time_created") or payload.get("time", {}).get("created"))
            if not in_range(ts, start_utc, end_utc):
                continue
            sid = str(data.get("session_id") or "unknown")
            role = str(payload.get("role") or "")
            text = "\n".join(parts_by_message.get(data.get("id"), []))
            item = by_session.setdefault(sid, {"first": ts, "messages": []})
            item["first"] = min(item["first"], ts)
            item["messages"].append({"role": role, "text": clip(text)})
        for sid, item in by_session.items():
            meta = session_meta.get(sid, {})
            records.append(make_record(
                "opencode",
                item["first"],
                tz,
                sid,
                meta.get("directory") or meta.get("cwd") or meta.get("project"),
                db_path,
                item["messages"],
                [],
            ))
        conn.close()
    except Exception as exc:
        details["parse_error"] = str(exc)
    return records, details


def parse_kimi(root, start_utc, end_utc, tz):
    """Parse Kimi Code CLI history from ~/.kimi/sessions/."""
    root = Path(root)
    if not root.exists():
        return []
    records = []

    # Each session hash dir contains subdirs (UUIDs) with context.jsonl + wire.jsonl + state.json
    for session_dir in sorted(root.iterdir()):
        if not session_dir.is_dir():
            continue
        session_hash = session_dir.name

        for sub_dir in sorted(session_dir.iterdir()):
            if not sub_dir.is_dir():
                continue

            wire_path = sub_dir / "wire.jsonl"
            if not wire_path.exists():
                continue

            messages = []
            commands = []
            first_ts = None
            session_id = sub_dir.name

            for obj in read_jsonl(wire_path):
                msg = obj.get("message", {})
                msg_type = msg.get("type")
                payload = msg.get("payload", {})

                # Extract timestamp from wire record
                ts = parse_time(obj.get("timestamp"))

                if msg_type == "TurnBegin":
                    if ts and first_ts is None:
                        first_ts = ts
                    user_input = payload.get("user_input")
                    if user_input is not None:
                        text = text_from_content(user_input)
                        if text and not is_noise(text):
                            messages.append({"role": "user", "text": clip(text)})

                elif msg_type == "ContentPart":
                    part = payload
                    if part.get("type") == "text":
                        text = part.get("text", "")
                        if text and not is_noise(text):
                            messages.append({"role": "assistant", "text": clip(text)})

                elif msg_type == "ToolCall":
                    func = payload.get("function", {})
                    name = func.get("name", "")
                    args = func.get("arguments", "")
                    commands.append(clip(f"{name}: {args}", 500))

            if in_range(first_ts, start_utc, end_utc):
                records.append(make_record(
                    "kimi-code",
                    first_ts,
                    tz,
                    session_id,
                    None,  # cwd not directly available in wire.jsonl
                    wire_path,
                    messages,
                    commands,
                ))

    return records


def resolve_sources(args):
    home = Path.home()
    if args.source_root:
        source = Path(args.source_root)
        return {
            "codex": Path(args.codex_sessions) if args.codex_sessions else source / "codex" / "sessions",
            "claude_code": Path(args.claude_projects) if args.claude_projects else source / "claude" / "projects",
            "opencode": Path(args.opencode_db) if args.opencode_db else source / "opencode" / "opencode.db",
            "kimi_code": Path(args.kimi_sessions) if args.kimi_sessions else source / "kimi" / "sessions",
        }
    return {
        "codex": Path(args.codex_sessions) if args.codex_sessions else home / ".codex" / "sessions",
        "claude_code": Path(args.claude_projects) if args.claude_projects else home / ".claude" / "projects",
        "opencode": Path(args.opencode_db) if args.opencode_db else home / ".local" / "share" / "opencode" / "opencode.db",
        "kimi_code": Path(args.kimi_sessions) if args.kimi_sessions else home / ".kimi" / "sessions",
    }


def main():
    args = parse_args()
    start_utc, end_utc, tz = local_day_bounds(args.start, args.end, args.timezone)
    sources = resolve_sources(args)
    codex = parse_codex(sources["codex"], start_utc, end_utc, tz)
    claude = parse_claude(sources["claude_code"], start_utc, end_utc, tz)
    opencode, opencode_schema = parse_opencode(sources["opencode"], start_utc, end_utc, tz)
    kimi = parse_kimi(sources["kimi_code"], start_utc, end_utc, tz)
    records = sorted(codex + claude + opencode + kimi, key=lambda r: (r["date"], r["tool"], r["timestamp"]))
    output = {
        "range": {
            "start": args.start,
            "end": args.end,
            "timezone": args.timezone,
            "start_utc": start_utc.isoformat(),
            "end_utc_exclusive": end_utc.isoformat(),
        },
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "sources": {key: str(value) for key, value in sources.items()},
        "source_exists": {key: Path(value).exists() for key, value in sources.items()},
        "opencode_schema": opencode_schema,
        "records": records,
    }
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {out_path} with {len(records)} records")
    for tool in ("codex", "claude-code", "opencode", "kimi-code"):
        print(tool, sum(1 for r in records if r["tool"] == tool))


if __name__ == "__main__":
    main()
