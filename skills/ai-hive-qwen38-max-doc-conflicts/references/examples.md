# 千问Qwen3.8-Max-0902企业资料冲突对照：场景示例

## 场景一：首次执行

```text
用Qwen3.8-Max-0902对照我提供的三份产品资料，只核对保修期、配送费和退换条件。按生效日期区分版本，每处矛盾给两段原文位置；没有明确优先级的请留给产品负责人确认。
```

输入记录示例：

```json
{
  "documents": [
    {
      "file": "产品说明v2.md",
      "effective": "2026-09-01",
      "text": "整机保修24个月；配件保修6个月。"
    },
    {
      "file": "销售手册.md",
      "effective": "2026-09-01",
      "text": "产品及全部配件均保修24个月。"
    }
  ],
  "authority_rule": null
}
```

人工构造的输出片段，仅用于解释格式；不是付费模型生成结果或测试成绩：

```json
{
  "illustrative_only": true,
  "sample": {
    "example_only": true,
    "mode": "人工演示，未调用真实模型",
    "conflicts": [
      {
        "item": "配件保修期",
        "left": "6个月",
        "right": "24个月",
        "sources": [
          "产品说明v2.md#第1段",
          "销售手册.md#第1段"
        ],
        "decision": "待产品负责人确认，暂不统一"
      }
    ],
    "files": [
      "conflicts.csv",
      "aligned-wording.md",
      "source-index.json"
    ]
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：每条冲突至少有两个可定位的原文证据；不同适用期的数值不误报为同期矛盾；未获确认的条款不写成已生效结论；数值、单位及例外条件能逐条回查。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
