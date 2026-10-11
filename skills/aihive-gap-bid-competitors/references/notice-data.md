# 标讯资料与本地计算规范

只有使用公告去重、差分或统计脚本时才需要本规范。脚本是离线数据助手，不是爬虫、全国标讯库或第三方接口客户端。

## 输入

输入为 UTF-8 JSON 数组。示例见 `assets/notice-demo.json`，它是虚构测试记录，不是商机。

- 必需：`source_id`、`notice_id`、`title`、`source_ref`。来源内稳定公告ID优先；没有官方ID可用稳定URL哈希并明确派生规则，不能以标题当ID。
- 项目包：`buyer`、`project_id`、`package_id`。全项目且确认无分包时填写 `whole`；未知包号留空，不写whole。不同来源的同一项目必须有证据才能手工统一这些字段。
- 事件：`notice_type` 可为 intent/tender/correction/award/contract/termination/cancellation，`published_at` 为原始发布日期，`deadline` 有时刻时带时区。缺失不猜。
- 金额：`amount` 仅数值，`amount_unit` 用元/万元，`currency` 明确CNY等币种；`amount_type` 用budget/award/contract/ceiling。单价、折扣率、费率和分项价不写成项目总额。保留原文于来源材料。
- 分析字段：`region`、`category`。`observed_at` 仅表示本次采集时间，不代表内容更新。

## 命令

Python 3.9+ 标准库，无额外安装，不联网。输出必须是新文件，已有文件拒绝覆盖。

```bash
python3 scripts/notice_ledger.py normalize assets/notice-demo.json --output notice-normalized.json
python3 scripts/notice_ledger.py stats assets/notice-demo.json --output notice-statistics.json
python3 scripts/notice_ledger.py diff current.json --previous previous.json --output notice-changes.json
```

`normalize` 仅消除字段完全相同的事件副本（忽略observed_at），不自动模糊合并不同来源。字段不同会全部保留；人工规范化应保留别名映射与原始资料。

`diff` 用source_id＋notice_id对比两次原始数组；“本次未见”不是撤销。一个身份有多份不同内容则列冲突，不擅选最后一份。

`stats` 按项目包＋币种＋金额性质分组，元／万元换算用精确十进制。多个不同事件落入同一统计口径时默认排除，要求人工依据更正关系确认有效版本。应先确认终止状态、联合体归属与统计期间，再统计有效样本。脚本不知道本次没提供的后续公告。

## 不能由脚本证明的事

脚本不能证明来源真实、项目仍有效、企业符合资格、关联公司同一、时间是最新，不能自动决定联合体金额归属或把样本推算成全国市场。返回结构正确不等于业务结论已经通过复核。
