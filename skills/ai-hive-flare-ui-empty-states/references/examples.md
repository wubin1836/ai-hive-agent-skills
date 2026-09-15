# Flare空状态插画与界面资源小套件：场景示例

## 场景一：首次执行

```text
用Flare给我的记账应用做三张无文字空状态插画：尚无记录、搜索无结果、网络失败。统一蓝绿色和圆润几何风，给标题与按钮留白，只交付图片和状态映射。
```

输入记录示例：

```json
{
  "states": [
    "no-records",
    "no-results",
    "network-error"
  ],
  "palette": [
    "蓝绿",
    "米白"
  ],
  "style": "圆润几何",
  "frame_px": [
    480,
    320
  ],
  "text_in_image": false
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
      "empty-states-preview.png",
      "empty-state-assets.json",
      "empty-state-spec.md"
    ],
    "asset_ids": [
      "no-records",
      "no-results",
      "network-error"
    ],
    "deliverable_type": "raster-not-svg"
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：每个状态语义明确且不混淆错误原因；目标UI尺寸下主体仍可辨认；色彩、视角和留白符合统一规格；透明通道、文件格式与实际一致。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
