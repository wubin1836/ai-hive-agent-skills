# 万相3双语台词短片与字幕逐句核对：场景示例

## 场景一：首次执行

```text
用万相3做一个原创机器人小剧场，机器人A说中文“欢迎来到工作室”，机器人B说英文“Let's build something useful.”。台词逐句核对，字幕后期处理，不模仿任何真人声音。
```

输入记录示例：

```json
{
  "dialogue": [
    {
      "id": "L01",
      "speaker": "原创机器人A",
      "language": "zh-CN",
      "text": "欢迎来到工作室"
    },
    {
      "id": "L02",
      "speaker": "原创机器人B",
      "language": "en",
      "text": "Let's build something useful."
    }
  ],
  "target_seconds": 10,
  "voice_imitation": false
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
      "wan3-bilingual.mp4",
      "wan3-dialogue.srt",
      "wan3-dialogue-review.csv"
    ],
    "approved_line_ids": [
      "L01",
      "L02"
    ],
    "audio_verified": false
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：每句批准台词有可定位的实际音频或缺失记录；语言、说话人和句序符合确认脚本；字幕时序与真实音频对应；未声称未经检测的口型精度或声音身份一致。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
