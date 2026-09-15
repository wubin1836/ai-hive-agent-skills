# GPT Astra截图转界面规范助手：场景示例

## 场景一：首次执行

```text
用GPT Astra分析后台截图，做组件规范，没看到的点击行为不要猜，标出需要产品经理确认的地方。
```

输入记录示例：

```json
{
  "screenshot": "dashboard.png",
  "width": 1440
}
```

人工构造的输出片段，仅用于解释格式；不是付费模型生成结果或测试成绩：

```json
{
  "illustrative_only": true,
  "sample": {
    "example_only": true,
    "observed": [
      "左侧导航"
    ],
    "inferred_interactions": [],
    "unknown": [
      "按钮点击结果"
    ]
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：不臆造截图之外功能；可见文字逐项核对；设计复用需素材权利。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
