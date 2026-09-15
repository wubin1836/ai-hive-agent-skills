# 千问Qwen3.8-Max-0902需求与源码差异审查：场景示例

## 场景一：首次执行

```text
用Qwen3.8-Max-0902只读审查这个提交是否实现PRD里的优惠券需求。把每条需求对应到源码和测试，重点查过期、叠加与权限条件；没有跑过的用例不要写通过。
```

输入记录示例：

```json
{
  "commit": "固定提交A",
  "requirement": "过期优惠券不可使用，并返回coupon_expired",
  "code_excerpt": "if (coupon.expired) return { error: 'invalid_coupon' };",
  "tests_executed": false
}
```

人工构造的输出片段，仅用于解释格式；不是付费模型生成结果或测试成绩：

```json
{
  "illustrative_only": true,
  "sample": {
    "example_only": true,
    "mode": "人工演示，未调用真实模型",
    "gaps": [
      {
        "requirement": "过期时返回coupon_expired",
        "status": "部分实现",
        "evidence": "coupon.ts#演示第1行",
        "difference": "阻止使用但错误码与需求不一致",
        "test_status": "待运行"
      }
    ],
    "files": [
      "requirement-code-map.csv",
      "delivery-gaps.md",
      "acceptance-cases.json"
    ]
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：每个已实现判断都有当前提交下的代码定位；未执行测试明确写待运行，不伪造通过；功能开关关闭或权限限制纳入结论；需求未定义的行为标记待确认而非自动判错。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
