# 第 1 课 Starter Pack：从大语言模型到智能体

《朱晨的 AI 智能体课：Claude Code 经济学研究实战》· 朱晨 · 中国农业大学经济管理学院

这个文件夹里是第 1 课课后作业要用的全部材料。作业约 1.5 小时，自学完成，不需要提交。对照 `lab1_verify_checklist.md` 自查，全部通过后再进入第 2 课。

## 文件说明

| 文件 | 用途 |
| --- | --- |
| `第1课课后作业使用说明.pdf` | 图文版操作说明，第一次用终端的同学先看这份 |
| `lab1_handout.md` | 作业说明：A 环境、B CLAUDE.md、C 一个经过核对的任务 |
| `lab1_verify_checklist.md` | 验收清单，逐项自查 |
| `CLAUDE.md.template` | CLAUDE.md 模板，复制到你的项目根目录后改成你自己的版本 |
| `setup_check_prompt.md` | 让 Claude Code 帮你检查环境的提示 |
| `codex_adapt_prompt.md` | 用 Codex 的同学：让 Codex 自动生成 AGENTS.md 的提示 |
| `prompts_tried.md` | 记录你自己的“模糊 → 具体”提示改写 |
| `download_wdi.py` | 参考脚本：从世界银行 API 下载 GDP 增速。先让智能体自己写，写完再和这份对照 |
| `exit_ticket.md` | 课后 exit ticket |

## 使用方法

1. 把整个文件夹解压到你的主目录，得到 `~/lab1/`。
2. 在终端进入这个文件夹：`cd ~/lab1`，然后运行 `claude`。
3. 按 `lab1_handout.md` 的顺序完成 A、B、C 三部分。

## 字体说明（PPT 显示用）

课程 PPT 使用三种免费字体。没有安装时 PowerPoint 会自动替换，内容不受影响，但版式可能略有差异：

- 标题：Noto Serif SC（思源宋体）
- 代码：JetBrains Mono
- 正文：Noto Sans SC（思源黑体）

## 数据说明

第 1 课只用世界银行 WDI 的公开数据，不需要任何授权数据。

第 3、4 课要用 CHNS 或 CHARLS。**课程不分发任何数据**，请现在就按各数据官网的流程自行申请下载。申请可能需要几天到几周。
