# 第 3 课 Starter Pack：微观调查数据的审查、清理、合并

《朱晨的 AI 智能体课：Claude Code 经济学研究实战》· 朱晨 · 中国农业大学经济管理学院

第 3 课的课后作业约 2 小时，自学完成，不需要提交。第一次做的同学，先看 `第3课课后作业使用说明.pdf`。

本课的项目文件夹用 research harness 仓库：
https://github.com/maxwell2732/claudecode-research-harness-workflow

这个 starter pack 解压到 `~/lab3_starter/`，只当参考资料，不要把数据放进来。

## 文件说明

| 文件 | 用途 |
| --- | --- |
| `第3课课后作业使用说明.pdf` | 图文版操作说明，先看这份 |
| `lab3_handout.md` | 作业说明（文字版） |
| `lab3_verify_checklist.md` | 验收清单，做完逐项自查 |
| `prompts.md` | 本课用到的提示：可行性、审查、清理、新会话检查、子智能体 |
| `data_rules_for_CLAUDE.md` | 授权数据规则，用 `cat` 追加到项目 CLAUDE.md 的末尾，然后重启 Claude Code |
| `settings.json.template` | 禁止智能体编辑原始数据的 deny 规则，复制为 `.claude/settings.json` |
| `hash_raw.py` | 原始数据哈希校验：清理前存，清理后核对 |
| `codebook_from_dta.py` | 参考脚本：从 Stata 变量标签生成变量清单和 codebook |
| `checked_merge.py` | 参考函数：带报告的合并，自动检查合并关系 |
| `download_wdi_modules.py` | 备选路线：下载世界银行的几个“模块”文件 |
| `exit_ticket.md` | 课后 exit ticket |

## 数据说明

- 课程不分发任何数据。CHNS、CHARLS 请自行申请下载，不得分享，不得上传到公开仓库。
- 原始数据和清理后的个体数据都不进 Git。`raw_hashes.txt` 只有文件名和哈希值，可以提交。
