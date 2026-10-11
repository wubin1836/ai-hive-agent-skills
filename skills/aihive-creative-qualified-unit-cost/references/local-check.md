# 合格素材成本

需要 Python 3.9+，仅标准库，不安装包、不联网、不访问密钥。读取用户明确指定的文件，默认只输出JSON到终端，不写改原文件。

## 从本Skill目录运行

```sh
python3 scripts/cost.py examples/valid-input.json
python3 scripts/cost.py examples/invalid-input.json
```

第二条是刻意失败的测试，退出码应为2，不是程序故障。通过返回0，输入错误/检查不通过返回2；warning仍需人工复核。换成真实输入时使用你已获授权的明确路径。

## 输入契约

records每行是一笔实际费用，包含output_id、cost（非负数字）、currency（三位大写）、accepted（布尔值）。所有重试与人工归集费用均需记录。相同output_id的合格次数去重；同一output_id不可跨币种。

## 输出与限制

按币种返回总成本、尝试条数、唯一合格件数、单位成本。零合格返回null；不提供跨币种总计。费用缺失不能填0。accepted用于最终合格统计，不表示真实AI质检。

## 样例

examples中仅含虚构测试数据。valid-expected.json给出真实运行该样例的结果；invalid-expected.json记录应被拦截的错误。不要把这些样例结果宣传为平台实际测评。
