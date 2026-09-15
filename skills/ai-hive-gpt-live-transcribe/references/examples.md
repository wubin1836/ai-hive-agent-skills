# GPT Live Transcribe实时转写助手：场景示例

## 场景一：首次执行

```text
用GPT-Live-Transcribe给这次演示实时出字，只接我选的麦克风，先确认授权和时长上限；断流就标记缺口，不要凭上下文补句子。
```

输入记录示例：

```json
{
  "audio_source": "用户选择的麦克风",
  "language_hints": [
    "zh"
  ],
  "keywords": [
    "澄光台灯",
    "SKU-A17"
  ],
  "max_minutes": 10,
  "retain_raw_audio": false,
  "consent": "pending"
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
      "gpt-live-transcript.txt",
      "gpt-live-events.jsonl",
      "gpt-live-session.json"
    ],
    "acceptance_plan": {
      "source_scope": "selected_microphone",
      "max_minutes": 10,
      "partial_policy": "replace_by_segment_id",
      "gap_policy": "mark_only"
    },
    "session_id": null
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：暂态与最终文本区分且无重复增量拼接；断流缺口显式标记，没有补写未听见内容；会话结束后采集确已关闭；文本片段能回溯到真实会话与事件。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
