# LoRA训练数据准备与泄漏检查助手：场景示例

## 场景一：首次执行

```text
请整理这批售后知识问答用于LoRA试验，按原始文档分组划分训练和验证集，查重复、错误标签与个人信息。只生成候选数据和验收报告，不上传或训练。
```

输入记录示例：

```json
{
  "mode": "演示数据",
  "samples": [
    {
      "id": "s1",
      "source_group": "docA",
      "text": "支持七天退货"
    },
    {
      "id": "s2",
      "source_group": "docA",
      "text": "七天内可退货"
    }
  ],
  "license_verified": true
}
```

人工构造的输出片段，仅用于解释格式；不是付费模型生成结果或测试成绩：

```json
{
  "illustrative_only": true,
  "sample": {
    "mode": "人工演示，未训练模型",
    "near_duplicate_group": [
      "s1",
      "s2"
    ],
    "split_rule": "docA整体留在同一集合",
    "training_started": false
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：训练许可不明和敏感样本未混入可训练集合。；同来源近重复样本不跨训练与验证集合。；格式和聊天模板与目标框架一致。；没有训练日志时不报告训练效果或权重产出。。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
