# 简单分账瀑布

需要 Python 3.9+，仅标准库，不安装包、不联网、不访问密钥。读取用户明确指定的文件，默认只输出JSON到终端，不写改原文件。

## 从本Skill目录运行

```sh
python3 scripts/share.py examples/valid-input.json
python3 scripts/share.py examples/invalid-input.json
```

第二条是刻意失败的测试，退出码应为2，不是程序故障。通过返回0，输入错误/检查不通过返回2；warning仍需人工复核。换成真实输入时使用你已获授权的明确路径。

## 输入契约

gross、deductions、recoup_due为非负金额；share_rate在0到1；currency必填；minor_units为0到6，默认2。输入金额须符合已确认结算小数位，超出则拒绝，先明确合同舍入规则。仅用于合同已确认先扣除、再回本、再分成的场景。

## 输出与限制

净收入=收入-扣除；可回本=min(max(净收入,0),待回本)；分配池=max(净收入-回本,0)；分成按比例四舍五入。单列亏缺、未回本及余额。复杂阶梯/税费/保底条款拒绝套用。

## 样例

examples中仅含虚构测试数据。valid-expected.json给出真实运行该样例的结果；invalid-expected.json记录应被拦截的错误。不要把这些样例结果宣传为平台实际测评。
