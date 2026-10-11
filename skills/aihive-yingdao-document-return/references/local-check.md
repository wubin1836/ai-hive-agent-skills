# 抽取字段检查

需要 Python 3.9+，仅标准库，不安装包、不联网、不访问密钥。读取用户明确指定的文件，默认只输出JSON到终端，不写改原文件。

## 从本Skill目录运行

```sh
python3 scripts/fields.py examples/valid-input.json
python3 scripts/fields.py examples/invalid-input.json
```

第二条是刻意失败的测试，退出码应为2，不是程序故障。通过返回0，输入错误/检查不通过返回2；warning仍需人工复核。换成真实输入时使用你已获授权的明确路径。

## 输入契约

required为非空字段名数组；fields为name、value、source对象数组。必填不能为null/空字符串；已有值必须有来源文本。

## 输出与限制

返回缺值、缺来源和业务复核状态。不比较原文件、不做OCR、不核实来源真实性或算术。

## 样例

examples中仅含虚构测试数据。valid-expected.json给出真实运行该样例的结果；invalid-expected.json记录应被拦截的错误。不要把这些样例结果宣传为平台实际测评。
