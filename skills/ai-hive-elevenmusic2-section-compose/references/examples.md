# Eleven Music v2分段作曲助手：场景示例

## 场景一：首次执行

```text
用ElevenMusicv2做一首60秒器乐，10秒前奏、20秒主段、20秒变化段和10秒结尾，变化段加弦乐，给我实际段界而不是只给计划。
```

输入记录示例：

```json
{
  "sections": [
    {
      "name": "intro",
      "seconds": 10
    },
    {
      "name": "theme",
      "seconds": 20
    },
    {
      "name": "variation",
      "seconds": 20,
      "add": "弦乐"
    },
    {
      "name": "outro",
      "seconds": 10
    }
  ],
  "vocals": false,
  "reference_audio": null
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
      "eleven-section-song.wav",
      "eleven-section-map.csv",
      "eleven-section-task.json"
    ],
    "acceptance_plan": {
      "section_order": [
        "intro",
        "theme",
        "variation",
        "outro"
      ],
      "total_seconds": 60
    },
    "measured_boundaries": null
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：段落顺序与重复规则符合确认计划；各段目标时长和实测偏差已列明；参考音频来源与允许使用范围可追溯；整曲、切段和分轨的交付类型不混淆。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
