# 混元 3D 3.1资产验收助手：场景示例

## 场景一：首次执行

```text
检查这份声称由混元3D3.1生成的茶壶模型能否用于网页展示，别改原文件，也别重新生成。缺贴图、破面和未验证项都要标出来。
```

输入记录示例：

```json
{
  "asset": "teapot-model.glb",
  "textures_directory": "textures",
  "source_receipt": null,
  "target_use": "网页展示",
  "limits": {
    "max_triangles": 100000
  },
  "read_only": true
}
```

人工构造的输出片段，仅用于解释格式；不是付费模型生成结果或测试成绩：

```json
{
  "illustrative_only": true,
  "sample": {
    "demo_only": true,
    "generation_status": "not_requested",
    "actual_model": null,
    "task_id": null,
    "expected_files": [
      "hy3d-asset-check.csv",
      "hy3d-review-evidence.zip",
      "hy3d-remediation.md"
    ],
    "acceptance_plan": {
      "read_only": true,
      "target_use": "网页展示",
      "triangle_limit": 100000
    },
    "provenance_status": "user_claim_only_until_receipt_checked",
    "inspection_status": "not_started"
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：原模型和纹理未被覆盖或自动修复；每个检测结论都有真实工具结果或证据截图；未知来源与未验证项目明确保留；展示、动画和制造用途没有混作同一合格标准。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
