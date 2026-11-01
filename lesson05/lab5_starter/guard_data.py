#!/usr/bin/env python3
"""阻止数据文件、论文 PDF、密钥被提交到 Git。

同一个脚本有两种用法：

1. Claude Code 的 PreToolUse hook（智能体执行 git add / git commit 之前检查）
   在 .claude/settings.json 里加上 hooks_settings_snippet.json 的内容，
   脚本放在 .claude/hooks/guard_data.py。命中规则时退出码为 2，
   Claude Code 会拦下这条命令，并把原因告诉智能体。

2. Git 的 pre-commit hook（不管是谁提交，Claude、Codex 还是你自己，都会检查）
       cp guard_data.py .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit
   或者在 .git/hooks/pre-commit 里写一行：
       python3 .claude/hooks/guard_data.py --git-pre-commit

规则在下面的 BLOCK_DIRS、BLOCK_EXT、MAX_MB 里，按你的项目修改。
"""
import json
import shlex
import subprocess
import sys
from pathlib import PurePosixPath

BLOCK_DIRS = ("data/raw/", "data/intermediate/", "data/processed/", "papers/")
BLOCK_EXT = (".dta", ".sav", ".sas7bdat", ".parquet", ".feather", ".rds", ".RData", ".pdf", ".zip")
BLOCK_NAMES = (".env", "credentials.json", "id_rsa")
ALLOW = ("reports/", "output/figures/")  # 这些目录下的 PDF 等可以提交
MAX_MB = 20


def git(*args):
    r = subprocess.run(["git", *args], capture_output=True, text=True)
    return r.stdout.splitlines() if r.returncode == 0 else []


def problems(paths):
    found = []
    for p in paths:
        p = p.strip().strip('"')
        if not p:
            continue
        pp = PurePosixPath(p)
        reason = None
        if any(p.startswith(d) or f"/{d}" in p for d in BLOCK_DIRS):
            reason = "数据或论文目录"
        elif pp.name in BLOCK_NAMES:
            reason = "密钥或凭证"
        elif pp.suffix in BLOCK_EXT and not any(p.startswith(a) for a in ALLOW):
            reason = f"{pp.suffix} 文件"
        else:
            try:
                import os
                if os.path.getsize(p) > MAX_MB * 1024 * 1024:
                    reason = f"超过 {MAX_MB} MB"
            except OSError:
                pass
        if reason:
            found.append((p, reason))
    return found


def files_for_command(cmd):
    """找出一条 shell 命令会让哪些文件进入提交。"""
    files = []
    for part in cmd.replace("&&", ";").replace("||", ";").split(";"):
        try:
            tok = shlex.split(part)
        except ValueError:
            continue
        if len(tok) < 2 or tok[0] != "git":
            continue
        if tok[1] == "add":
            out = git("add", "--dry-run", *tok[2:])  # 列出将被加入的文件
            files += [ln.split("'", 2)[1] if "'" in ln else ln for ln in out]
        elif tok[1] == "commit":
            files += git("diff", "--cached", "--name-only")
            if any(t in ("-a", "--all") or (t.startswith("-") and not t.startswith("--") and "a" in t) for t in tok[2:]):
                files += git("diff", "--name-only")
    return files


def report(found, where):
    lines = [f"{where}：下面的文件不能提交到 Git："]
    lines += [f"  {p}（{why}）" for p, why in found]
    lines.append("数据、论文 PDF 和密钥只留在本地。确需例外，请人工修改 guard_data.py 的规则并说明原因。")
    print("\n".join(lines), file=sys.stderr)


def main():
    if "--git-pre-commit" in sys.argv or sys.argv[0].endswith("pre-commit"):
        found = problems(git("diff", "--cached", "--name-only"))
        if found:
            report(found, "pre-commit 检查")
            sys.exit(1)
        sys.exit(0)

    # Claude Code hook：从标准输入读 JSON
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)
    if data.get("tool_name") != "Bash":
        sys.exit(0)
    cmd = (data.get("tool_input") or {}).get("command", "")
    if "git" not in cmd:
        sys.exit(0)
    found = problems(files_for_command(cmd))
    if found:
        report(found, "hook 拦下了这条命令")
        sys.exit(2)  # 退出码 2：Claude Code 阻止这次工具调用
    sys.exit(0)


if __name__ == "__main__":
    main()
