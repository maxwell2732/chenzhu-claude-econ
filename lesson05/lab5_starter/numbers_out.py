"""把正文要用到的数字由脚本写出来，正文只引用，不手打。

在你的分析脚本里：

    from numbers_out import record          # 本文件放在 scripts/numbers_out.py；不要命名为 numbers.py，会和 Python 自带模块重名
    record("did_att_employment", att, fmt="{:.3f}", note="表 2 第 1 列，csdid 总体 ATT")
    record("n_individuals", n, fmt="{:,}")

每次调用会更新两个文件：
    output/numbers.json   数字、格式化后的文字、来源说明、生成脚本
    output/numbers.tex    LaTeX 宏，例如 \\newcommand{\\didAttEmployment}{0.042}

写 LaTeX 正文时用 \\didAttEmployment；写 Word 或 Markdown 时，
用 check_numbers.py 核对正文里的每个数字都能在 numbers.json 里找到。

Stata 用户：在 do 文件末尾用 file write 写出同样格式的 CSV（name,value,text,note），
再用 python numbers_out.py --from-csv output/numbers.csv 转成 json 和 tex。
"""
import csv
import inspect
import json
import re
import sys
from pathlib import Path

OUT = Path("output")


def _macro(name):
    parts = re.split(r"[^A-Za-z]+", name)
    parts = [p for p in parts if p]
    if not parts:
        raise ValueError(f"名字里至少要有字母：{name}")
    return parts[0].lower() + "".join(p.capitalize() for p in parts[1:])


def _write(store):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "numbers.json").write_text(json.dumps(store, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = ["% 由 numbers_out.py 自动生成，不要手改"]
    for k, v in sorted(store.items()):
        tex = v["text"].replace("%", "\\%")
        lines.append(f"\\newcommand{{\\{_macro(k)}}}{{{tex}}}  % {v.get('note', '')}")
    (OUT / "numbers.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")


def _load():
    p = OUT / "numbers.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}


def record(name, value, fmt="{:.3f}", note=""):
    store = _load()
    caller = inspect.stack()[1].filename
    store[name] = {"value": float(value), "text": fmt.format(value), "note": note, "script": Path(caller).name}
    _write(store)
    return store[name]["text"]


def from_csv(path):
    store = _load()
    with open(path, newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            store[r["name"]] = {"value": float(r["value"]), "text": r.get("text") or r["value"],
                                "note": r.get("note", ""), "script": Path(path).name}
    _write(store)
    print(f"已写入 {len(store)} 个数字 → output/numbers.json, output/numbers.tex")


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--from-csv":
        from_csv(sys.argv[2])
    else:
        print(__doc__)
