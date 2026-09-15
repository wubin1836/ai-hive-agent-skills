# OpenRouter Fusion 方案分歧证据评审：场景示例

## 场景一：首次执行

```text
评审我们应先做站内搜索还是知识库问答，用相同的三个月资源约束比较，保留分歧和证据。先核验 Fusion 可用性并给成本方案；不要把多个模型赞同当成事实。
```

输入记录示例：

```json
{
  "options": [
    "站内搜索",
    "知识库问答"
  ],
  "team": "2名工程师",
  "deadline": "3个月",
  "decision_basis": [
    "资料可用性",
    "维护成本",
    "用户任务完成率"
  ],
  "execute": false
}
```

人工构造的输出片段，仅用于解释格式；不是付费模型生成结果或测试成绩：

```json
{
  "illustrative_only": true,
  "sample": {
    "example": true,
    "execution_status": "plan_only",
    "key_disagreement": "现有资料是否足以支持可靠问答",
    "required_evidence": [
      "授权资料样本",
      "用户查询失败记录"
    ],
    "decision": null
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：保留面板间的分歧和少数有效意见；关键事实能追溯到原始来源；多模型一致不等同于事实已验证；明确原生 Fusion、替代编排或仅方案的实际执行模式。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
