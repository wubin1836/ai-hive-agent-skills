# Claude Opus 5旧系统改造助手：场景示例

## 场景一：首次执行

```text
用Claude Opus 5改造这个旧报表服务，先只把CSV导出模块迁到新接口，旧调用方必须继续可用。先做依赖图和基线测试，再交一个可回退的小补丁，不动生产库。
```

输入记录示例：

```json
{
  "repository": "legacy-reporting",
  "target_module": "csv-export",
  "compatibility": "保留旧export接口及列顺序",
  "excluded": [
    "生产数据库",
    "登录模块"
  ],
  "rollback_requirement": "可恢复旧适配器"
}
```

人工构造的输出片段，仅用于解释格式；不是付费模型生成结果或测试成绩：

```json
{
  "illustrative_only": true,
  "sample": {
    "example_only": true,
    "execution_status": "人工示例，未执行",
    "phase": {
      "id": "M1",
      "change": "新增导出适配层并保留旧接口",
      "acceptance": "同一样例导出的列顺序与转义一致",
      "rollback": "恢复旧适配器路由"
    },
    "baseline_status": "待运行"
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：每个阶段明确输入依赖、验收标准和回退条件；本轮补丁没有扩展到未授权模块；关键接口和业务行为有前后对照证据；未执行的数据迁移或回退演练不写成成功。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
