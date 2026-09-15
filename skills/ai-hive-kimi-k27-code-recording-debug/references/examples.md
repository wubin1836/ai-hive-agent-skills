# Kimi K2.7 Code录屏排错与复现：场景示例

## 场景一：首次执行

```text
用Kimi K2.7 Code检查这段脱敏录屏：切换筛选后列表一直转圈。请先给准确时间线和最小复现，再结合我提供的源码与日志定位；没有运行条件就交未应用补丁和待运行测试。
```

输入记录示例：

```json
{
  "recording": "筛选故障.mp4",
  "observations": [
    {
      "time": "00:08",
      "event": "清空全部筛选"
    },
    {
      "time": "00:10",
      "event": "加载图标持续显示"
    }
  ],
  "code_excerpt": "if (!filters.length) return;",
  "runtime_available": false
}
```

人工构造的输出片段，仅用于解释格式；不是付费模型生成结果或测试成绩：

```json
{
  "illustrative_only": true,
  "sample": {
    "example_only": true,
    "mode": "人工演示，未读取真实录屏或调用模型",
    "hypothesis": "空筛选提前返回可能遗漏加载状态复位，需结合完整函数确认",
    "patch_status": "未应用草案",
    "regression": [
      {
        "case": "清空筛选后加载状态结束",
        "status": "待运行"
      }
    ],
    "files": [
      "recording-repro.md",
      "fix-draft.patch",
      "regression-checks.json"
    ]
  }
}
```

## 场景二：复核与返工

```text
请检查本次输出是否满足：每条视觉异常有录屏时间点或帧定位；网络和后端结论有日志证据，不能单凭转圈画面推断；补丁是否应用与测试是否运行分别记录；没有视频读取能力时不声称看过录屏。
把结论分成已验证、未验证、需补资料三类。只修复有证据的问题，不覆盖原文件；先列返工清单和额外调用费用。
```

复核记录建议字段：`check / evidence / actual / status / next_action`。

## 场景三：当前模型或工具不可用

```text
如果当前AI-HIVE没有本任务需要的精确模型或工具，请不要生成冒名结果。给我已发现的能力、缺失条件、可先完成的本地准备材料，以及需要我选择的替代方案。
```

本地演练：在MCP未配置时仍可执行 `scripts/workflow.py`，但其结果必须保持 `phase=offline_plan`、`model_calls=0`。这只能验证工作单，不是验证模型能力。
