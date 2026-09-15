# Seedream 5.0 Pro商品图精修助手：场景示例

## 场景一：首次执行

```text
用Seedream5.0Pro修一下这张保温杯图的过曝反光，只处理杯身右侧，杯盖、刻度和商标都别改，只出一张。
```

输入记录示例：

```json
{
  "sku": "CUP-DEMO-08",
  "source_image": "cup-overexposed.png",
  "edit_region": "杯身右侧高光",
  "locked": [
    "杯盖",
    "刻度",
    "商标"
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
      "seedream-product-retouched.png",
      "seedream-product-diff.json",
      "seedream-product-task.json"
    ],
    "acceptance_plan": {
      "sku": "CUP-DEMO-08",
      "target_region": "杯身右侧",
      "protected_items": 3
    },
    "comparison_status": "awaiting_actual_images"
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：SKU与原图对应且结构数量未被改变；标签文字与用户确认原文一致或明确标为不合格；只改变授权区域并披露越界变化；文件尺寸和精修任务ID可核对。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
