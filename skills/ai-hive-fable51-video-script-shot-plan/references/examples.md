# Fable短视频脚本与分镜助手：场景示例

## 场景一：首次执行

```text
用Fable5.1为这款桌面收纳架写30秒竖屏介绍，受众是租房上班族。只有白底产品图，别虚构承重测试或用户评价。给口播、逐镜头表和待拍素材单，这次不出图、不生成视频。
```

输入记录示例：

```json
{
  "product": "桌面收纳架",
  "duration_seconds": 30,
  "aspect_ratio": "9:16",
  "facts": [
    "两层结构",
    "可拆装"
  ],
  "available_assets": [
    "产品白底图.jpg"
  ],
  "generation_requested": false
}
```

人工构造的输出片段，仅用于解释格式；不是付费模型生成结果或测试成绩：

```json
{
  "illustrative_only": true,
  "sample": {
    "example_only": true,
    "execution_status": "人工示例，未执行",
    "shot": {
      "id": "S02",
      "start": 4,
      "end": 10,
      "visual": "同一桌面使用收纳架前后对照",
      "voiceover": "把常用物品分成上下两层，桌面更好整理。",
      "asset_status": "待拍摄"
    },
    "video_generated": false
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：镜头时长合计符合目标且旁白时长标为估算或实测；产品宣称均来自用户提供的事实资料；分镜中每项素材有已有、待拍或待生成状态；没有图片或视频输出时不声称已生成画面或成片。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
