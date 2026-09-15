# Claude Fable软件项目开发助手：场景示例

## 场景一：首次执行

```text
用Claude Fable 5.1做一个本地设备借用登记工具，支持登记、归还和逾期列表，先不做登录与消息通知。用SQLite和样例数据，交付能启动的源码、说明及验收表，不上线。
```

输入记录示例：

```json
{
  "project": "设备借用登记",
  "features": [
    "登记借用",
    "登记归还",
    "逾期列表"
  ],
  "stack": "Python与SQLite",
  "excluded": [
    "登录",
    "发消息",
    "公网部署"
  ],
  "output_directory": "equipment-demo"
}
```

人工构造的输出片段，仅用于解释格式；不是付费模型生成结果或测试成绩：

```json
{
  "illustrative_only": true,
  "sample": {
    "example_only": true,
    "execution_status": "人工示例，未执行",
    "entities": [
      "equipment",
      "loan"
    ],
    "acceptance_case": {
      "id": "A03",
      "given": "借用单到期且未归还",
      "expected": "显示在逾期列表",
      "status": "待实现与运行"
    },
    "data_mode": "样例数据"
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：主流程可按启动说明在本地复现或明确列出阻塞；样例配置没有真实密钥和生产地址；需求与验收用例一一对应；演示数据、未接入服务和未实现功能标记清楚。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
