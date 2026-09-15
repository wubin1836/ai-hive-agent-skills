# Flare分镜预演图与镜头连续性检查：场景示例

## 场景一：首次执行

```text
用Flare给这三个镜头做预演图：咖啡师取杯、倒咖啡、客人接杯。保持吧台方向和杯子一致，只做三张16:9静帧，给我连续性问题，不生成视频。
```

输入记录示例：

```json
{
  "shots": [
    {
      "id": "S01",
      "action": "取杯"
    },
    {
      "id": "S02",
      "action": "倒咖啡"
    },
    {
      "id": "S03",
      "action": "接杯"
    }
  ],
  "ratio": "16:9",
  "locked": [
    "吧台方向",
    "同一杯型"
  ],
  "video_requested": false
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
      "shot-previs-board.png",
      "shot-previs.json",
      "continuity-notes.csv"
    ],
    "shot_ids": [
      "S01",
      "S02",
      "S03"
    ],
    "video_generated": false
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：每张图对应单一镜头ID和关键时刻；主体屏幕方向与空间关系可逐镜核对；不存在把未生成的视频标为完成的状态；改动故事或镜数需用户明确确认。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
