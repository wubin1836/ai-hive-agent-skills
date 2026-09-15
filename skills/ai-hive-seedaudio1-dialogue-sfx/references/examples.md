# Seed Audio 1.0对白音效制作助手：场景示例

## 场景一：首次执行

```text
用Seed Audio1.0做10秒咖啡店短剧声音：店员说欢迎光临，客人说一杯拿铁，杯碟轻响不要盖住台词，用原创声音。
```

输入记录示例：

```json
{
  "duration_seconds": 10,
  "dialogue": [
    {
      "role": "店员",
      "text": "欢迎光临",
      "target_start": 1
    },
    {
      "role": "客人",
      "text": "一杯拿铁",
      "target_start": 4
    }
  ],
  "sfx": [
    "轻微杯碟声"
  ],
  "ambience": "安静咖啡店",
  "voice_source": "原创描述"
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
      "seed-dialogue-scene.wav",
      "seed-dialogue-events.csv",
      "seed-dialogue-task.json"
    ],
    "acceptance_plan": {
      "dialogue_lines": 2,
      "roles": [
        "店员",
        "客人"
      ],
      "masking_check": "杯碟声不得盖词"
    },
    "stem_availability": "not_assumed"
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：每句确认台词都有实听结果或缺失标记；角色轮次正确且没有未经授权的音色模仿；音效没有遮盖核心台词；混合音频与可用分轨状态明确区分。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
