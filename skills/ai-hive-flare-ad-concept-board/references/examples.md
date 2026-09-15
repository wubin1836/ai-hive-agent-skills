# Flare广告生图与三案创意比较：场景示例

## 场景一：首次执行

```text
用GPT Image2.5 Flare为便携咖啡杯做三张无字广告概念：通勤、露营、桌面。保持同一杯型和4:3比例，先确认三张总预算，别替我投放。
```

输入记录示例：

```json
{
  "product": "便携咖啡杯",
  "concepts": [
    "通勤",
    "露营",
    "桌面"
  ],
  "ratio": "4:3",
  "text": "无字",
  "count": 3
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
      "ad-concepts.png",
      "ad-concepts.json",
      "ad-comparison.csv"
    ],
    "concept_ids": [
      "A-commute",
      "B-camping",
      "C-desk"
    ],
    "performance_tested": false
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：三案有明确不同的创意假设；所有图遵守同一事实和品牌约束；案号、原图路径与任务ID不混淆；没有虚构投放数据或效果承诺。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
