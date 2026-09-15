# Seedream 5.0 Pro多语言海报制作助手：场景示例

## 场景一：首次执行

```text
用Seedream5 Pro做这张活动海报的中英双语独立版本，价格和日期不变，先让我确认英文文案，再逐字校对成图。
```

输入记录示例：

```json
{
  "base_poster": "sale-cn.png",
  "languages": [
    "zh-CN",
    "en"
  ],
  "locked_values": {
    "price": "¥199",
    "date": "2026-10-08"
  },
  "approved_copy": {
    "headline_cn": "秋日上新",
    "headline_en": "Autumn Arrivals"
  },
  "size": "1080x1440"
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
      "seedream-posters.zip",
      "seedream-copy-proof.csv",
      "seedream-poster-tasks.json"
    ],
    "acceptance_plan": {
      "versions": [
        "zh-CN",
        "en"
      ],
      "locked_values": {
        "price": "¥199",
        "date": "2026-10-08"
      },
      "proof_required": [
        "价格",
        "日期",
        "标题"
      ]
    }
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：每个语言版本与确认文案一一对应；币种、日期、单位和数字无未经确认改写；正文可读且没有截断、乱码或被遮挡；压缩包仅含实际已生成文件并标明未过审版本。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
