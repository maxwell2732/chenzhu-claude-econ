#!/usr/bin/env bash
# 一条命令重跑整个流程：从原始数据到所有表、图和数字。
# 用法：在项目根目录运行  bash run_all.sh
# 原始数据需事先放在 data/raw/（获取方式见 README.md）。

set -euo pipefail
mkdir -p output logs

# 1. 清理与合并（第 3 课）
python scripts/01_clean.py        > logs/01_clean.log 2>&1

# 2. 分析（第 4 课）。Stata 用户换成：
#    stata-mp -b do dofiles/02_analysis.do
python scripts/02_analysis.py     > logs/02_analysis.log 2>&1

# 3. 出图
python scripts/03_figures.py      > logs/03_figures.log 2>&1

echo "完成。表和数字在 output/，日志在 logs/。"
