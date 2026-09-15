# Wan3多素材参考成片与输入组合核对：场景示例

## 场景一：首次执行

```text
用Wan3参考我的台灯照片、运镜视频和授权环境音做10秒展示，分别只参考外观、镜头运动、环境声。先检查三种素材能否在当前MCP同用，不能不要静默删掉任何一项。
```

输入记录示例：

```json
{
  "references": [
    {
      "id": "REF-I1",
      "file": "lamp.png",
      "role": "外观"
    },
    {
      "id": "REF-V1",
      "file": "camera-move.mp4",
      "role": "运镜"
    },
    {
      "id": "REF-A1",
      "file": "room-tone.wav",
      "role": "环境音"
    }
  ],
  "target_seconds": 10,
  "ratio": "16:9"
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
      "wan3-reference-film.mp4",
      "reference-roles.csv",
      "wan3-input-review.json"
    ],
    "combination_status": "待实时schema核验",
    "roles": [
      "外观",
      "运镜",
      "环境音"
    ]
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：所有已使用素材有编号与授权用途；实际请求没有非法或被静默丢弃的素材类型；主体与动作参考没有互相串位；成片与输入组合、实际模型及任务ID对应。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
