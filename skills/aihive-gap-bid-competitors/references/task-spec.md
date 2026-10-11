# 竞争对手中标情报助手：交付契约

## 任务示例

看看这两家同行在我提供的公开中标样本里主要做什么地区和采购类别，联合体项目单独列。

## 人工测试场景（不是实际客户案例）

人工测试：A与B联合体中标100万元，无法分配成员金额时只记录联合体100万元，A、B各自金额均为未知。

## 反例与停止点

简称相同、注册地区不同且无一致识别信息：分别保留为待核对实体。

## 交付字段

### entity-review.csv

observed_name,canonical_entity,public_id,decision,evidence_ref。

### competitor-awards.csv

entity,project_key,buyer,region,category,amount_type,amount,consortium_role,source_ref。

### competitive-map.md

样本趋势、联合体归属限制、未覆盖区域与可验证结论。

字段名是文件契约，不是AI-HIVE工具参数。具体调用仍读实时schema。缺失项保留空值和原因，不把未知填0；CSV供表格打开时防止以 =、+、-、@ 开头的非数值来源文字变成公式。

## 执行证据

交付时附本次输入范围、实际处理工具、输出位置及已检查／未检查项。说明资料来自用户、官方网页还是模型分析。不得把人工示例、待填模板、模型推断写成已发生事实。

如果需要Word／Excel／PPT／音视频成品，检查宿主是否真有对应制作和检查工具；没有就交付当前可完成的中间文件，并列明尚缺的工具。对外发布、发送或系统写入另需对应授权。
