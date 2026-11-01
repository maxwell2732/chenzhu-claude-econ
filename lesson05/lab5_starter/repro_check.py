"""模拟“别人拿到你的仓库后重跑一遍”，比较输出是否一致。

用法（在项目根目录运行）：
    python repro_check.py --cmd "bash run_all.sh" --outputs output --data data/raw

它会做四件事：
1. 确认工作区没有未提交的修改（否则比较没有意义）。
2. 把当前仓库 git clone 到一个临时文件夹，并删掉克隆里已提交的输出目录。克隆里只有提交过的文件，
   数据不在 Git 里，所以把你本地的数据目录用符号链接接过去（只读使用）。
3. 在克隆里运行 --cmd 指定的命令，也就是 README 里写的那条重跑命令。
4. 比较克隆里生成的 --outputs 和你本地的 --outputs：文本类文件（csv、tex、json、txt、md、tsv）
   逐个比较哈希值。图片和 PDF 只报告是否存在，不比较内容。

结果：
    一致      重跑得到的表格和数字和你本地的完全一样
    不一致    列出哪些文件不同，常见原因是随机数种子、样本排序、软件版本
    缺失      本地有、重跑没生成，通常是 README 里漏了一步
"""
import argparse
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

TEXT = {".csv", ".tex", ".json", ".txt", ".md", ".tsv"}


def sh(cmd, cwd=None):
    return subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True)


def digest(root):
    out = {}
    for p in sorted(Path(root).rglob("*")):
        if p.is_file():
            rel = str(p.relative_to(root))
            out[rel] = hashlib.sha256(p.read_bytes()).hexdigest() if p.suffix in TEXT else "binary"
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cmd", required=True, help="重跑整个流程的命令，和 README 里写的一致")
    ap.add_argument("--outputs", default="output")
    ap.add_argument("--data", default="data/raw", help="不在 Git 里的原始数据目录")
    ap.add_argument("--allow-dirty", action="store_true")
    a = ap.parse_args()

    if not a.allow_dirty and sh("git status --porcelain").stdout.strip():
        sys.exit("工作区有未提交的修改。先提交，再检查。")
    if not Path(a.outputs).exists():
        sys.exit(f"本地没有 {a.outputs}，先在本地跑一遍。")

    tmp = Path(tempfile.mkdtemp(prefix="repro_"))
    clone = tmp / "clone"
    r = sh(f'git clone -q "{Path.cwd()}" "{clone}"')
    if r.returncode:
        sys.exit("git clone 失败：" + r.stderr)
    if Path(a.data).exists():
        (clone / a.data).parent.mkdir(parents=True, exist_ok=True)
        if not (clone / a.data).exists():
            os.symlink(Path(a.data).resolve(), clone / a.data)
    if (clone / a.outputs).exists():
        shutil.rmtree(clone / a.outputs)  # 删掉克隆里已提交的输出，确保全部由重跑生成
    print(f"在全新克隆里运行：{a.cmd}\n（位置：{clone}）")
    r = sh(a.cmd, cwd=clone)
    (tmp / "rerun.log").write_text(r.stdout + "\n" + r.stderr, encoding="utf-8")
    if r.returncode:
        print(r.stderr[-1500:])
        sys.exit(f"重跑失败，退出码 {r.returncode}。完整日志：{tmp / 'rerun.log'}")

    local, rerun = digest(a.outputs), digest(clone / a.outputs)
    missing = [k for k in local if k not in rerun]
    differ = [k for k in local if k in rerun and local[k] != "binary" and local[k] != rerun[k]]
    same = [k for k in local if k in rerun and local[k] != "binary" and local[k] == rerun[k]]
    binary = [k for k in local if local[k] == "binary"]

    print(f"文本输出一致 {len(same)} 个，不一致 {len(differ)} 个，缺失 {len(missing)} 个；图片/PDF {len(binary)} 个只核对存在。")
    for k in differ:
        print("  不一致：", k)
    for k in missing:
        print("  缺失：  ", k)
    if differ or missing:
        sys.exit(1)
    print("全新克隆重跑通过。")


if __name__ == "__main__":
    main()
