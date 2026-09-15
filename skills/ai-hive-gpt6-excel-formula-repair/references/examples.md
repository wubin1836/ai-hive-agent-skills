# GPT6 Excel表格公式修复助手：场景示例

## 场景一：首次执行

```text
用GPT6检查销售表的合计为什么不对，先用三行样本复算，确认后只改汇总公式并保留原文件。
```

输入记录示例：

```json
{
  "file": "销售.xlsx",
  "cell": "汇总!F10",
  "expected": 1200
}
```

人工构造的输出片段，仅用于解释格式；不是付费模型生成结果或测试成绩：

```json
{
  "illustrative_only": true,
  "sample": {
    "example_only": true,
    "suspected": "文本数字未参与求和",
    "patch_applied": false,
    "baseline": 1200
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：关键样例复算通过；不自动运行宏或外部链接；未授权工作表未变更。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
