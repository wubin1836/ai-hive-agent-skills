# Grok4.6数据讲解交互网页制作：场景示例

## 场景一：首次执行

```text
用Grok4.6把这份渠道数据做成本地交互页面，让同事按渠道查看订单、客单价和收入。保留公式和来源，空筛选要有提示，不连外网、不上线；交HTML代码及真实或待运行的测试记录。
```

输入记录示例：

```json
{
  "data": [
    {
      "channel": "直营网店",
      "orders": 10,
      "average_order_value": 80
    },
    {
      "channel": "线下",
      "orders": 0,
      "average_order_value": null
    }
  ],
  "formula": "收入=订单数×客单价",
  "publish": false
}
```

人工构造的输出片段，仅用于解释格式；不是付费模型生成结果或测试成绩：

```json
{
  "illustrative_only": true,
  "sample": {
    "example_only": true,
    "mode": "人工演示，未调用真实模型",
    "computed_example": {
      "channel": "直营网店",
      "revenue": 800,
      "unit": "元"
    },
    "empty_state": "所选渠道无有效数据",
    "browser_test": "待运行",
    "files": [
      "index.html",
      "data-sources.csv",
      "page-validation.md"
    ]
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：页面数字可根据给定公式和源数据复算；无数据与零值状态不会生成误导图形或无穷值；样例数据与真实数据在页面明确区分；未执行浏览器测试时不写已验证兼容性。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
