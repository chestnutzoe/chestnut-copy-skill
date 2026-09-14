#!/usr/bin/env python3
"""Fetch or normalize WeChat Official Account articles for style analysis."""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


API_BASE = "https://api.weixin.qq.com"
DEFAULT_OUTPUT = Path(os.environ.get("STYLE_ANALYZER_ARTICLES", "./outputs/articles.json"))


class WeChatAPIError(RuntimeError):
    pass


def load_env_files() -> None:
    candidates: list[Path] = []
    explicit = os.environ.get("WECHAT_MP_ENV_FILE")
    if explicit:
        candidates.append(Path(explicit).expanduser())

    script_dir = Path(__file__).resolve().parent.parent
    candidates.extend(
        [
            Path.cwd() / ".env",
            Path.cwd() / ".secrets" / "wechat-mp.env",
            script_dir / ".env",
            script_dir / ".secrets" / "wechat-mp.env",
            Path.home() / ".wechat-mp.env",
        ]
    )

    for path in candidates:
        if path.exists():
            load_env_file(path)


def load_env_file(path: Path) -> None:
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("'\"")
        if key and key not in os.environ:
            os.environ[key] = value


def request_json(method: str, url: str, *, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = None
    headers: dict[str, str] = {}
    if payload is not None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json; charset=utf-8"

    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            raw = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        raise WeChatAPIError(f"HTTP {exc.code}: {raw}") from exc
    except urllib.error.URLError as exc:
        raise WeChatAPIError(f"Network error: {exc}") from exc

    try:
        result = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise WeChatAPIError(f"Invalid JSON response: {raw}") from exc

    if result.get("errcode") not in (None, 0):
        raise WeChatAPIError(json.dumps(result, ensure_ascii=False))
    return result


def get_access_token(appid: str, appsecret: str) -> str:
    query = urllib.parse.urlencode(
        {"grant_type": "client_credential", "appid": appid, "secret": appsecret}
    )
    result = request_json("GET", f"{API_BASE}/cgi-bin/token?{query}")
    token = result.get("access_token")
    if not token:
        raise WeChatAPIError(f"No access_token in response: {result}")
    return str(token)


def strip_html(value: str) -> str:
    value = re.sub(r"(?is)<(script|style).*?>.*?</\1>", "", value)
    value = re.sub(r"(?i)<br\s*/?>", "\n", value)
    value = re.sub(r"(?i)</p\s*>", "\n\n", value)
    value = re.sub(r"(?i)</div\s*>", "\n", value)
    value = re.sub(r"(?s)<[^>]+>", "", value)
    value = html.unescape(value)
    value = re.sub(r"[ \t\r\f\v]+", " ", value)
    value = re.sub(r"\n{3,}", "\n\n", value)
    return value.strip()


def normalize_article(raw: dict[str, Any], *, source: str, container: dict[str, Any] | None = None) -> dict[str, Any]:
    container = container or {}
    html_content = str(raw.get("content") or raw.get("content_html") or "")
    text = str(raw.get("text") or raw.get("content_text") or "").strip() or strip_html(html_content)
    title = str(raw.get("title") or raw.get("name") or "Untitled")

    return {
        "source": source,
        "title": title,
        "author": raw.get("author") or container.get("author") or "",
        "digest": raw.get("digest") or "",
        "url": raw.get("url") or raw.get("content_source_url") or "",
        "content_html": html_content,
        "content_text": text,
        "update_time": raw.get("update_time") or container.get("update_time"),
        "publish_time": raw.get("publish_time") or container.get("publish_time"),
        "media_id": container.get("media_id") or raw.get("media_id"),
        "article_id": container.get("article_id") or raw.get("article_id"),
    }


def extract_wechat_articles(payload: dict[str, Any], *, source: str) -> list[dict[str, Any]]:
    articles: list[dict[str, Any]] = []
    for item in payload.get("item", []) or []:
        content = item.get("content") or {}
        news_items = content.get("news_item") or item.get("news_item") or []
        if isinstance(news_items, dict):
            news_items = [news_items]
        for raw_article in news_items:
            if isinstance(raw_article, dict):
                articles.append(normalize_article(raw_article, source=source, container=item))
    return articles


def fetch_articles(source: str, offset: int, count: int, appid: str, appsecret: str) -> list[dict[str, Any]]:
    access_token = get_access_token(appid, appsecret)
    endpoint = "freepublish/batchget" if source == "published" else "draft/batchget"
    query = urllib.parse.urlencode({"access_token": access_token})
    payload = {"offset": offset, "count": count, "no_content": 0}
    result = request_json("POST", f"{API_BASE}/cgi-bin/{endpoint}?{query}", payload=payload)
    return extract_wechat_articles(result, source=source)


def load_json_articles(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return [
            normalize_article(item, source=str(item.get("source") or "local"))
            for item in data
            if isinstance(item, dict)
        ]
    if isinstance(data, dict):
        if isinstance(data.get("articles"), list):
            return [
                normalize_article(item, source=str(item.get("source") or "local"))
                for item in data["articles"]
                if isinstance(item, dict)
            ]
        return extract_wechat_articles(data, source="local")
    raise WeChatAPIError(f"Unsupported JSON shape: {path}")


def load_local_article(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() in {".html", ".htm"}:
        return normalize_article({"title": path.stem, "content": text}, source="local")
    return normalize_article({"title": path.stem, "text": text}, source="local")


def load_local(path: Path) -> list[dict[str, Any]]:
    if path.is_file() and path.suffix.lower() == ".json":
        return load_json_articles(path)
    if path.is_file():
        return [load_local_article(path)]
    if not path.is_dir():
        raise WeChatAPIError(f"Local path not found: {path}")

    articles: list[dict[str, Any]] = []
    for child in sorted(path.rglob("*")):
        if child.is_file() and child.suffix.lower() in {".html", ".htm", ".md", ".markdown", ".txt"}:
            articles.append(load_local_article(child))
        elif child.is_file() and child.suffix.lower() == ".json":
            articles.extend(load_json_articles(child))
    return articles


def merge_articles(existing: list[dict[str, Any]], incoming: list[dict[str, Any]]) -> list[dict[str, Any]]:
    merged: list[dict[str, Any]] = []
    seen: set[str] = set()
    for article in existing + incoming:
        key = str(
            article.get("article_id")
            or article.get("media_id")
            or article.get("url")
            or f"{article.get('title')}::{article.get('content_text', '')[:80]}"
        )
        if key in seen:
            continue
        seen.add(key)
        merged.append(article)
    return merged


def write_articles(path: Path, articles: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "article_count": len(articles),
        "articles": articles,
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    load_env_files()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", choices=["published", "draft"], default="published")
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--count", type=int, default=20)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--append", type=Path, help="Existing article JSON to merge before writing output")
    parser.add_argument("--local", type=Path, help="Local JSON, HTML, Markdown, TXT file, or folder")
    parser.add_argument("--appid", default=os.environ.get("WECHAT_MP_APPID"))
    parser.add_argument("--appsecret", default=os.environ.get("WECHAT_MP_APPSECRET"))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not 1 <= args.count <= 20:
        raise WeChatAPIError("--count must be between 1 and 20.")

    if args.local:
        incoming = load_local(args.local)
    else:
        if not args.appid or not args.appsecret:
            raise WeChatAPIError("Set WECHAT_MP_APPID and WECHAT_MP_APPSECRET or pass --appid/--appsecret.")
        incoming = fetch_articles(args.source, args.offset, args.count, args.appid, args.appsecret)

    existing: list[dict[str, Any]] = []
    if args.append:
        if args.append.exists():
            existing = load_json_articles(args.append)
        else:
            raise WeChatAPIError(f"--append file not found: {args.append}")

    articles = merge_articles(existing, incoming)
    write_articles(args.output, articles)
    print(json.dumps({"status": "success", "article_count": len(articles), "output": str(args.output)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except WeChatAPIError as exc:
        print(json.dumps({"status": "error", "message": str(exc)}, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(1)
