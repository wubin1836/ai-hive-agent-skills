# SRT时间与负荷检查

需要 Python 3.9+，仅标准库，不安装包、不联网、不访问密钥。读取用户明确指定的文件，默认只输出JSON到终端，不写改原文件。

## 从本Skill目录运行

```sh
python3 scripts/subtitle.py examples/valid-input.srt
python3 scripts/subtitle.py examples/invalid-input.srt
```

第二条是刻意失败的测试，退出码应为2，不是程序故障。通过返回0，输入错误/检查不通过返回2；warning仍需人工复核。换成真实输入时使用你已获授权的明确路径。

## 输入契约

输入UTF-8/BOM SRT文件。序号从1连续；时间格式HH:MM:SS,mmm --> HH:MM:SS,mmm。--max-cps可设置每秒可见字符提示阈值，默认20只是样例阈值，不是平台规范。

## 输出与限制

检测格式、倒序、非正时长、重叠与空字幕；超负荷作为warning。不能证明翻译、口型、发音或版权正确。

## 样例

examples中仅含虚构测试数据。valid-expected.json给出真实运行该样例的结果；invalid-expected.json记录应被拦截的错误。不要把这些样例结果宣传为平台实际测评。
