#!/usr/bin/env python3
"""Create a WeChat Official Account draft from an HTML or simple Markdown file."""

from __future__ import annotations

import argparse
import html
import json
import mimetypes
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path


API_BASE = "https://api.weixin.qq.com"


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


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def truncate(text: str, limit: int) -> str:
    return text if len(text) <= limit else text[:limit]


def request_json(method: str, url: str, *, payload: dict | None = None, timeout: int = 60) -> dict:
    data = None
    headers = {}
    if payload is not None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json; charset=utf-8"

    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
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


def multipart_json(url: str, field_name: str, file_path: Path, timeout: int = 60) -> dict:
    boundary = f"----CodexWeChatBoundary{uuid.uuid4().hex}"
    mime_type = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
    file_bytes = file_path.read_bytes()

    parts = [
        f"--{boundary}\r\n".encode("utf-8"),
        (
            f'Content-Disposition: form-data; name="{field_name}"; '
            f'filename="{file_path.name}"\r\n'
        ).encode("utf-8"),
        f"Content-Type: {mime_type}\r\n\r\n".encode("utf-8"),
        file_bytes,
        b"\r\n",
        f"--{boundary}--\r\n".encode("utf-8"),
    ]
    body = b"".join(parts)
    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            raw = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        raise WeChatAPIError(f"HTTP {exc.code}: {raw}") from exc
    except urllib.error.URLError as exc:
        raise WeChatAPIError(f"Network error: {exc}") from exc

    result = json.loads(raw)
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
    return token


def upload_cover(access_token: str, cover_path: Path) -> str:
    query = urllib.parse.urlencode({"access_token": access_token, "type": "image"})
    result = multipart_json(
        f"{API_BASE}/cgi-bin/material/add_material?{query}", "media", cover_path
    )
    media_id = result.get("media_id")
    if not media_id:
        raise WeChatAPIError(f"No media_id in cover upload response: {result}")
    return media_id


def upload_inline_image(access_token: str, image_path: Path) -> str:
    query = urllib.parse.urlencode({"access_token": access_token})
    result = multipart_json(f"{API_BASE}/cgi-bin/media/uploadimg?{query}", "media", image_path)
    url = result.get("url")
    if not url:
        raise WeChatAPIError(f"No url in inline image upload response: {result}")
    return url


def simple_markdown_to_html(markdown: str) -> str:
    blocks: list[str] = []
    paragraph: list[str] = []

    def flush_paragraph() -> None:
        if paragraph:
            text = " ".join(paragraph).strip()
            blocks.append(f"<p>{text}</p>")
            paragraph.clear()

    for raw_line in markdown.splitlines():
        line = raw_line.strip()
        if not line:
            flush_paragraph()
            continue
        image_match = re.match(r"!\[([^\]]*)\]\(([^)]+)\)", line)
        if image_match:
            flush_paragraph()
            alt, src = image_match.groups()
            blocks.append(f'<p><img src="{html.escape(src)}" alt="{html.escape(alt)}"></p>')
            continue
        heading_match = re.match(r"^(#{1,4})\s+(.+)$", line)
        if heading_match:
            flush_paragraph()
            level = len(heading_match.group(1))
            text = html.escape(heading_match.group(2))
            blocks.append(f"<h{level}>{text}</h{level}>")
            continue
        paragraph.append(html.escape(line))

    flush_paragraph()
    return "\n".join(blocks)


def load_content(content_path: Path) -> str:
    text = read_text(content_path)
    if content_path.suffix.lower() in {".html", ".htm"}:
        return text
    if content_path.suffix.lower() in {".md", ".markdown"}:
        return simple_markdown_to_html(text)
    if "<p" in text or "<section" in text or "<h1" in text:
        return text
    return simple_markdown_to_html(text)


def replace_local_images(html_text: str, content_dir: Path, access_token: str | None) -> str:
    pattern = re.compile(r'(<img\b[^>]*\bsrc=["\'])([^"\']+)(["\'][^>]*>)', re.IGNORECASE)

    def replace(match: re.Match[str]) -> str:
        before, src, after = match.groups()
        if src.startswith(("http://", "https://")):
            return match.group(0)
        if src.startswith("data:"):
            raise WeChatAPIError("Inline data: images are not supported. Save them as files first.")
        image_path = Path(src)
        if not image_path.is_absolute():
            image_path = content_dir / image_path
        if not image_path.exists():
            raise WeChatAPIError(f"Inline image not found: {image_path}")
        if access_token is None:
            return match.group(0)
        uploaded_url = upload_inline_image(access_token, image_path)
        return f"{before}{uploaded_url}{after}"

    return pattern.sub(replace, html_text)


