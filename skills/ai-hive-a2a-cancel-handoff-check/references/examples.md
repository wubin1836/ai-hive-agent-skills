# A2A跨智能体取消与交接状态核验助手：场景示例

## 场景一：首次执行

```text
主Agent显示已取消，但子Agent仍有产物返回。请根据我提供的任务事件核对真正终态和已发生动作，给出只读核验清单，不再发取消或重新派单。
```

输入记录示例：

```json
{
  "mode": "演示数据",
  "task_id": "remote_9",
  "events": [
    {
      "type": "cancel_requested"
    },
    {
      "type": "state",
      "value": "working"
    },
    {
      "type": "artifact",
      "name": "draft.md"
    }
  ]
}
```

人工构造的输出片段，仅用于解释格式；不是付费模型生成结果或测试成绩：

```json
{
  "illustrative_only": true,
  "sample": {
    "mode": "人工演示，未联系远端",
    "canceled_verified": false,
    "observed_state": "working",
    "artifact_received": "draft.md",
    "next": "在授权范围查询remote_9的最新终态"
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：消息接收回执不被当作任务完成。；取消请求已发送与远端已取消分开记录。；产物可回指任务且符合约定完成标准。；网络未知不会自动再创建同一远端任务。。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
