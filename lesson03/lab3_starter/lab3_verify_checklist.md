# 第 3 课验收清单

逐项自查。全部打勾后再进入第 4 课。

**保护**

- [ ] `.claude/settings.json` 里有 `Edit(./data/raw/**)` 的 deny 规则，`/permissions` 里能看到
- [ ] `git check-ignore data/raw` 有输出；`git status` 里看不到任何数据文件
- [ ] 清理前运行过 `hash_raw.py save`，清理后 `hash_raw.py check` 显示全部一致

**审查**

- [ ] 可行性提问的回答存进了 DECISIONS.md
- [ ] `reports/data_audit_report.md` 在清理脚本之前生成，你读过一遍
- [ ] 审查报告里列出了特殊缺失码、ID 是否唯一、各轮变量名差异；对含义不确定的编码，你对照问卷核对过（写下核对了哪几个：`____________`）

**清理与合并**

- [ ] 清理计划写明了每次合并的键、关系和预期匹配率
- [ ] 每次合并都有报告：左表、右表、合并后行数，匹配与未匹配数量；匹配率达到预期，或者解释了原因
- [ ] 至少一处合并用了 validate 参数检查关系
- [ ] 主路线：至少三轮合并成个人-年份面板；备选路线：剔除了汇总行，只保留国家

**Codebook**

- [ ] codebook 有 description 列，定义覆盖率 ≥ 99%（新造变量也有定义）
- [ ] 新会话只读 codebook，五个变量的含义都答对了
