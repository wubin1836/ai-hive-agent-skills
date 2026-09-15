# Kimi K3项目交接与未决事项追踪：场景示例

## 场景一：首次执行

```text
用Kimi K3把这批资料整理成新项目经理接手包，基准日为9月15日。区分已批准和仍在讨论的改动，列出证据不足的完成项，以及接任者第一天要找谁确认什么。
```

输入记录示例：

```json
{
  "cutoff": "2026-09-15",
  "records": [
    {
      "source": "纪要0910.md#第3段",
      "text": "建议改为周五上线，待负责人批准。"
    },
    {
      "source": "交接0914.md#第2段",
      "text": "测试报告尚未收到。"
    }
  ]
}
```

人工构造的输出片段，仅用于解释格式；不是付费模型生成结果或测试成绩：

```json
{
  "illustrative_only": true,
  "sample": {
    "example_only": true,
    "mode": "人工演示，未调用真实模型",
    "current_state": {
      "launch_date": "未批准，不能按周五已确定安排",
      "test_report": "缺少完成凭据"
    },
    "first_checks": [
      "向项目负责人确认上线日期",
      "向测试负责人补齐报告"
    ],
    "files": [
      "project-handoff.md",
      "decision-and-action-ledger.csv",
      "handoff-questions.md"
    ]
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：已完成状态必须有执行凭据而非讨论记录；被撤回的决策不继续列为有效任务；责任与期限不明确时留空并指定待确认问题；交接路线包含依赖和禁止重复的外部操作。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
