# GPT Realtime 2.1语音接待配置助手：场景示例

## 场景一：首次执行

```text
用GPT-Realtime-2.1帮我配置门店语音接待，先只做测试：报单号要复述，听到找店长就转人工，但不要接生产号码，也别自动打给客户。
```

输入记录示例：

```json
{
  "business": "示例咖啡店",
  "faq": [
    "营业时间",
    "地址"
  ],
  "handoff_phrase": "找店长",
  "tools": [
    "只读营业信息"
  ],
  "environment": "test_only",
  "production_binding": false
}
```

人工构造的输出片段，仅用于解释格式；不是付费模型生成结果或测试成绩：

```json
{
  "illustrative_only": true,
  "sample": {
    "demo_only": true,
    "generation_status": "not_submitted",
    "actual_model": null,
    "task_id": null,
    "expected_files": [
      "gpt-reception-config.json",
      "gpt-reception-cases.csv",
      "gpt-reception-report.json"
    ],
    "acceptance_plan": {
      "model_id": "gpt-realtime-2.1",
      "cases": [
        "单号复述",
        "静音",
        "打断",
        "转人工"
      ],
      "production_binding": false
    },
    "config_status": "draft_until_host_schema_checked",
    "executed_cases": 0
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：实际模型ID为gpt-realtime-2.1而非同族默认型号；配置不含凭据且业务工具权限最小化；测试状态区分通过、失败和未执行；转人工等外部动作只凭真实平台回执判定。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
