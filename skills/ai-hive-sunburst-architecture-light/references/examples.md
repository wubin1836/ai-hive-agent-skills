# Sunburst建筑效果改图与日夜光照方案：场景示例

## 场景一：首次执行

```text
用Sunburst把这张咖啡馆白天照片做成暖光夜景方案，门窗和招牌文字完全照原图，新增灯只做示意，不要改建筑结构或给施工结论。
```

输入记录示例：

```json
{
  "source": "cafe-day.png",
  "time": "夜晚",
  "lighting": "暖色入口与室内透光",
  "locked": [
    "门窗数量",
    "招牌文字",
    "立面分格"
  ],
  "purpose": "灯光视觉方案"
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
      "architecture-night.png",
      "facade-preservation.csv",
      "lighting-concept.json"
    ],
    "engineering_certification": false,
    "locked_review": [
      "门窗",
      "招牌",
      "立面"
    ]
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：门窗、楼层、栏杆数量与原图一致；建筑竖线及立面结构无明显变形；招牌文字无未授权修改；不附虚构照度、能耗或施工合规数值。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
