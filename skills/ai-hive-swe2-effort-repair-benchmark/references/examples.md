# SWE-2 修复任务推理档位对照验收：场景示例

## 场景一：首次执行

```text
用两个可复现的接口 bug 比较 SWE-2 medium 与 high，固定起始版本和回归测试，每个任务预算由我确认。先输出测试设计和接入检查，不改主分支、不自动提交。
```

输入记录示例：

```json
{
  "cases": [
    "空数组导致分页错误",
    "重复请求返回不一致"
  ],
  "efforts": [
    "medium",
    "high"
  ],
  "baseline": "待用户指定版本",
  "execute": false
}
```

人工构造的输出片段，仅用于解释格式；不是付费模型生成结果或测试成绩：

```json
{
  "illustrative_only": true,
  "sample": {
    "example": true,
    "execution_status": "plan_only",
    "planned_runs": 4,
    "metrics": [
      "有效修复",
      "回归通过",
      "实际费用",
      "耗时"
    ],
    "recommended_effort": null
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：每次比较使用相同基线与测试口径；不能只凭补丁可读或模型自述判成功；费用字段无真实回执时保持未知；失败和超预算样本不从结果中删除。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
