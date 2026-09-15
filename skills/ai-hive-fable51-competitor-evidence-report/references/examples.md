# Claude Fable竞品调研报告助手：场景示例

## 场景一：首次执行

```text
用Claude Fable 5.1比较这三家预约系统在中国市场面向小店的方案，重点看排班、数据导出和服务限制。只用可公开核对的材料，每个结论给链接和日期，没证实的不要猜，不注册试用账号。
```

输入记录示例：

```json
{
  "competitors": [
    "示例预约A",
    "示例预约B",
    "示例预约C"
  ],
  "market": "中国",
  "dimensions": [
    "排班",
    "数据导出",
    "服务限制"
  ],
  "research_date": "2026-09-15"
}
```

人工构造的输出片段，仅用于解释格式；不是付费模型生成结果或测试成绩：

```json
{
  "illustrative_only": true,
  "sample": {
    "example_only": true,
    "execution_status": "人工示例，未执行",
    "comparison": [
      {
        "vendor": "示例预约A",
        "dimension": "数据导出",
        "finding": "待打开官方说明验证",
        "source_url": null,
        "confidence": "未证实"
      }
    ],
    "excluded_actions": [
      "注册账号",
      "联系销售",
      "付费试用"
    ]
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：每个关键事实有实际打开的来源链接；价格和功能比较使用相同地区、版本及时间口径；找不到证据不写成明确不存在；建议与事实分开且不伪称亲自试用。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
