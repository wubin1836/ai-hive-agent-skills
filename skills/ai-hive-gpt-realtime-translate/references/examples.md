# GPT Realtime Translate实时语音翻译助手：场景示例

## 场景一：首次执行

```text
用GPT-Realtime-Translate把我授权的中文演示实时翻成英语，产品型号照读，输出别回灌麦克风；先确认支持语言和录存方式。
```

输入记录示例：

```json
{
  "audio_source": "授权演示音频",
  "source_language": "zh",
  "target_language": "en",
  "terms": [
    "CUP-A17"
  ],
  "record_translation": true,
  "record_source": false,
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
      "gpt-translation-audio.wav",
      "gpt-translation-review.csv",
      "gpt-translation-session.json"
    ],
    "acceptance_plan": {
      "target_language": "en",
      "term_lock": [
        "CUP-A17"
      ],
      "source_recording": false,
      "echo_isolation": true
    },
    "session_id": null
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：目标语言与实际音频输出符合选择；输入输出隔离且无重复翻译回声；关键数字与否定表达复核并标疑点；录存范围与用户授权一致，结束后采集关闭。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
