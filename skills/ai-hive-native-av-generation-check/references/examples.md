# 原生音视频生成与音画一致性验收助手：场景示例

## 场景一：首次执行

```text
我有一条人物拿杯子说欢迎的视频。请检查这是否记录为原生音频生成，并核对对白、放杯子的碰撞声和口型，输出时间点问题表，先不重生成或配新声音。
```

输入记录示例：

```json
{
  "mode": "演示数据",
  "visible_event": {
    "action": "杯子落桌",
    "time_s": 2.0
  },
  "user_reported_sound": {
    "event": "碰撞声",
    "time_s": 2.6
  },
  "generation_metadata": null
}
```

人工构造的输出片段，仅用于解释格式；不是付费模型生成结果或测试成绩：

```json
{
  "illustrative_only": true,
  "sample": {
    "mode": "人工演示，仅依据给定事件",
    "candidate_offset_s": 0.6,
    "native_generation_verified": false,
    "next": "核验原始成片及生成记录后确认原因"
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：实际生成方式、模型和版本明确。；每个同步问题有可定位的事件或时间点。；对白内容正确性与口型同步分别检查。；未生成或未听取的样本不标通过。。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
