# Image2.5图片生成与编辑：场景示例

## 场景一：首次执行

```text
用Image2.5把我上传的杯子照片改成暖光书桌场景，杯型和印字不变，只出一张4:3图片。先确认AI-HIVE可用型号和预算，不支持就告诉我，别换成旧版本。
```

输入记录示例：

```json
{
  "task_type": "edit",
  "source_image": "cup-original.png",
  "ratio": "4:3",
  "count": 1,
  "keep": [
    "杯型",
    "杯身原有文字"
  ],
  "change": [
    "背景变成暖光书桌"
  ],
  "budget": "提交前确认"
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
      "image25-result.png",
      "image25-checks.json",
      "image25-task.json"
    ],
    "acceptance_plan": {
      "count": 1,
      "ratio": "4:3",
      "locked_items": [
        "杯型",
        "杯身原有文字"
      ]
    }
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：文件能解码且比例、张数符合确认要求；编辑任务保留原图并逐项核对未授权变化；请求文字与实际可见文字逐字核对；最终图片与真实任务ID一一对应。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
