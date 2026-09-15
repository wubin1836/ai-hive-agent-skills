# MiniMax Music 3.0品牌歌曲制作助手：场景示例

## 场景一：首次执行

```text
用MiniMax Music3.0为原创小店澄光做一首品牌短歌，只讲咖啡和阅读，品牌名读清楚，不模仿任何歌手，先给我确认歌词和费用。
```

输入记录示例：

```json
{
  "brand": "澄光",
  "pronunciation": "chéng guāng",
  "verified_themes": [
    "咖啡",
    "阅读"
  ],
  "target_seconds": 35,
  "style": "轻快木吉他",
  "voice": "原创中性人声"
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
      "minimax-brand-song.wav",
      "minimax-brand-lyrics.csv",
      "minimax-brand-task.json"
    ],
    "acceptance_plan": {
      "brand_tokens": [
        "澄光"
      ],
      "allowed_themes": [
        "咖啡",
        "阅读"
      ],
      "target_seconds": 35
    },
    "license_status": "awaiting_current_terms_review"
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：品牌名与口号实际唱出内容正确或明确标失败；歌词没有未经确认的新卖点；音频可播放且结尾完整；来源、声音授权及使用许可状态明确。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
