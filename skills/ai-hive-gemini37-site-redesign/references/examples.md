# Gemini3.7 Flash旧网站改版与回归检查：场景示例

## 场景一：首次执行

```text
用Gemini3.7 Flash改进旧站产品页的手机布局和询价表单，保留现有接口、字段和路由。先说明改动范围，再给补丁及回归检查；没有浏览器就把视觉测试标为待运行，不上线。
```

输入记录示例：

```json
{
  "page": "/products/a",
  "issues": [
    "360px宽度出现横向滚动",
    "提交中状态不明显"
  ],
  "must_preserve": [
    "POST /api/inquiry",
    "字段name和email"
  ],
  "browser_available": false
}
```

人工构造的输出片段，仅用于解释格式；不是付费模型生成结果或测试成绩：

```json
{
  "illustrative_only": true,
  "sample": {
    "example_only": true,
    "mode": "人工演示，未调用真实模型",
    "plan": [
      "约束商品图区宽度并检查长文本换行",
      "增加提交状态提示，不改API字段"
    ],
    "patch_status": "未应用草案",
    "checks": [
      {
        "case": "360px无横向溢出",
        "status": "待运行"
      }
    ],
    "files": [
      "redesign.patch",
      "before-after-review.md",
      "site-regression.json"
    ]
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：既有路由、表单字段和接口契约未被静默改变；移动端与键盘操作有真实检查结果或待测标记；视觉对照截图必须来自真实工具，不伪造浏览器验证；改版范围与补丁文件符合用户授权。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
