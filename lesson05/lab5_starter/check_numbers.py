"""核对正文里的数字是否都能追到脚本生成的 numbers.json。

用法：
    python check_numbers.py paper/draft.md output/numbers.json
    python check_numbers.py paper/main.tex output/numbers.json

脚本会找出正文里所有带小数点的数、百分数、以及四位以上的整数（会跳过 1900–2100 之间的年份），
逐个到 numbers.json 里找：文字完全一致，或者数值在正文显示的精度内一致，都算找到。
找不到的列出来，并给出所在行。它们要么是手打的数字，要么来自没有登记的脚本。

一些数字本来就不需要登记（例如文献里别人的估计值、问卷题号），
把它们写进和正文同一个文件夹里的 numbers_allow.txt，一行一个。
"""
import json
import re
import sys
from pathlib import Path

PAT = re.compile(r"(?<![\w.])[-−]?\d{1,3}(?:,\d{3})+(?:\.\d+)?%?|(?<![\w.])[-−]?\d+\.\d+%?|(?<![\w.])\d{4,}%?")


def normalize(tok):
    t = tok.replace("−", "-").replace(",", "")
    pct = t.endswith("%")
    t = t.rstrip("%")
    decimals = len(t.split(".")[1]) if "." in t else 0
    return float(t), decimals, pct


def main():
    if len(sys.argv) != 3:
        sys.exit("用法：python check_numbers.py <正文文件> <numbers.json>")
    text_path, num_path = Path(sys.argv[1]), Path(sys.argv[2])
    store = json.loads(num_path.read_text(encoding="utf-8"))
    texts = {v["text"] for v in store.values()}
    values = [v["value"] for v in store.values()]
    allow_file = text_path.parent / "numbers_allow.txt"
    allow = set(allow_file.read_text(encoding="utf-8").split()) if allow_file.exists() else set()

    body = text_path.read_text(encoding="utf-8")
    body = re.sub(r"\\(?:cite|ref|label|eqref)\{[^}]*\}", "", body)  # 跳过引用标签

    found, missing = 0, []
    for ln_no, line in enumerate(body.splitlines(), 1):
        for m in PAT.finditer(line):
            tok = m.group(0)
            if tok in allow or tok in texts:
                found += tok not in allow
                continue
            val, dec, pct = normalize(tok)
            if dec == 0 and not pct and 1900 <= val <= 2100:
                continue  # 年份
            tol = 0.5 * 10 ** (-dec)
            cands = [val, val / 100] if pct else [val]
            if any(abs(c - v) <= tol * (0.01 if (pct and c != val) else 1) + 1e-12 for c in cands for v in values):
                found += 1
            else:
                missing.append((ln_no, tok, line.strip()[:70]))

    print(f"正文里能追到 numbers.json 的数字：{found} 个")
    if missing:
        print(f"追不到的数字：{len(missing)} 个")
        for ln_no, tok, ctx in missing:
            print(f"  第 {ln_no} 行  {tok:>10}  {ctx}")
        print("这些数字要么改成由脚本生成，要么确认不需要登记后写进 numbers_allow.txt。")
        sys.exit(1)
    print("全部可追溯。")


if __name__ == "__main__":
    main()
