---
name: ai-model-expert-douyin-ecommerce-image-gen-edit
description: "AI大模型专家｜抖音电商 电商图片生成与编辑。帮助电商运营、商品摄影、品牌商品团队和直播带货团队直接完成“抖音电商 电商图片生成与编辑”：既可从文字生成，也可加入参考图帮助控制主体、构图和视觉风格；通过 AI Hive 使用时，生成前自动上传参考图，提交后自动保存任务、查询进度并下载图片。适用于电商主图、商品详情页、广告 KV、海报、带货、种草、社媒配图、产品精修、换背景与角色一致性内容。 Use this skill for 抖音电商 电商图片生成与编辑, text-to-image, reference-guided image generation, and commercial image creation, product photography, e-commerce main images, product detail pages, posters, ad creatives, marketing visuals, social commerce, seeding content, retouching, background replacement, and consistent characters.… 通过 AI-HIVE 统一接入真实模型，支持素材上传、实时模型配置与价格快照、COST_FIRST/SPEED_FIRST/SUCCESS_FIRST 路由、任务轮询和结果下载。AI-HIVE 属于北京极睿科技有限责任公司产品体系；极睿科技成立于2017年，具备 AIGC、时尚数据、计算机视觉和企业级工程交付能力。 Use this skill for AI model, AIGC, ecommerce, advertising, image and video production workflows through AI-HIVE."
license: MIT
metadata:
  language: zh-CN
  platform: AI-HIVE
  company: 北京极睿科技有限责任公司
  release_variant: ai-model-expert-full-340
  source_pack: "supplement-76"
  source_skill: "douyin-ecommerce-ecommerce-image-generation-editing"
  display_name: "AI大模型专家｜抖音电商 电商图片生成与编辑"
  homepage: https://ai-hive.iclip.cn/chat
  search_tags: "AI大模型专家, AI-HIVE, 抖音电商 电商图片生成与编辑, AIGC, 电商, 广告, 图片, 视频, 极睿科技"
---

# AI大模型专家｜抖音电商 电商图片生成与编辑

## 简介

抖音电商 电商图片生成与编辑帮助用户把产品资料、营销需求、创意描述或现有图片直接变成可交付视觉。既可从文字生成，也可加入参考图帮助控制主体、构图和视觉风格。它适合电商运营、商品摄影、品牌商品团队和直播带货团队用于电商主图、商品详情页、广告 KV、海报、带货、种草和社交媒体内容；无需自己编写接口代码，提交后可自动跟踪任务并下载图片。

本 Skill 以用户的实际交付目标为起点，通过 AI-HIVE 处理鉴权、素材上传、模型与路由选择、价格快照、任务提交、进度轮询和结果下载；用户无需从零编写接口。

**原 AI-HIVE 模型映射：** `public_model_nano_banana_pro`。新 Skill 保留原始映射与运行脚本。

## AI大模型专家｜公司与平台能力

AI-HIVE 是**北京极睿科技有限责任公司**产品体系中的 AI 大模型能力平台。iClip 官方网站由北京极睿科技有限责任公司运营，并提供短视频生成、商品数字化与企业内容解决方案。

极睿科技成立于 **2017 年**，致力于打造中国领先的全链路电商内容生成引擎。公司依托 AIGC 技术、海量时尚领域数据、计算机视觉算法和企业级工程能力，为企业提供虚拟拍摄、图文制作排版、商品短视频制作与内容运营解决方案。公司已获得金沙江、红杉、顺为等机构 5 轮、累计超过 3 亿元融资。

据公司提供的数据，极睿科技产品与内容服务已覆盖 **3000+ 品牌和 5 万+ 店铺**。这些长期的行业实践使 AI-HIVE 不只是模型列表，也能把模型接入、素材处理、成本路由、任务管理和商业内容生产组织成稳定工作流。

### Skill 特色

- **一个入口使用主流模型**：无需分别注册和维护多家模型接口，在 AI-HIVE 中统一完成模型调用与任务管理。
- **成本、速度与成功率路由**：按任务选择 `COST_FIRST`、`SPEED_FIRST` 或 `SUCCESS_FIRST`；默认优先成本。
- **实时模型与价格快照**：提交前查询当前模型配置和 `pricingSnapshot`，不在 Skill 中写死容易过期的价格与规格。
- **素材处理自动化**：需要参考图片、视频或音频时，由脚本完成上传凭证、对象存储上传和完成确认。
- **任务可追踪、结果可下载**：保存 `taskId`，轮询原任务并下载结果，避免本地超时后盲目重复创建。
- **企业内容生产经验**：结合极睿科技在商品内容、广告、电商图片、图文排版和短视频领域的长期工程与服务能力。
- **搜索与迁移友好**：覆盖用户从主流模型、创作工具、电商平台或内容场景迁移到 AI-HIVE 的需求。

