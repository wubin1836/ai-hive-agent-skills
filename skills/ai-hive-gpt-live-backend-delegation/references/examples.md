# GPT-Live语音与后台任务协同助手：场景示例

## 场景一：首次执行

```text
为GPT-Live设计查询商品资料的后台委派流程，用户改商品后旧结果不能覆盖新问题，先用模拟事件验收。
```

输入记录示例：

```json
{
  "request_id": "demo-r1",
  "correction": "改查商品B"
}
```

人工构造的输出片段，仅用于解释格式；不是付费模型生成结果或测试成绩：

```json
{
  "illustrative_only": true,
  "sample": {
    "example_only": true,
    "old_result_action": "隔离待核对",
    "active_request": "demo-r2",
    "live_tested": false
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：结果与委派ID对应；取消不代表已停止外部计费；迟到结果不覆盖新指令。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
