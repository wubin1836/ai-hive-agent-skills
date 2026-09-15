# FLUX 3 Video广告镜头接续助手：场景示例

## 场景一：首次执行

```text
用FLUX 3 Video给这个台灯广告接一个缓慢调亮的镜头，灯臂结构和桌面摆设都不变，不新增功能，不直接改原片。
```

输入记录示例：

```json
{
  "source_video": "lamp-ad.mp4",
  "tail_action": "灯光缓慢变亮",
  "target_extra_seconds": 3,
  "locked": [
    "灯臂结构",
    "桌面摆设"
  ],
  "advertised_feature": "已确认调光功能"
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
      "flux-ad-tail.mp4",
      "flux-ad-continuity.json",
      "flux-ad-task.json"
    ],
    "acceptance_plan": {
      "source_protected": true,
      "extra_seconds": 3,
      "claim_scope": [
        "调光"
      ]
    },
    "publish_status": "not_requested"
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：原片保持不变且补段来源可追溯；商品名称、结构与功能表达未越界；连接处运动和声音没有未披露明显突变；交付仅含真实完成片段而非草稿占位。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
