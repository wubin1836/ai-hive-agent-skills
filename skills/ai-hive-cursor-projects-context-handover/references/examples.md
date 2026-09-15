# Cursor Projects 长项目上下文交接包：场景示例

## 场景一：首次执行

```text
给这个持续三周的 Cursor Projects 迁移项目做接手包：区分已经验证的结论与旧假设，列出测试命令、未完成里程碑和不可变范围。先只输出本地文件，不创建项目或自动订阅。
```

输入记录示例：

```json
{
  "project": "订单服务拆分",
  "revision": "用户提供的当前版本",
  "next_milestone": "只读查询迁移",
  "forbidden_scope": [
    "支付写链路"
  ],
  "publish": false
}
```

人工构造的输出片段，仅用于解释格式；不是付费模型生成结果或测试成绩：

```json
{
  "illustrative_only": true,
  "sample": {
    "example": true,
    "execution_status": "illustrative_only",
    "stable_constraints": [
      "不改支付写链路"
    ],
    "unverified": [
      "查询回归测试命令待执行"
    ],
    "next_task": {
      "name": "核对查询接口契约",
      "acceptance": "字段和错误码逐项对应"
    }
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：每个事实标注来源与核验状态；历史决定和当前要求不混写；未验证命令不标记为测试通过；共享资料不含真实密钥或无关个人信息。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
