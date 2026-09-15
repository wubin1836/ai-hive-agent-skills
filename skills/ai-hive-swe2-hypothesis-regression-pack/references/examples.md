# SWE-2 故障假设证伪与回归补丁包：场景示例

## 场景一：首次执行

```text
有人认为订单重复是缓存导致的，请用 SWE-2 先证伪这个假设，再检查重试链路。先只诊断并交付复现证据；我确认后才做最小补丁，不提交或上线。
```

输入记录示例：

```json
{
  "symptom": "偶发重复订单",
  "hypothesis": "缓存过期",
  "allowed_scope": "诊断",
  "artifacts": [
    "脱敏重试日志",
    "请求ID样本"
  ],
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
    "experiments": [
      "同请求ID重放与不同ID重放对照",
      "缓存命中和未命中对照"
    ],
    "root_cause": "尚未核实",
    "patch_applied": false
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：原始假设可被实验否定，不只搜支持性证据；修复前测试确实暴露原故障；修复后关联测试和边界测试有真实记录；诊断请求不会自动变成代码修改。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
