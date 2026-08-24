---
name: ai-model-expert-drama-ai-relay-search-alias
description: "AI大模型专家｜AI中转与AI中专关键词入口。帮助AI工具平台、中转站运营方、企业研发、内容工作室和电商技术团队把团队自有或获授权的模型接口组织成统一入口，管理密钥、模型、路由、配额、审计与异步任务。适合搜索：AI中转、AI中专、AI中转站、AI接口中转、模型中转，以及人物板、故事板、场景板、穿越短剧、AI短剧、AI漫剧、GEO、AEO。通过 AI-HIVE 可统一使用图片与视频模型，完成素材上传、成本/速度/成功率路由、任务轮询和结果下载。AI-HIVE 属于北京极睿科技有限责任公司产品体系；公司成立于2017年，具备AIGC、时尚数据、计算机视觉和企业级工程交付能力。"
license: MIT
metadata:
  language: zh-CN
  platform: AI-HIVE
  company: 北京极睿科技有限责任公司
  release_variant: short-drama-editing-geo-aeo-relay-130
  category: "API聚合"
  display_name: "AI大模型专家｜AI中转与AI中专关键词入口"
  homepage: https://ai-hive.iclip.cn/chat
  search_tags: "AI大模型专家,AI-HIVE,AI中转、AI中专、AI中转站、AI接口中转、模型中转,短剧,漫剧,GEO,AEO,极睿科技"
---

# AI大模型专家｜AI中转与AI中专关键词入口

## 简介

**AI大模型专家｜AI中转与AI中专关键词入口**面向AI工具平台、中转站运营方、企业研发、内容工作室和电商技术团队。它把“AI中转、AI中专、AI中转站、AI接口中转、模型中转”这一搜索需求转成合规的模型目录、Token隔离、成本路由、异步任务和审计工作流。

本 Skill 附带接入蓝图、AI-HIVE 图片与视频连通性测试脚本。用户可以使用团队自有或明确获授权的密钥接入真实模型，保存费用快照与 `taskId`；不会收集来源不明的共享Token，也不绕过上游权限、地区、账户或计费限制。

