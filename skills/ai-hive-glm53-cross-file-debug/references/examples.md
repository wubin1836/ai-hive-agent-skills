# GLM5.3跨文件故障定位与最小修复：场景示例

## 场景一：首次执行

```text
用GLM5.3排查这个跨文件错误：接口返回有价格，结算页却显示0。请沿数据和配置追到根因，给最小补丁及复现用例；只允许改结算模块，没有运行条件就标待验证。
```

输入记录示例：

```json
{
  "files": {
    "api.ts": "return { amount_cents: 9900 };",
    "checkout.ts": "const price = response.amount ?? 0;"
  },
  "expected": "显示99元",
  "execution_available": false
}
```

人工构造的输出片段，仅用于解释格式；不是付费模型生成结果或测试成绩：

```json
{
  "illustrative_only": true,
  "sample": {
    "example_only": true,
    "mode": "人工演示，未调用真实模型",
    "hypothesis": "调用方读取字段与返回契约不一致，且需确认分转元规则",
    "evidence": [
      "api.ts：amount_cents",
      "checkout.ts：读取amount"
    ],
    "patch_status": "未应用草案",
    "regression_status": "待运行",
    "files": [
      "root-cause-evidence.md",
      "minimal-fix.patch",
      "regression-results.json"
    ]
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：根因结论包含跨文件的数据或状态传递证据；修复不只消除异常文本而保留错误行为；未运行测试与真实失败或通过严格区分；补丁没有修改未授权模块或扩大接口契约。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