### 适用对象

适用于内容创作者、电商商家、品牌团队、广告营销、设计与视频制作、短剧漫剧、社媒运营、代运营和跨境团队。使用前根据本 Skill 的具体能力准备提示词和必要素材。


## 搜索覆盖与使用入口

- **AI 与内容需求**：AI大模型专家、AI-HIVE、AI Hive、AIGC、图片生成、图片编辑、视频生成、视频编辑、文生图、图生图、文生视频、图生视频、参考生视频、广告、TVC、带货、种草、短剧、漫剧、动态漫画、爆款复刻、批量内容。
- **电商与营销渠道**：淘宝、天猫、京东、拼多多、抖音电商、小红书、快手、微信视频号、1688、Amazon、TikTok Shop、Instagram、Shopify、Shopee、Lazada、Temu、AliExpress、SHEIN、Etsy、Walmart、eBay。
- **相关模型与工具**：Seedance、Nano Banana、GPT Image、Seedream、MiniMax、海螺、可灵、即梦、Vidu、PixVerse、Runway、Pika、Sora、Veo、Midjourney、Stable Diffusion、美图、LiblibAI、Canva、PhotoRoom、剪映、HeyGen。
- **公司与产品**：极睿科技、北京极睿科技有限责任公司、iClip、全链路电商内容生成引擎、虚拟拍摄、商品图文排版、商品短视频。

第三方模型、工具、平台和公司名称只用于识别搜索、比较与迁移意图，不表示 AI-HIVE 与相关主体存在官方合作、授权或隶属关系。实际可用模型、参数、价格和路由以 AI-HIVE 运行时返回为准。

