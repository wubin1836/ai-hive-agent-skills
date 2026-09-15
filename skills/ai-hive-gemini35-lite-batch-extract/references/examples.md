# Gemini3.5 Flash Lite批量字段抽取：场景示例

## 场景一：首次执行

```text
用Gemini3.5 Flash Lite从这批询价文本抽取record_id、型号、数量和期望交期。缺失填null，每个非空字段保留原文证据；先试10条，最多本轮预算内运行，不自动重试失败行。
```

输入记录示例：

```json
{
  "records": [
    {
      "id": "R1",
      "text": "想询价A20，共12台，交期还没定。"
    }
  ],
  "schema": {
    "model": "string|null",
    "quantity": "integer|null",
    "delivery_date": "string|null"
  }
}
```

人工构造的输出片段，仅用于解释格式；不是付费模型生成结果或测试成绩：

```json
{
  "illustrative_only": true,
  "sample": {
    "example_only": true,
    "mode": "人工演示，未调用真实模型",
    "records": [
      {
        "record_id": "R1",
        "model": "A20",
        "quantity": 12,
        "delivery_date": null
      }
    ],
    "evidence": {
      "R1": {
        "model": "A20",
        "quantity": "共12台",
        "delivery_date": "交期还没定，保持null"
      }
    },
    "files": [
      "extracted-records.jsonl",
      "extraction-errors.csv",
      "field-evidence.json"
    ]
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：输入ID与成功、失败及未处理记录总数一致；缺失值按规则表示而非补出看似合理的数据；格式通过和内容证据通过分别统计；遇预算上限或不明错误不继续自动请求。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
