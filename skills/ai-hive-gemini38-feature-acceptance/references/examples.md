# Gemini3.8 Flash新增功能验收追踪：场景示例

## 场景一：首次执行

```text
用Gemini3.8 Flash帮我追踪这次新增导出功能的验收。覆盖正常导出、无权限、空列表和任务失败，逐项对应实现与测试证据；只有写了代码但未验证的不要标完成，先不发布。
```

输入记录示例：

```json
{
  "feature": "订单CSV导出",
  "requirements": [
    "有权限可导出当前筛选结果",
    "无权限不得获取数据",
    "空列表给出明确提示"
  ],
  "evidence": {
    "code_present": true,
    "tests_run": false
  }
}
```

人工构造的输出片段，仅用于解释格式；不是付费模型生成结果或测试成绩：

```json
{
  "illustrative_only": true,
  "sample": {
    "example_only": true,
    "mode": "人工演示，未调用真实模型",
    "acceptance": [
      {
        "id": "EXP-01",
        "condition": "导出当前筛选结果",
        "implementation": "有代码线索，待核对",
        "test": "未运行",
        "status": "未验收"
      },
      {
        "id": "EXP-02",
        "condition": "无权限不得获取数据",
        "implementation": "待检查",
        "test": "未运行",
        "status": "未验收"
      }
    ],
    "files": [
      "feature-acceptance.csv",
      "acceptance-evidence.md",
      "release-open-items.json"
    ]
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：每个完成标记同时满足约定的实现与验收证据；只有代码存在但没有测试的项目不标已验收；权限、异常和空数据路径不被正常演示替代；环境阻断和产品待决策分开记录，未自动上线。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
