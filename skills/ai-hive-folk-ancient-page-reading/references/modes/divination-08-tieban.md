# 铁板神数条文检索助手

这是古籍工具的可选专题模式。仅在用户点名且有相应授权原件时使用，不改变基础OCR任务。

仅供传统文化、学习与娱乐参考，尊重科学；不宣称能够科学预测命运，不作为投资、医疗、法律、婚姻等重大决策依据。

## 本模式输入

- 用户合法持有的带条文号图页或表格
- 书名、版本及页码
- 已有条文号清单；不要求生辰或家属信息

## 专题处理

1. OCR 提取条文号、文本和页码，数码易混淆位置要求人工确认
2. 脚本建立版本内唯一键，检测重号、跳号与不同版本相同编号的文字差异
3. 导出离线检索页与重号漏号报告，只按用户给定编号检索不推算命数

## 专题输出

- `tieban-lookup.html`
- `tieban-entries.csv`
- `tieban-number-audit.pdf`

## 验收与边界

仅供传统文化研究、娱乐参考，尊重科学。不凭条文断亲属、能力、寿命或灾祸；不索取家族隐私做所谓考刻，不承诺神准或改命。

来源以用户指定的具体版本为准；所有条目保留章节、页码与不确定标记。

仅对本模式交付使用对应 JSON 规格运行 artifact_audit.py verify，不要求同时生成未选择模式的文件。

## 搜索叫法

铁版神数、鐵版神數、铁板神算、铁版数、铁版条文查询

## 来源入口

- [资料入口 1](https://rbook.ncl.edu.tw/NCLSearch/Search/SearchDetail?HasImage=&SourceID=1&item=49f4fe556f704d2e95005f9acc9515ebfDQxMDg4OA2.qnNRVTXqBwc45Fho4aWgdvXq9lbmqsskkj7irkPnENI_&page=14&sourceWhereString=&whereString=IChDcmVhdGVyX05hbWUgbGlrZSAnJemCtembjSUnIG9yIERvY3VtZW50X1dyaXRlciBsaWtlICcl6YK16ZuNJScgb3IgSm91cm5hbF9Xcml0ZXIgbGlrZSAnJemCtembjSUnICkg0.W_lha9rDT5_i5Z2XvmwCFQgyWBnMw5wVZAJZb4ixaaQ_))
- [资料入口 2](https://isbn.ncl.edu.tw/NEW_ISBNNet/main_DisplayRecord_Popup.php?KeepThis=true&Pact=view&Pkey=1150609%2A0217&TB_iframe=true&height=480&width=780)
