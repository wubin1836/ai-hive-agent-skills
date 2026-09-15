# GPT6短视频脚本与制作任务单：场景示例

## 场景一：首次执行

```text
用GPT6把产品资料做成30秒介绍视频脚本，卖点要真实，分镜写出哪些实拍、哪些需要AI生成，先不花费生成。
```

输入记录示例：

```json
{
  "duration": 30,
  "product": "保温杯",
  "claims": [
    "容量500ml"
  ]
}
```

人工构造的输出片段，仅用于解释格式；不是付费模型生成结果或测试成绩：

```json
{
  "illustrative_only": true,
  "sample": {
    "example_only": true,
    "shots": [
      {
        "seconds": "0-5",
        "content": "展示产品",
        "generation_status": "待确认"
      }
    ]
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：主张能追溯资料；口播与时长匹配；成片模型不标成GPT6。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
