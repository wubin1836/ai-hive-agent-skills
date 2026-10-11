# 结果、证据与离线校验

本包：客户跟进私人销售助手。
专用领域字段：customer_ref, stage, last_promise, next_action, contact_permission。

## 结果记录

使用 assets/result-template.json 中的records，每项有稳定id，多个输入不要互相覆盖。
domain每个字段用state标记known / unknown / not_applicable；known附source_ref，not_applicable附reason。unknown不等于零或否。
来源可以是用户文件行号、页码、实际工具回执或明确的计算输入。模型推测不能伪装成已观察事实。

状态可选 planned / awaiting_user / ready / submitted / completed / accepted / review_required / failed / cancelled。
- planned等执行前状态：executed=false。
- completed：必须有实际执行、证据及产物。
- accepted：除以上条件，还需checked=true，关键领域字段不含unknown。
- 草稿也能作为本次“制作草稿”请求的合格产物；但要保持action_kind=draft，不能宣称完成对外操作。
- 对外发信、付款、删除、业务回写必须有本次明确授权的引用；authorization_ref仅存位置/编号，不存密钥。
- external_receipt必须有真实provider_task_id；不存在官方编号时保持待人工核验，不编造。

artifacts每项保存相对path和真实文件sha256。默认在结果文件目录内核验，禁止借路径越界读取其他文件。
如果用户只要答复，可把可审阅结果保存为本地文件再记录，不需要制造多余业务动作。

## 运行只读检查器

从Skill目录运行：
```sh
python3 scripts/check_result.py /absolute/path/to/result.json --artifact-root /absolute/path/to/output-directory
```

检查器只读JSON与指定目录的产物，检查结构、状态前提、来源引用、重复id和文件哈希；不会联网、发消息、付款或上传文件。
通过检查不代表内容真实、授权充分、业务办理成功或模型效果已测。仍需针对本任务查看真实产物并用领域验收条件复核。
