# Sunburst色卡换色与商品色差核对：场景示例

## 场景一：首次执行

```text
用Sunburst把这张沙发图的布面改成我色卡里的C17苔绿，木腿和房间不变。先做一张，给我原图与改色图的对照，不要说等同实物颜色。
```

输入记录示例：

```json
{
  "source": "sofa.png",
  "swatch": "C17.png",
  "sku": "SOFA-C17",
  "editable_material": "布面",
  "locked": [
    "木腿",
    "房间",
    "缝线"
  ],
  "count": 1
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
      "color-samples.png",
      "color-map.csv",
      "color-review.json"
    ],
    "mapping_preview": {
      "sku": "SOFA-C17",
      "swatch": "C17",
      "result": "expected-sofa-c17.png"
    },
    "color_certification": false
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：每个SKU和色卡编号唯一对应；logo、五金与背景未被连带换色；纹理与原有明暗层次可辨；任何色差数值都有真实测量方法与采样依据。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
