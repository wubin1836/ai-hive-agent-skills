# 任务依赖检查

需要 Python 3.9+，仅标准库，不安装包、不联网、不访问密钥。读取用户明确指定的文件，默认只输出JSON到终端，不写改原文件。

## 从本Skill目录运行

```sh
python3 scripts/graph.py examples/valid-input.json
python3 scripts/graph.py examples/invalid-input.json
```

第二条是刻意失败的测试，退出码应为2，不是程序故障。通过返回0，输入错误/检查不通过返回2；warning仍需人工复核。换成真实输入时使用你已获授权的明确路径。

## 输入契约

tasks为非空对象数组。id唯一；depends_on为已有id数组；approval_required为布尔值，为true时approver必须非空。

## 输出与限制

返回拓扑序、缺节点/依赖环/缺审批人。不能验证真实权限，也不执行流程。

## 样例

examples中仅含虚构测试数据。valid-expected.json给出真实运行该样例的结果；invalid-expected.json记录应被拦截的错误。不要把这些样例结果宣传为平台实际测评。
