# Sunburst海报改字与多语版面保留：场景示例

## 场景一：首次执行

```text
用Sunburst把海报的“9月20日开业”改为“9月28日开业”，其它字、商品和二维码不变。先给文案对照，改后逐字核验，不要重做整张版式。
```

输入记录示例：

```json
{
  "source": "opening-poster.png",
  "replacements": [
    {
      "from": "9月20日开业",
      "to": "9月28日开业"
    }
  ],
  "locked": [
    "商品",
    "二维码",
    "其他文字"
  ],
  "language": "zh-CN"
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
      "poster-revised.png",
      "poster-copy-diff.csv",
      "poster-revision.json"
    ],
    "copy_preview": [
      {
        "from": "9月20日开业",
        "to": "9月28日开业"
      }
    ],
    "qr_validation": "需实际检查"
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：批准文字无漏字、错数字或未经确认改写；图片、logo和二维码保持可核对；无旧文字残影、重叠或越界；字号与换行变化均在确认范围。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
