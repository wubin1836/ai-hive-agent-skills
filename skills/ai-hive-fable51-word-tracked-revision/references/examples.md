# Claude Fable Word文档修订助手：场景示例

## 场景一：首次执行

```text
用Claude Fable 5.1按意见表修改客户方案.docx，报价表和交付日期不能动。要求原生修订记录，保留每条意见的处理状态；工具不支持时先说明，不要用高亮冒充修订。
```

输入记录示例：

```json
{
  "file": "客户方案.docx",
  "comments": "意见表.csv",
  "protected": [
    "第4节报价表",
    "2026年10月20日"
  ],
  "track_changes": true
}
```

人工构造的输出片段，仅用于解释格式；不是付费模型生成结果或测试成绩：

```json
{
  "illustrative_only": true,
  "sample": {
    "example_only": true,
    "execution_status": "人工示例，未执行",
    "revisions": [
      {
        "comment_id": "C03",
        "anchor": "第2节第3段",
        "action": "压缩重复背景",
        "status": "待写入"
      }
    ],
    "conflicts": [
      {
        "comment_ids": [
          "C07",
          "C09"
        ],
        "question": "案例是否允许对外公开"
      }
    ],
    "native_track_changes": "待核验宿主支持"
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：原稿未覆盖且指定数字逐项保留；每条意见均有定位与处理状态；原生修订不可用时在交付中明确说明；导出后已回读并检查表格和页眉页脚。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
