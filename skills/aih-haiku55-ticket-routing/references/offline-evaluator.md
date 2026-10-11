# 离线评估说明

Python 3标准库，无网络、不改输入文件。输入为JSON数组，不是CSV，示例全部虚构。

在本Skill目录运行：

    python3 scripts/evaluate.py assets/example-input.json

将参数换成用户授权的记录文件即可。JSON输出到终端，异常仅回报类型，不回显任意输入。若需保存，由宿主按用户选定路径保存，不覆盖唯一原件。

每条是同一模型的一个案例，重试费用先合并到cost；不允许重复case_id。status为completed/failed/timeout/cancelled/pending；passed仅true/false/null，通过要求completed及evidence。未知费用null，币种分组，合格任务成本包括失败费用；任一费用缺失则total_cost和cost_per_accepted为null。p95为现有延迟样本的nearest-rank，不代表生产SLA。

assets/result-template.csv是人工交接表，不是脚本输入。该脚本不发请求，也不能证明模型已接通。
