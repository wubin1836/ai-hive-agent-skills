# 本地互动状态格式与检查

```json
{"start":"intro","states":[{"id":"intro","transitions":[{"event":"choose","to":"scene"},{"event":"exit","to":"end"}]},{"id":"scene","transitions":[{"event":"finish","to":"end"},{"event":"exit","to":"end"}]},{"id":"end","terminal":true,"transitions":[]}]}
```

在当前 Skill 目录运行 `python3 scripts/check_story_state.py story-state.json`。
若要回放事件，另建 JSON 文件，内容如 `["choose","finish"]`，再运行 `python3 scripts/check_story_state.py story-state.json --events events.json`。

检查包括重复状态、未知目标、同状态同事件歧义、不可达节点、无出口和无法抵达结局的循环。合法循环只要保留退出路径就可通过；存在路径不证明所有用户一定会退出。回放结束 `ended:false` 表示仍处中间状态，不应谎报完整结局。成功退出码 0，结构或事件错误为 1。脚本无网络、无计费、无视频播放或生成，不能用于宣称实时性能达标。真实系统还需会话ID、时间戳、权限与取消机制。
