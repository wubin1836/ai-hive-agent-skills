# Seed Audio 1.0场景环境声助手：场景示例

## 场景一：首次执行

```text
用Seed Audio1.0做20秒安静书店环境声，远处轻翻页、近处偶尔放杯子，没有人声和音乐；先出非循环版，不要自动帮我做视频。
```

输入记录示例：

```json
{
  "scene": "安静书店室内",
  "duration_seconds": 20,
  "layers": {
    "base": "轻微室内底噪",
    "far": [
      "翻页"
    ],
    "near": [
      "放杯子"
    ]
  },
  "forbidden": [
    "人声",
    "音乐"
  ],
  "loop": false
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
      "seed-ambience.wav",
      "seed-ambience-review.json",
      "seed-ambience-task.json"
    ],
    "acceptance_plan": {
      "duration_seconds": 20,
      "forbidden": [
        "人声",
        "音乐"
      ],
      "loop_required": false
    },
    "audio_layers": "混合音频，未承诺分轨"
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：实际音频中没有未授权的对白或音乐；持续声与偶发声符合场景空间关系；时长及循环状态经过实听实测；输入文本说明与实际模型接入方式明确。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
