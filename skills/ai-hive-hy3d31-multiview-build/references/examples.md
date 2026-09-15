# 混元 3D 3.1多视图建模助手：场景示例

## 场景一：首次执行

```text
用混元3D3.1根据这组同一茶壶的四个方向照片建模，先确认支持多视图。看不见的底部标成推测，给我能打开的模型和纹理，不要只给预览图。
```

输入记录示例：

```json
{
  "object": "示例茶壶",
  "views": [
    {
      "file": "teapot-front.png",
      "view": "front"
    },
    {
      "file": "teapot-back.png",
      "view": "back"
    },
    {
      "file": "teapot-left.png",
      "view": "left"
    },
    {
      "file": "teapot-right.png",
      "view": "right"
    }
  ],
  "known_height_mm": null,
  "output_goal": "带材质三维资产"
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
      "hy3d-model-assets.zip",
      "hy3d-view-map.csv",
      "hy3d-build-review.json"
    ],
    "acceptance_plan": {
      "view_count": 4,
      "unknown_geometry": [
        "底部",
        "内部"
      ],
      "must_open_in_3d_viewer": true
    },
    "actual_asset_format": null
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：实际产物可被三维工具打开并旋转检查；多视图全部纳入或明确拒绝不支持部分；模型与纹理依赖齐全且来源可追溯；推测几何与用户给定尺寸清楚区分。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
