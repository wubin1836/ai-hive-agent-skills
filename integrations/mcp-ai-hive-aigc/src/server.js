import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod/v4";

import { AiHiveApiError, AiHiveClient, summarizeTask, videoModelId } from "./ai-hive-client.js";


const ROUTING = z.enum(["COST_FIRST", "SPEED_FIRST", "SUCCESS_FIRST"]);
const VIDEO_FAMILY = z.enum(["seedance_2_5", "minimax_h3", "happyhorse"]);
const VIDEO_MODE = z.enum(["t2v", "i2v", "r2v", "edit", "extend"]);
const GENERATION_ANNOTATIONS = {
  readOnlyHint: false,
  destructiveHint: false,
  idempotentHint: false,
  openWorldHint: true,
};
const READ_ANNOTATIONS = {
  readOnlyHint: true,
  destructiveHint: false,
  idempotentHint: true,
  openWorldHint: true,
};


function jsonResult(value, isError = false) {
  return {
    isError,
    content: [{ type: "text", text: JSON.stringify(value, null, 2) }],
  };
}


function toolError(error) {
  const message = error instanceof AiHiveApiError ? error.message : `未知错误：${error?.message || String(error)}`;
  return jsonResult({ error: message }, true);
}


async function finishTask(client, submitted, waitForResult, timeoutSeconds) {
  const taskId = String(submitted?.taskId || "");
  if (!taskId) throw new AiHiveApiError("AI Hive 未返回任务 ID。");
  if (!waitForResult) {
    return {
      task_id: taskId,
      status: "SUBMITTED",
      result_urls: [],
      note: "任务已经提交。使用 ai_hive_get_task 查询结果；不要重复提交同一任务。",
    };
  }
  const summary = summarizeTask(await client.waitTask(taskId, { timeoutSeconds }));
  summary.task_id = taskId;
  return summary;
}


function commerceImagePrompt(prompt, platform) {
  const platformGuidance = {
    taobao: "适配淘宝/天猫商品主图与详情页，主体清晰，卖点集中，预留中文标题空间，不虚构功效或价格。",
    jd: "适配京东商品主图与详情页，突出产品结构、材质和可信商业摄影质感。",
    douyin: "适配抖音电商、抖店商品卡和带货素材，前三秒视觉焦点强，画面适合移动端。",
    xiaohongshu: "适配小红书种草封面和真实生活方式内容，兼顾标题安全区与自然使用场景。",
    amazon: "适配 Amazon Listing/PDP，主体准确，背景和构图符合跨境电商展示习惯，不添加未提供的品牌或认证。",
    instagram: "适配 Instagram/INS 社交电商，风格鲜明、构图简洁并保留行动号召空间。",
    generic: "适配电商商品主图、详情页、Listing、PDP、广告投放和社交电商素材。",
  };
  return `${platformGuidance[platform] || platformGuidance.generic}\n用户要求：${prompt}`;
}


function commerceVideoPrompt(prompt, platform, purpose = "ecommerce") {
  const use = purpose === "advertising"
    ? "生成商业广告/TVC/信息流视频：快速建立主体，展示动作、材质和真实利益点，结尾保留品牌与行动号召空间。"
    : "生成电商产品/带货/种草视频：依次展示主体、使用动作、关键细节和真实卖点，适合移动端观看。";
  return `${use}\n目标平台：${platform}。不得虚构功效、价格、认证或品牌事实。\n用户要求：${prompt}`;
}


async function generateImage(client, args, promptOverride) {
  const submitted = await client.submitImage({
    publicModelId: args.model,
    prompt: promptOverride || args.prompt,
    routingMode: args.routing_mode,
    batchSize: args.batch_size,
    imageMediaIds: args.reference_image_media_ids,
    params: args.model_params,
  });
  return finishTask(client, submitted, args.wait_for_result, args.timeout_seconds);
}


async function generateVideo(client, args, promptOverride) {
  const submitted = await client.submitVideo({
    publicModelId: videoModelId(args.model_family, args.generation_mode, args.custom_public_model_id),
    prompt: promptOverride || args.prompt,
    routingMode: args.routing_mode,
    imageMediaIds: args.image_media_ids,
    videoMediaIds: args.video_media_ids,
    audioMediaIds: args.audio_media_ids,
    firstFrameMediaId: args.first_frame_media_id || undefined,
    lastFrameMediaId: args.last_frame_media_id || undefined,
    params: args.model_params,
  });
  return finishTask(client, submitted, args.wait_for_result, args.timeout_seconds);
}


