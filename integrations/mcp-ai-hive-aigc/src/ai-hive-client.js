const TERMINAL_STATUSES = new Set(["COMPLETED", "FAILED"]);


export class AiHiveApiError extends Error {
  constructor(message, statusCode = null) {
    super(message);
    this.name = "AiHiveApiError";
    this.statusCode = statusCode;
  }
}


export class AiHiveClient {
  constructor({ apiKey, baseUrl = "https://ai-hive.iclip.cn/api", timeoutMs = 30_000, fetchImpl = fetch }) {
    this.apiKey = String(apiKey || "").trim();
    this.baseUrl = String(baseUrl).replace(/\/$/, "");
    this.timeoutMs = timeoutMs;
    this.fetchImpl = fetchImpl;
  }

  url(path) {
    return `${this.baseUrl}/openapi/v1/${String(path).replace(/^\//, "")}`;
  }

  async request(method, path, { body, headers = {}, timeoutMs = this.timeoutMs } = {}) {
    if (!this.apiKey) {
      throw new AiHiveApiError(
        "缺少 AI Hive API Key。请配置 x-ai-hive-api-key 请求头，或在本地设置 AI_HIVE_API_KEY。",
        401,
      );
    }
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), timeoutMs);
    try {
      const response = await this.fetchImpl(this.url(path), {
        method,
        headers: {
          Authorization: `Bearer ${this.apiKey}`,
          "Content-Type": "application/json",
          ...headers,
        },
        body: body === undefined ? undefined : JSON.stringify(body),
        signal: controller.signal,
      });
      if (!response.ok) {
        const detail = await response.text();
        throw new AiHiveApiError(`AI Hive 请求失败（${response.status}）：${detail.slice(0, 1000)}`, response.status);
      }
      if (response.status === 204) return null;
      return await response.json();
    } catch (error) {
      if (error instanceof AiHiveApiError) throw error;
      if (error?.name === "AbortError") {
        throw new AiHiveApiError(`AI Hive 请求超时（${timeoutMs}ms）。`);
      }
      throw new AiHiveApiError(`无法连接 AI Hive：${error?.message || String(error)}`);
    } finally {
      clearTimeout(timer);
    }
  }

  getUserInfo() {
    return this.request("GET", "user-info");
  }

  async listModels(modelType) {
    const suffix = modelType ? `?modelType=${encodeURIComponent(modelType)}` : "";
    const models = await this.request("GET", `models${suffix}`);
    if (!Array.isArray(models)) throw new AiHiveApiError("AI Hive 模型列表格式异常。");
    return models;
  }

  async findModel(publicModelId, modelType) {
    const models = await this.listModels(modelType);
    const model = models.find((item) => item.publicModelId === publicModelId);
    if (!model) throw new AiHiveApiError(`当前账户未找到模型：${publicModelId}`);
    return model;
  }

  static pricingSnapshot(model, routingMode) {
    const snapshot = (model.pricingSnapshot || []).find((item) => item.routingMode === routingMode);
    if (!snapshot) {
      throw new AiHiveApiError(`模型 ${model.publicModelId || ""} 不支持路由模式 ${routingMode}。`);
    }
    return snapshot;
  }

  async uploadBlob({ filename, mimeType, data }) {
    const buffer = Buffer.isBuffer(data) ? data : Buffer.from(data);
    const token = await this.request("POST", "media/upload-token", {
      body: {
        filename,
        contentType: mimeType,
        sizeBytes: buffer.byteLength,
      },
    });
    const mediaId = token?.mediaId;
    const upload = token?.upload || {};
    if (!mediaId || !upload.url) throw new AiHiveApiError("AI Hive 未返回有效的素材上传凭证。");

    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 300_000);
    try {
      const response = await this.fetchImpl(upload.url, {
        method: upload.method || "PUT",
        headers: upload.headers || {},
        body: buffer,
        signal: controller.signal,
      });
      if (!response.ok) throw new AiHiveApiError(`素材上传失败（${response.status}）。`);
    } catch (error) {
      if (error instanceof AiHiveApiError) throw error;
      throw new AiHiveApiError(`素材上传失败：${error?.message || String(error)}`);
    } finally {
      clearTimeout(timer);
    }
    await this.request("POST", `media/${mediaId}/complete`);
    return { mediaId: String(mediaId), mimeType };
  }

  async submitImage({ publicModelId, prompt, routingMode = "COST_FIRST", batchSize = 1, imageMediaIds = [], params = {} }) {
    const model = await this.findModel(publicModelId, "IMAGE");
    return this.request("POST", "generation/image", {
      body: {
        publicModelId,
        routingMode,
        prompt,
        batchSize,
        imageMediaIds,
        params,
        pricingSnapshot: AiHiveClient.pricingSnapshot(model, routingMode),
      },
    });
  }

  async submitVideo({
    publicModelId,
    prompt,
    routingMode = "COST_FIRST",
    imageMediaIds = [],
    videoMediaIds = [],
    audioMediaIds = [],
    firstFrameMediaId,
    lastFrameMediaId,
    params = {},
  }) {
    const model = await this.findModel(publicModelId, "VIDEO");
    const body = {
      publicModelId,
      routingMode,
      prompt,
      imageMediaIds,
      videoMediaIds,
      audioMediaIds,
      params,
      pricingSnapshot: AiHiveClient.pricingSnapshot(model, routingMode),
    };
    if (firstFrameMediaId) body.firstFrameMediaId = firstFrameMediaId;
    if (lastFrameMediaId) body.lastFrameMediaId = lastFrameMediaId;
    return this.request("POST", "generation/video", { body });
  }

  getTask(taskId) {
    return this.request("GET", `generation/tasks/${encodeURIComponent(taskId)}`);
  }

  async waitTask(taskId, { timeoutSeconds = 600, intervalMs = 3000 } = {}) {
    const deadline = Date.now() + timeoutSeconds * 1000;
    while (Date.now() < deadline) {
      const task = await this.getTask(taskId);
      const items = task?.items || [];
      if (items.length && items.every((item) => TERMINAL_STATUSES.has(String(item.status)))) return task;
      await new Promise((resolve) => setTimeout(resolve, intervalMs));
    }
    throw new AiHiveApiError(`等待任务超时。任务仍可继续运行，请稍后查询：${taskId}`);
  }
}


