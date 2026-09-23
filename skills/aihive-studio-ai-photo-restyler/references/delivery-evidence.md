# 离线交付证据检查

仅在需要交付核对或断点续作时使用。脚本不联网、不改业务文件、不判断文案或媒体质量。

在输出目录建立 delivery-record.json，填真实信息：status为example、offline_checked或model_completed；artifacts为非空列表，各项path是输出目录内非空实际文件的相对路径，可附真实sha256；quality_review填写实际做过的预览或人工检查。

model_completed另须model_evidence对象，包含provider、model、request_or_task_id、completed_at。没有真实执行证据不得填这个状态。模型任务编号不是密钥，不记录Token。

运行：`python3 scripts/delivery_check.py /实际输出目录/delivery-record.json`。脚本会检查文件、路径边界、重复路径、可选哈希和状态证据字段；不会向服务端核实任务ID，不能用字段齐全代替真实执行或专业审查。产物的质量仍按本任务验收要求检查。
