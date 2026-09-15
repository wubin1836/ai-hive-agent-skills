# Claude Sonnet 5批量文档处理助手：场景示例

## 场景一：首次执行

```text
用Claude Sonnet 5整理我选定的30份会议纪要，统一提取日期、议题和行动项，输出Markdown归档。先试3份，保留原文件；表格或扫描页提取失败的单列，不无限重试。
```

输入记录示例：

```json
{
  "selected_directory": "会议纪要_授权批次",
  "target_format": "Markdown",
  "required_fields": [
    "日期",
    "议题",
    "行动项"
  ],
  "sample_size": 3,
  "overwrite_originals": false
}
```

人工构造的输出片段，仅用于解释格式；不是付费模型生成结果或测试成绩：

```json
{
  "illustrative_only": true,
  "sample": {
    "example_only": true,
    "execution_status": "人工示例，未执行",
    "manifest_item": {
      "id": "DOC-008",
      "input": "部门B/周会.docx",
      "output": "DOC-008-周会.md",
      "status": "待处理"
    },
    "failure_example": {
      "id": "DOC-019",
      "reason": "扫描页需要OCR工具",
      "automatic_retry": false
    }
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：清单内每个文件恰有一个明确处理状态；原文件未覆盖且同名文件不会互相替换；完成项经过目标格式和关键内容检查；空白、损坏或未支持格式不会被标成成功。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
