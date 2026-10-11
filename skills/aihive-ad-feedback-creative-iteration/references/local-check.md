# 投放指标核算

需要 Python 3.9+，仅标准库，不安装包、不联网、不访问密钥。读取用户明确指定的文件，默认只输出JSON到终端，不写改原文件。

## 从本Skill目录运行

```sh
python3 scripts/campaign.py examples/valid-input.json
python3 scripts/campaign.py examples/invalid-input.json
```

第二条是刻意失败的测试，退出码应为2，不是程序故障。通过返回0，输入错误/检查不通过返回2；warning仍需人工复核。换成真实输入时使用你已获授权的明确路径。

## 输入契约

records每行含asset_id、impressions、clicks、conversions、spend、revenue、currency。计数为非负整数；金额非负。一次输入必须相同归因/统计周期，币种分别聚合。

## 输出与限制

CTR=点击/曝光，CVR=转化/点击，CPA=消耗/转化，ROAS=收入/消耗。CTR/CVR是比率不是百分数；零分母返回null。计数异常提示，不推断显著性或因果。

## 样例

examples中仅含虚构测试数据。valid-expected.json给出真实运行该样例的结果；invalid-expected.json记录应被拦截的错误。不要把这些样例结果宣传为平台实际测评。
