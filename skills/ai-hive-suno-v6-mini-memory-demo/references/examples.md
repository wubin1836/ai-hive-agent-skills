# Suno v6-mini 照片日记到纪念歌小样：场景示例

## 场景一：首次执行

```text
根据我授权的毕业照片说明和三段日记，做一首送给同学的原创纪念歌，避开真实住址和姓名。先给歌词及 v6-mini 小样请求；模型不可用就只交付方案，不要假装生成。
```

输入记录示例：

```json
{
  "memory_notes": [
    "雨天共用一把伞",
    "最后一班校车",
    "操场合影"
  ],
  "occasion": "毕业",
  "names": "不用真实姓名",
  "target_seconds": 60,
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
    "chorus_draft": "那把伞还装着夏天，末班车把笑声送远",
    "private_details_removed": true,
    "audio_generated": false
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：歌词中的具体人物事件来自用户提供的信息；没有输出未经同意的个人敏感细节；没有把文字提示方案当成已生成音频；记录真实支持的输入模态，不假定各入口能力一致。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
