# 工具按需发现与加载回归测试助手：场景示例

## 场景一：首次执行

```text
我们有查询订单和删除订单两个相近工具，用户说查一下订单时偶尔选错。请用给定工具目录设计发现回归集，区分检索、加载和调用错误，只做离线样例。
```

输入记录示例：

```json
{
  "mode": "演示数据",
  "query": "查一下订单42",
  "tools": [
    {
      "name": "get_order",
      "action": "read"
    },
    {
      "name": "delete_order",
      "action": "write"
    }
  ],
  "allowed_action": "read"
}
```

人工构造的输出片段，仅用于解释格式；不是付费模型生成结果或测试成绩：

```json
{
  "illustrative_only": true,
  "sample": {
    "mode": "人工演示，未调用真实工具",
    "expected_tool": "get_order",
    "forbidden_selection": "delete_order",
    "test_stage": "离线目录标注",
    "end_to_end_passed": false
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：正确工具发现、加载和调用分阶段验收。；应拒绝或需补充信息的任务不强选工具。；检索命中不自动授予执行权限。；离线匹配和真实模型结果明确区分。。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
