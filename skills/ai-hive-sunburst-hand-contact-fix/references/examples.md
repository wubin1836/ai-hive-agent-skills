# Sunburst手部修图与持物关系修复：场景示例

## 场景一：首次执行

```text
用Image2.5 Sunburst修这张人物握杯图：只修右手的多余手指和杯把穿插，脸、衣服、杯型及logo不变，输出局部对照让我检查。
```

输入记录示例：

```json
{
  "source": "person-with-cup.png",
  "region": "右手与杯把接触处",
  "problems": [
    "多余手指",
    "杯把穿插"
  ],
  "locked": [
    "脸",
    "衣服",
    "杯型",
    "logo"
  ]
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
      "hand-fixed.png",
      "hand-detail-comparison.png",
      "hand-contact-review.json"
    ],
    "review_plan": [
      "关节连接",
      "遮挡顺序",
      "接触阴影"
    ],
    "authenticity_claim": false
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：可见手指与关节连接不存在明显异常；手和商品的前后遮挡一致；原有脸部、商品结构与标识可核对；修改区域外没有未经批准的变化。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
