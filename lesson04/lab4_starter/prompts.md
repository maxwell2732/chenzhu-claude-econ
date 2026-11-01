# 第 4 课提示

方括号里的内容换成你自己的。每个提示后面写了一个好的回答应该包括什么，用来判断它有没有做对。

## DID 路线

### 1. DID 可行性

```
我想用 data/processed/ 里的面板，评估【政策】对【结果变量】的影响。
动手之前先告诉我：处理组和对照组怎么定义，处理时间从哪里来、怎样核对，
哪几轮在处理前，有没有需要担心的同期政策。先不要写代码。
```

好的回答会提到：处理时间要逐个单位核对出处；处理前至少需要两轮；对照组里有没有后来也被处理的单位；同一时期的其他政策。

### 2. 处理时间表

```
帮我找【政策】在各个【城市/省份】的起始时间，填进 reports/treatment_timing.csv，
列是 unit, unit_name, treat_start, source, source_url_or_page, note。
每一行都要写出处；找不到原文的，treat_start 留空，note 写“待核对”。不要猜。
```

拿到以后，你自己逐行打开出处核对。

### 3. 估计

```
按 reports/treatment_timing.csv 的起始时间编码处理变量。
先估计一个 TWFE，再用【csdid / did / fixest::sunab】估计事件研究，
基期设为 -1，标准误按【单位】聚类。
系数存成 reports/event_study_coefs.csv（rel_time, estimate, ci_low, ci_high）。
不要改动我在 DECISIONS.md 里写的主设定。
```

出图：`python ~/lab4_starter/event_study_plot.py reports/event_study_coefs.csv reports/figures/event_study.png`

### 4. 审稿

```
用 econometric-reviewer 审查估计代码和 reports/treatment_timing.csv。
重点看处理时间、对照组、聚类层级和处理前趋势。按严重程度列出问题，先不要改代码。
```

逐条决定接受还是拒绝，理由写进 `DECISIONS.md`。

## 复现路线

### 5. 读论文

```
读 papers/【论文】.pdf，按 ~/lab4_starter/paper_reading_template.md 的六项，
写 reports/paper_notes.md。主要结果写明表号、列号、系数、标准误和样本量。
找不到的写“论文未说明”，不要补。
```

### 6. 定目标

```
从 paper_notes.md 里选表【X】第【Y】列，按 ~/lab4_starter/replication_targets_template.md
写 reports/replication_targets.md，并填 reports/targets.csv（our_value 留空）。
容差先给建议，停下来等我确认。
```

确认后运行 `compare_targets.py lock`。

### 7. 复现和对比

```
按 replication_targets.md 复现这一列。先逐行照原文的设定做，不要“改进”。
样本量和原文差得多的话，停下来告诉我每一步筛选后的样本量。
结果填进 reports/targets.csv 的 our_value，然后运行
python ~/lab4_starter/compare_targets.py compare reports/targets.csv。
```

## Skill

### 8. 起草 skill（在同一个会话里）

```
把我们刚才做的流程写成 .claude/skills/【did-checklist 或 replication-targets】/SKILL.md。
我纠正过你的地方写成规则；需要人判断的地方写成“停下来问我”；
产出写明文件名和位置。description 写成什么情况下该用它、什么情况下不用，不要写成标题。
```

### 9. 新会话测试

退出，重新启动 `claude`，不要提 skill 的名字。

应该触发（DID）：

```
我想看看【另一项政策】对【另一个结果】的影响。
```

应该触发（复现）：

```
我想复现【另一篇论文】的主要结果。
```

不该触发：

```
帮我画一张【某变量】的分布图。
```

记录：有没有调用，调用后有没有先做第一步（核对处理时间，或先定目标和容差）。
