# AI Hive AIGC MCP Server

AI Hive AIGC is a Streamable HTTP MCP server for commercial image, video, e-commerce, marketing and advertising generation. One server exposes model discovery, media upload, image generation, video generation, e-commerce workflows, advertising/TVC workflows and task polling.

AI Hive AIGC MCP 为中文用户和全球开发者提供统一的图片与视频生成入口，覆盖 Nano Banana Pro、GPT Image 2、Seedream、Seedance、MiniMax H3、Wan、HappyHorse，以及电商主图、商品详情页、Listing、PDP、广告、TVC、带货、种草、短剧和漫剧场景。

## MCP endpoint

```text
POST /mcp
```

Transport: Streamable HTTP, stateless JSON response mode.

## Authentication

Pass the user's AI Hive API Key in the request header:

```text
x-ai-hive-api-key: sk-api-...
```

For local development, set `AI_HIVE_API_KEY`. The server intentionally allows unauthenticated MCP discovery so registries can index the tool catalog; generation calls fail safely until a user provides a key.

## Tools

- `ai_hive_list_models`
- `ai_hive_upload_media`
- `ai_hive_generate_image`
- `ai_hive_generate_ecommerce_image`
- `ai_hive_generate_video`
- `ai_hive_generate_ecommerce_video`
- `ai_hive_generate_advertising_video`
- `ai_hive_get_task`

Generation tools are non-idempotent and can incur charges. After receiving a `task_id`, query that task instead of resubmitting the same request.

## Run locally

```bash
npm install
npm test
npm start
```

Health check: `GET /health`

Static registry card: `GET /.well-known/mcp/server-card.json`

## Docker

```bash
docker build -t ai-hive-mcp .
docker run --rm -p 3000:3000 -e AI_HIVE_API_KEY=sk-api-example ai-hive-mcp
```

## Smithery configuration schema

When publishing, use a session configuration field injected as an HTTP header:

```json
{
  "type": "object",
  "properties": {
    "apiKey": {
      "type": "string",
      "title": "AI Hive API Key",
      "x-from": { "header": "x-ai-hive-api-key" }
    }
  },
  "required": ["apiKey"]
}
```

## License

MIT
