# 缓存命中与模型账单核对助手：场景示例

## 场景一：首次执行

```text
请用我提供的调用明细、缓存字段说明和当天价目表复算模型账单，分别列普通输入、缓存读写和输出费用，把缺证据的差额单独列出来，不替我提交申诉。
```

输入记录示例：

```json
{
  "mode": "演示数据",
  "input_total": 10000,
  "cache_read_included": 8000,
  "cache_write": 0,
  "input_price_per_million": 1,
  "cache_read_price_per_million": 0.1,
  "currency": "演示币"
}
```

人工构造的输出片段，仅用于解释格式；不是付费模型生成结果或测试成绩：

```json
{
  "illustrative_only": true,
  "sample": {
    "mode": "人工演示，仅复算所给数字",
    "ordinary_input": 2000,
    "ordinary_cost": 0.002,
    "cache_read_cost": 0.0008,
    "input_subtotal": 0.0028,
    "excludes": [
      "未提供的输出用量",
      "税费与折扣"
    ]
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：输入与缓存是否重叠已明确，避免重复计费计算。；使用的是对应日期和版本的价格，不套用最新价。；未知字段和折扣单独列示，不补造金额。；合计能从逐项公式复算，币种不混加。。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
