# Sunburst包装换版与标签信息核对：场景示例

## 场景一：首次执行

```text
用Sunburst把这瓶洗发水照片换成我上传的2026-B标签稿，保持500mL瓶型、泵头和封口，逐字检查正面文字。只做展示预览，不生成生产批号。
```

输入记录示例：

```json
{
  "product": "SHAMPOO-500",
  "photo": "bottle-old.png",
  "approved_label": "label-2026-B.png",
  "locked": [
    "500mL瓶型",
    "泵头",
    "封口"
  ],
  "purpose": "展示预览"
}
```

人工构造的输出片段，仅用于解释格式；不是付费模型生成结果或测试成绩：

```json
{
  "illustrative_only": true,
  "sample": {
    "demo_only": true,
    "generation_status": "not_submitted",
    "actual_model": null,
    "task_id": null,
    "expected_files": [
      "package-preview.png",
      "package-version-check.csv",
      "package-provenance.json"
    ],
    "version_preview": {
      "sku": "SHAMPOO-500",
      "label_version": "2026-B"
    },
    "print_ready": false
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：商品照片与新版稿属于同一SKU；可见容量、品牌与文字顺序对照一致；瓶型、封口和不可编辑部件未变；没有把条码、生产批号或认证信息凭空补齐。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
