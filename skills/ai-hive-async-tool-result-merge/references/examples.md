# 异步工具调用与迟到结果归并助手：场景示例

## 场景一：首次执行

```text
请检查我提供的两条询价工具记录：A尚未返回，B已返回。整理能继续的工作、必须等待的比较步骤及跨轮迟到结果的归并规则，生成本地回放样例，不调用供应商接口。
```

输入记录示例：

```json
{
  "mode": "演示数据",
  "calls": [
    {
      "call_id": "c_a",
      "handle": "price_a",
      "state": "pending"
    },
    {
      "call_id": "c_b",
      "handle": "price_b",
      "state": "completed"
    }
  ],
  "next_step": "比较A与B报价"
}
```

人工构造的输出片段，仅用于解释格式；不是付费模型生成结果或测试成绩：

```json
{
  "illustrative_only": true,
  "sample": {
    "mode": "人工演示，未调用真实服务",
    "comparison": "等待price_a",
    "independent_work": "整理报价字段说明",
    "late_result_rule": "回到c_a并仅归并一次",
    "new_submissions": 0
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：每条结果能回指原调用编号，句柄不重复。；跨轮迟到结果不会覆盖后来已确认的新事实。；依赖未满足的步骤保持等待，独立步骤可以继续。；未知写入结果不会触发自动再次提交。。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
