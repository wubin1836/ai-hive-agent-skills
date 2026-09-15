# MiniMax Music 3.0段落编曲助手：场景示例

## 场景一：首次执行

```text
用MiniMax Music3.0做45秒纯器乐，前10秒钢琴，10到30秒加入鼓和贝斯，最后15秒减回钢琴，给我实际乐器变化点。
```

输入记录示例：

```json
{
  "total_seconds": 45,
  "sections": [
    {
      "range": [
        0,
        10
      ],
      "instruments": [
        "钢琴"
      ]
    },
    {
      "range": [
        10,
        30
      ],
      "instruments": [
        "钢琴",
        "鼓",
        "贝斯"
      ]
    },
    {
      "range": [
        30,
        45
      ],
      "instruments": [
        "钢琴"
      ]
    }
  ],
  "vocals": false
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
      "minimax-arrangement.wav",
      "minimax-arrangement-map.csv",
      "minimax-arrangement-task.json"
    ],
    "acceptance_plan": {
      "total_seconds": 45,
      "transitions": [
        10,
        30
      ],
      "final_instruments": [
        "钢琴"
      ]
    },
    "actual_transition_seconds": null
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：曲式顺序和重要乐器变化可以实听确认；目标段界与实际段界偏差已列明；结尾无未披露硬截断；未把音频整曲称为MIDI、乐谱或多轨工程。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
