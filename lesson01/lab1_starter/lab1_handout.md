# 第 1 课作业：安装、CLAUDE.md、一个经过核对的任务

预计用时约 1.5 小时。按顺序完成，每部分结束时对照 `lab1_verify_checklist.md` 打勾。

---

## A. 环境（约 25 分钟）

目标：`claude` 能在新终端里启动，Python 或 Stata 能在命令行直接调用。

1. 按官方文档安装 Claude Code，并用你的订阅或 API Key 登录。
2. **关掉终端，重新打开一个**，运行 `claude`，确认能启动。
3. 检查你的分析软件能否在命令行调用：
   - Python：`python --version` 或 `python3 --version`
   - Stata：确认能以批处理方式运行 do 文件。不同系统和版本的命令不一样，Windows 上通常是调用 Stata 程序加 `/e do 文件名`，macOS/Linux 上通常是 `stata-mp -b do 文件名`（或 `stata-se`）。
4. 也可以把 `setup_check_prompt.md` 里的提示粘贴给 Claude Code，让它帮你检查。

> **常见错误**：看到 `command not found` 就以为是智能体的问题。它没有自己的 Python 或 Stata，用的是你本机已安装的版本。

---

## B. 写你自己的 CLAUDE.md（约 15 分钟）

1. 在 `~/lab1/` 里运行 `claude`，输入 `/init`，让它生成一份初稿。
2. 打开 `CLAUDE.md.template`，参考它把初稿**改成你自己的版本**。至少写清楚：
   - 原始数据放在哪里、是否只读；
   - 你用的软件和版本；
   - 产出规则：所有表和图都必须由脚本生成。
3. **退出会话（`/exit`），重新运行 `claude`**，问它：“这个项目里原始数据放在哪里？哪些文件不能修改？”回答应该和你写的一致。

> **常见错误**：会话中途改了 CLAUDE.md，就以为马上生效。改完要开新会话再确认。

用 Codex 的同学：把 `codex_adapt_prompt.md` 里的提示交给 Codex，让它生成 AGENTS.md，再用同样的方法确认它读到了。

---

## C. 一个经过核对的任务（约 40 分钟）

三档任选其一。无论选哪一档，都要满足三条：

- 任务由一个**有名字的脚本**完成，不是从聊天里复制的结果；
- 至少有**一个数字和独立来源核对过**，并写下核对了什么、来源在哪里；
- 在 `prompts_tried.md` 里记下一次你自己的“模糊 → 具体”改写。

### 基础档

下载中国 2000–2024 年 GDP 实际增速（世界银行指标 `NY.GDP.MKTP.KD.ZG`），计算全期均值和标准差。挑一年，和国家统计局《国民经济和社会发展统计公报》中的数字核对。

> 提示：两个来源的数字可能有小差异，因为统计口径和修订时间不同。差异本身不是错误，但要写进 `LOG.md`，并说明你认为的原因。

### 标准档

在基础档之上，加入 5 个对比国家（例如印度、印度尼西亚、越南、巴西、美国），用脚本画一张折线图，保存为 `output/gdp_growth.png`。

### 进阶档

在标准档之上，按 2000–2009、2010–2019、2020–2024 三个时期计算各国均值，输出 `output/growth_by_period.csv` 和 `output/growth_by_period.tex`。

### 推荐的开场提示（四要素：文件、操作、层级、产出）

先用 Plan mode（Shift+Tab 切换）让它给出计划，读完计划再执行。

```
请写一个脚本 scripts/download_wdi.py，用世界银行 API 下载中国 2000–2024 年的
GDP 实际增速（指标 NY.GDP.MKTP.KD.ZG），保存到 data/raw/wdi_china.csv。
然后写 scripts/gdp_growth.py：读取这个文件，计算全期均值和标准差，
结果保存到 output/growth_summary.csv。
最后在回复里列出 2020 年的数值，供我和统计公报核对。
所有结果都必须由脚本生成，不要只在聊天里报告。
```

写完后，可以把智能体的下载脚本和 starter pack 里的 `download_wdi.py` 对照一下：两者的思路一样吗？哪个更稳健？

---

## 完成之后

1. 对照 `lab1_verify_checklist.md` 逐项自查。
2. 填写 `exit_ticket.md`。
3. **现在就开始申请 CHNS 或 CHARLS 数据**（第 3 课前需要拿到）。
4. 为第 2 课做准备：安装 Chrome，以及 Claude in Chrome 扩展或 Playwright MCP。
