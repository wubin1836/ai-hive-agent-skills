# Claude Sonnet 5多语商品文案助手：场景示例

## 场景一：首次执行

```text
用Claude Sonnet 5把这款500mL不锈钢水杯做成德语和日语商品文案，标题各不超过80字符，保留容量和材质。没有保温时长证明，不要写保温多少小时或认证标志；给字段CSV和事实核对表，不上架。
```

输入记录示例：

```json
{
  "sku": "CUP-500",
  "facts": {
    "capacity": "500mL",
    "material": "不锈钢",
    "lid": "旋盖"
  },
  "locales": [
    "de-DE",
    "ja-JP"
  ],
  "title_max_characters": 80,
  "unsupported_claims": [
    "保温时长",
    "认证"
  ]
}
```

人工构造的输出片段，仅用于解释格式；不是付费模型生成结果或测试成绩：

```json
{
  "illustrative_only": true,
  "sample": {
    "example_only": true,
    "execution_status": "人工示例，未执行",
    "localized_field": {
      "sku": "CUP-500",
      "locale": "de-DE",
      "title": "Edelstahlbecher, 500 ml, mit Schraubdeckel"
    },
    "fact_mapping": {
      "500 ml": "capacity",
      "Edelstahl": "material"
    },
    "claims_omitted": [
      "保温时长",
      "认证"
    ],
    "published": false
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：规格、数字及限制条件与原始事实逐项一致；没有增加未获证明的认证、疗效或排名；每个SKU与目标语言的必需字段齐全；地区表达差异和待人工确认译法明确列出。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
