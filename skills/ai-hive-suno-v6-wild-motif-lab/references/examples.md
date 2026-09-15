# Suno v6-wild 音乐动机探索与收敛：场景示例

## 场景一：首次执行

```text
为我的原创播客片头探索三种声音：节拍固定 96 BPM，只变化主奏音色，想要轻微神秘但不恐怖。先用 v6-wild 设计可比较的实验与评分表，未确认模型和预算不要生成。
```

输入记录示例：

```json
{
  "theme": "城市夜行播客",
  "fixed_bpm": 96,
  "variable": "主奏音色",
  "max_candidates": 3,
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
    "variants": [
      "木质拨弦",
      "柔和合成器",
      "气息长笛"
    ],
    "score_axes": [
      "主题贴合",
      "动机辨识",
      "后期可用"
    ],
    "winner": null
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：候选之间的主要变化可解释，不同时乱改全部条件；未超过确认的数量和预算上限；评分只针对已拿到的真实音频；精修单保留入选片段来源，不自动替换指定模型。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
