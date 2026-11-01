"""对比复现结果和论文目标值，生成 PASS / FAIL / NOTE 报告。

两步用法：

1. 跑任何回归之前，填好 targets.csv 的 target、source、paper_value、tolerance、tol_type，
   然后锁定目标和容差：
       python compare_targets.py lock reports/targets.csv
   这一步会生成 reports/targets.lock，记录这几列的哈希值。

2. 复现完成后，把结果填进 our_value 列，再运行：
       python compare_targets.py compare reports/targets.csv
   脚本先核对锁文件：目标值或容差在锁定之后被改过，就停下来报错。
   然后逐项判断，写出 reports/replication_comparison.md。

targets.csv 的列：
    target       目标名称，例如“女性身高系数”
    source       出处，例如“表2 第7列”
    paper_value  论文里的数值
    tolerance    容差
    tol_type     abs（绝对差）或 rel（相对差，0.05 表示 5%）
    our_value    你的复现结果，复现之前留空
    note         备注

判断规则：
    PASS  差距在容差内，且符号一致
    FAIL  差距超出容差，或符号相反
    NOTE  没有复现值，或没有设容差（需要文字说明）
"""
import csv
import hashlib
import sys
from pathlib import Path

LOCKED_COLS = ["target", "source", "paper_value", "tolerance", "tol_type"]


def read_rows(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    missing = [c for c in LOCKED_COLS + ["our_value"] if rows and c not in rows[0]]
    if missing:
        sys.exit(f"targets 文件缺少列：{missing}")
    return rows


def fingerprint(rows):
    h = hashlib.sha256()
    for r in rows:
        h.update(("|".join((r.get(c) or "").strip() for c in LOCKED_COLS) + "\n").encode("utf-8"))
    return h.hexdigest()


def to_float(x):
    try:
        return float(str(x).replace(",", "").strip())
    except (TypeError, ValueError):
        return None


def judge(r):
    paper, ours, tol = to_float(r["paper_value"]), to_float(r["our_value"]), to_float(r["tolerance"])
    kind = (r.get("tol_type") or "abs").strip().lower()
    if ours is None:
        return "NOTE", "", "还没有复现值"
    if paper is None:
        return "NOTE", "", "论文值不是数字"
    diff = ours - paper
    if tol is None:
        return "NOTE", f"{diff:+.4g}", "没有设容差"
    limit = abs(paper) * tol if kind == "rel" else tol
    same_sign = (paper == 0) or (ours == 0) or ((paper > 0) == (ours > 0))
    if abs(diff) <= limit and same_sign:
        return "PASS", f"{diff:+.4g}", ""
    reason = "符号相反" if not same_sign else f"超出容差（允许 ±{limit:.4g}）"
    return "FAIL", f"{diff:+.4g}", reason


def main():
    if len(sys.argv) != 3 or sys.argv[1] not in ("lock", "compare"):
        sys.exit("用法：python compare_targets.py lock|compare <targets.csv>")
    mode, path = sys.argv[1], Path(sys.argv[2])
    rows = read_rows(path)
    lock = path.with_suffix(".lock")

    if mode == "lock":
        if any((r.get("our_value") or "").strip() for r in rows):
            print("提醒：our_value 已经有值。容差应该在看到结果之前定好。")
        lock.write_text(fingerprint(rows) + "\n", encoding="utf-8")
        print(f"已锁定 {len(rows)} 个目标 → {lock}")
        return

    if not lock.exists():
        sys.exit(f"没有找到 {lock}。请先在复现之前运行 lock。")
    if lock.read_text(encoding="utf-8").strip() != fingerprint(rows):
        sys.exit("目标值或容差在锁定之后被改过。请在 DECISIONS.md 里说明原因，确认后重新 lock。")

    results = [(r, *judge(r)) for r in rows]
    counts = {k: sum(1 for x in results if x[1] == k) for k in ("PASS", "FAIL", "NOTE")}
    overall = "PASS" if counts["FAIL"] == 0 and counts["NOTE"] == 0 else ("PARTIAL" if counts["PASS"] else "FAIL")

    out = path.parent / "replication_comparison.md"
    lines = [
        "# 复现对比报告", "",
        f"目标文件：`{path.name}`（锁定哈希 `{fingerprint(rows)[:12]}`）", "",
        f"PASS {counts['PASS']} 项，FAIL {counts['FAIL']} 项，NOTE {counts['NOTE']} 项。总体：**{overall}**", "",
        "| 目标 | 出处 | 论文 | 复现 | 差 | 容差 | 判断 | 说明 |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for r, status, diff, reason in results:
        tol = (r["tolerance"] or "").strip()
        tol_txt = f"{tol} ({(r.get('tol_type') or 'abs').strip()})" if tol else ""
        lines.append(f"| {r['target']} | {r['source']} | {r['paper_value']} | {r['our_value']} | {diff} | {tol_txt} | {status} | {reason or (r.get('note') or '')} |")
    lines += ["", "## 偏差说明", "", "每个 FAIL 和 NOTE 都要在下面写出原因和出处。", ""]
    for r, status, _, _ in results:
        if status != "PASS":
            lines.append(f"- **{r['target']}**（{status}）：")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")

    for r, status, diff, reason in results:
        print(f"{status:5s} {r['target']}: 论文 {r['paper_value']}，复现 {r['our_value'] or '—'} {reason}")
    print(f"总体 {overall}。报告 → {out}")


if __name__ == "__main__":
    main()
