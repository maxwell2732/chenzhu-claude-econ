"""
原始数据哈希校验（第 3 课）

给 data/raw/ 下的每个文件算 SHA-256。清理前存一次，清理后核对一次，
用来证明原始数据没有被改过。只用 Python 标准库。

用法：
    python hash_raw.py save     # 清理前：写入 raw_hashes.txt
    python hash_raw.py check    # 清理后：逐个核对，报告是否一致

可选：--dir 指定原始数据目录（默认 data/raw），--out 指定哈希文件（默认 raw_hashes.txt）
    python hash_raw.py save --dir data/raw --out raw_hashes.txt

raw_hashes.txt 只含文件路径和哈希值，不含数据内容，可以提交到 Git。
"""

import argparse
import hashlib
import os
import sys


def sha256(path, chunk=1024 * 1024):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def list_files(root):
    out = []
    for d, _, files in os.walk(root):
        for name in files:
            if name in ("READONLY.md", ".DS_Store"):
                continue
            out.append(os.path.relpath(os.path.join(d, name), root).replace("\\", "/"))
    return sorted(out)


def save(root, out_path):
    files = list_files(root)
    if not files:
        print(f"[save] {root} 下没有文件，请先把原始数据放进去。")
        sys.exit(1)
    with open(out_path, "w", encoding="utf-8") as f:
        for rel in files:
            f.write(f"{sha256(os.path.join(root, rel))}  {rel}\n")
    print(f"[save] 已记录 {len(files)} 个文件的 SHA-256，写入 {out_path}")


def check(root, out_path):
    if not os.path.exists(out_path):
        print(f"[check] 找不到 {out_path}，请先运行 save。")
        sys.exit(1)
    expected = {}
    with open(out_path, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            digest, rel = line.split("  ", 1)
            expected[rel] = digest
    current = set(list_files(root))
    changed, missing, added = [], [], sorted(current - set(expected))
    for rel, digest in expected.items():
        p = os.path.join(root, rel)
        if not os.path.exists(p):
            missing.append(rel)
        elif sha256(p) != digest:
            changed.append(rel)
        else:
            print(f"[check] {rel}   一致")
    for rel in changed:
        print(f"[check] {rel}   已被修改！")
    for rel in missing:
        print(f"[check] {rel}   不见了！")
    for rel in added:
        print(f"[check] {rel}   新增文件（不在记录里）")
    ok = not (changed or missing or added)
    print(f"[check] 共 {len(expected)} 个文件，" + ("全部一致" if ok else f"修改 {len(changed)}，缺失 {len(missing)}，新增 {len(added)}"))
    sys.exit(0 if ok else 2)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="原始数据哈希校验")
    ap.add_argument("mode", choices=["save", "check"])
    ap.add_argument("--dir", default=os.path.join("data", "raw"))
    ap.add_argument("--out", default="raw_hashes.txt")
    a = ap.parse_args()
    (save if a.mode == "save" else check)(a.dir, a.out)
