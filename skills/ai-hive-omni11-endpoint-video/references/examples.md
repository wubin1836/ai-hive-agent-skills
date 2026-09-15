# Omni 1.1 Flash首尾帧视频制作助手：场景示例

## 场景一：首次执行

```text
用Omni1.1Flash把空花瓶图和插好花的尾帧做成6秒插花过程，机位固定、花瓶不变，不要让花突然出现；先确认模型支持两张端点图。
```

输入记录示例：

```json
{
  "start_image": "vase-empty.png",
  "end_image": "vase-filled.png",
  "duration_seconds": 6,
  "motion": "手逐支插花",
  "camera": "locked",
  "endpoint_policy": "主体和构图对照"
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
      "omni-endpoints.mp4",
      "omni-endpoints-review.json",
      "omni-endpoints-task.json"
    ],
    "acceptance_plan": {
      "endpoint_files": [
        "vase-empty.png",
        "vase-filled.png"
      ],
      "sample_fractions": [
        0,
        0.25,
        0.5,
        0.75,
        1
      ],
      "forbidden": "花束瞬间出现"
    }
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：首尾画面与指定图片的主体和构图相符；过渡动作符合确认的因果顺序；主体数量稳定且无未披露明显变形；时长比例与任务回执一致。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
