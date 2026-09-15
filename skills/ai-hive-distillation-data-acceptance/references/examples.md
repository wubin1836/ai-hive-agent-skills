# 模型蒸馏样本与师生对照验收助手：场景示例

## 场景一：首次执行

```text
我想让小模型处理固定产品分类。请检查教师生成的样本能否用于训练，剔除错误和测试集重复项，整理候选数据及师生验收门槛，现在不启动训练。
```

输入记录示例：

```json
{
  "mode": "演示数据",
  "teacher_samples": [
    {
      "id": "t1",
      "label": "配件",
      "verified_label": "主机"
    }
  ],
  "training_use_permission": "已核验",
  "student_trained": false
}
```

人工构造的输出片段，仅用于解释格式；不是付费模型生成结果或测试成绩：

```json
{
  "illustrative_only": true,
  "sample": {
    "mode": "人工演示，未训练模型",
    "quarantined": [
      {
        "id": "t1",
        "reason": "教师标签与已核验标签冲突"
      }
    ],
    "student_result": null,
    "training_started": false
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：教师输出使用许可已明确，保留题未泄漏。；教师答案中的错误经过识别而非直接复制。；样本格式与目标训练方式相符。；未训练的学生不被标成蒸馏模型，未测结果留空。。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
