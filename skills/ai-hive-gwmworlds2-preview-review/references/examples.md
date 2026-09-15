# GWM Worlds 2交互世界方案与预览验收助手：场景示例

## 场景一：首次执行

```text
为GWM Worlds2设计一个可探索书店世界的预览验收方案：走到柜台再回头时摆设应保持。现在没有预览权限就只给方案和未执行用例，别说已经生成。
```

输入记录示例：

```json
{
  "scene": "虚拟书店",
  "actions": [
    "走到柜台",
    "回头",
    "返回入口"
  ],
  "state_invariants": [
    "书架布局",
    "柜台位置"
  ],
  "preview_access": false,
  "request_mode": "plan_only"
}
```

人工构造的输出片段，仅用于解释格式；不是付费模型生成结果或测试成绩：

```json
{
  "illustrative_only": true,
  "sample": {
    "demo_only": true,
    "generation_status": "not_requested",
    "actual_model": null,
    "task_id": null,
    "expected_files": [
      "gwm-world-plan.md",
      "gwm-preview-cases.csv",
      "gwm-access-review.json"
    ],
    "acceptance_plan": {
      "actions": [
        "走到柜台",
        "回头",
        "返回入口"
      ],
      "invariants": [
        "书架布局",
        "柜台位置"
      ]
    },
    "access_status": "no_access",
    "executed_cases": 0
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：方案、录屏观察和亲自执行三种状态分开；每个通过结论有真实动作与可见证据；无访问时测试均标未执行而非通过；没有承诺公开API、正式部署或可信物理模拟。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
