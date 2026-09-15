# GPT6数据分析助手：多表核对与归因：场景示例

## 场景一：首次执行

```text
用GPT6核对订单表和退款表，计算净收入，分开解释真实结果和可能原因，给我复算脚本。
```

输入记录示例：

```json
{
  "orders": "orders.csv",
  "refunds": "refunds.csv",
  "join_key": "order_id"
}
```

人工构造的输出片段，仅用于解释格式；不是付费模型生成结果或测试成绩：

```json
{
  "illustrative_only": true,
  "sample": {
    "example_only": true,
    "metrics_status": "待计算",
    "unmatched_rows": [],
    "hypotheses": []
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：每个数值可复算；异常连接不静默丢行；不把相关性冒充因果。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
