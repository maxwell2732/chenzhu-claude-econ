<p align="right"><img src="assets/gzh_logo.jpg" width="72" alt="公众号：遗传社科研究"></p>

# 朱晨的 AI 智能体课：Claude Code 经济学研究实战

朱晨　中国农业大学经济管理学院　·　公众号：遗传社科研究

这是一门写给经济学研究者的 AI 智能体实操课，以 Claude Code 为主要工具，也可以改用 Codex。课程从安装讲起，逐步做到一条可复现的实证流程：数据采集与清理、计量分析、论文复现、理论建模和写作。每一步都要留下证据：表和图由脚本生成，数据处理有记录，关键数字经过独立核对。

课程共 6 次，前 5 次动手做，第 6 次讨论。每次课约 2 小时，包括讲义和现场演示；课后作业自学完成，每课配一份图文操作说明和一个作业包（starter pack）。

## 课程安排与讲义资料

| 课次 | 主题 | 现场演示 | 课后作业 | 讲义 | 作业说明 | 作业包 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 从大语言模型到智能体 | 写 CLAUDE.md，用 Plan mode 完成一个小任务 | 安装、写自己的 CLAUDE.md、完成一个核对过的任务 | [PDF](lesson01/第1课_从大语言模型到智能体.pdf) | [PDF](lesson01/第1课课后作业使用说明.pdf) | [zip](lesson01/lab1_starter.zip) |
| 2 | 从一个模糊的想法到一张可用在论文中的图表 | 小红书评论采集：智能体操作浏览器，人扫码登录 | 从空文件夹到一张能复现的图（世界银行数据或社媒评论） | [PDF](lesson02/第2课_从模糊想法到论文图表.pdf) | [PDF](lesson02/第2课课后作业使用说明.pdf) | [zip](lesson02/lab2_starter.zip) |
| 3 | 微观调查数据：审查、清理、合并 | 用 research harness 清理 CHNS，生成 codebook | 审查报告、清理后的面板、带变量定义的 codebook | coming soon | coming soon | coming soon |
| 4 | 计量识别与论文复现，写出第一个 Skill | CHARLS 长护险 staggered DID；一篇论文的复现 | DID 或复现结果，以及你自己写的 SKILL.md | coming soon | coming soon | coming soon |
| 5 | 理论建模、写作与可审计性 | 用 pAI-Econ 构建理论模型；clean-room 审稿 | 加固后的复制包（capstone） | coming soon | coming soon | coming soon |
| 6 | 研讨：AI 与经济学知识生产 | HLER 的设计原理；APE 项目案例讨论 | 一页立场备忘录：2036 年我还靠什么做研究 | coming soon | coming soon | coming soon |

## 每一课的材料

以第 1 课为例，`lesson01/` 里有：

| 文件 | 用途 |
| --- | --- |
| `第1课_从大语言模型到智能体.pdf` | 讲义 |
| `第1课课后作业使用说明.pdf` | 课后作业的图文操作说明，第一次用终端的同学先看这份 |
| `lab1_starter.zip` | 作业包，下载后解压使用 |
| `lab1_starter/` | 作业包内容，可以在网页上直接浏览 |

## 怎样开始

1. 按第 1 课的作业说明（见上表）装好环境：Claude Code（或 Codex）、Python 或 Stata、Git。
2. 每一课先看讲义，再按作业说明完成作业，最后对照验收清单自查。
3. **现在就申请数据。** 第 3、4 课要用 CHNS 或 CHARLS，请按各数据官网的流程自行申请下载，可能需要几天到几周。

## 先修要求

- 会用 Stata 或 R/Python 中的一种，了解基本的计量方法。
- 不需要用过 Claude Code 或其他智能体工具。
- 面向博士生、高年级硕士生和青年教师。本科生建议先用传统方式打好专业基础。

## 用 Codex 的同学

课程材料按 Claude Code 组织（`CLAUDE.md`、`.claude/skills/`）。用 Codex 的同学可以让它读取这些文件，自动生成对应的 `AGENTS.md`，提示见各课作业包里的 `codex_adapt_prompt.md`。

Codex 默认的沙箱不允许终端命令联网，下载数据的脚本会报错（Windows 上是 `WinError 10013`）。在 `~/.codex/config.toml` 里加上下面两行，然后重启 Codex：

```toml
[sandbox_workspace_write]
network_access = true
```

## 数据说明

- 课程不分发任何数据。CHNS、CHARLS 等授权数据请自行申请，不得分享，不得上传到公开仓库。
- 第 1、2 课的基础作业只用世界银行等机构的公开数据。
- 社交媒体数据只用于个人学习和研究。采集时遵守平台用户协议，控制频率，个人信息去标识化，原始数据不公开。

## 相关仓库

课程中会用到我开发的几个工作流：

| 仓库 | 用途 | 课次 |
| --- | --- | --- |
| [claudecode-research-harness-workflow](https://github.com/maxwell2732/claudecode-research-harness-workflow) | 可审计、可复现的实证研究流程：审查、清理、计划、执行、审阅、发布 | 2、3、5 |
| [codex-stata-for-economists](https://github.com/maxwell2732/codex-stata-for-economists) | Stata 计量分析流水线 | 4、5 |
| [paper-replicate-agent-demo](https://github.com/maxwell2732/paper-replicate-agent-demo) | 论文复现 | 4 |
| [pAI-Econ-claude](https://github.com/maxwell2732/pAI-Econ-claude) | 经济学理论模型构建 | 5 |
| [hler-working-papers](https://github.com/maxwell2732/hler-working-papers) | HLER 人机协作研究系统的工作论文 | 6 |

## 致谢与参考

本课程主要参考了以下材料：

- Barrios, John M. *Claude Code for Accounting Research*. Yale School of Management, 2026. 课程网站：https://johnmbarrios.com/claude-code-accounting/ ；
- Sant'Anna, Pedro H. C. *claude-code-my-workflow*. https://github.com/pedrohcgs/claude-code-my-workflow


## 联系

问题和建议欢迎在本仓库提 Issue，也可以关注公众号“遗传社科研究”。