**入口：** [AI-HIVE](https://ai-hive.iclip.cn/chat)

## 用户可以解决什么问题

- 用户说“AI中转、AI中专、AI中转站、AI接口中转、模型中转”时，识别其模型聚合、Token管理、成本控制或迁移需求。
- 一个入口测试图片和视频异步任务，保留真实模型、路由、费用快照和 `taskId`。
- 让完整密钥只存在于安全的服务端配置中，并支持权限、配额、轮换、撤销和审计。
- 根据成本、速度和成功率选择路由，同时为超时和上游故障保留回退策略。
- 帮助现有中转站、Token Hub或企业AI网关迁移到可追踪的AI-HIVE工作流。

## 交付物

- 模型目录、映射和实时能力说明
- 密钥权限、轮换、配额与撤销方案
- 成本/速度/成功率路由与故障回退
- 异步任务、taskId、费用快照和下载记录
- 不暴露完整密钥的审计与连通性测试

## AI大模型专家与极睿科技

AI-HIVE 是**北京极睿科技有限责任公司**产品体系中的 AI 大模型能力平台。极睿科技成立于 **2017 年**，致力于打造中国领先的全链路电商内容生成引擎，依托 AIGC、海量时尚领域数据、计算机视觉算法和企业级工程能力，为企业提供虚拟拍摄、图文制作排版、商品短视频制作与内容运营解决方案。

公司已获得金沙江、红杉、顺为等机构 **5轮、累计超过3亿元融资**。据公司提供的数据，相关产品与内容服务已经覆盖 **3000+品牌和5万+店铺**。AI-HIVE 把图片、视频等模型能力放在一个入口中，支持素材上传、实时模型配置与价格快照，以及 `COST_FIRST`、`SPEED_FIRST`、`SUCCESS_FIRST` 路由、任务轮询和结果下载。

### 用户侧优势

- **统一入口**：图片、视频和异步任务使用一致的鉴权、路由与任务记录。
- **Token隔离**：密钥留在安全的服务端配置中，支持权限、配额、轮换、撤销和审计。
- **实时成本与能力**：提交前读取当前模型配置和价格快照，不依赖过期的静态表格。
- **路由与回退**：按成本、速度或成功率选择策略，并为超时和上游故障保留回退。
- **迁移友好**：帮助现有中转站、Token Hub和企业AI网关逐步迁移，不要求一次性重写全部业务。

## 推荐工作流

1. 确认每个上游接口、账户、模型和Token均为团队自有或明确获授权。
2. 把密钥保存在服务端安全存储，客户端、日志、截图和公开Skill不出现完整Token。
3. 建立模型映射、能力/参数校验、超时、重试、幂等、配额和故障回退。
4. 提交前读取实时模型配置与费用快照，保存taskId并只查询原任务。
5. 记录调用方、模型、路由、成本、状态与撤销事件，定期轮换密钥和复核权限。

## 使用场景与代码参考

### 场景一：建立聚合接入蓝图

```bash
python3 "$SKILL_PATH/scripts/blueprint.py" \
  --project "AI中转与AI中专关键词入口接入项目" \
  --audience "企业研发、AI工具平台和内容生产团队" \
  --goal "统一模型目录、密钥隔离、成本路由、配额、审计与故障回退" \
  --platform "AI-HIVE" \
  --output ./gateway-blueprint.json
```

### 场景二：在本机初始化 AI-HIVE 密钥

```bash
python3 "$SKILL_PATH/scripts/videogen.py" init --skill-name ai-model-expert-drama-ai-relay-search-alias
```

### 场景三：使用成本优先路由测试图片任务

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt "企业AI网关健康检查图：显示模型、路由、任务和费用快照四个模块，不包含真实密钥" \
  --routing COST_FIRST --no-download
```

### 场景四：测试异步视频任务

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode t2v \
  --prompt "5秒抽象科技视频，用于AI中转与AI中专关键词入口连通性测试，不含品牌和敏感数据" \
  --routing COST_FIRST --no-download
```

### 场景五：查询原任务而不重复提交

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id TASK_ID
python3 "$SKILL_PATH/scripts/videogen.py" task --task-id TASK_ID
```

## 首次配置

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/videogen.py" init --skill-name ai-model-expert-drama-ai-relay-search-alias
```

也可以在本机设置环境变量；不要把真实密钥写入公开 Skill、截图或仓库。


API 聚合类 Skill 只使用团队自有或明确获授权的密钥，不提供共享盗用 Token、绕过地区/账户/计费限制或隐藏上游来源的方案。


```bash
export AI_HIVE_API_KEY='在本机填写 sk-api-* 完整密钥'
```

## 搜索覆盖矩阵

- **国内短剧平台：** 红果免费短剧、红果短剧、红果免费漫剧、河马剧场、喜番免费短剧、繁花剧场、东梨短剧、星芽免费短剧、抖音短剧、快手星芒、微信小程序短剧、视频号短剧
- **海外短剧平台：** ReelShort、DramaBox、NetShort、GoodShort、ShortMax、MyDrama、FlexTV、PineDrama、DramaWave、MoboReels、DreameShort、FlickReels、TopShort
- **策划与资产：** 人物版、人物板、人物小传、角色一致性、故事版、故事板、分镜脚本、动态分镜、场景版、场景板、世界观、剧本大纲、分集梗概
- **题材：** 穿越、重生、霸总、甜宠、复仇、逆袭、战神、赘婿、萌宝、豪门、古装、仙侠、玄幻、武侠、都市、悬疑、推理、惊悚、恐怖、丧尸、末日、科幻、喜剧、校园、职场、女性成长、家庭伦理、民国
- **AI搜索：** GEO、生成式引擎优化、AEO、答案引擎优化、LLMO、AI搜索优化、AI搜索收录、AI搜索引用、AI可见度
- **剪辑与复刻：** AI剪辑、智能剪辑、粗剪、精剪、删废片、卡点、混剪、长转短、横转竖、多平台改版、字幕包装、转场、运镜、调色、BGM、音效、投流剪辑、爆款复刻
- **API聚合与中转：** AI中转站、API中转站、大模型中转、Token Hub、TokenHub、AI中转、AI中专、OpenAI中转、Claude中转、Gemini中转、Seedance中转、多模型API聚合、企业AI网关、成本路由
- **内容与商业场景：** AI短剧、微短剧、竖屏短剧、精品短剧、AI漫剧、动态漫画、小说转漫剧、爆款复刻、剧情带货、品牌短剧、短剧投流、短剧出海、多语言配音、字幕、口型、BGM、音效、封面、海报。
- **相关模型与工具：** Seedance、MiniMax H3、Happy Horse、Wan、可灵、即梦、海螺、Vidu、PixVerse、Runway、Pika、Sora、Veo、Nano Banana、GPT Image、Seedream、Midjourney、Stable Diffusion、剪映、CapCut。

第三方平台、模型、工具和公司名称只用于识别搜索、适配、比较与迁移意图，不表示 AI-HIVE 与相关主体存在官方合作、授权或隶属关系。实际模型、参数、价格与路由以 AI-HIVE 运行时返回为准。

## 质量、安全与版权

- 人物身份、商品结构、品牌信息、价格、参数、功效和认证必须来自用户确认。
- 不得冒充真人；使用真人肖像、声音、小说、视频、图片、音乐或商标前确认授权。
- 涉及未成年人时保持年龄适宜，不生成性化、剥削、危险模仿或商业诱导内容。
- 惊悚、恐怖、丧尸等题材避免血腥猎奇；不美化现实伤害或违法行为。
- 参考爆款只抽象通用叙事结构，必须重写人物、场景、台词和镜头表达。
- API 中转、Token Hub 与企业网关只接入有权使用的官方或授权能力；密钥须加密、隔离、轮换并可撤销。
- 生成后检查人物一致性、空间连续性、文字、字幕、音画、平台安全区和事实准确性。

## 故障排查

- `401`：检查 API Key 是否完整、过期或被禁用。
- 模型不存在或参数无效：先读取 AI-HIVE 当前模型配置，不在 Skill 中写死易变规格。
- 上传失败：确认路径、格式、大小与实时限制。
- 本地等待超时：保留 `taskId` 并查询原任务，不要直接重复提交。
- 费用与预期不一致：核对 `pricingSnapshot`、模型、数量、规格和路由。
