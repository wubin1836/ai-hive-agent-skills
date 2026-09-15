# Google Pics 图片内文字本地化校对包：场景示例

## 场景一：首次执行

```text
把这张授权活动海报的文字改成日文，保持品牌和版式，先按区域给译文与长度检查。我要 Google Pics 交接单；不能接入时不要假装已经改图。
```

输入记录示例：

```json
{
  "image": "event-poster.png",
  "target_locale": "ja-JP",
  "locked": [
    "品牌标识",
    "主视觉",
    "日期数字"
  ],
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
    "regions": [
      {
        "id": "T1",
        "source": "秋日市集",
        "translation": "秋のマルシェ",
        "status": "待用户确认"
      }
    ],
    "image_edited": false
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：译文与图片中实际文字逐字对应；数字、品牌和单位未被意外替换；非目标区域的变化有记录；没有将 Google Pics 与所有 Nano Banana 接口能力等同。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
