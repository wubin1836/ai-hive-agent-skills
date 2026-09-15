# Fable PDF资料对照助手：场景示例

## 场景一：首次执行

```text
用Fable5.1对照设备手册V2.pdf和V3.pdf，重点看电源、温度范围和保修条款。每个变化给两边页码，扫描文字看不清就标待确认，别把重新分页算实质变化。
```

输入记录示例：

```json
{
  "files": [
    "设备手册V2.pdf",
    "设备手册V3.pdf"
  ],
  "baseline": "V2",
  "fields": [
    "电源",
    "温度范围",
    "保修条款"
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
    "differences": [
      {
        "field": "温度范围",
        "old": "0至40℃",
        "new": "0至45℃",
        "old_page": 7,
        "new_page": 9,
        "classification": "参数变化",
        "visual_verified": false
      }
    ],
    "uncertain": [
      "V3第12页保修脚注OCR待复核"
    ]
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：每项实质变化能回到两份文件的具体页；OCR未确认文字不能当成确定事实；数字差异同时比较单位及时间口径；排版变化与内容变化分开统计。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
