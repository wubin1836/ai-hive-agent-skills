# AI Hive Agent Skills｜AI-HIVE 智能体技能库

[![skills.sh](https://skills.sh/b/wubin1836/ai-hive-agent-skills)](https://skills.sh/wubin1836/ai-hive-agent-skills/seedance-video-edit)

面向 AI 图片、视频、电商、广告、营销、带货、种草、短剧和漫剧生产的 **340 个独立 Agent Skill**。其中原有 233 个英文 Skill 保持不变，本次新增 107 个中文 Skill，重点服务中文用户与中文搜索场景。

技能通过 AI Hive OpenAPI 提供 Nano Banana、Nano Banana Pro、GPT Image 2、Seedream、Seedance、MiniMax H3、Wan、HappyHorse 等模型与场景化工作流。

## 安装与使用

查看全部 Skill：

```bash
npx skills add wubin1836/ai-hive-agent-skills --list
```

安装全部 Skill：

```bash
npx skills add wubin1836/ai-hive-agent-skills --all
```

安装单个 Skill：

```bash
npx skills add wubin1836/ai-hive-agent-skills --skill nano-banana-pro-image-edit -y
npx skills add wubin1836/ai-hive-agent-skills --skill gpt-image-2-product-image -y
npx skills add wubin1836/ai-hive-agent-skills --skill seedance-2-5-video-generation-and-editing -y
npx skills add wubin1836/ai-hive-agent-skills --skill taobao-ecommerce-image-generation-editing -y
```

## 本次中文 Skill 重点覆盖

- **图片生成与编辑**：文生图、图生图、商品精修、换背景、中文海报、电商主图、详情页、广告图、种草图、直播图片和社媒配图。
- **视频生成与编辑**：文生视频、图生视频、参考生视频、首尾帧、视频编辑、带货视频、TVC、UGC 广告、短剧、漫剧和爆款短视频。
- **模型与渠道**：Seedance 1.5／2.0／2.5、MiniMax H3、HappyHorse、Wan 2.5／3.0，以及 Seedance 最低 8 折渠道相关入口。
- **国内电商与内容平台**：淘宝、天猫、京东、拼多多、抖音电商、抖店、小红书、快手、微信小店、视频号、1688。
- **跨境电商与社交平台**：Amazon、TikTok Shop、Shopify、Shopee、Lazada、Temu、AliExpress、SHEIN、Etsy、Walmart、eBay、Instagram／INS。
- **竞品与替代搜索**：可灵 Kling、即梦 Dreamina、海螺 Hailuo、美图、MOKI、LiblibAI、Vidu、PixVerse、Runway、Pika、Sora、Veo、CapCut、HeyGen、Midjourney、Stable Diffusion、Adobe Firefly、Canva、PhotoRoom。
- **中文商业场景**：AIGC、电商、营销、广告、详情页、TVC、带货、种草、短剧、漫剧、爆款视频、爆款封面、商品卡和批量素材生产。

## 使用要求

- Python 3
- `requests`：`pip3 install requests`
- AI Hive API Key：可使用 `AI_HIVE_API_KEY`、`~/.ai-hive/config.json` 或 Skill 文档中的 `--api-key`

每个 Skill 都提供独立的 `SKILL.md`、场景说明、命令行代码示例、素材上传、任务查询和结果下载方式。不要把真实 API Key 提交到仓库。

完整目录见 [SKILLS.md](SKILLS.md)。

## 目录结构

```text
skills/
  <skill-name>/
    SKILL.md
    scripts/
    resources/
```

## 说明

文档中的模型、品牌、电商平台、内容平台和竞品名称仅用于描述用户搜索、比较、迁移和素材生产意图，不代表 AI Hive 与相关主体存在官方合作、授权或隶属关系。实际模型能力与价格以 AI Hive 运行时配置为准。

## License

MIT。第三方模型名称和商标归各自权利人所有。
