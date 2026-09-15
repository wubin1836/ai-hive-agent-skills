# 混元Hy4-preview预览接入验收：场景示例

## 场景一：首次执行

```text
我想试用混元Hy4-preview整理产品问题。请先看官方说明和我提供的通道截图，区分模型公开、账号能用和AI-HIVE已接入；没有权限就给待申请与待测试清单，不实际调用。
```

输入记录示例：

```json
{
  "model": "Hy4-preview",
  "visible_channels": [
    "现有文本通道A"
  ],
  "hy4_access": "未确认",
  "task": "将脱敏产品问题分类",
  "allow_calls": false
}
```

人工构造的输出片段，仅用于解释格式；不是付费模型生成结果或测试成绩：

```json
{
  "illustrative_only": true,
  "sample": {
    "example_only": true,
    "mode": "人工演示，未调用真实模型",
    "availability": {
      "official_status": "preview",
      "account_access": "未确认",
      "aihive_access": "未确认",
      "business_test": "待运行"
    },
    "next_action": "补充经授权的真实通道能力信息",
    "files": [
      "preview-availability.json",
      "preview-test-cases.json",
      "access-readiness.md"
    ]
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：preview标记贯穿结果，不称正式现货或默认可调用；官方描述、账号权限与实测能力有独立状态；没有通道或授权时没有虚构请求和测试成绩；未知输入格式、许可或资源条件明确留待核验。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
