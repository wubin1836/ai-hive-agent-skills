# Eleven Music v2广告配乐助手：场景示例

## 场景一：首次执行

```text
用Eleven Music v2给我这条20秒手冲咖啡广告配纯器乐，3到12秒要给旁白留位置，18秒品牌出现时落一个清晰音乐点，先报本次生成范围。
```

输入记录示例：

```json
{
  "duration_seconds": 20,
  "voiceover_interval": [
    3,
    12
  ],
  "brand_cue_seconds": 18,
  "style": "温暖原声，轻节奏",
  "vocals": false
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
      "eleven-ad-score.wav",
      "eleven-ad-cues.csv",
      "eleven-ad-task.json"
    ],
    "acceptance_plan": {
      "target_seconds": 20,
      "voiceover_clearance": [
        3,
        12
      ],
      "brand_cue": 18
    },
    "mix_status": "not_started"
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：实际时长满足用户确认的容差；旁白区没有未经允许的人声或强干扰；关键落点与镜头表可逐项比对；音频来源与使用条件已记录。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
