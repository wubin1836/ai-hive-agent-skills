# GPT Transcribe录音转文字助手：场景示例

## 场景一：首次执行

```text
用GPT-Transcribe把这份访谈录音转成文字，保留说话原意，客户姓名匿名化，金额和产品型号要回听，听不清的地方列出来。
```

输入记录示例：

```json
{
  "audio_file": "interview-demo.m4a",
  "language_hints": [
    "zh",
    "en"
  ],
  "terms": [
    "A17",
    "柔光模式"
  ],
  "transcript_style": "忠实轻断句",
  "anonymize_people": true
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
      "gpt-recording-transcript.txt",
      "gpt-recording-uncertain.csv",
      "gpt-recording-tasks.json"
    ],
    "acceptance_plan": {
      "anonymize_people": true,
      "spot_check_types": [
        "金额",
        "产品型号"
      ],
      "unknown_policy": "列疑点"
    },
    "audio_coverage": null
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：所有源音频区间均有对应结果或明确缺口；切分重叠没有重复句或误删正文；重要数字、人名及术语已抽听核验；未经确认不将听不清内容写成确定事实。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
