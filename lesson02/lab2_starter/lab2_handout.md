# 第 2 课作业：从空文件夹到一张可用在论文中的图表

预计用时约 2 小时。三档选一，要求相同。

## 选一档

| 档次 | 任务 | 需要登录平台吗 |
| --- | --- | --- |
| 基础 | 用世界银行数据画中国的结构转型：农业就业占比（SL.AGR.EMPL.ZS）与人均 GDP（NY.GDP.PCAP.KD）。可以画时间序列，也可以画两者的散点轨迹 | 不需要 |
| 标准 | 自选一个和经济学相关的关键词，在小红书或知乎采集 200–500 条评论，清理后画描述性图（例如按月评论数、主题占比） | 需要，扫码登录 |
| 进阶 | 在标准档基础上，比较两个关键词或两段时间，并做一个简单的文本分类（词表或模型均可，方法写进 DECISIONS.md） | 需要，扫码登录 |

## 三档相同的要求

1. 从空文件夹开始。starter pack 解压在 `~/lab2_starter/`，只当参考资料；项目另建一个空文件夹：

   ```
   mkdir ~/lab2 && cd ~/lab2 && git init
   cp ~/lab2_starter/CLAUDE.md.template CLAUDE.md
   cp ~/lab2_starter/gitignore.txt .gitignore
   ```

   改好 CLAUDE.md 后再启动 `claude`。需要用到模板时，在提示里写明路径，例如“参照 ~/lab2_starter/DATA_PROFILE_template.md”。
2. 用 `opening_prompt_template.md` 改写你的开场提示。**留痕部分一字不删。** 最终发出的提示原文存进 `prompts_used.md`。
3. `DATA_PROFILE.md` 写在第一张图之前。读完再往下做。
4. 先画原始序列（例如每篇笔记的评论数、每天的评论数；基础档画逐年原始值），再汇总。
5. 看图之前，把两个检查写进 README：一个完整性或基准检查，一个合理性检查，都注明来源。
6. 图出来以后，最多改三轮。
7. 最后让智能体写 README，你在一个新文件夹里按 README 重跑一遍。

## 标准档和进阶档：开始采集之前

1. 按 `setup_browser.md` 装好 Playwright MCP 或 Claude in Chrome。
2. 把 `collection_rules.md` 的内容复制进你的 CLAUDE.md。
3. 先用 `clarify_prompts.md` 里的深度提示，和智能体聊清楚你到底想知道什么，再写开场提示。

## 采集时

- 智能体打开登录页时会停下，你用手机扫码，然后告诉它继续。
- 遇到验证码，停下来。由你处理，或者结束本次采集。
- 原始数据存为带日期的文件，例如 `data/raw/xhs_20261101.json`。
- 采集完成后，让它写 `COLLECTION_LOG.md`（模板见 `COLLECTION_LOG_template.md`）。

## 完成之后

1. 对照 `lab2_verify_checklist.md` 自查。
2. 填写 `exit_ticket.md`。
3. 确认 CHNS 或 CHARLS 已下载到本地。还没拿到的，第 3 课先用公开数据。
