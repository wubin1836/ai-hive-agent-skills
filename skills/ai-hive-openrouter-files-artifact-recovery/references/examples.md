# OpenRouter Files 文件复用与产物回收清单：场景示例

## 场景一：首次执行

```text
给这 8 个授权 CSV 设计 OpenRouter Files 复用和产物回收流程。保留本地原件，不上传敏感字段，不删除任何远端文件；先输出台账和区域限制检查。
```

输入记录示例：

```json
{
  "files": [
    "orders-redacted.csv",
    "refunds-redacted.csv"
  ],
  "region_requirement": "待确认",
  "backup": "用户指定本地目录",
  "upload_authorized": false
}
```

人工构造的输出片段，仅用于解释格式；不是付费模型生成结果或测试成绩：

```json
{
  "illustrative_only": true,
  "sample": {
    "example": true,
    "execution_status": "plan_only",
    "uploads": [],
    "blocking_question": "是否允许全球入口处理这些文件",
    "originals_must_be_preserved": true,
    "downloaded_artifacts": []
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：本地原件保留，不依赖上传文件可直接下载；文件标识归属明确且不跨工作区猜测；交付状态包含真实下载与完整性检查；上传及保存规则不违反用户数据区域要求。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
