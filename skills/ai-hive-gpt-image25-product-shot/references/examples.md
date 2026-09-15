# GPT Image 2.5商品图制作：场景示例

## 场景一：首次执行

```text
用GPT Image 2.5给SKU CUP-01做一张咖啡桌商品图，保留杯盖、杯把和原有logo，旁边可以有书，不加文字和认证标。请先核对参考图，不要自动上传店铺。
```

输入记录示例：

```json
{
  "sku": "CUP-01",
  "references": [
    "cup-front.png",
    "cup-detail.png"
  ],
  "physical_height_cm": 12,
  "scene": "咖啡桌与一本书",
  "forbidden": [
    "新logo",
    "认证标",
    "价格字样"
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
      "product-scene.png",
      "product-fidelity.json",
      "product-task.json"
    ],
    "review_items": [
      "杯盖和杯把形状",
      "标识原样",
      "接地阴影",
      "相对比例"
    ]
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：SKU与全部参考图绑定正确；部件数量、主体轮廓和可见标识不被随意改写；无悬浮或明显穿插，商品比例符合确认规格；未增加用户未提供的功能、认证或价格。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
