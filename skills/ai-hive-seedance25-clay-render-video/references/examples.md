# Seedance2.5白模参考成片与动作路径对照：场景示例

## 场景一：首次执行

```text
用Seedance2.5把这段桌面机械玩具的白模预演变成木质材质视频，保留运镜、三块零件和装配顺序。每个装配节点给白模与成片对照，不改成工业生产指导。
```

输入记录示例：

```json
{
  "clay_video": "toy-clay.mp4",
  "material_reference": "wood-material.png",
  "locked": [
    "运镜",
    "3块零件",
    "装配顺序"
  ],
  "purpose": "玩具视觉预演",
  "engineering_use": false
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
      "seedance25-clay-render.mp4",
      "clay-render-comparison.png",
      "clay-motion-review.csv"
    ],
    "checkpoint_ids": [
      "insert-01",
      "rotate-02",
      "finish-03"
    ],
    "physics_validated": false
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：镜头轨迹与主体屏幕方向按关键点可核对；零件数量和动作顺序未被改造；材料和光照符合确认参考；未声称输出3D工程文件或真实物理仿真。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
