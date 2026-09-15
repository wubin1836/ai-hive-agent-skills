# 豆包Seed2.1 Turbo工单归并与异常分流：场景示例

## 场景一：首次执行

```text
用豆包Seed2.1 Turbo整理这批脱敏售后记录，抽取订单号、诉求和状态。只把同订单同事件标为疑似重复，缺订单号或内容冲突的进入人工队列；先给待导入CSV，不写客服系统。
```

输入记录示例：

```json
{
  "records": [
    {
      "id": "T01",
      "order": "A100",
      "text": "包裹漏发充电线，请补发。"
    },
    {
      "id": "T02",
      "order": "A101",
      "text": "包裹漏发充电线。"
    },
    {
      "id": "T03",
      "order": null,
      "text": "还没收到补发件。"
    }
  ],
  "required_fields": [
    "order",
    "request"
  ]
}
```

人工构造的输出片段，仅用于解释格式；不是付费模型生成结果或测试成绩：

```json
{
  "illustrative_only": true,
  "sample": {
    "example_only": true,
    "mode": "人工演示，未调用真实模型",
    "accounting": {
      "input": 3,
      "draft": 2,
      "manual_review": 1
    },
    "duplicates": [],
    "manual_review": [
      {
        "id": "T03",
        "reason": "缺订单号，不能与其他记录归并"
      }
    ],
    "files": [
      "tickets-draft.csv",
      "duplicate-candidates.json",
      "manual-review.csv"
    ]
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：每条输入记录都有输出或明确异常去向；不同客户或订单不因文本相似自动合并；未提及的退款、优先级和承诺不被编造；批量错误计数可对账，未自动联系客户或写CRM。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
