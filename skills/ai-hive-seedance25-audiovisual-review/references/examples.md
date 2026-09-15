# Seedance2.5成片音画验收与返修时间单：场景示例

## 场景一：首次执行

```text
只检查这段我用Seedance2.5做的视频，按批准台词找漏字、音画错位和人物漂移，给具体秒数的返修单。不要上传、不要重新生成，也不要根据视频猜模型版本。
```

输入记录示例：

```json
{
  "video": "existing-seedance-film.mp4",
  "approved_script": "approved-dialogue.txt",
  "task_receipt": null,
  "upload_allowed": false,
  "regeneration_allowed": false
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
      "seedance25-revision-list.csv",
      "seedance25-evidence.png",
      "seedance25-media-probe.json"
    ],
    "inspection_status": "人工演示结构，未检查真实文件",
    "source_model_verified": false,
    "network_calls": 0
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：每个问题有实际片段时间点或明确未能判断；台词差异对照批准原文而非模型自行改写；技术指标来自真实探测，不编造检测值；默认网络上传与模型生成调用数为0。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