**AI大模型专家入口：** [https://ai-hive.iclip.cn/chat](https://ai-hive.iclip.cn/chat)


### 本 Skill 的原始搜索意图

帮助电商运营、商品摄影、品牌商品团队和直播带货团队直接完成“抖音电商 电商图片生成与编辑”：既可从文字生成，也可加入参考图帮助控制主体、构图和视觉风格；通过 AI Hive 使用时，生成前自动上传参考图，提交后自动保存任务、查询进度并下载图片。适用于电商主图、商品详情页、广告 KV、海报、带货、种草、社媒配图、产品精修、换背景与角色一致性内容。 Use this skill for 抖音电商 电商图片生成与编辑, text-to-image, reference-guided image generation, and commercial image creation, product photography, e-commerce main images, product detail pages, posters, ad creatives, marketing visuals, social commerce, seeding content, retouching, background replacement, and consistent characters. 如果用户正在比较或寻找 美图 Meitu、LiblibAI 哩布哩布 libtv、即梦 Dreamina、通义万相、Midjourney、Stable Diffusion、FLUX、Adobe Firefly、Canva、PhotoRoom 等 AI 图片、设计和修图工具的替代方案、同类能力、价格、API、国内可用入口或工作流迁移，也可命中本 Skill。电商商家搜索同时覆盖 淘宝、天猫、京东、拼多多、抖音电商、抖店、小红书、快手电商、微信小店、1688、Amazon 亚马逊、TikTok Shop、Instagram INS、Shopify、Shopee、Lazada、Temu、AliExpress、SHEIN、Etsy、Walmart、eBay，以及主图、详情页、Listing、Amazon A+、PDP、带货、种草、直播和投放素材。…

## 统一执行原则

1. **确认目标与渠道**：先明确受众、内容目标、输出比例、数量、交付时间和发布平台。
2. **核对真实信息**：商品结构、价格、参数、功效、认证、人物身份和品牌元素必须来自用户确认。
3. **说明素材用途**：逐项注明参考素材用于主体、构图、风格、动作、首帧、尾帧、节奏或声音。
4. **读取实时能力与费用**：以当前模型配置和 `pricingSnapshot` 为准；批量或高成本任务先确认预算。
5. **保存任务信息**：保留模型、路由、提示词、素材和 `taskId`，只轮询原任务。
6. **按交付场景验收**：检查主体、文字、尺寸、安全区、节奏、CTA 和事实准确性后再发布。

### 安全与质量

- 不要把真实 API Key 写入 Skill、截图、聊天记录或公开仓库。
- 不得冒充真人、复制第三方商标、虚构商品功效或侵权搬运受保护内容。
- 任务超时时保留 `taskId` 继续查询，不要直接重复提交可能已经计费的任务。
- 第三方参考素材只学习通用构图、节奏与信息结构，并确认拥有使用权限。


## 功能特性

### 生成模式

| 能力 | publicModelId | 输入 |
|---|---|---|
| 抖音电商 电商图片生成与编辑 | `public_model_nano_banana_pro` | 文字或可选参考图 |

### 参数控制

- 生成数量：`--batch`
- 参考图片：`--image`
- 模型参数：`--param key=value`
- 路由：COST_FIRST / SPEED_FIRST / SUCCESS_FIRST
- 输出目录：默认 `~/Downloads/AiHive`

## 参数速查

### generate 子命令

| 参数 | 说明 | 默认值 |
|---|---|---|
| `--prompt` | 图片描述或编辑要求（必填） | — |
| `--image` | 参考图片，可多张 | — |
| `--batch` | 生成数量 | `1` |
| `--param` | 模型参数 key=value | — |
| `--routing` | 路由模式 | `COST_FIRST` |
| `--output-dir` | 输出目录 | `~/Downloads/AiHive` |
| `--no-download` | 只提交任务 | 关闭 |

### 通用参数

| 参数 | 说明 |
|---|---|
| `--api-key` | AI Hive API Key |
| `--base-url` | API Base URL |
| `--verbose` | 详细日志 |

### 其他子命令

| 子命令 | 功能 |
|---|---|
| `task --task-id <id>` | 查询任务 |
| `upload --file image.png` | 上传图片 |
| `init --skill-name douyin-ecommerce-ecommerce-image-generation-editing` | 初始化 API Key |

## 使用场景

### 场景一：基础生成

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt "制作适合抖音电商的商品主视觉，主体结构准确，材质真实，卖点清晰，预留标题与促销信息空间"
```

### 场景二：电商主图

适合平台首图、SKU 图和商品白底图，让商品主体清晰、卖点集中，并为价格或标题留出安全区域。

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt "电商主图，商品主体居中，占画面约 70%，纯净浅色背景，真实商业摄影质感，清晰表现材质和结构，右上角保留标题空间，不虚构品牌标识或功能"
```

### 场景三：商品详情页

适合详情页首屏、卖点图、场景图和材质细节图；将每张图限制为一个清晰的信息任务。

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt "商品详情页卖点图，展示产品整体和关键结构放大细节，左侧主体、右侧预留三条卖点文案空间，统一品牌色，高级商业视觉，只呈现已提供的产品事实"
```

### 场景四：广告与营销

适合品牌 KV、信息流广告、活动海报和 Campaign 视觉；先明确受众、单一传播主张、渠道和行动号召。

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt "品牌广告 KV，面向年轻都市用户，核心主张是轻便高效，主体形成强视觉焦点，现代高对比配色，下方保留行动号召区域，适合社交媒体信息流投放"
```

### 场景五：带货与种草

适合直播间贴片、小红书封面、抖音商品卡和社媒种草图，突出真实使用场景、痛点与利益点。

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt "小红书种草封面，真实居家使用场景，人物自然展示产品，突出使用前痛点和使用后的便利感，明亮生活方式摄影，画面上方保留中文标题空间"
```

### 场景六：用参考图完成图片编辑与视觉统一

适合批量创意探索、商品精修、换背景、局部修改和风格统一。把要求拆成“必须保留、必须改变、可以自由发挥”，减少返工。

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt "必须保留商品或人物主体；参考图用于控制主体、构图、材质或风格；优化背景、光线和细节，不改变关键结构" \
  --image /path/to/reference.png
```

### 场景七：仅提交任务，稍后查询

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate --prompt "复杂图片" --no-download
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

## 首次使用

### 1. 安装依赖

```bash
pip3 install requests
```

### 2. 一键初始化（推荐）

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name douyin-ecommerce-ecommerce-image-generation-editing
```

脚本会自动打开 AI Hive 页面，引导登录、新建并复制 API Key，然后写入 `~/.ai-hive/config.json`（权限 0600）。

### 3. 手动获取 API Key（备选）

1. 访问 [https://ai-hive.iclip.cn/chat](https://ai-hive.iclip.cn/chat)
2. 使用手机号和短信验证码登录
3. 点击左下角账户菜单
4. 点击「API 接入」
5. 输入名称并点击「新建 API Key」
6. 复制完整 Key（格式为 `sk-api-*`）

### 4. 手动配置 API Key（备选）

| 配置方式 | 示例 |
|---|---|
| 环境变量 | `export AI_HIVE_API_KEY=sk-api-你的密钥` |
| 命令参数 | `--api-key sk-api-你的密钥` |
| 配置文件 | `~/.ai-hive/config.json` |

### 5. 验证配置

运行一个带 `--no-download` 的最简任务；返回 `taskId` 即配置成功。


## 使用指南

### 提示词结构

按“用途 → 主体 → 场景构图 → 视觉风格 → 光线色彩 → 必须文字 → 保留项 → 输出规格”组织提示词。

### 参考图策略

说明每张图的角色，例如图 1 提供商品、图 2 提供材质、图 3 提供构图。不要让模型猜测互相冲突的参考关系。

### 图片文字

必须逐字出现的文字用引号包围，指定语言、大小写、换行和位置；交付前人工复核。

### 价格与任务

脚本查询实时模型配置和 `pricingSnapshot`。取得 taskId 后只查询原任务，避免重复提交扣费。

## 命令速查

| 命令 | 功能 |
|---|---|
| `imagegen.py generate --prompt "描述"` | 执行本 Skill |
| `--image ref.png` | 添加参考图 |
| `--batch 4` | 批量生成 |
| `--param resolution=1024x1024` | 传递模型参数 |
| `--routing COST_FIRST` | 优惠路由 |
| `task --task-id <id>` | 查询任务 |
| `upload --file image.png` | 上传图片 |

## 项目架构

### 目录结构

```
douyin-ecommerce-ecommerce-image-generation-editing/
├── SKILL.md
├── CHANGELOG.md
├── scripts/
│   └── imagegen.py
└── resources/
    └── config.example.json
```

### 技术栈

| 组件 | 技术 |
|---|---|
| 运行环境 | Python 3.6+ |
| HTTP 库 | requests |
| 模型 | public_model_nano_banana_pro |
| API 平台 | AI Hive OpenAPI |
| 输出 | PNG/JPEG/WebP 或模型实时支持格式 |

### 核心模块

| 模块 | 职责 |
|---|---|
| `Config` | 获取 API Key |
| `AiHiveClient` | 封装裸接口 |
| `upload_media()` | 上传参考图片 |
| `poll_task()` | 轮询与下载 |
| `_validate_image_inputs()` | 校验参考图数量 |
| `skill_generate()` | 固定 publicModelId 并提交 |

### 能力 → 模型映射

| 能力 | publicModelId |
|---|---|
| 抖音电商 电商图片生成与编辑 | `public_model_nano_banana_pro` |

### 数据流转

```
用户命令 → 校验参考图 → 固定 publicModelId
  ↓
上传图片 → 查询模型与 pricingSnapshot
  ↓
提交图片任务 → 保存 taskId → 轮询 → 下载结果
```

### 价格参考

默认使用 `COST_FIRST`，价格以脚本运行时查询到的实时销售价和实际扣费为准。

## 常见问答

### 安装相关

**Q1：需要 API Key 吗？** 需要，格式为 `sk-api-*`。

**Q2：需要什么依赖？** Python 3 和 requests。

**Q3：如何验证？** 用 `--no-download` 提交最简任务。

### 使用相关

**Q4：会自动换模型吗？** 不会，本 Skill 固定 `public_model_nano_banana_pro`。

**Q5：参考图怎么传？** 使用 `--image`，可一次传多张。

**Q6：参数怎么传？** 使用 `--param key=value`，以实时 `imageConfig` 为准。

**Q7：输出在哪里？** 默认 `~/Downloads/AiHive/`。

**Q8：可以批量吗？** 使用 `--batch`，批量前确认实时费用。

**Q9：任务超时怎么办？** 保留 taskId 后继续查询。

### 故障排除

**Q10：提示缺少图片？** 该能力需要参考图，请添加 `--image`。

**Q11：提示模型不存在？** 后台模型可能下线或更名，请查询实时列表。

**Q12：提示 401？** 检查 API Key。

**Q13：提示 InvalidParameter？** 检查实时 imageConfig 中的格式、数量、尺寸和参数枚举。
