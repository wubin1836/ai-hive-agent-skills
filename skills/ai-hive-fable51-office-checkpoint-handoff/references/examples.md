# Claude Fable多步骤办公任务助手：场景示例

## 场景一：首次执行

```text
用Claude Fable 5.1整理这次客户活动的四项待办：合并名单、写主持稿、汇总物料和准备通知草稿。只做本地材料，不发消息。缺负责人就记录，完成一项留一个检查点，方便明天继续。
```

输入记录示例：

```json
{
  "tasks": [
    "合并名单",
    "写主持稿",
    "汇总物料",
    "准备通知草稿"
  ],
  "files": [
    "报名表.xlsx",
    "活动流程.docx"
  ],
  "allowed_actions": [
    "本地整理",
    "生成草稿"
  ],
  "forbidden_actions": [
    "发送通知",
    "创建日程"
  ]
}
```

人工构造的输出片段，仅用于解释格式；不是付费模型生成结果或测试成绩：

```json
{
  "illustrative_only": true,
  "sample": {
    "example_only": true,
    "execution_status": "人工示例，未执行",
    "task": {
      "id": "T04",
      "name": "准备通知草稿",
      "depends_on": [
        "T01",
        "T02"
      ],
      "status": "待上游完成",
      "external_send": "未授权"
    },
    "checkpoint": {
      "resume_from": "T01",
      "required_input": "确认重复报名处理口径"
    }
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：完成状态必须对应可找到且已检查的产物；每个阻塞有缺失条件和可继续的下一步；恢复任务不会重复外发或覆盖已修改成果；邮件发送、日程创建和发布不因待办文字自动执行。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
