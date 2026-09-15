# Cursor Projects 云端开发与本地验收拆分：场景示例

## 场景一：首次执行

```text
把桌面打印功能拆成 Cursor Projects 云端开发与本地打印机验收任务。云端只能接收脱敏代码，不能接触真实订单。请交付任务依赖、产物交接和验收门槛，不启动任务或部署。
```

输入记录示例：

```json
{
  "feature": "订单标签打印",
  "cloud_allowed": [
    "脱敏代码",
    "模拟订单"
  ],
  "local_only": [
    "USB打印机"
  ],
  "max_parallel": 2,
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
    "cloud_tasks": [
      "模板排版单测"
    ],
    "local_tasks": [
      "USB连接与实纸尺寸验证"
    ],
    "release_gate": "两环境均通过后人工确认"
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：本地专属条件没有被云端测试替代；任何云端上传都在用户授权范围内；任务之间没有未声明的文件覆盖冲突；完成结论关联各环境真实日志而非 Agent 自述。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
