# WeChat Official Account Article API Notes

## Endpoints

Get access token:

```text
GET https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=APPID&secret=APPSECRET
```

Get published article records:

```text
POST https://api.weixin.qq.com/cgi-bin/freepublish/batchget?access_token=TOKEN
Content-Type: application/json
```

Payload:

```json
{
  "offset": 0,
  "count": 20,
  "no_content": 0
}
```

Upload permanent cover image:

```text
POST https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=TOKEN&type=image
multipart form field: media=@cover.jpg
```

Upload inline article image:

```text
POST https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token=TOKEN
multipart form field: media=@image.jpg
```

Create draft:

```text
POST https://api.weixin.qq.com/cgi-bin/draft/add?access_token=TOKEN
Content-Type: application/json
```

Payload:

```json
{
  "articles": [
    {
      "title": "Title",
      "author": "Chestnut",
      "digest": "Digest",
      "content": "<p>HTML body</p>",
      "content_source_url": "",
      "thumb_media_id": "permanent-cover-media-id",
      "show_cover_pic": 0,
      "need_open_comment": 0,
      "only_fans_can_comment": 0
    }
  ]
}
```

Get draft-box articles:

```text
POST https://api.weixin.qq.com/cgi-bin/draft/batchget?access_token=TOKEN
Content-Type: application/json
```

Payload:

```json
{
  "offset": 0,
  "count": 20,
  "no_content": 0
}
```

## Source Guidance

- Use `freepublish/batchget` for published historical articles.
- Use `draft/batchget` only when analyzing drafts.
- Use `draft/add` only to create a draft for manual backend review.
- `count` should be between 1 and 20.
- `offset` starts at 0 and increases by `count`.
- `no_content=0` asks the API to return article content.

## Common Response Shapes

Published articles commonly return nested article lists under `item[].content.news_item[]`.
Drafts commonly return nested article lists under `item[].content.news_item[]`.

Fields may vary by account permissions and API version. The script normalizes common fields:

- title
- author
- digest
- content
- content_source_url
- url
- update_time
- publish_time
- article_id
- media_id

## Common Errors

- `40164`: current IP is not in the WeChat Official Account IP whitelist.
- invalid credential: AppID/AppSecret is wrong, expired, or for the wrong account.
- API unauthorized: the official account does not have the required interface permission.
- empty content: retry with `no_content=0`; verify the selected endpoint is correct.
- missing `thumb_media_id`: upload a permanent cover image or pass an existing cover media ID.
- invalid image URL in draft content: upload local inline images with `media/uploadimg` and replace `src`.

## Cover Rules

WeChat drafts require a cover represented by `thumb_media_id`.

- If the user has a local image, upload it with `material/add_material` through `--cover`.
- If the user already has a permanent-material cover ID, pass it through `--thumb-media-id`.
- If the user has neither, ask for a cover image or provide cover directions / image-generation prompts first.
- Do not assume an AI-generated cover exists; generation and upload are separate steps.

## Credential Rules

Never commit AppID, AppSecret, access tokens, downloaded article JSON, or generated private style guides unless the user explicitly decides they are safe to publish. Use `.gitignore` defaults.
