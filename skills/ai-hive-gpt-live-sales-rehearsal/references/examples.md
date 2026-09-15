# GPT Live销售演练与语音复盘方案：场景示例

## 场景一：首次执行

```text
设计GPT Live的SaaS销售模拟客户，客户担心数据迁移；练后评我是否问清现状，不许承诺零风险。
```

输入记录示例：

```json
{
  "objection": "迁移风险",
  "forbidden": [
    "零风险"
  ]
}
```

人工构造的输出片段，仅用于解释格式；不是付费模型生成结果或测试成绩：

```json
{
  "illustrative_only": true,
  "sample": {
    "example_only": true,
    "trigger": "提及数据丢失",
    "response_goal": "询问备份与测试方案",
    "real_calls": false
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：反馈有对话证据；禁止编造效果保证；演练不发给真实客户。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
