# MiniMax M3研究与代码仓库交接：场景示例

## 场景一：首次执行

```text
用MiniMax M3整理这份论文、实验笔记和固定提交的仓库，交给新同事。列出每个主要结论对应的代码、配置与日志，缺数据或未跑过的不要补写成绩；先只读，不训练。
```

输入记录示例：

```json
{
  "claim": "方法B在验证集优于基线",
  "repo_files": [
    "train.py",
    "configs/b.yaml"
  ],
  "results_present": false,
  "data_access": "待申请",
  "execution_allowed": false
}
```

人工构造的输出片段，仅用于解释格式；不是付费模型生成结果或测试成绩：

```json
{
  "illustrative_only": true,
  "sample": {
    "example_only": true,
    "mode": "人工演示，未调用真实模型",
    "mapping": [
      {
        "claim": "方法B优于基线",
        "implementation": "configs/b.yaml与train.py待逐行核对",
        "result_evidence": null,
        "status": "论文主张，本地未验证"
      }
    ],
    "blockers": [
      "缺结果日志",
      "数据访问待申请"
    ],
    "files": [
      "research-code-map.csv",
      "reproduction-readiness.md",
      "research-handoff.md"
    ]
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：每项研究结论有代码或结果证据，缺失处明确留空；论文报告指标与本地实际运行指标分开标记；未获得数据访问权时不声称可复现；未执行训练或实验时不生成虚构运行日志。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
