# 万相3产品资料做视频与原文溯源：场景示例

## 场景一：首次执行

```text
用万相3把这个公开产品说明页做成15秒介绍片，只有文档写明的功能可以说，每个镜头给我原文依据。先查AI-HIVE能否直接用网页参考，不能就说明，不要换模型。
```

输入记录示例：

```json
{
  "source_url": "https://example.com/public-product-manual",
  "source_is_fictional_example": true,
  "target_seconds": 15,
  "ratio": "16:9",
  "allowed_claims": [
    "以批准原文为准"
  ],
  "publish": false
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
      "wan3-product-brief.mp4",
      "brief-source-map.csv",
      "wan3-brief-task.json"
    ],
    "source_mapping_preview": {
      "shot_id": "W01",
      "claim": "经确认的产品功能",
      "source_locator": "待真实读取定位"
    },
    "video_created": false
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：每条事实性台词有可定位来源；未新增用户未确认的功能、认证或数字；真实视频可播放且时长比例符合确认规格；文档或链接输入方式符合本次实际schema。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
