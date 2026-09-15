# Opus5代码审查与上线前检查：场景示例

## 场景一：首次执行

```text
用Opus5审查这个版本相对main的变更，重点看导出任务和权限校验。只报告能说明触发条件的问题，运行已有本地测试可以，但别改代码、别发PR评论、别部署。
```

输入记录示例：

```json
{
  "base": "main",
  "target": "release-candidate",
  "focus": [
    "导出任务",
    "权限校验"
  ],
  "allowed_diagnostics": [
    "本地已有测试"
  ],
  "mode": "只读审查"
}
```

人工构造的输出片段，仅用于解释格式；不是付费模型生成结果或测试成绩：

```json
{
  "illustrative_only": true,
  "sample": {
    "example_only": true,
    "execution_status": "人工示例，未执行",
    "candidate_finding": {
      "path": "src/export/job.ts",
      "line": 84,
      "trigger": "用户撤销导出后任务继续执行",
      "impact": "产生用户已取消的文件",
      "verification": "待隔离复现",
      "priority": "待证据确认"
    },
    "source_modified": false
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：每个确定问题均有代码定位和具体触发条件；优先级反映真实影响而非措辞强烈程度；已验证缺陷与待验证风险明确分开；没有擅自修复、提交评论或部署。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
