# 用 Codex 的同学：让它自动适配

本课程的材料按 Claude Code 组织（`CLAUDE.md`、`.claude/skills/`、`.claude/agents/`）。Codex 的项目说明文件叫 `AGENTS.md`，写法基本相同。不需要手工改，让 Codex 自己适配即可。

在项目根目录启动 Codex，把下面这段交给它：

```
读取本仓库的 CLAUDE.md，以及 .claude/skills/ 和 .claude/agents/（如果存在），
生成功能等价的 AGENTS.md，并把每个 skill 改写成 Codex 可以调用的形式。
不要修改任何原文件。
最后列出你无法等价迁移的部分，以及原因。
```

最后一句很关键：让它说出迁移不了的地方，而不是假装全部成功。

完成后，用和 Claude Code 一样的方法确认：退出、重新启动 Codex，问它一个只有读过 AGENTS.md 才能回答的问题。