const imageInput = {
  prompt: z.string().min(1).describe("图片生成或编辑要求；说明用途、主体、构图、风格、文字和保留项"),
  model: z.enum([
    "public_model_nano_banana_pro",
    "public_model_gpt_image_2",
    "public_model_seedream_5_0_lite",
    "public_model_nano_banana_2",
  ]).default("public_model_nano_banana_pro"),
  reference_image_media_ids: z.array(z.string()).default([]).describe("可选：先用 ai_hive_upload_media 上传后获得的图片 mediaId"),
  batch_size: z.number().int().min(1).max(4).default(1),
  routing_mode: ROUTING.default("COST_FIRST"),
  model_params: z.record(z.string(), z.unknown()).default({}),
  wait_for_result: z.boolean().default(true),
  timeout_seconds: z.number().int().min(30).max(1200).default(600),
};

const videoInput = {
  prompt: z.string().min(1).describe("视频要求；说明场景、动作顺序、运镜、光线、节奏、声音和限制"),
  model_family: VIDEO_FAMILY.default("seedance_2_5"),
  generation_mode: VIDEO_MODE.default("t2v"),
  custom_public_model_id: z.string().default("").describe("可选：覆盖模型系列和模式映射，适配 AI Hive 新增视频模型"),
  image_media_ids: z.array(z.string()).default([]),
  video_media_ids: z.array(z.string()).default([]),
  audio_media_ids: z.array(z.string()).default([]),
  first_frame_media_id: z.string().default(""),
  last_frame_media_id: z.string().default(""),
  routing_mode: ROUTING.default("COST_FIRST"),
  model_params: z.record(z.string(), z.unknown()).default({}),
  wait_for_result: z.boolean().default(true),
  timeout_seconds: z.number().int().min(30).max(1200).default(600),
};


