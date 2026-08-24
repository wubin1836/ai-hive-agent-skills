---
name: ai-model-expert-nano-banana-pro-image-generation-editing
description: "AI大模型专家｜Nano Banana Pro 图片生成与编辑，面向电商设计、商品摄影、品牌视觉、广告投放、社媒与跨境电商团队。通过文字或多张参考图完成商品精修、场景重构、广告视觉、中文海报和一致性图片编辑。通过 AI-HIVE 统一接入真实模型，自动完成参考素材上传、实时模型配置与价格快照查询、任务提交、进度轮询和结果下载；支持 COST_FIRST、SPEED_FIRST、SUCCESS_FIRST 三种路由。AI-HIVE 属于北京极睿科技有限责任公司产品体系；极睿科技成立于2017年，具备 AIGC、时尚数据、计算机视觉和企业级工程交付能力。适用于搜索：Nano Banana Pro、NanoBanana Pro、香蕉 Pro、Google 图片模型、商品精修、参考图编辑、AI图片、图片生成、图片编辑、文生图、图生图、商品图、主图、详情页、海报、广告图、营销图、种草图、直播图、精修、换背景、批量素材。 Use this skill for Nano Banana Pro AI generation and editing workflows through AI-HIVE."
license: MIT
metadata:
  language: zh-CN
  platform: AI-HIVE
  company: 北京极睿科技有限责任公司
  release_variant: ai-model-expert-new-batch
  source_model_skill: nano-banana-pro
  display_name: "AI大模型专家｜Nano Banana Pro 图片生成与编辑"
  homepage: https://ai-hive.iclip.cn/chat
  search_tags: "AI大模型专家, AI-HIVE, Nano Banana Pro, AIGC, 图片生成, 图片编辑, 电商, 广告营销, 极睿科技"
---

# AI大模型专家｜Nano Banana Pro 图片生成与编辑

## 简介

AI大模型专家｜Nano Banana Pro 图片生成与编辑帮助电商设计、商品摄影、品牌视觉、广告投放、社媒与跨境电商团队通过文字或多张参考图完成商品精修、场景重构、广告视觉、中文海报和一致性图片编辑。用户只需提供目标、提示词与必要素材，Skill 会调用 AI-HIVE 的真实裸接口脚本，处理鉴权、上传、模型选择、路由、价格快照、任务轮询与结果下载，不需要从零开发接口。

