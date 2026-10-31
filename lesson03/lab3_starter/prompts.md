# 第 3 课用到的提示

把【】里的内容换成你自己的。复杂的步骤先在 Plan mode（Shift+Tab）里看计划，读完再执行。

---

## 1. 可行性（审查之前）

```
我想要一个【CHARLS 2011、2013、2015、2018】年的个人-年份面板，包含【出生年、性别、教育、婚姻、是否有医保】。
原始数据在 data/raw/ 里。动手之前，先告诉我要做哪些事、可能缺什么、哪些地方你没有把握。
先不要写代码。
```

读完回答，把要点存进 `DECISIONS.md`。

## 2. 建立项目（setup）

```
/research-harness-setup
研究问题：【一句话】。原始数据在 data/raw/，按轮次放在子文件夹里。请按 CLAUDE.md 执行。
```

## 3. 审查（audit）

```
/research-harness-audit --all
```

如果数据轮次多，可以让子智能体并行：

```
/research-harness-audit --all
每一轮数据分给一个子智能体审查，最后汇总成一份 reports/data_audit_report.md。
```

审查报告读完，再往下做。

## 4. 清理计划

```
根据 reports/data_audit_report.md，帮我起草 reports/data_cleaning_plan.md。
列出：每一轮用哪些文件和变量；变量名的跨轮映射；特殊缺失码的处理；新造变量的定义；
每一次合并的键、关系（一对一或多对一）和预期匹配率；样本筛选条件。
起草完先给我看，不要执行。
```

逐条核对，特别是编码含义（对照问卷）和预期匹配率，改好再执行下一步。

## 5. 清理与合并（clean）

```
/research-harness-clean
请按 reports/data_cleaning_plan.md 执行，生成数据 csv 和 codebook csv（要同时加上变量定义，比如变量 label 或 description）以及工作报告。
每次合并按 ~/lab3_starter/checked_merge.py 的方式打印报告。
```

## 6. 新会话检查 codebook

退出 Claude Code，重新启动一个新会话，然后：

```
只读 data/processed/codebook.csv，不要读数据本身。
告诉我这五个变量是什么意思、单位是什么、从哪里来：【变量1】【变量2】【变量3】【变量4】【变量5】
```

对照你自己的理解，五个都答对才算合格。

---

## 备选路线（世界银行数据）

```
data/raw/ 里有四个世界银行文件：三个指标文件（国家-年份）和一个国家信息表。
请先审查：每个文件一行是什么、唯一性、缺失、有没有不属于国家的汇总行。
然后把三个指标按（国家，年份）一对一合并，再按国家把国家信息表多对一合并进来，
只保留真正的国家，生成国家-年份面板和 codebook。每次合并都打印报告。
```
