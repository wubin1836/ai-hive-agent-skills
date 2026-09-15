# Sunburst扩图补景与主体位置保留：场景示例

## 场景一：首次执行

```text
用Sunburst把这张4:3山景扩成9:16壁纸，山峰位置和大小不动，向上补天空给时间留白。先计算原图落位，扩图后对照山峰有没变化。
```

输入记录示例：

```json
{
  "source": "mountain-4x3.png",
  "target_ratio": "9:16",
  "anchor": "bottom-center",
  "extend": "top",
  "locked": [
    "山峰位置",
    "山峰尺度"
  ],
  "safe_area": "顶部时间区域"
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
      "image-outpainted.png",
      "canvas-placement.json",
      "outpaint-review.json"
    ],
    "placement_preview": {
      "anchor": "bottom-center",
      "extension": "top"
    },
    "pixel_identity_claim": false
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：目标比例与原图落位参数有明确记录；主体尺度及位置符合确认容差；扩展边缘无明显接缝或透视突变；文案留白区域没有意外主体或文字。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
