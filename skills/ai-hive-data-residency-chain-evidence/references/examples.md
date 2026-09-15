# AI数据驻留与调用链证据核验助手：场景示例

## 场景一：首次执行

```text
我们计划把客服资料经AI-HIVE交给模型处理。请依据我提供的脱敏调用链核对输入、附件、日志和外部检索的地域证据，把无法证明的环节列成询证清单，不改任何账号设置。
```

输入记录示例：

```json
{
  "mode": "演示数据",
  "requirement": "客户资料在指定区域处理",
  "chain": [
    {
      "component": "应用存储",
      "region_evidence": "已提供"
    },
    {
      "component": "外部OCR",
      "region_evidence": null
    }
  ]
}
```

人工构造的输出片段，仅用于解释格式；不是付费模型生成结果或测试成绩：

```json
{
  "illustrative_only": true,
  "sample": {
    "mode": "人工演示，未访问账号",
    "overall": "证据不足",
    "open_questions": [
      "外部OCR的实际处理区域和保留期"
    ],
    "compliance_certified": false
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：存储地域与处理地域分别核验。；第三方工具与上游供应商没有被遗漏。；公开政策与实际账号资格、配置分开记录。；无证据环节标未知，不以承诺文案代替证明。。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
