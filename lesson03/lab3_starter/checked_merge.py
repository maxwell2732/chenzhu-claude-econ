"""
参考函数：带报告的合并（第 3 课）

每次合并都打印：左表、右表、合并后的行数；匹配、只在左边、只在右边的数量；
并用 pandas 的 validate 参数检查合并关系（一对一、多对一……），关系不对就直接报错。

在你的清理脚本里这样用：
    from checked_merge import checked_merge
    panel = checked_merge(person, household, keys=["householdID", "wave"],
                          how="left", validate="m:1", expect_match=0.99,
                          label="个人表 + 家户表")

直接运行本文件会跑一个小例子：
    python checked_merge.py
"""

import pandas as pd


def checked_merge(left, right, keys, how="left", validate="m:1", expect_match=None, label="merge"):
    nl, nr = len(left), len(right)
    # 只用键列做匹配统计，不复制整张宽表
    lk = left[keys].drop_duplicates()
    rk = right[keys].drop_duplicates()
    ind = lk.merge(rk, on=keys, how="outer", indicator=True)
    both = left[keys].merge(rk, on=keys, how="inner")
    n_match = len(both)
    only_left = nl - n_match
    only_right = int((ind["_merge"] == "right_only").sum())

    out = left.merge(right, on=keys, how=how, validate=validate)   # 关系不对会抛出 MergeError

    rate = n_match / nl if nl else 0.0
    print(f"[merge] {label}   键 = {tuple(keys)}   关系 = {validate}   方式 = {how}")
    print(f"        左表 n = {nl:,}    右表 n = {nr:,}")
    print(f"        合并后 n = {len(out):,}")
    print(f"        匹配 {n_match:,} ({rate:.1%})   只在左边 {only_left:,}   右表中没匹配上的键 {only_right:,}")
    if expect_match is not None:
        status = "通过" if rate >= expect_match else "未通过，请检查没匹配上的是谁"
        print(f"        预期匹配率 ≥ {expect_match:.0%}     结果：{status}")
    if how == "left" and validate in ("m:1", "1:1") and len(out) != nl:
        print("        注意：左连接后行数变了，说明右表的键有重复")
    return out


if __name__ == "__main__":
    person = pd.DataFrame({"pid": [1, 2, 3, 4, 5], "householdID": [10, 10, 20, 30, 40], "wave": [2011] * 5})
    household = pd.DataFrame({"householdID": [10, 20, 30, 50], "wave": [2011] * 4, "hh_income": [5.1, 3.2, 8.0, 1.0]})
    checked_merge(person, household, keys=["householdID", "wave"], expect_match=0.95, label="个人表 + 家户表（示例）")
    print()
    bad = pd.concat([household, household.iloc[[0]]])   # 右表键重复
    try:
        checked_merge(person, bad, keys=["householdID", "wave"], label="右表键重复的例子")
    except pd.errors.MergeError as e:
        print(f"[merge] 合并被拦下：{e}")
