# Fable代码修复与测试助手：场景示例

## 场景一：首次执行

```text
用Fable5.1修复这个仓库里空购物车结算报500的问题。先复现，再加回归测试，只改结算相关代码。把实际测试命令和结果一起交付，不提交、不部署。
```

输入记录示例：

```json
{
  "repository": "shop-demo",
  "symptom": "空购物车POST /checkout返回500",
  "expected": "返回400和明确提示",
  "test_command": "npm test -- checkout",
  "scope": [
    "src/checkout",
    "tests/checkout"
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
    "hypothesis": "空数组读取首个商品时缺少校验",
    "proposed_test": "empty-cart-returns-400",
    "test_status": "待宿主复现及运行",
    "excluded": [
      "支付生产接口",
      "订单模块重构"
    ]
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：修复对应可说明的根因而非仅隐藏报错；新增测试在修复前失败、修复后通过或明确记录无法验证；没有覆盖用户已有修改或扩展无关重构；只报告实际执行过的测试。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
