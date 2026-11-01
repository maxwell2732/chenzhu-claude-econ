# 第 5 课综合作业：复制包或理论机制，二选一

预计用时约 2 小时。两条路线选一条；第三部分“写作”两条路线都要做。

| 路线 | 在哪里做 | 产出 |
| --- | --- | --- |
| 复制包路线 | `~/lab3`（第 3、4 课的项目） | 别人按 README 能重跑的复制包，全新克隆重跑通过 |
| 理论机制路线 | `~/pAI-Econ-claude` | 一节理论机制、一个可检验假说、假说依赖表、新会话审查意见 |

## 一、复制包路线

1. 一条命令重跑。参考 `run_all_template.sh`，在 `~/lab3` 写 `run_all.sh`，从原始数据一直跑到表、图和数字。
2. 数字由脚本生成。把 `numbers_out.py` 复制到 `scripts/`，在分析脚本里登记正文要用的数字（至少 5 个）。Stata 用户见 `numbers_out.py` 里的说明。
3. 装上 hook：

   ```
   mkdir -p .claude/hooks
   cp ~/lab5_starter/guard_data.py .claude/hooks/
   printf '#!/bin/sh\npython3 .claude/hooks/guard_data.py --git-pre-commit\n' > .git/hooks/pre-commit
   chmod +x .git/hooks/pre-commit
   ```

   再把 `hooks_settings_snippet.json` 里的 `"hooks"` 一段加进现有的 `.claude/settings.json`，和 `"permissions"` 并列。重启 Claude Code。
4. 测试 hook：让它 `git add` 一个 `.dta` 文件，确认被拦下。
5. 审查。有 `analysis_plan.md` 的运行 `/research-harness-review`；没有的，用 `prompts.md` 第 2 条在新会话里审查，裁决也写成 APPROVE / REQUEST_CHANGES / BLOCK。
6. 按 `README_replication_template.md` 写 `README.md`。
7. 提交所有修改，然后全新克隆重跑：

   ```
   python ~/lab5_starter/repro_check.py --cmd "bash run_all.sh" --outputs output --data data/raw
   ```

   不一致的文件，找到原因（随机数种子、样本排序、软件版本），修好再跑。

## 二、理论机制路线

1. 克隆 pAI-Econ-claude，在它的目录里启动 Claude Code：

   ```
   cd ~
   git clone https://github.com/maxwell2732/pAI-Econ-claude.git
   cd pAI-Econ-claude
   claude
   ```

2. 复制 `empirical_brief_template.txt` 到 `~/pAI-Econ-claude/my_brief.txt`，填上你第 4 课的结果和你认为的机制。没有显著结果也可以：把机制写成待检验的假说。
3. 运行：

   ```
   /mode empirical-companion --task my_brief.txt
   ```

4. 每次停下来都认真看，尤其是写完模型时的硬停（HiL-4）：基本设定和均衡概念由你确认。
5. 按 `hypothesis_dependence_template.md`，列出每个假说依赖哪些假设、哪些依赖特定函数形式。
6. 开一个新会话（可以在任何目录），用 `prompts.md` 第 5 条，只给模型设定和证明草图，让它检查推导。把意见和你的回应写下来。

## 三、写作（两条路线都做）

按我的写作顺序走一段，不用写完整篇论文。顺序和提示见 `prompts.md` 第二部分：

分析完成 → 1 数据与方法 → 2 定主题 → 3 文献综述 → 4 定贡献 → 5 定题目 → 6 列大纲 → 7 确认大纲 → 8 一章一章写

第 2、4、5、7 步由你决定，不交给它。论文稿放在 `paper/` 下，每一章一个文件。

1. **数据与方法**（W1）：让它根据脚本、日志、报告起草，写进 `paper/02_data_methods.md`。复制包路线写完跑 `check_numbers.py`。理论机制路线改写“模型设定”一节。
2. **贡献和题目**（W3）：自己在 `paper/contribution.md` 写三句话（发现了什么、文献缺什么、补上了什么）和一个暂定题目。可以让它挑毛病，不让它代写。
3. **大纲**（W4）：让它列大纲，你改到满意，在开头写“已确认”。
4. **只写一章**（W5）：按大纲写一节（建议写结果部分），写完它停下；你审改，再用 W6 让它当编辑过一遍，改不改你决定。`git commit`。
5. **记录**：按 `AI_USE_template.md` 记下每一步怎样用了 AI。
6. 可选：文献综述（W2），每条文献逐个核对 DOI 或链接；把 `writing_rules_example.md` 追加到 CLAUDE.md 并改成你的规则。

## 完成之后

1. 对照 `lab5_verify_checklist.md` 自查。
2. 填写 `exit_ticket.md`。
