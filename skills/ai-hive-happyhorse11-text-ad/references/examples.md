# HappyHorse 1.1文生广告视频助手：场景示例

## 场景一：首次执行

```text
用HappyHorse1.1按文字做一条桌面收纳广告，只讲分类收纳这个已确认卖点，画面是概念示意，不要写折扣或夸张功能，先给我确认镜头和费用。
```

输入记录示例：

```json
{
  "product": "桌面收纳架概念",
  "verified_claims": [
    "分区收纳"
  ],
  "duration_seconds": 10,
  "aspect_ratio": "9:16",
  "voiceover": "桌面物品，各归其位",
  "visual_status": "concept"
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
      "happyhorse-text-ad.mp4",
      "happyhorse-ad-claims.json",
      "happyhorse-text-ad-task.json"
    ],
    "acceptance_plan": {
      "model_id": "happyhorse-1.1-t2v",
      "claim_scope": [
        "分区收纳"
      ],
      "concept_label_required": true
    },
    "advertising_publish_status": "not_requested"
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：实际调用为happyhorse-1.1-t2v；广告表达未超出用户确认事实；旁白与画面关键动作可对照；概念外观与真实商品展示状态明确。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
