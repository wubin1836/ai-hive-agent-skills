# Suno v6 多首原创素材混编交接单：场景示例

## 场景一：首次执行

```text
用我自作 A 歌的人声和 B 歌的鼓组设计一首 90 秒活动主题曲，目标 100 BPM，不能使用第三方歌曲。先交付素材时间表和混编结构，确认 Suno v6 真正可用与预算后才试做。
```

输入记录示例：

```json
{
  "sources": [
    {
      "file": "a-vocal.wav",
      "role": "人声",
      "rights": "自有"
    },
    {
      "file": "b-drums.wav",
      "role": "鼓组",
      "rights": "自有"
    }
  ],
  "target_seconds": 90,
  "bpm": 100,
  "execute": false
}
```

人工构造的输出片段，仅用于解释格式；不是付费模型生成结果或测试成绩：

```json
{
  "illustrative_only": true,
  "sample": {
    "example": true,
    "execution_status": "plan_only",
    "sections": [
      {
        "name": "开场",
        "seconds": "0-8",
        "roles": [
          "鼓组"
        ]
      },
      {
        "name": "主歌",
        "seconds": "8-32",
        "roles": [
          "人声",
          "鼓组"
        ]
      }
    ],
    "rights_checked_against_user_statement": true,
    "audio_generated": false
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：所有被使用的素材均有明确来源及处理授权；每个要求的音乐元素能对应一个输入来源；调性和速度冲突有显式处理策略；未经实际试听不得写已融合成功或可商用。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
