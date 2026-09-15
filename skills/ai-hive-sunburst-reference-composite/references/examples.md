# Sunburst多参考图合成与元素归属核对：场景示例

## 场景一：首次执行

```text
用Sunburst把REF1的台灯和REF2的笔记本放进REF3的书房，台灯在左、笔记本在右，不使用REF3里的品牌标识。先给我元素归属表，再生成一张横图。
```

输入记录示例：

```json
{
  "references": [
    {
      "id": "REF1",
      "file": "lamp.png",
      "role": "台灯外观"
    },
    {
      "id": "REF2",
      "file": "notebook.png",
      "role": "笔记本外观"
    },
    {
      "id": "REF3",
      "file": "study.png",
      "role": "房间布局"
    }
  ],
  "layout": "台灯左、笔记本右",
  "exclude": [
    "REF3品牌标识"
  ]
}
```

人工构造的输出片段，仅用于解释格式；不是付费模型生成结果或测试成绩：

```json
{
  "illustrative_only": true,
  "sample": {
    "demo_only": true,
    "generation_status": "not_submitted",
    "actual_model": null,
    "task_id": null,
    "expected_files": [
      "reference-composite.png",
      "reference-map.csv",
      "composite-review.json"
    ],
    "mapping_preview": {
      "台灯": "REF1",
      "笔记本": "REF2",
      "房间": "REF3"
    }
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：每个输出主体可追溯到批准的参考编号；主体数量与布局一致，无意外混合对象；前后遮挡与接触关系合理；未使用明确排除的商标、人物或背景元素。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
