# Sunburst反光商品修图与高光控制：场景示例

## 场景一：首次执行

```text
用Image2.5 Sunburst减轻这只不锈钢保温杯正面的刺眼反光，杯型与刻字不变。如果刻字已经过曝看不清，列出需要补拍的位置，不要猜字。
```

输入记录示例：

```json
{
  "source": "steel-cup.png",
  "detail_reference": "engraving-closeup.png",
  "target_region": "杯身中央眩光",
  "keep": [
    "刻字",
    "金属质感",
    "外轮廓"
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
      "reflection-fixed.png",
      "reflection-before-after.png",
      "reflection-review.json"
    ],
    "recovery_claim": "仅凭参考可核对区域",
    "review_items": [
      "刻字",
      "高光方向",
      "金属材质"
    ]
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：商品外轮廓和部件数未变化；材质仍具有合理高光或透射特征；文字与刻度未凭空补造；不可恢复区域明确标为未确认。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
