# 第 4 课验收清单

做完逐项打勾。打不了勾的，在 `LOG.md` 里写明原因。

## DID 路线

- [ ] `reports/treatment_timing.csv` 里每个处理单位都有起始时间和出处，我核对过原文
- [ ] 对照组的定义和理由写在 `DECISIONS.md`
- [ ] 看事件研究图的标准，在出图之前写进了 `DECISIONS.md`
- [ ] 至少用了一种 staggered 估计量，和 TWFE 的结果放在一起比较
- [ ] 事件研究图有基期、置信区间，处理前至少两期
- [ ] 审稿子智能体的每条意见都有回应（接受，或拒绝并说明理由）
- [ ] 计划外换过的设定都记了下来；结论没有超出设计能支持的范围

## 复现路线

- [ ] `reports/paper_notes.md` 六项都填了，主要结果写明表号和列号
- [ ] 目标和容差在跑回归之前锁定（有 `reports/targets.lock`）
- [ ] `compare_targets.py compare` 能跑通，没有提示锁定后被改过
- [ ] 每个 FAIL 和 NOTE 都写了原因，原因能查到出处
- [ ] 总体评价（PASS / PARTIAL / FAIL）写得和结果一致

## Skill

- [ ] `.claude/skills/<名字>/SKILL.md` 存在，开头有 name 和 description
- [ ] description 写的是什么情况下用，不是标题
- [ ] 正文有按顺序的步骤、停下来问人的地方、产出文件的位置
- [ ] 至少一条规则来自这次作业里纠正过的错误
- [ ] 新会话测试：应该触发的那句触发了，不该触发的那句没有触发
- [ ] 测试结果记在 `LOG.md`

## 数据

- [ ] `hash_raw.py check` 全部一致
- [ ] `git status` 里没有数据文件、论文 PDF
