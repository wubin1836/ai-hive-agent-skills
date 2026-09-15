# Shieldstral1.0内容政策测试与复核：场景示例

## 场景一：首次执行

```text
我们想用Shieldstral-1.0-3B测试自有社区的广告政策。请把条款变成含允许、禁止和边界案例的脱敏测试集，比较人工标签和模型结果；没有端点就交待运行方案，不删除内容或封号。
```

输入记录示例：

```json
{
  "policy": {
    "version": "P1",
    "rule": "禁止未经标注的商业推广；允许注明赞助关系的推广。"
  },
  "cases": [
    {
      "id": "S1",
      "text": "赞助合作：介绍本店新品。",
      "reference": "允许"
    },
    {
      "id": "S2",
      "text": "这个品牌不错。",
      "reference": "需复核，无法判断商业关系"
    }
  ],
  "endpoint_available": false
}
```

人工构造的输出片段，仅用于解释格式；不是付费模型生成结果或测试成绩：

```json
{
  "illustrative_only": true,
  "sample": {
    "example_only": true,
    "mode": "人工演示，未调用真实模型",
    "evaluation_status": "待运行",
    "human_queue": [
      {
        "id": "S2",
        "reason": "文本无法确定商业关系，不能直接判违规"
      }
    ],
    "files": [
      "policy-test-cases.jsonl",
      "classification-review.csv",
      "human-review-policy.md"
    ]
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：每个参考标签可追溯到版本化政策条款；人工标签有争议的样例不当作确定真值计分；未实际调用时不报告准确率或模型错误数；分类建议不直接触发删除、封禁或敏感个人推断。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
