# 万相3视频续接与片尾接缝检查：场景示例

## 场景一：首次执行

```text
用万相3把这段机器人走向门口的视频向后续6秒，让它开门走出，原片不要改。保持机器人外观和运动方向，给我接缝前后检查，不要自动再延长第二次。
```

输入记录示例：

```json
{
  "source": "robot-door.mp4",
  "extend_direction": "forward",
  "additional_seconds": 6,
  "next_action": "开门走出",
  "locked": [
    "机器人外观",
    "行走方向"
  ],
  "max_rounds": 1
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
      "wan3-extension.mp4",
      "wan3-joined.mp4",
      "wan3-seam-review.json"
    ],
    "seam_review_plan": [
      "位置",
      "外观",
      "运动",
      "音轨"
    ],
    "measured_extension_seconds": null
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：原片未被覆盖且续接点可定位；新增时长有真实探测结果；接缝处主体状态与运动方向可连续理解；音轨断裂、身份漂移和闪变均被记录。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
