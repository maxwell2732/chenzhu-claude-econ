"""
参考脚本：从世界银行 API 下载 GDP 实际增速（NY.GDP.MKTP.KD.ZG）。

用法：
    python download_wdi.py                      # 只下载中国
    python download_wdi.py CHN IND IDN VNM BRA USA

建议先让智能体自己写一个下载脚本，写完再和这份对照。
只用 Python 标准库，不需要安装任何包。
"""

import csv
import json
import os
import sys
import urllib.request

INDICATOR = "NY.GDP.MKTP.KD.ZG"   # GDP 实际增速（年度，%）
START, END = 2000, 2024
OUT_DIR = os.path.join("data", "raw")


def fetch(countries):
    """调用世界银行 API v2，返回记录列表。"""
    url = (
        f"https://api.worldbank.org/v2/country/{';'.join(countries)}"
        f"/indicator/{INDICATOR}?format=json&date={START}:{END}&per_page=2000"
    )
    with urllib.request.urlopen(url, timeout=60) as resp:
        payload = json.load(resp)
    # API 返回 [元数据, 记录列表]；出错时只有一个包含 message 的元素
    if not isinstance(payload, list) or len(payload) < 2 or payload[1] is None:
        raise RuntimeError(f"API 没有返回数据：{payload}")
    meta, records = payload[0], payload[1]
    if meta.get("pages", 1) > 1:
        raise RuntimeError("结果超过一页，请调大 per_page 或分批下载")
    return records


def main():
    countries = [c.upper() for c in sys.argv[1:]] or ["CHN"]
    records = fetch(countries)

    os.makedirs(OUT_DIR, exist_ok=True)
    name = "wdi_china.csv" if countries == ["CHN"] else "wdi_growth.csv"
    out_path = os.path.join(OUT_DIR, name)

    rows = []
    for r in records:
        rows.append({
            "iso3": r.get("countryiso3code"),
            "country": r["country"]["value"],
            "year": int(r["date"]),
            "gdp_growth": r["value"],   # 缺失值保留为空，不要填 0
        })
    rows.sort(key=lambda x: (x["iso3"], x["year"]))

    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["iso3", "country", "year", "gdp_growth"])
        writer.writeheader()
        writer.writerows(rows)

    # 简单的数据画像：每个国家多少年、多少缺失
    print(f"已保存 {out_path}，共 {len(rows)} 行")
    for iso in sorted({r["iso3"] for r in rows}):
        sub = [r for r in rows if r["iso3"] == iso]
        missing = sum(1 for r in sub if r["gdp_growth"] is None)
        print(f"  {iso}: {len(sub)} 年，缺失 {missing} 个")


if __name__ == "__main__":
    main()