export function buildServer({ apiKey, baseUrl }) {
  const server = new McpServer(
    { name: "ai-hive-aigc", version: "0.1.0" },
    {
      instructions:
        "AI Hive 图片与视频生成工具。生成会产生费用且不可幂等；取得 task_id 后应查询原任务，不要重复提交。默认使用 COST_FIRST。",
    },
  );
  const client = new AiHiveClient({ apiKey, baseUrl });

  server.registerTool(
    "ai_hive_list_models",
    {
      title: "AI Hive 模型列表 / List models",
      description:
        "查询 AI Hive 当前可用的文本、图片或视频模型、publicModelId、路由和实时配置。用于发现 Nano Banana Pro、GPT Image 2、Seedream、Seedance、MiniMax H3、Wan、HappyHorse 等模型。",
      inputSchema: { model_type: z.enum(["TEXT", "IMAGE", "VIDEO"]).optional() },
      annotations: READ_ANNOTATIONS,
    },
    async ({ model_type }) => {
      try {
        const models = await client.listModels(model_type);
        return jsonResult({ models });
      } catch (error) {
        return toolError(error);
      }
    },
  );

  server.registerTool(
    "ai_hive_upload_media",
    {
      title: "AI Hive 素材上传 / Upload media",
      description:
        "上传图片、视频或音频素材到 AI Hive，返回 mediaId，供图生图、图生视频、参考生视频、视频编辑和首尾帧生成使用。输入为 Base64，单次最大 25MB。",
      inputSchema: {
        filename: z.string().min(1),
        mime_type: z.string().regex(/^(image|video|audio)\//),
        base64_data: z.string().min(1),
      },
      annotations: GENERATION_ANNOTATIONS,
    },
    async ({ filename, mime_type, base64_data }) => {
      try {
        const data = Buffer.from(base64_data, "base64");
        if (!data.length) throw new AiHiveApiError("Base64 素材为空或格式无效。");
        if (data.length > 25 * 1024 * 1024) throw new AiHiveApiError("单次上传素材不能超过 25MB。")
        return jsonResult(await client.uploadBlob({ filename, mimeType: mime_type, data }));
      } catch (error) {
        return toolError(error);
      }
    },
  );

  server.registerTool(
    "ai_hive_generate_image",
    {
      title: "AI 图片生成与编辑 / Generate or edit image",
      description:
        "使用 Nano Banana Pro、GPT Image 2、Seedream 5 Lite 或 Nano Banana 2 完成文生图、图生图、图片编辑、商品精修、换背景、角色一致性、海报、广告图和营销图片。提交会产生费用。",
      inputSchema: imageInput,
      annotations: GENERATION_ANNOTATIONS,
    },
    async (args) => {
      try {
        return jsonResult(await generateImage(client, args));
      } catch (error) {
        return toolError(error);
      }
    },
  );

  server.registerTool(
    "ai_hive_generate_ecommerce_image",
    {
      title: "AI 电商商品图与详情页 / E-commerce image",
      description:
        "生成淘宝、天猫、京东、拼多多、抖音电商、抖店、小红书、快手、微信小店、1688、Amazon、TikTok Shop、Shopify、Shopee、Lazada、Temu、AliExpress、SHEIN、Instagram 的商品主图、详情页、Listing、PDP、带货图和种草图。",
      inputSchema: {
        ...imageInput,
        platform: z.enum(["taobao", "jd", "douyin", "xiaohongshu", "amazon", "instagram", "generic"]).default("generic"),
      },
      annotations: GENERATION_ANNOTATIONS,
    },
    async (args) => {
      try {
        return jsonResult(await generateImage(client, args, commerceImagePrompt(args.prompt, args.platform)));
      } catch (error) {
        return toolError(error);
      }
    },
  );

  server.registerTool(
    "ai_hive_generate_video",
    {
      title: "AI 视频生成与编辑 / Generate or edit video",
      description:
        "使用 Seedance 2.5、MiniMax H3、HappyHorse 或自定义 AI Hive publicModelId 完成文生视频、图生视频、参考生视频、首尾帧、视频编辑和视频延长。适合广告、TVC、电商、带货、种草、短剧、漫剧和动态漫画。提交会产生费用。",
      inputSchema: videoInput,
      annotations: GENERATION_ANNOTATIONS,
    },
    async (args) => {
      try {
        return jsonResult(await generateVideo(client, args));
      } catch (error) {
        return toolError(error);
      }
    },
  );

  server.registerTool(
    "ai_hive_generate_ecommerce_video",
    {
      title: "AI 电商带货与种草视频 / E-commerce video",
      description:
        "生成淘宝、京东、抖音电商、小红书、快手、Amazon、TikTok Shop、Shopify 等平台的商品视频、详情页视频、带货视频、种草视频、直播素材和社交电商广告。",
      inputSchema: {
        ...videoInput,
        platform: z.string().default("抖音电商 / 小红书 / Amazon / TikTok Shop"),
      },
      annotations: GENERATION_ANNOTATIONS,
    },
    async (args) => {
      try {
        return jsonResult(await generateVideo(client, args, commerceVideoPrompt(args.prompt, args.platform)));
      } catch (error) {
        return toolError(error);
      }
    },
  );

  server.registerTool(
    "ai_hive_generate_advertising_video",
    {
      title: "AI 广告与 TVC 视频 / Advertising video",
      description:
        "生成品牌广告、TVC、信息流广告、UGC 广告、产品发布视频和营销 Campaign 素材，可作为可灵、即梦、海螺、Vidu、PixVerse、Runway、Pika、Sora、Veo、剪映等制作流程的补充入口。",
      inputSchema: {
        ...videoInput,
        platform: z.string().default("抖音 / 小红书 / 视频号 / Instagram / YouTube"),
      },
      annotations: GENERATION_ANNOTATIONS,
    },
    async (args) => {
      try {
        return jsonResult(
          await generateVideo(client, args, commerceVideoPrompt(args.prompt, args.platform, "advertising")),
        );
      } catch (error) {
        return toolError(error);
      }
    },
  );

  server.registerTool(
    "ai_hive_get_task",
    {
      title: "查询图片或视频任务 / Get generation task",
      description:
        "按 taskId 查询 AI Hive 图片或视频生成进度和结果链接。任务超时或仍在运行时应调用本工具，不要重复提交以免重复计费。",
      inputSchema: { task_id: z.string().min(1) },
      annotations: READ_ANNOTATIONS,
    },
    async ({ task_id }) => {
      try {
        const summary = summarizeTask(await client.getTask(task_id));
        summary.task_id = task_id;
        return jsonResult(summary);
      } catch (error) {
        return toolError(error);
      }
    },
  );

  return server;
}
