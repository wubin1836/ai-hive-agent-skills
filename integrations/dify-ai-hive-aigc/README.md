# AI Hive AIGC Models for Dify

AI Hive AIGC Models brings commercial image and video generation into Dify through one provider credential. It is designed for e-commerce operators, designers, marketing and advertising teams, brands, content creators, short-drama teams and AI workflow builders.

AI Hive AIGC 模型插件让 Dify 用户通过一个 API Key 调用多种图片与视频模型，适合电商主图、商品详情页、广告 KV、海报、产品精修、换背景、带货、种草、TVC、短剧、漫剧和社交媒体素材生产。

## Tools / 工具

- **Generate or Edit Image / 图片生成与编辑**
  - Nano Banana Pro
  - GPT Image 2
  - Seedream 5 Lite
  - Nano Banana 2
- **Generate or Edit Video / 视频生成与编辑**
  - Seedance 2.5: text-to-video, image-to-video, reference-to-video, editing and extension
  - MiniMax H3: text-to-video, image-to-video and reference-to-video
  - HappyHorse: text-to-video, image-to-video, reference-to-video and editing
- **Query Generation Task / 查询生成任务**
  - Continue checking an existing task without resubmitting it.

## Typical use cases / 典型场景

- 淘宝、天猫、京东、拼多多、抖音电商、抖店、小红书、快手、微信小店、1688
- Amazon、TikTok Shop、Shopify、Shopee、Lazada、Temu、AliExpress、SHEIN、Instagram
- 商品主图、详情页、Listing、PDP、海报、广告图、直播图片、商品精修、换背景
- 产品视频、带货视频、种草视频、广告、TVC、UGC、短剧、漫剧、动态漫画

## Configuration / 配置

1. Install the plugin in Dify.
2. Open the AI Hive provider authorization panel.
3. Paste an AI Hive API Key beginning with `sk-api-`.
4. Keep the default API URL unless your AI Hive administrator provides another endpoint.

在 AI Hive 聊天页左下角进入“API 接入”，新建 API Key 后粘贴到 Dify 插件授权面板即可。

## Development

```bash
python3 -m unittest discover -s tests -v
dify plugin package ./ai-hive-dify-plugin
```

The plugin reads live model metadata and pricing snapshots before every submission. It never stores the user's AI Hive API Key in source code.

## Trademark notice

Model names, platform names and company names are used only to describe search, comparison, migration and production intent. This plugin does not claim an official partnership with those third parties.

## License

MIT
