# 第 4 课 Starter Pack：计量识别与论文复现，写出第一个 Skill

《朱晨的 AI 智能体课：Claude Code 经济学研究实战》· 朱晨 · 中国农业大学经济管理学院

第 4 课的课后作业约 2 小时，自学完成，不需要提交。第一次做的同学，先看 `第4课课后作业使用说明.pdf`。

作业接着在第 3 课的项目文件夹 `~/lab3` 里做，那里已经有清理好的面板和数据保护设置。这个 starter pack 解压到 `~/lab4_starter/`，只当参考资料，不要把数据放进来。

## 文件说明

| 文件 | 用途 |
| --- | --- |
| `第4课课后作业使用说明.pdf` | 图文版操作说明，先看这份 |
| `lab4_handout.md` | 作业说明（文字版） |
| `lab4_verify_checklist.md` | 验收清单，做完逐项自查 |
| `prompts.md` | 本课用到的提示：DID 可行性、处理时间表、审稿、读论文、定目标、起草和测试 skill |
| `treatment_timing_template.csv` | DID 路线：处理时间表模板，每个处理单位一行，注明出处 |
| `paper_reading_template.md` | 复现路线：六项格式读论文 |
| `replication_targets_template.md` | 复现路线：复现目标和容差的写法 |
| `targets_template.csv` | 复现路线：给 `compare_targets.py` 用的目标表 |
| `compare_targets.py` | 先锁定目标和容差，复现后自动判断 PASS / FAIL / NOTE |
| `event_study_plot.py` | 从系数表画事件研究图，并汇总处理前系数 |
| `SKILL_skeleton.md` | SKILL.md 骨架，附 description 的好坏例子 |
| `llm_measurement_checklist.md` | 用大模型构造变量时的检查清单：八个问题、前视偏差、六步验证、成本 |
| `exit_ticket.md` | 课后 exit ticket |

## 数据说明

- 课程不分发任何数据。CHNS、CHARLS 请自行申请下载，不得分享，不得上传到公开仓库。
- 没有 CHNS 或 CHARLS 的同学，可以用自己手头的数据，配一篇用同类数据的已发表文献来练。
- 论文 PDF 有版权，放在本地，不要提交到公开仓库。
