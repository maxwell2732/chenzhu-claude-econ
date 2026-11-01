# 第 4 课作业：DID 或论文复现，写出你的第一个 skill

预计用时约 2 小时。两条路线选一条，最后都要写出一个 skill，并在新会话里测试。

## 两条路线

| 路线 | 做什么 | 写出的 skill |
| --- | --- | --- |
| DID 路线 | 用第 3 课的面板，评估一项你熟悉的政策 | `did-checklist` |
| 复现路线 | 选一篇用同类数据的已发表论文，复现一张主表 | `replication-targets` |

没有 CHNS 或 CHARLS 的同学：用自己手头的数据，配一篇用同类数据的已发表文献。DID 路线需要数据里有地区和年份，以及一项在不同地区、不同时间推行的政策；复现路线需要论文的样本和变量在你的数据里大体能找到。

## 准备

```
cd ~/lab3
mkdir -p reports/figures .claude/agents .claude/skills papers
python ~/lab3_starter/hash_raw.py check      # 原始数据仍然一致
```

可选：把审稿子智能体放进项目。

```
cd ~
git clone https://github.com/maxwell2732/codex-stata-for-economists.git
cp ~/codex-stata-for-economists/.claude/agents/econometric-reviewer.md ~/lab3/.claude/agents/
```

## DID 路线

1. 启动 `claude`，用 `prompts.md` 的 “DID 可行性” 提问。先不写代码。
2. 复制 `treatment_timing_template.csv` 到 `reports/treatment_timing.csv`，每个处理单位一行，起始时间和出处你自己核对政策原文。智能体可以帮你找文件，最后由你确认。
3. 在 `DECISIONS.md` 写下：对照组怎么定义，看事件研究图的标准（出图之前写）。
4. 让它估计：先 TWFE，再用一种 staggered 估计量（csdid、did、fixest::sunab 等），系数存成 `reports/event_study_coefs.csv`。
5. 用 `event_study_plot.py` 出图，对照第 3 步写下的标准判断。
6. 让 econometric-reviewer 审一遍，逐条回应，写进 `DECISIONS.md`。
7. 结果不理想，就如实写“设计支持不了因果结论”。不要换设定直到显著。

## 复现路线

1. 论文 PDF 放进 `~/lab3/papers/`（不要提交）。
2. 用 `prompts.md` 的 “读论文” 提问，按 `paper_reading_template.md` 写 `reports/paper_notes.md`。
3. 选一张主表，按 `replication_targets_template.md` 写目标和容差，同时填好 `reports/targets.csv`（`our_value` 留空）。
4. 跑回归之前锁定：`python ~/lab4_starter/compare_targets.py lock reports/targets.csv`。
5. 让它复现，把结果填进 `our_value`，运行 `python ~/lab4_starter/compare_targets.py compare reports/targets.csv`。
6. 在 `reports/replication_comparison.md` 的“偏差说明”里，给每个 FAIL 和 NOTE 写出原因。

## 写 skill（两条路线都做）

1. 在同一个会话里，用 `prompts.md` 的 “起草 skill” 让它写 `.claude/skills/<名字>/SKILL.md`。
2. 你来改：description 写成触发条件，需要人判断的地方写成“停下来问我”。参考 `SKILL_skeleton.md`。
3. 退出，开一个新会话。说一句应该触发的话，再说一句不该触发的话，记录结果。
4. 按测试结果改一轮，把两次测试的结果记进 `LOG.md`。

## 完成之后

1. 运行 `python ~/lab3_starter/hash_raw.py check`。
2. 对照 `lab4_verify_checklist.md` 自查。
3. 填写 `exit_ticket.md`。
