# 第 5 课 Starter Pack：理论建模、写作与可审计性

《朱晨的 AI 智能体课：Claude Code 经济学研究实战》· 朱晨 · 中国农业大学经济管理学院

第 5 课的综合作业约 2 小时，自学完成，不需要提交。第一次做的同学，先看 `第5课课后作业使用说明.pdf`。

综合作业两条路线选一条：

- **复制包路线**：在 `~/lab3` 里，把第 3 课或第 4 课的流程加固成别人能重跑的复制包。
- **理论机制路线**：克隆 pAI-Econ-claude，用实证配套模式给第 4 课的结果写一节理论机制。

这个 starter pack 解压到 `~/lab5_starter/`，只当参考资料，不要把数据放进来。

## 文件说明

| 文件 | 用途 |
| --- | --- |
| `第5课课后作业使用说明.pdf` | 图文版操作说明，先看这份 |
| `lab5_handout.md` | 作业说明（文字版） |
| `lab5_verify_checklist.md` | 验收清单，做完逐项自查 |
| `prompts.md` | 本课用到的提示：加固、审查、按写作顺序的七条写作提示、检查推导 |
| `guard_data.py` | 数据文件不进 Git：可作 Claude Code 的 hook，也可作 Git 的 pre-commit |
| `hooks_settings_snippet.json` | `.claude/settings.json` 里 hook 和 deny 规则的写法 |
| `numbers_out.py` | 分析脚本里登记正文要用的数字，生成 numbers.json 和 LaTeX 宏 |
| `check_numbers.py` | 核对正文里的数字是否都能追到 numbers.json |
| `repro_check.py` | 全新克隆重跑，比较输出是否一致 |
| `run_all_template.sh` | 一条命令重跑整个流程的模板 |
| `README_replication_template.md` | 复制包 README 模板 |
| `AI_USE_template.md` | 记录哪些部分用了 AI、怎样核对 |
| `writing_rules_example.md` | 我的写作规则，可追加到你的 CLAUDE.md |
| `empirical_brief_template.txt` | 理论机制路线：给 pAI-Econ 的实证简报 |
| `hypothesis_dependence_template.md` | 理论机制路线：每个假说依赖哪些假设 |
| `exit_ticket.md` | 课后 exit ticket |

## 数据说明

- 课程不分发任何数据。CHNS、CHARLS 请自行申请下载，不得分享，不得上传到公开仓库。
- 没有 CHNS 或 CHARLS 的同学，用你自己的数据和第 4 课用过的文献。
- 复制包里不放数据，只写清楚怎样申请、放在哪个目录。
