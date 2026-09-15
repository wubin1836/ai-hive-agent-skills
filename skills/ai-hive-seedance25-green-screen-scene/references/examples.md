# Seedance2.5绿幕换景与人物边缘检查：场景示例

## 场景一：首次执行

```text
用Seedance2.5把我的授权绿幕舞蹈视频放进空旷摄影棚，动作、脸和服装不变，只允许环境灯光协调。重点检查发丝、手和地面接触，不换装也不发到社交平台。
```

输入记录示例：

```json
{
  "source": "licensed-dance-green.mp4",
  "background": "empty-studio.png",
  "locked": [
    "动作",
    "脸",
    "服装"
  ],
  "allowed_change": [
    "环境",
    "协调光照"
  ],
  "publish": false
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
      "seedance25-green-scene.mp4",
      "green-edge-check.png",
      "green-screen-review.json"
    ],
    "review_regions": [
      "发丝",
      "手",
      "脚底"
    ],
    "alpha_output_claim": false
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：主体衣物、脸部和动作未有未授权改动；发丝、手指与道具边缘问题被记录；机位、光照和接地关系没有明显冲突；交付文件没有被误称为带Alpha透明通道的视频。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
