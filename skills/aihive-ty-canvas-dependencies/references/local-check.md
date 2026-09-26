# 镜头依赖图格式与检查

边 `from -> to` 表示 to 执行前需要 from；纯相似、引用说明不要伪造成执行依赖。

```json
{"nodes":[{"id":"actor"},{"id":"shot01"},{"id":"export"}],"edges":[{"from":"actor","to":"shot01"},{"from":"shot01","to":"export"}]}
```

在当前 Skill 目录运行 `python3 scripts/check_dependency_graph.py dependencies.json`。
程序只读输入并向标准输出打印审计 JSON，成功退出码 0；缺失节点、重复 ID 或循环时退出码 1。`cycle_or_downstream_blocked` 可能含循环下游节点，不是精确循环成员列表。它不生成图片、不会提交模型任务。根据输出先修复图，再绘制本地看板。
