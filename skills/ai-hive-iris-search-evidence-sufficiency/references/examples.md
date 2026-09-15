# Iris 中文公开资料检索与证据止步清单：场景示例

## 场景一：首次执行

```text
用 Iris 的搜索 Agent 思路核实三款工具是否支持企业私有分享，只查各自官方文档，记录版本差异和未知项，最多 8 轮检索。先确认 Iris 与搜索工具可用；没有就给查询计划。
```

输入记录示例：

```json
{
  "question": "三款工具是否支持企业私有分享",
  "products": [
    "用户指定工具A",
    "用户指定工具B",
    "用户指定工具C"
  ],
  "allowed_sources": "各自官方文档",
  "max_search_rounds": 8,
  "model": "Iris-mini"
}
```

人工构造的输出片段，仅用于解释格式；不是付费模型生成结果或测试成绩：

```json
{
  "illustrative_only": true,
  "sample": {
    "example": true,
    "execution_status": "plan_only",
    "claims_to_verify": [
      "分享对象范围",
      "登录要求",
      "公开可发现性"
    ],
    "stop_conditions": [
      "每项有直接官方证据",
      "8轮用尽"
    ],
    "verified_answers": []
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：每个确定性结论有实际打开的原始资料支持；旧版与新版、产品与模型名称没有混为一谈；到达预算上限后保留未知而非继续无界搜索；没有把模型卡基准成绩当成当前任务的正确性保证。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
