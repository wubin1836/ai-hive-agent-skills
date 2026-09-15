# FLUX 3 Video多关键帧视频制作助手：场景示例

## 场景一：首次执行

```text
用FLUX3Video把盒子闭合、打开、取出耳机这三张图做成演示短片，依次完成三个动作，不要把盒子变形，先确认实际关键帧上限。
```

输入记录示例：

```json
{
  "keyframes": [
    "box-closed.png",
    "box-open.png",
    "earbuds-out.png"
  ],
  "sequence": [
    "闭合",
    "打开",
    "取出"
  ],
  "duration_seconds": 8,
  "audio": "轻微开盒声，无旁白",
  "max_attempts": 1
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
      "flux-keyframes.mp4",
      "flux-keyframe-review.csv",
      "flux-keyframe-tasks.json"
    ],
    "acceptance_plan": {
      "keyframe_count": 3,
      "action_order": [
        "闭合",
        "打开",
        "取出"
      ],
      "review_points": "按真实输出对齐"
    },
    "segment_count": "待能力发现"
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：全部关键帧纳入计划且无静默丢帧；核心动作按确认顺序发生；关键时点主体外观及空间关系可对照；原生结果与宿主拼接处理分别记录。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
