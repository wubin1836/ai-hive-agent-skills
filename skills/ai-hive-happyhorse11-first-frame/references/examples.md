# HappyHorse 1.1首帧图生视频助手：场景示例

## 场景一：首次执行

```text
用HappyHorse1.1让这张台灯图动起来，只让灯光轻微呼吸，镜头慢慢靠近，灯臂和桌面东西都别变，先查首帧接口。
```

输入记录示例：

```json
{
  "first_frame": "desk-lamp.png",
  "subject_motion": "灯光轻微呼吸",
  "camera_motion": "缓慢推近",
  "locked": [
    "灯臂",
    "桌面摆设"
  ],
  "duration_seconds": 5
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
      "happyhorse-first-frame.mp4",
      "happyhorse-first-frame-check.json",
      "happyhorse-first-frame-task.json"
    ],
    "acceptance_plan": {
      "model_id": "happyhorse-1.1-i2v",
      "keyframes_to_check": [
        "start",
        "middle",
        "end"
      ],
      "locked_count": 2
    }
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：首画面与用户指定图对应而非重新生图；主体结构和物件数量无未披露改变；主体动作与相机运动分别验收；单次任务数量、时长和费用范围可追溯。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
