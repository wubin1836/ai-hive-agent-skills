# Mistral Vibe 旧代码数值对齐迁移包：场景示例

## 场景一：首次执行

```text
把这段有基线输入的 Fortran 77 计算模块迁移到 C++，参考 Mistral Vibe 的数值对齐方法。先整理 COMMON 状态、调用关系和中间检查点，确认容差后才改一个叶子模块，不动主程序。
```

输入记录示例：

```json
{
  "source_language": "Fortran 77",
  "target_language": "C++",
  "scope": "一个密度计算叶子模块",
  "baseline_available": true,
  "tolerance": "等待领域负责人确认",
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
    "required_checkpoints": [
      "输入压力",
      "插值索引",
      "输出密度"
    ],
    "migration_started": false,
    "blocking_item": "确认数值容差与边界样本"
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：迁移前有真实可运行基线，不以模型推测替代；最终输出和关键中间量均有对齐证据；容差来自任务与领域确认，不随失败结果放宽；架构变化没有只换语法仍复制全部旧全局状态；未通过对齐的模块不自动合并。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
