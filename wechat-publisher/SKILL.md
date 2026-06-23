---
name: wechat-publisher
description: Use when a creator has an approved local Markdown or HTML article and wants to prepare title, digest, cover handling, WeChat API credential/IP preflight, and Official Account draft-box upload for manual backend review.
---

# 公众号发布

## Purpose

This skill prepares and uploads approved local articles to the WeChat Official Account draft box.

It answers one question:

> 这篇文章怎么落地到公众号后台？

It is a publishing helper, not a writing skill. Use it after the draft, title, and direction are already approved.

## Boundary

Default behavior:

- create draft only,
- no automatic publish,
- no mass send,
- no scheduled send,
- final backend review stays with the user.

Always remind the user to inspect title, digest, cover, formatting, images, links, and typos in the WeChat backend before publishing.

## Credential Setup

Use persistent local credentials by default. The script reads:

1. `WECHAT_MP_ENV_FILE`
2. `./.env`
3. `./.secrets/wechat-mp.env`
4. the same files inside this skill directory
5. `~/.wechat-mp.env`

Existing environment variables win over file values.

Never commit AppID, AppSecret, access tokens, article JSON, or private generated drafts.

## API Preflight

Before any live WeChat API call, check whether the user has already configured the local WeChat API setup.

If `WECHAT_MP_APPID` and `WECHAT_MP_APPSECRET` are missing from environment variables and the known env files, ask first:

```text
你本机已经配置公众号 API 了吗？
需要有 WECHAT_MP_APPID 和 WECHAT_MP_APPSECRET。
如果还没有，请先在本地创建 .secrets/wechat-mp.env；不要把 AppSecret 发到聊天里。
```

If the user has credentials but has not confirmed the current machine IP is in the WeChat Official Account IP whitelist, ask them to do the IP whitelist step before running a real upload.

Only proceed to `publish_draft.py` when:

- AppID/AppSecret are available locally, and
- the current public IP is confirmed in the WeChat API whitelist, and
- the user has approved creating a draft.

## First Live API Check

Before a real WeChat API call from a new network, get the current IP:

```bash
curl -s https://api.ipify.org
```

Tell the user to add it in:

```text
公众号后台 -> 设置与开发 -> 基本设置 -> IP 白名单
```

If the API returns `40164`, the current IP is not allowlisted.

Read `references/wechat-api.md` when endpoint details or WeChat errors matter.

## Cover Preflight

WeChat drafts require a cover represented by `thumb_media_id`.

Before creating a real draft, ask:

```text
你现在有公众号封面图吗？
如果有，请给我本地图片路径；
如果已经有永久素材 thumb_media_id，也可以直接给 media_id。
没有的话，我先给你封面方向 / AI 生成提示词，等你确认封面后再创建草稿。
```

Rules:

- Do not assume an AI-generated cover exists.
- Do not create a real draft without `--cover` or `--thumb-media-id`.
- If there is no cover yet, provide cover directions or image-generation prompts.
- Use `--dry-run` when checking fields without creating a real draft.

## Create Draft

Use an existing permanent cover:

```bash
python3 -B scripts/publish_draft.py \
  --title "文章标题" \
  --content "/absolute/path/article.md" \
  --thumb-media-id "MEDIA_ID_FROM_WECHAT" \
  --author "${WECHAT_MP_AUTHOR:-}" \
  --digest "摘要"
```

Use a local cover image:

```bash
python3 -B scripts/publish_draft.py \
  --title "文章标题" \
  --content "/absolute/path/article.html" \
  --cover "/absolute/path/cover.jpg" \
  --author "${WECHAT_MP_AUTHOR:-}" \
  --digest "摘要"
```

Dry run:

```bash
python3 -B scripts/publish_draft.py \
  --title "文章标题" \
  --content "/absolute/path/article.md" \
  --thumb-media-id "MEDIA_ID_FROM_WECHAT" \
  --dry-run
```

Use `python3 -B` so Python does not write cache files in restricted app environments.

## Handoff From Other Skills

From `文风分析`, use the generated voice guide only if copy still needs editing.

From `爆款文案 SOP`, expect:

- final mother draft path,
- selected title,
- digest,
- cover direction or cover file,
- manual approval from the user.

If any of these are missing, pause and collect them before uploading.
