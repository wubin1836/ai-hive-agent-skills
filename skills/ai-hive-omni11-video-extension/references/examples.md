# Gemini Omni 1.1 Flash视频续写助手：场景示例

## 场景一：首次执行

```text
用Gemini Omni 1.1 Flash把这个杯子被端起的短片接着延长，继续放回桌面，杯型、灯光和机位不变。先确认实际续写模式与费用，再给我接缝检查。
```

输入记录示例：

```json
{
  "source_video": "cup-lift.mp4",
  "continue_action": "手把杯子放回原位",
  "target_extra_seconds": 4,
  "locked": [
    "杯型",
    "固定机位",
    "暖灯"
  ],
  "audio_policy": "保留原声并检查接缝",
  "spend_authorization": "pending"
}
```

人工构造的输出片段，仅用于解释格式；不是付费模型生成结果或测试成绩：

```json
{
  "illustrative_only": true,
  "sample": {
    "demo_only": true,
    "generation_status": "not_submitted",
    "actual_model": null,
    "task_id": null,
    "expected_files": [
      "omni-extension.mp4",
      "omni-seam-review.json",
      "omni-extension-task.json"
    ],
    "acceptance_plan": {
      "seam_ref": "原视频末帧时间码",
      "target_extra_seconds": 4,
      "locked_count": 3
    },
    "review_status": "awaiting_real_video"
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：原视频未覆盖且续写时长落在确认范围内；接缝处主体朝向与主要动作连续；背景固定物和光线无未披露明显突变；音轨处理方式及真实任务ID可追溯。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