export function summarizeTask(task) {
  const items = task?.items || [];
  const statuses = items.map((item) => String(item.status || "UNKNOWN"));
  let status = String(task?.status || "RUNNING");
  if (items.length && statuses.every((item) => item === "COMPLETED")) status = "COMPLETED";
  else if (items.length && statuses.every((item) => TERMINAL_STATUSES.has(item))) {
    status = statuses.includes("COMPLETED") ? "PARTIAL" : "FAILED";
  } else if (new Set(statuses).size === 1) status = statuses[0];

  return {
    task_id: String(task?.taskId || task?.id || ""),
    task_type: String(task?.taskType || ""),
    status,
    result_urls: items
      .filter((item) => item.status === "COMPLETED" && item.resultUrl)
      .map((item) => String(item.resultUrl)),
    last_frame_urls: items.filter((item) => item.lastFrameUrl).map((item) => String(item.lastFrameUrl)),
    errors: items
      .filter((item) => item.status === "FAILED" && item.errorMessage)
      .map((item) => String(item.errorMessage)),
  };
}


export function videoModelId(family, mode, customPublicModelId = "") {
  if (customPublicModelId) {
    if (!customPublicModelId.startsWith("public_model_")) {
      throw new AiHiveApiError("custom_public_model_id 应以 public_model_ 开头。");
    }
    return customPublicModelId;
  }
  const mapping = {
    "seedance_2_5:t2v": "public_model_seedance_2_5_t2v",
    "seedance_2_5:i2v": "public_model_seedance_2_5_i2v",
    "seedance_2_5:r2v": "public_model_seedance_2_5_r2v",
    "seedance_2_5:edit": "public_model_seedance_2_5_video_edit",
    "seedance_2_5:extend": "public_model_seedance_2_5_video_extend",
    "minimax_h3:t2v": "public_model_minimax_h3_t2v",
    "minimax_h3:i2v": "public_model_minimax_h3_i2v",
    "minimax_h3:r2v": "public_model_minimax_h3_r2v",
    "happyhorse:t2v": "public_model_happyhorse_t2v",
    "happyhorse:i2v": "public_model_happyhorse_i2v",
    "happyhorse:r2v": "public_model_happyhorse_r2v",
    "happyhorse:edit": "public_model_happyhorse_video_edit",
  };
  const model = mapping[`${family}:${mode}`];
  if (!model) throw new AiHiveApiError("所选模型系列暂不支持该视频模式。");
  return model;
}
