# 文件包检查

需要 Python 3.9+，仅标准库，不安装包、不联网、不访问密钥。读取用户明确指定的文件，默认只输出JSON到终端，不写改原文件。

## 从本Skill目录运行

```sh
python3 scripts/manifest.py examples/valid-input.json --root examples/payload
python3 scripts/manifest.py examples/invalid-input.json --root examples/payload
```

第二条是刻意失败的测试，退出码应为2，不是程序故障。通过返回0，输入错误/检查不通过返回2；warning仍需人工复核。换成真实输入时使用你已获授权的明确路径。

## 输入契约

files为非空相对路径数组；--root指定用户授权包根目录。禁止绝对路径、..、反斜杠歧义和指向根目录外的符号链接。仅在可信静态目录运行，避免检查过程中修改路径。

## 输出与限制

只读返回文件体积、SHA256、缺文件、空文件及相同内容清单。不创建压缩包、不移动、不删除、不输出文件正文，不判断内容合法性。

## 样例

examples中仅含虚构测试数据。valid-expected.json给出真实运行该样例的结果；invalid-expected.json记录应被拦截的错误。不要把这些样例结果宣传为平台实际测评。
