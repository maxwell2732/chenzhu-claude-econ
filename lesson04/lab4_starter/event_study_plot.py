"""从系数表画事件研究图。

用法：
    python event_study_plot.py reports/event_study_coefs.csv reports/figures/event_study.png

输入 CSV 的列：
    rel_time   相对处理时间（整数，基期一般是 -1）
    estimate   系数
    ci_low     置信区间下限
    ci_high    置信区间上限
    （如果没有 ci_low/ci_high，也可以给 se 列，脚本按 1.96*se 计算 95% 区间）

基期那一行可以写 estimate=0、ci_low=0、ci_high=0，也可以不写，脚本会补上。

脚本还会打印处理前系数的简单汇总。注意：处理前系数都不显著，
不能证明平行趋势成立，只是没有发现明显的反例。看图的标准要在出图之前写下来。
"""
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


def main():
    if len(sys.argv) < 3:
        sys.exit("用法：python event_study_plot.py <coefs.csv> <out.png> [基期，默认 -1]")
    src, out = Path(sys.argv[1]), Path(sys.argv[2])
    base = int(sys.argv[3]) if len(sys.argv) > 3 else -1

    df = pd.read_csv(src)
    if "ci_low" not in df.columns and "se" in df.columns:
        df["ci_low"] = df["estimate"] - 1.96 * df["se"]
        df["ci_high"] = df["estimate"] + 1.96 * df["se"]
    need = {"rel_time", "estimate", "ci_low", "ci_high"}
    if not need.issubset(df.columns):
        sys.exit(f"缺少列：{sorted(need - set(df.columns))}")
    if base not in set(df["rel_time"]):
        df = pd.concat([df, pd.DataFrame([{"rel_time": base, "estimate": 0.0, "ci_low": 0.0, "ci_high": 0.0}])])
    df = df.sort_values("rel_time").reset_index(drop=True)

    pre = df[df["rel_time"] < base]
    excl = pre[(pre["ci_low"] > 0) | (pre["ci_high"] < 0)]
    print(f"处理前系数 {len(pre)} 个（不含基期 {base}），其中置信区间不含 0 的 {len(excl)} 个。")
    if len(pre) < 2:
        print("提醒：处理前只有不到两个系数，很难判断处理前趋势。")
    if len(excl):
        print("需要警惕：处理前已有显著偏离，rel_time =", list(excl["rel_time"]))
    print("提醒：处理前不显著不等于平行趋势成立。")

    fig, ax = plt.subplots(figsize=(6.4, 3.8), dpi=200)
    ax.axhline(0, color="#9AA0A6", lw=0.8, ls="--")
    ax.axvline(base + 0.5, color="#B5452F", lw=0.8, ls="--")
    ax.vlines(df["rel_time"], df["ci_low"], df["ci_high"], color="#2A2C30", lw=1.4)
    ax.scatter(df["rel_time"], df["estimate"], color="#2A2C30", s=22, zorder=3)
    ax.set_xticks(df["rel_time"])
    ax.set_xlabel("Periods relative to treatment")
    ax.set_ylabel("Estimate (95% CI)")
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    fig.tight_layout()
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out)
    print("图 →", out)


if __name__ == "__main__":
    main()
