# 用 Codex、Trae 或 WorkBuddy 的同学：让它自动适配

本课程的材料按 Claude Code 组织（`CLAUDE.md`、`.claude/skills/`、`.claude/agents/`）。Codex 的项目说明文件叫 `AGENTS.md`，写法基本相同。不需要手工改，让 Codex 自己适配即可。

在项目根目录启动 Codex，把下面这段交给它：

```
读取本仓库的 CLAUDE.md，以及 .claude/skills/ 和 .claude/agents/（如果存在），
生成功能等价的 AGENTS.md，并把每个 skill 改写成 Codex 可以调用的形式。
不要修改任何原文件。
最后列出你无法等价迁移的部分，以及原因。
```

最后一句很关键：要求它说出哪些地方迁移不了。

完成后，用和 Claude Code 一样的方法确认：退出、重新启动 Codex，问它一个只有读过 AGENTS.md 才能回答的问题。

## Trae 和 WorkBuddy

国内的 Trae（字节跳动）和 WorkBuddy（腾讯）也支持 skill，也就是“一个文件夹加一个 SKILL.md”的结构。

- Trae 的桌面版可以直接读取项目根目录的 `CLAUDE.md` 和 `AGENTS.md`，需要在“设置 → 规则”里打开对应开关；skill 放在 `.trae/skills/<名字>/`。
- WorkBuddy 也有自己的 skill 体系。可以把上面那段提示交给它，让它按自己的规则文件格式改写，同样要求它列出迁移不了的部分。

这些工具更新很快，具体位置和开关以它们当前的官方文档为准。
