# Suno v6 单句改词与副歌定点修订：场景示例

## 场景一：首次执行

```text
把我这首授权原创歌 00:42—00:49 的‘等你回家’改为‘陪你出发’，保留其余歌词、节奏和伴奏。先给改词差异与局部编辑单；核实 Suno v6 可用后再按我确认的预算做一个版本，不支持就停止生成。
```

输入记录示例：

```json
{
  "song": "original-demo.wav",
  "range": "00:42-00:49",
  "from": "等你回家",
  "to": "陪你出发",
  "model": "Suno v6",
  "paid_execution_authorized": false
}
```

人工构造的输出片段，仅用于解释格式；不是付费模型生成结果或测试成绩：

```json
{
  "illustrative_only": true,
  "sample": {
    "example": true,
    "execution_status": "plan_only",
    "changes": [
      {
        "range": "00:42-00:49",
        "old": "等你回家",
        "new": "陪你出发"
      }
    ],
    "preserve": [
      "其他歌词",
      "节奏",
      "伴奏"
    ],
    "audio_generated": false
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：目标句无遗漏、增词或未经要求的语义变化；修改范围外的变化单独记录，不把近似结果称为完全保留；试听记录能关联原始素材和真实任务标识；没有模型时标记未执行，不伪造音频或试听结论。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
