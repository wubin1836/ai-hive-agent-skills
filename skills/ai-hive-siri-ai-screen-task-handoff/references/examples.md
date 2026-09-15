# Siri AI 屏幕任务的中文人工交接方案：场景示例

## 场景一：首次执行

```text
我在中国，用这张活动通知截图整理日程候选和要问主办方的问题，参考 Siri AI 的屏幕任务思路，但不要读取我的手机、改系统设置或创建日历。缺失字段请列出来。
```

输入记录示例：

```json
{
  "region": "中国",
  "input": "活动通知截图",
  "visible_text": "周五下午两点到店",
  "goal": "整理日程候选",
  "execute_external_actions": false
}
```

人工构造的输出片段，仅用于解释格式；不是付费模型生成结果或测试成绩：

```json
{
  "illustrative_only": true,
  "sample": {
    "example": true,
    "execution_status": "manual_handoff_only",
    "known": {
      "time": "14:00"
    },
    "needs_confirmation": [
      "周五的具体日期",
      "门店地址",
      "时区"
    ],
    "calendar_created": false
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：没有声称获得系统屏幕、个人语境或苹果应用原生权限；日程包含明确日期与时区，模糊信息等待确认；发送和写入动作保持未执行，除非用户另行授权且工具可用；地区与语言不可用时清楚标记而不是提供绕过方案。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
