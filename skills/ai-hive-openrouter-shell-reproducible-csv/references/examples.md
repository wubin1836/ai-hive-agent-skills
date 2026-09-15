# OpenRouter Shell 隔离式表格校验与复算包：场景示例

## 场景一：首次执行

```text
用 OpenRouter Shell 校验脱敏订单表的实收金额与退款汇总，缺失金额不按零补。先给复算脚本和上传说明，确认后才在禁网沙箱运行，最终交付结果与执行证据。
```

输入记录示例：

```json
{
  "file": "orders-redacted.csv",
  "formula": "实收合计减已完成退款",
  "null_amount_policy": "列为异常",
  "network": "disabled",
  "execute": false
}
```

人工构造的输出片段，仅用于解释格式；不是付费模型生成结果或测试成绩：

```json
{
  "illustrative_only": true,
  "sample": {
    "example": true,
    "execution_status": "plan_only",
    "checks": [
      "金额可解析",
      "订单ID重复",
      "退款状态口径"
    ],
    "computed_total": null,
    "sandbox_started": false
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：运行环境与用户要求一致，没有误用本机终端；关键结果由真实执行产生并有退出状态；独立汇总与主结果一致或有可解释差异；网络和上传仅限授权范围；待运行文件不伪装成实际计算结果。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
