# DeepSeek V4.1代码助手与回归测试：场景示例

## 场景一：首次执行

```text
用DeepSeek V4.1修这个分页bug，只生成小补丁，测试不通过不要提交，先让我看预计调用次数。
```

输入记录示例：

```json
{
  "bug": "末页重复一条",
  "test_command": "项目既有命令"
}
```

人工构造的输出片段，仅用于解释格式；不是付费模型生成结果或测试成绩：

```json
{
  "illustrative_only": true,
  "sample": {
    "example_only": true,
    "repro_case": "页大小10，总数21",
    "expected": "末页1条",
    "executed": false
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：修复经过真实测试；预算耗尽停止；不自动合并PR。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
