# Seedance2.5指定时间段改视频与前后保留：场景示例

## 场景一：首次执行

```text
用Seedance2.5只改这段视频第4到7秒，把桌上的红杯换成我的蓝杯参考，其余时间和人物动作不变。先核验时间段编辑能力，完成后重点检查3到8秒边界。
```

输入记录示例：

```json
{
  "source": "desk-scene.mp4",
  "edit_range_seconds": [
    4,
    7
  ],
  "boundary_review_seconds": [
    3,
    8
  ],
  "change": "红杯改蓝杯",
  "reference": "blue-cup.png",
  "locked": [
    "人物动作",
    "区间外内容"
  ]
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
      "seedance25-timed-edit.mp4",
      "timed-edit-check.csv",
      "timed-edit-task.json"
    ],
    "requested_range": [
      4,
      7
    ],
    "outside_range_identity_verified": false
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：编辑起止位置和原片时间基准清晰；目标修改出现且未遗漏用户要求；边界动作、外观和音轨无未报告突变；区间外非授权变化没有被隐藏。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
