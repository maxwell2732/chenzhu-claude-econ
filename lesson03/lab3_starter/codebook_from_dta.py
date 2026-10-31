"""
参考脚本：从 Stata 文件的变量标签生成 codebook（第 3 课）

先让智能体自己写，写完再对照。需要 pandas 和 pyreadstat：
    pip install pandas pyreadstat pyarrow

两种用法：

1) 变量清单：只读元数据，扫描目录下所有 .dta 文件，几秒钟就能完成。
       python codebook_from_dta.py inventory data/raw
   输出 data/processed/var_list.csv：文件、变量名、变量标签。

2) 清理后数据的 codebook：读取清理后的面板（csv 或 parquet），
   用变量清单里的标签补上定义，再算每个变量的统计量。
       python codebook_from_dta.py codebook data/processed/panel.parquet
   输出 data/processed/codebook.csv。清理时新造的变量没有 Stata 标签，
   定义写在 extra_labels.csv（两列：variable_name, description），脚本会一并读入。
"""

import os
import sys

import pandas as pd

OUT_DIR = os.path.join("data", "processed")


def inventory(raw_dir):
    import pyreadstat
    rows = []
    for d, _, files in os.walk(raw_dir):
        for name in sorted(files):
            if not name.lower().endswith(".dta"):
                continue
            path = os.path.join(d, name)
            _, meta = pyreadstat.read_dta(path, metadataonly=True)   # 只读元数据，不读数据
            labels = meta.column_labels or [None] * len(meta.column_names)
            for var, lab in zip(meta.column_names, labels):
                rows.append({"file": os.path.relpath(path, raw_dir).replace("\\", "/"),
                             "var_name": var, "label": lab or ""})
    os.makedirs(OUT_DIR, exist_ok=True)
    out = pd.DataFrame(rows)
    out.to_csv(os.path.join(OUT_DIR, "var_list.csv"), index=False, encoding="utf-8-sig")
    print(f"[inventory] {out['file'].nunique() if len(out) else 0} 个文件，{len(out)} 个变量 -> data/processed/var_list.csv")


def codebook(panel_path):
    df = pd.read_parquet(panel_path) if panel_path.endswith(".parquet") else pd.read_csv(panel_path)
    labels = {}
    vl = os.path.join(OUT_DIR, "var_list.csv")
    if os.path.exists(vl):
        v = pd.read_csv(vl).fillna("")
        for var, lab in zip(v["var_name"], v["label"]):
            if lab and var not in labels:
                labels[var] = lab
                labels.setdefault(var.lower(), lab)
                labels.setdefault(var.upper(), lab)
    if os.path.exists("extra_labels.csv"):
        e = pd.read_csv("extra_labels.csv").fillna("")
        labels.update(dict(zip(e["variable_name"], e["description"])))

    rows = []
    for c in df.columns:
        s = df[c]
        num = pd.api.types.is_numeric_dtype(s)
        rows.append({
            "variable_name": c,
            "description": labels.get(c, ""),
            "dtype": str(s.dtype),
            "n_nonmissing": int(s.notna().sum()),
            "missing_pct": round(float(s.isna().mean()) * 100, 2),
            "min": s.min() if num and s.notna().any() else "",
            "max": s.max() if num and s.notna().any() else "",
            "n_unique": int(s.nunique(dropna=True)),
        })
    cb = pd.DataFrame(rows)
    cb.to_csv(os.path.join(OUT_DIR, "codebook.csv"), index=False, encoding="utf-8-sig")
    covered = (cb["description"] != "").mean() * 100
    print(f"[codebook] {len(cb)} 个变量，定义覆盖率 {covered:.1f}% -> data/processed/codebook.csv")
    empty = cb.loc[cb["description"] == "", "variable_name"].tolist()
    if empty:
        print(f"[codebook] 以下变量还没有定义，请写进 extra_labels.csv：{', '.join(empty[:20])}" + (" ……" if len(empty) > 20 else ""))


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] not in ("inventory", "codebook"):
        print(__doc__)
        sys.exit(1)
    (inventory if sys.argv[1] == "inventory" else codebook)(sys.argv[2])
