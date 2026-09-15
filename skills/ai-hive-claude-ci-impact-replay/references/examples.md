# Claude CI 测试影响分析的离线回放验收：场景示例

## 场景一：首次执行

```text
按 Claude CI 测试影响分析的思路，离线回放我们一周的测试结果，重点验证新增测试、listener 延迟和重复事件是否造成漏选。先只交付证据和保守回退，不改生产 CI。
```

输入记录示例：

```json
{
  "window": "用户提供的一周事件",
  "scenarios": [
    "新增测试",
    "结果延迟20分钟",
    "重复事件"
  ],
  "mode": "offline",
  "production_write": false
}
```

人工构造的输出片段，仅用于解释格式；不是付费模型生成结果或测试成绩：

```json
{
  "illustrative_only": true,
  "sample": {
    "example": true,
    "execution_status": "plan_only",
    "baseline_required": "全量测试或人工确认的正确测试集",
    "fallback": "映射未知或状态过期时扩大测试范围",
    "measured_misses": null
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：事件输入输出数量可对账，重复与乱序有处理结论；新增测试和已修复测试不会因旧状态被永久排除；测试选择结果不是由语言模型凭直觉决定；无生产 CI 写入或未经批准削弱测试门槛。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
