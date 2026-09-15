# Flare游戏道具图标与缩略可读性检查：场景示例

## 场景一：首次执行

```text
用GPT Image2.5 Flare做三个原创背包道具图标：药草瓶、铜钥匙、蓝晶石。统一左上光、3/4视角，最终在64像素下能认清，不参考任何现有游戏IP。
```

输入记录示例：

```json
{
  "items": [
    {
      "asset_id": "potion-01",
      "name": "药草瓶"
    },
    {
      "asset_id": "key-01",
      "name": "铜钥匙"
    },
    {
      "asset_id": "crystal-01",
      "name": "蓝晶石"
    }
  ],
  "display_size_px": 64,
  "light": "左上",
  "view": "3/4"
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
      "prop-icons-preview.png",
      "prop-assets.json",
      "prop-readability.csv"
    ],
    "target_display_px": 64,
    "engine_import_performed": false
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：asset_id唯一且与道具名称对应；缩略图下不同道具不易混淆；主光、视角和边距保持同套规则；无未经授权的商业游戏标识或资产复刻。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