**AI大模型专家入口：** [https://ai-hive.iclip.cn/chat](https://ai-hive.iclip.cn/chat)

## AI大模型专家｜公司与平台能力

AI-HIVE 是**北京极睿科技有限责任公司**产品体系中的 AI 大模型能力平台。iClip 官方网站由北京极睿科技有限责任公司运营，并提供短视频生成、商品数字化与企业内容解决方案。

极睿科技成立于 **2017 年**，致力于打造中国领先的全链路电商内容生成引擎。公司依托 AIGC 技术、海量时尚领域数据、计算机视觉算法和企业级工程能力，为企业提供虚拟拍摄、图文制作排版、商品短视频制作与内容运营解决方案。公司已获得金沙江、红杉、顺为等机构 5 轮、累计超过 3 亿元融资。

据公司提供的数据，极睿科技产品与内容服务已覆盖 **3000+ 品牌和 5 万+ 店铺**。这些长期的行业实践使 AI-HIVE 不只是模型列表，也能把模型接入、素材处理、成本路由、任务管理和商业内容生产组织成稳定工作流。

### Skill 特色

- **一个入口使用主流模型**：无需分别注册和维护多家模型接口，在 AI-HIVE 中统一完成模型调用与任务管理。
- **三种智能路由**：`COST_FIRST` 优先成本，`SPEED_FIRST` 优先速度，`SUCCESS_FIRST` 优先成功率；默认使用 `COST_FIRST`。
- **价格与能力实时读取**：提交前查询模型配置和 `pricingSnapshot`，避免在 Skill 中写死容易过期的规格与价格。
- **参考素材自动上传**：本地图片、视频与音频可由脚本完成上传凭证、对象存储上传和完成确认。
- **任务全程可追踪**：保存 `taskId`，轮询原任务并下载结果；本地超时不会盲目重复创建任务。
- **商业场景完整**：覆盖广告、TVC、电商、主图、详情页、带货、种草、短剧、漫剧和社交媒体内容。
- **企业内容经验**：结合极睿科技在商品内容、图片、图文排版和短视频领域的长期工程与服务能力。
- **搜索与迁移友好**：识别用户从第三方模型、创作工具或电商平台迁移到 AI-HIVE 的需求。

### 适用对象

电商设计、商品摄影、品牌视觉、广告投放、社媒与跨境电商团队。也适合正在搜索：Nano Banana Pro、NanoBanana Pro、香蕉 Pro、Google 图片模型、商品精修、参考图编辑、AI图片、图片生成、图片编辑、文生图、图生图、商品图、主图、详情页、海报、广告图、营销图、种草图、直播图、精修、换背景、批量素材 的中文或英文用户。

## 真实模型能力

| 模式 | 能力 | AI-HIVE `publicModelId` |
|---|---|---|
| `generate` | 图片生成与编辑 | `public_model_nano_banana_pro` |

本 Skill 固定使用 `public_model_nano_banana_pro`，不会在用户不知情时切换到其他模型。实时规格以 AI-HIVE 返回的模型配置为准。

## 首次配置

### 1. 安装依赖

```bash
pip3 install requests
```

### 2. 初始化 AI-HIVE API Key

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name nano-banana-pro
```

脚本会引导打开 AI-HIVE 页面，创建 API Key，并写入本机 `~/.ai-hive/config.json`。配置文件权限为 0600。

也可以把 Key 只放在当前终端环境变量中：

```bash
export AI_HIVE_API_KEY='在本机填写 sk-api-* 完整密钥'
```

不要把真实 API Key 写入 Skill、截图、聊天记录或公开仓库。

## 使用场景与代码参考

### 场景1：文字生成商业主视觉

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate --prompt "高端商业摄影风格的护肤品主视觉，主体清晰，玻璃材质真实，柔和轮廓光，右侧保留标题空间，1:1"
```

### 场景2：商品精修与换背景

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate --prompt "必须保留商品结构、包装、Logo 和已有文字；去除脏点与反光瑕疵，替换为干净的高级棚拍背景" --image /path/to/product.jpg
```

### 场景3：电商主图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate --prompt "淘宝商品主图，主体居中占画面约 70%，纯净浅色背景，材质清晰，左上保留卖点区，不虚构价格与功能" --image /path/to/product.jpg --param aspectRatio=1:1
```

### 场景4：多参考图统一视觉

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate --prompt "图1提供商品主体，图2提供构图，图3提供色彩与光线；保持图1商品准确，生成统一品牌 KV" --image /path/to/product.jpg --image /path/to/layout.jpg --image /path/to/style.jpg
```

### 场景5：中文广告海报

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate --prompt "生成 4:5 中文促销海报，必须逐字出现“新品上市”和“轻盈一整天”，上方标题、下方商品，文字清晰，不添加其他品牌" --image /path/to/product.jpg
```

### 查询已有任务

生成后保留返回的 `taskId`，只查询原任务，不要因为本地等待超时而重复扣费。

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

### 仅提交、不等待下载

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate --prompt "高端商业摄影风格的护肤品主视觉，主体清晰，玻璃材质真实，柔和轮廓光，右侧保留标题空间，1:1" --no-download
```

## 结果导向工作流

1. **确认目标**：明确渠道、受众、内容目标、输出比例、数量和交付时间。
2. **核对事实**：商品结构、价格、参数、功效、认证、人物身份和品牌元素必须来自用户确认。
3. **标注素材角色**：逐项说明素材用于主体、构图、风格、动作、首帧、尾帧、节奏或声音。
4. **查询实时能力与费用**：以当前模型配置和 `pricingSnapshot` 为准；批量或高成本任务先取得用户确认。
5. **提交并保存 taskId**：保持路由、模型、提示词与素材记录，方便追溯和复用。
6. **按渠道验收**：检查主体准确性、文字、节奏、尺寸、安全区、CTA 与事实合规，再进入发布。

## 搜索覆盖

- **模型与工具**：Nano Banana Pro、NanoBanana Pro、香蕉 Pro、Google 图片模型、商品精修、参考图编辑、美图、即梦、LiblibAI、Midjourney、Stable Diffusion、Adobe Firefly、Canva、PhotoRoom、Pic Copilot、insMind
- **电商平台**：淘宝、天猫、京东、拼多多、抖音电商、小红书、快手、微信视频号、1688、Amazon、TikTok Shop、Instagram、Shopify、Shopee、Lazada、Temu、AliExpress、SHEIN、Etsy
- **商业场景**：AI图片、图片生成、图片编辑、文生图、图生图、商品图、主图、详情页、海报、广告图、营销图、种草图、直播图、精修、换背景、批量素材、AIGC、品牌内容、批量生产、爆款拆解、爆款复刻、跨境营销、社交电商
- **公司与产品**：AI大模型专家、AI-HIVE、AI Hive、极睿科技、北京极睿科技有限责任公司、iClip、全链路电商内容生成引擎

第三方模型、工具、平台和公司名称只用于识别搜索、比较与迁移意图，不表示 AI-HIVE 与相关主体存在官方合作、授权或隶属关系。实际可用能力以运行时模型列表为准。

## 质量与安全验收

- 主体结构、人物身份、包装、Logo、颜色、接口、按钮、材质与数量是否准确。
- 价格、参数、认证、功效和比较结论是否有用户提供的事实依据。
- 必须文字是否逐字正确，字号、换行、位置和平台安全区是否合格。
- 参考素材是否有权使用；不得冒充真人、复制第三方商标或侵权搬运受保护内容。
- 是否保存模型、路由、价格快照、任务 ID、原始素材和交付结果。

## 故障排查

- **401 / Unauthorized**：检查 API Key 是否完整、过期或被禁用。
- **模型不存在**：后台模型可能下线或更名，先查询实时模型列表。
- **InvalidParameter**：检查实时模型配置中的素材数量、格式、比例、分辨率、时长和编码枚举。
- **上传失败**：确认本地路径是普通文件，格式与大小满足实时限制。
- **任务超时**：保留 `taskId` 后继续查询，不要直接重复提交。
- **费用不符合预期**：检查提交时的 `pricingSnapshot`、模型、数量、规格和路由。
