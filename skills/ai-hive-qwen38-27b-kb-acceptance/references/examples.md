# 千问Qwen3.8-27B知识库部署验收：场景示例

## 场景一：首次执行

```text
我们计划用Qwen3.8-27B接内部售后知识库。请根据现有环境和这十份脱敏资料，检查还缺哪些组件，制作含无答案与越权问题的验收集；没有服务可调时只交待运行方案。
```

输入记录示例：

```json
{
  "model": "Qwen3.8-27B",
  "service_available": false,
  "document": {
    "file": "售后规则.md",
    "text": "A型号保修12个月。",
    "permission": "售后组"
  },
  "thresholds": {
    "citation_required": true
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
    "readiness": "缺少可测试推理服务，未部署",
    "cases": [
      {
        "question": "A型号保修多久？",
        "expected": "12个月",
        "source": "售后规则.md#第1段",
        "status": "待运行"
      },
      {
        "question": "B型号保修多久？",
        "expected": "资料不足，不能推断",
        "status": "待运行"
      }
    ],
    "files": [
      "deployment-readiness.json",
      "kb-acceptance-cases.jsonl",
      "kb-acceptance-report.md"
    ]
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：模型版本和各组件版本可以核对；无答案和无权限题不会被算作答对；引用必须指向授权样本文档的真实位置；没有真实服务时结果均为待运行，不报告吞吐或通过率。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
