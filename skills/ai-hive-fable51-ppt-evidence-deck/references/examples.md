# Claude Fable 5.1 PPT生成助手：场景示例

## 场景一：首次执行

```text
用Claude Fable 5.1把这份季度经营表和项目纪要做成10页汇报PPT，听众是业务负责人，时长8分钟。沿用模板，所有数字给出处，缺数别补。交付可编辑PPTX、引用表和版面检查；没有对应模型或导出工具就明确停在哪一步。
```

输入记录示例：

```json
{
  "files": [
    "Q3经营.xlsx",
    "项目纪要.md"
  ],
  "template": "公司模板.pptx",
  "pages": 10,
  "minutes": 8,
  "audience": "业务负责人"
}
```

人工构造的输出片段，仅用于解释格式；不是付费模型生成结果或测试成绩：

```json
{
  "illustrative_only": true,
  "sample": {
    "example_only": true,
    "execution_status": "人工示例，未执行",
    "slides": [
      {
        "page": 3,
        "claim": "新增客户主要来自渠道A",
        "source": "Q3经营.xlsx!渠道汇总!A2:D8",
        "chart": "分渠道新增客户柱状图"
      }
    ],
    "open_questions": [
      "渠道B九月数据未提供"
    ],
    "export_status": "PPTX待宿主制作与渲染"
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：所有经营数字能定位到源表或标明待补；图表单位、时间区间与原始资料一致；逐页渲染检查完成并记录未解决问题；PPTX无法导出时明确待执行，不把内容大纲冒充文件。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
