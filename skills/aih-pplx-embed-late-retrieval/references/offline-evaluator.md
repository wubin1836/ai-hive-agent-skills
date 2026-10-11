# 离线评估说明

Python 3标准库，无网络、不改输入文件。输入为JSON数组，不是CSV，示例全部虚构。

在本Skill目录运行：

    python3 scripts/evaluate.py assets/example-input.json

将参数换成用户授权的记录文件即可。JSON输出到终端，异常仅回报类型，不回显任意输入。若需保存，由宿主按用户选定路径保存，不覆盖唯一原件。

每条包含query_id、relevant_ids、retrieved_ids。ID必须非空且不重复；relevant_ids需人工确认且非空，retrieved_ids可为空。默认k=5，可加--k 2；统计每题Recall@K、RR@K与宏平均，不衡量最终回答正确性。

assets/result-template.csv是人工交接表，不是脚本输入。该脚本不发请求，也不能证明模型已接通。
