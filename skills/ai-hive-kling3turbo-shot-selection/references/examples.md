# 可灵 3.0 Turbo镜头预览筛选助手：场景示例

## 场景一：首次执行

```text
用可灵3.0Turbo预览两个咖啡倒入杯子的镜头，只比较俯拍和侧拍，最多各一条；列清楚哪里好哪里坏，选完不要自动生成正式版。
```

输入记录示例：

```json
{
  "candidates": [
    {
      "id": "top",
      "camera": "俯拍"
    },
    {
      "id": "side",
      "camera": "侧拍"
    }
  ],
  "action": "咖啡倒入杯中",
  "duration_seconds": 5,
  "max_candidates": 2,
  "auto_final": false
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
      "kling-turbo-previews.zip",
      "kling-shot-ranking.csv",
      "kling-preview-tasks.json"
    ],
    "acceptance_plan": {
      "candidate_ids": [
        "top",
        "side"
      ],
      "criteria": [
        "杯型保持",
        "动作完成",
        "构图"
      ],
      "max_candidates": 2
    },
    "selected_candidate": null
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：候选总数和费用范围未超出授权；相同请求没有因超时重复提交；评分有实际画面或声音证据；选中、失败和未完成候选分别列明。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
