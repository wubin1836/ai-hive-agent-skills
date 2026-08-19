import assert from "node:assert/strict";
import test from "node:test";

import { AiHiveApiError, summarizeTask, videoModelId } from "../src/ai-hive-client.js";


test("summarizeTask returns completed URLs", () => {
  const summary = summarizeTask({
    taskId: "task-1",
    taskType: "IMAGE",
    items: [
      { status: "COMPLETED", resultUrl: "https://example.com/a.png" },
      { status: "COMPLETED", resultUrl: "https://example.com/b.png" },
    ],
  });
  assert.equal(summary.status, "COMPLETED");
  assert.deepEqual(summary.result_urls, ["https://example.com/a.png", "https://example.com/b.png"]);
});

test("summarizeTask reports partial failure", () => {
  const summary = summarizeTask({
    id: "task-2",
    items: [
      { status: "COMPLETED", resultUrl: "https://example.com/a.mp4" },
      { status: "FAILED", errorMessage: "failed" },
    ],
  });
  assert.equal(summary.status, "PARTIAL");
  assert.deepEqual(summary.errors, ["failed"]);
});

test("videoModelId resolves known modes", () => {
  assert.equal(videoModelId("seedance_2_5", "extend"), "public_model_seedance_2_5_video_extend");
  assert.equal(videoModelId("minimax_h3", "i2v"), "public_model_minimax_h3_i2v");
});

test("videoModelId rejects unsupported modes", () => {
  assert.throws(() => videoModelId("minimax_h3", "edit"), AiHiveApiError);
});
