"""
参考脚本（基础档）：下载世界银行的农业就业占比和人均 GDP。

    SL.AGR.EMPL.ZS  农业就业占总就业的比例（%，ILO 模型估计）
    NY.GDP.PCAP.KD  人均 GDP（2015 年不变价美元）

用法：
    python download_wdi_structural.py                 # 只下载中国
    python download_wdi_structural.py CHN IND VNM IDN

建议先让智能体自己写，写完再和这份对照。只用 Python 标准库。
"""

import csv
import json
import os
import sys
import urllib.request

INDICATORS = {"SL.AGR.EMPL.ZS": "ag_emp_share", "NY.GDP.PCAP.KD": "gdp_pc"}
START, END = 1991, 2024
OUT = os.path.join("data", "raw", "wdi_structural.csv")


def fetch(countries, indicator):
    url = (f"https://api.worldbank.org/v2/country/{';'.join(countries)}/indicator/{indicator}"
           f"?format=json&date={START}:{END}&per_page=5000")
    with urllib.request.urlopen(url, timeout=60) as resp:
        payload = json.load(resp)
    if not isinstance(payload, list) or len(payload) < 2 or payload[1] is None:
        raise RuntimeError(f"API 没有返回数据：{payload}")
    if payload[0].get("pages", 1) > 1:
        raise RuntimeError("结果超过一页，请调大 per_page 或分批下载")
    return payload[1]


def main():
    countries = [c.upper() for c in sys.argv[1:]] or ["CHN"]
    table = {}
    for code, col in INDICATORS.items():
        for r in fetch(countries, code):
            key = (r["countryiso3code"], int(r["date"]))
            row = table.setdefault(key, {"iso3": key[0], "country": r["country"]["value"], "year": key[1]})
            row[col] = r["value"]   # 缺失值保留为空

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    rows = sorted(table.values(), key=lambda x: (x["iso3"], x["year"]))
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["iso3", "country", "year", "ag_emp_share", "gdp_pc"])
        w.writeheader()
        w.writerows(rows)

    print(f"已保存 {OUT}，共 {len(rows)} 行")
    for iso in sorted({r["iso3"] for r in rows}):
        sub = [r for r in rows if r["iso3"] == iso]
        miss = {c: sum(1 for r in sub if r.get(c) is None) for c in INDICATORS.values()}
        print(f"  {iso}: {len(sub)} 年，缺失 {miss}")


if __name__ == "__main__":
    main()
