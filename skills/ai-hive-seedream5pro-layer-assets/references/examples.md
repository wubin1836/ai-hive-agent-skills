# Seedream 5.0 Pro图层资产整理助手：场景示例

## 场景一：首次执行

```text
用Seedream5.0Pro把这张礼盒设计里的盒子、丝带和背景分开整理，保留原画布坐标，哪些被遮挡区域是补出来的要标清，不要假装导出了PSD。
```

输入记录示例：

```json
{
  "source_image": "gift-layout.png",
  "elements": [
    "礼盒",
    "丝带",
    "背景"
  ],
  "canvas": [
    1600,
    1200
  ],
  "allow_inpaint": [
    "丝带后方盒面"
  ],
  "requested_format": "带透明通道的可用资产"
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
      "seedream-layer-assets.zip",
      "seedream-layer-map.json",
      "seedream-layer-review.json"
    ],
    "acceptance_plan": {
      "element_ids": [
        "box",
        "ribbon",
        "background"
      ],
      "coordinate_space": [
        1600,
        1200
      ],
      "psd_promised": false
    },
    "missing_assets": "待真实任务检查"
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：每个资产有原图来源和唯一元素编号；透明通道通过实际文件检查而非背景颜色猜测；复合关系与原图可对照且缺层明确；推测补全和原图可见内容分别标记。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
