# Google Pics 视觉批注转局部编辑合同：场景示例

## 场景一：首次执行

```text
把三位同事对这张封面的批注变成 Google Pics 局部编辑合同：营销要放大标题，设计要保留留白，品牌要锁定 Logo。先列冲突和区域，不直接改图或发给同事。
```

输入记录示例：

```json
{
  "base_image": "cover-v1.png",
  "comments": [
    {
      "author_role": "营销",
      "change": "放大标题"
    },
    {
      "author_role": "设计",
      "change": "保留右侧留白"
    }
  ],
  "locked": [
    "Logo"
  ],
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
    "unresolved": [
      "标题增大后的留白下限需确认"
    ],
    "locked_objects": [
      "Logo"
    ],
    "applied_edits": []
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：每条批注能追溯到区域与处理结论；冲突意见没有未经授权自动裁决；修改对象之外的副作用单独检查；没有原图或实际输出时不声称视觉验收通过。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
