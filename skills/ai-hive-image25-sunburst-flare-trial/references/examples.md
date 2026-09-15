# Image2.5同题试图与Sunburst和Flare选择：场景示例

## 场景一：首次执行

```text
我想知道Sunburst和Flare哪个更适合这张产品图的换背景任务。先查两者是否都支持，只各试一张，预算先问我，按杯型保真和背景自然度比较，不猜价格。
```

输入记录示例：

```json
{
  "task": "产品图换背景",
  "models": [
    "gpt-image-2.5-sunburst",
    "gpt-image-2.5-flare"
  ],
  "trials_per_model": 1,
  "criteria": [
    "杯型保真",
    "背景自然度"
  ],
  "source": "cup.png"
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
      "image25-model-comparison.png",
      "image25-trials.csv",
      "image25-choice.md"
    ],
    "comparison_status": "演示结构，未执行比较",
    "cost": null,
    "latency": null,
    "winner": null
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：实际模型ID和输入版本可追溯；比较规格差异被明确披露；失败、超时和未知费用未被隐藏；结论只覆盖实际测试任务和样本规模。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
