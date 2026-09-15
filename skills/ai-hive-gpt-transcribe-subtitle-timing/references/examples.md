# GPT Transcribe字幕校时助手：场景示例

## 场景一：首次执行

```text
用GPT-Transcribe重做这段教程的字幕，原SRT越到后面越不同步。用真实音轨校时间，保留原文件，给我校时后的SRT和改动表。
```

输入记录示例：

```json
{
  "video": "tutorial-demo.mp4",
  "existing_subtitles": "tutorial-old.srt",
  "language": "zh",
  "max_lines": 2,
  "max_chars_per_line": 18,
  "known_offset_seconds": null
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
      "gpt-subtitles.srt",
      "gpt-subtitle-timing.csv",
      "gpt-subtitle-tasks.json"
    ],
    "acceptance_plan": {
      "timing_basis": "实际音频对齐",
      "max_lines": 2,
      "review_positions": [
        "开头",
        "中段",
        "尾部",
        "修改点"
      ]
    },
    "aligned_timestamps": null
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：所有字幕起止有真实时间依据且处于媒体时长内；无未解释倒序或不应有的时间重叠；关键语句通过播放检查而非只看SRT格式；阅读规则与用户确认一致，疑点明确列出。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
