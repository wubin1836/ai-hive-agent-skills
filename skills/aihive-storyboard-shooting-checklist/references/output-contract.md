# 输出契约

本项：短剧分镜转拍摄清单助手。下列文件是应生成的业务产物，未运行时明确标记草稿，不用虚构数据填满。

| 文件 | 必需内容或字段 |
|---|---|
| `shoot-checklist.csv` | shoot_order,story_order,shot_id,location,cast,props,camera,sound,reset |
| `resource-conflicts.csv` | resource,conflicting_shots,required_time,available_time,resolution |
| `media-return.csv` | shot_id,take,video_file,audio_file,usable,notes |

## 最小走读示例（纯虚构）

虚构两场共用咖啡馆可连拍，但上午/夜晚戏分别记录灯光方案和窗外状态。

这是演示决策边界，不是真实客户数据、测评、平台回执或生成结果。运行任务时替换为用户实际素材与核验记录。

## 验收逐项记录

- [ ] 每个分镜有拍摄或明确取消状态
- [ ] 声音素材能映射镜头
- [ ] 场地安全与许可由制作方核实
- [ ] 每个文件有任务ID、来源引用/版本和生成或计算日期；未知数据保留null/待确认，不能写0冒充已知。
- [ ] 计算给出公式、单位、时间范围；语言/图像判断附实际证据。
- [ ] 未做付费调用、未上传或未发布的环节如实标记，不把草稿当执行结果。

## 交付回复格式

已交付：文件与路径。核验：哪些静态/本地/人工检查通过。未完成：缺工具、缺资料或待批准事项。下一步：一项最小可执行动作。
