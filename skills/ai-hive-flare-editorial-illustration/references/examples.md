# Flare文章配图与事实边界检查：场景示例

## 场景一：首次执行

```text
用Flare给这篇讲工作注意力的文章做一张抽象配图：桌面上的任务块逐步聚焦，不画真实公司和人脸，横向16:9，图注注明概念示意。
```

输入记录示例：

```json
{
  "paragraph_id": "P03",
  "topic": "减少任务切换以提升专注",
  "style": "抽象编辑插画",
  "ratio": "16:9",
  "avoid": [
    "真实公司logo",
    "人物肖像",
    "虚构统计数字"
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
      "editorial-illustration.png",
      "illustration-map.json",
      "editorial-caption.md"
    ],
    "caption_preview": "生成的概念示意图，不代表真实工作现场。"
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：每张图对应清楚的文章段落和表达目的；无虚构数字、机构标识或真实事件现场；图注能区分概念示意与纪实材料；输出尺寸和留白满足媒体规格。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
