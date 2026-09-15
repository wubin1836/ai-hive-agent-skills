# Fable Excel表格修改助手：场景示例

## 场景一：首次执行

```text
用Fable5.1检查销售汇总.xlsx，九月总额比明细少。只允许修改汇总页D2:D20，保留原表和公式，给我副本、单元格差异及实际重算证据；无法计算的要列明。
```

输入记录示例：

```json
{
  "file": "销售汇总.xlsx",
  "editable_range": "汇总!D2:D20",
  "protected_sheets": [
    "原始明细"
  ],
  "expected_total": 128400
}
```

人工构造的输出片段，仅用于解释格式；不是付费模型生成结果或测试成绩：

```json
{
  "illustrative_only": true,
  "sample": {
    "example_only": true,
    "execution_status": "人工示例，未执行",
    "proposed_changes": [
      {
        "cell": "汇总!D20",
        "before": "=SUM(D2:D18)",
        "after": "=SUM(D2:D19)",
        "reason": "末行未计入"
      }
    ],
    "recalculation_status": "待宿主计算引擎验证",
    "original_preserved": true
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：原工作簿未覆盖且保护区域无变化；每处修改有工作表、单元格、旧值和新值；公式未无故替换成静态数值；未实际重算不能宣称公式验证通过。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
