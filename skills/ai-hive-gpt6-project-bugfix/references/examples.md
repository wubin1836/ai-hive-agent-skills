# GPT-6代码修复与项目调试助手：场景示例

## 场景一：首次执行

```text
用GPT-6修复这个仓库的CSV导入报错，只修改导入模块，先复现再给补丁和测试，不提交Git。
```

输入记录示例：

```json
{
  "repo": "./demo",
  "error": "empty cell causes crash"
}
```

人工构造的输出片段，仅用于解释格式；不是付费模型生成结果或测试成绩：

```json
{
  "illustrative_only": true,
  "sample": {
    "example_only": true,
    "suspect": "空值转换",
    "patch": "待分析后生成",
    "tests_run": []
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：失败样例修复前失败、修复后通过；无无关文件修改；不自动push或部署。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
