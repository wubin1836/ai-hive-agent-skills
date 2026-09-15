# SeedRealtime实时视觉讲解助手：场景示例

## 场景一：首次执行

```text
用SeedRealtime做一次桌面文具实时讲解演示，只看我选的摄像头，最多3分钟，我说停就关闭；不认识就说不确定，不要记住旁人的脸。
```

输入记录示例：

```json
{
  "scene": "桌面文具",
  "video_source": "用户选择的摄像头",
  "max_minutes": 3,
  "language": "zh",
  "proactive_events": [
    "指定红色剪刀出现"
  ],
  "retain_video": false
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
      "seedrealtime-guide-plan.json",
      "seedrealtime-guide-review.csv",
      "seedrealtime-session.json"
    ],
    "acceptance_plan": {
      "max_minutes": 3,
      "tests": [
        "指代",
        "画面切换",
        "打断",
        "目标出现"
      ],
      "face_identification": false
    },
    "access_status": "requires_verification",
    "session_id": null
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：摄像头与麦克风范围、时限和停止状态明确；讲解依据能对应当时画面，不用常识补造看见的内容；打断、场景变化和误认场景有真实测试记录；没有把无访问权限的方案写成已运行助手。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