def create_draft(
    access_token: str,
    *,
    title: str,
    content: str,
    thumb_media_id: str,
    author: str,
    digest: str,
    content_source_url: str,
    show_cover_pic: int,
    need_open_comment: int,
    only_fans_can_comment: int,
) -> str:
    payload = {
        "articles": [
            {
                "title": truncate(title, 64),
                "author": author,
                "digest": truncate(digest, 120),
                "content": content,
                "content_source_url": content_source_url,
                "thumb_media_id": thumb_media_id,
                "show_cover_pic": show_cover_pic,
                "need_open_comment": need_open_comment,
                "only_fans_can_comment": only_fans_can_comment,
            }
        ]
    }
    query = urllib.parse.urlencode({"access_token": access_token})
    result = request_json("POST", f"{API_BASE}/cgi-bin/draft/add?{query}", payload=payload)
    media_id = result.get("media_id")
    if not media_id:
        raise WeChatAPIError(f"No media_id in draft response: {result}")
    return media_id


def parse_args() -> argparse.Namespace:
    load_env_files()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--title", required=True)
    parser.add_argument("--content", required=True, type=Path, help="HTML or simple Markdown file")
    parser.add_argument("--cover", type=Path, help="Cover image path; uploads as permanent material")
    parser.add_argument("--thumb-media-id", help="Existing permanent cover media_id")
    parser.add_argument("--author", default=os.environ.get("WECHAT_MP_AUTHOR", ""))
    parser.add_argument("--digest", default="")
    parser.add_argument("--source-url", default="")
    parser.add_argument("--show-cover-pic", type=int, choices=[0, 1], default=0)
    parser.add_argument("--need-open-comment", type=int, choices=[0, 1], default=0)
    parser.add_argument("--only-fans-can-comment", type=int, choices=[0, 1], default=0)
    parser.add_argument("--appid", default=os.environ.get("WECHAT_MP_APPID"))
    parser.add_argument("--appsecret", default=os.environ.get("WECHAT_MP_APPSECRET"))
    parser.add_argument("--dry-run", action="store_true", help="Do not call WeChat APIs")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.content.exists():
        raise WeChatAPIError(f"Content file not found: {args.content}")
    if not args.thumb_media_id and not args.cover:
        raise WeChatAPIError("Provide --cover or --thumb-media-id.")
    if args.cover and not args.cover.exists():
        raise WeChatAPIError(f"Cover file not found: {args.cover}")

    article_html = load_content(args.content)

    if args.dry_run:
        article_html = replace_local_images(article_html, args.content.parent, None)
        print(
            json.dumps(
                {
                    "dry_run": True,
                    "title": truncate(args.title, 64),
                    "author": args.author,
                    "digest": truncate(args.digest, 120),
                    "content_chars": len(article_html),
                    "has_cover": bool(args.cover or args.thumb_media_id),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    if not args.appid or not args.appsecret:
        raise WeChatAPIError("Set WECHAT_MP_APPID and WECHAT_MP_APPSECRET or pass --appid/--appsecret.")

    access_token = get_access_token(args.appid, args.appsecret)
    thumb_media_id = args.thumb_media_id or upload_cover(access_token, args.cover)
    article_html = replace_local_images(article_html, args.content.parent, access_token)
    media_id = create_draft(
        access_token,
        title=args.title,
        content=article_html,
        thumb_media_id=thumb_media_id,
        author=args.author,
        digest=args.digest,
        content_source_url=args.source_url,
        show_cover_pic=args.show_cover_pic,
        need_open_comment=args.need_open_comment,
        only_fans_can_comment=args.only_fans_can_comment,
    )

    print(json.dumps({"status": "success", "draft_media_id": media_id}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except WeChatAPIError as exc:
        print(json.dumps({"status": "error", "message": str(exc)}, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(1)
