# Fable企业知识库整理助手：场景示例

## 场景一：首次执行

```text
用Fable5.1整理这些售后制度和FAQ，输出可导入知识条目。售后人员和经销商的口径要分开，保留来源和有效期；两版制度冲突不要替我决定，另给问答测试集。
```

输入记录示例：

```json
{
  "files": [
    "售后制度2026.pdf",
    "经销商FAQ.docx"
  ],
  "audiences": [
    "售后人员",
    "经销商"
  ],
  "fields": [
    "question",
    "answer",
    "source",
    "audience",
    "valid_until"
  ]
}
```

人工构造的输出片段，仅用于解释格式；不是付费模型生成结果或测试成绩：

```json
{
  "illustrative_only": true,
  "sample": {
    "example_only": true,
    "execution_status": "人工示例，未执行",
    "item": {
      "id": "KB-014",
      "question": "退件需要哪些资料",
      "answer": "需提供订单号与故障说明",
      "source": "经销商FAQ.docx#退件流程",
      "audience": "经销商",
      "valid_until": null
    },
    "review_reason": "有效期未提供",
    "online_import": "未执行"
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：每条答案有原始资料定位和适用范围；未提供的制度、负责人和有效期不编造；冲突版本未静默合并成新制度；测试集中包含无法回答时应说明缺证据的情形。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
