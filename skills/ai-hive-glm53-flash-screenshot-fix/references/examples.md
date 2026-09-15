# GLM5.3 Flash截图问题转修复任务：场景示例

## 场景一：首次执行

```text
用GLM5.3 Flash检查这张订单页截图：按钮在手机宽度被挤出卡片。请按位置和文案定位到组件，给只改布局的补丁及同尺寸复测清单，不改接口；不能实际截图就标待验证。
```

输入记录示例：

```json
{
  "image": "订单页脱敏截图.png",
  "viewport": {
    "width": 390,
    "height": 844
  },
  "observed": "确认按钮右侧超出卡片",
  "component": "OrderActions.tsx",
  "browser_available": false
}
```

人工构造的输出片段，仅用于解释格式；不是付费模型生成结果或测试成绩：

```json
{
  "illustrative_only": true,
  "sample": {
    "example_only": true,
    "mode": "人工演示，未读取真实图片或调用模型",
    "issue": {
      "anchor": "卡片底部“确认”按钮右侧",
      "category": "布局溢出待源码确认",
      "backend_cause": "截图不足以判断"
    },
    "patch_status": "未应用草案",
    "visual_test": "待运行",
    "files": [
      "screenshot-issues.csv",
      "ui-fix.patch",
      "visual-recheck.md"
    ]
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：每个问题有可见位置、文案或参考依据；后台原因不凭静态截图直接断定；前后验证条件包含尺寸、数据和页面状态；没有真实复截图时不报告像素对比通过。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
