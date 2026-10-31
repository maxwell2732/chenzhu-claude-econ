"""
备选路线：下载世界银行的几个“模块”文件，用来练习审查、清理、合并（第 3 课）

还没拿到 CHNS 或 CHARLS 的同学用这份数据走一遍流程。它会在 data/raw/ 下生成：
    wdi_ag_emp.csv        农业就业占比 SL.AGR.EMPL.ZS（国家-年份）
    wdi_gdp_pc.csv        人均 GDP，2015 年不变价美元 NY.GDP.PCAP.KD（国家-年份）
    wdi_urban.csv         城镇人口占比 SP.URB.TOTL.IN.ZS（国家-年份）
    wdi_countries.csv     国家信息：地区、收入组（每个国家一行）

这些文件故意保留原样，里面有审查时应该发现的问题，例如：
指标文件里混有地区和收入组的汇总行；缺失值；国家信息表里也有汇总行。
合并时：三个指标文件按（国家，年份）一对一合并；国家信息表按国家多对一合并。

用法：
    python download_wdi_modules.py
只用 Python 标准库。用 Codex 的同学，记得先在 config.toml 里打开联网。
"""

import csv
import json
import os
import urllib.request

START, END = 2000, 2023
INDICATORS = {"wdi_ag_emp.csv": "SL.AGR.EMPL.ZS", "wdi_gdp_pc.csv": "NY.GDP.PCAP.KD", "wdi_urban.csv": "SP.URB.TOTL.IN.ZS"}
OUT = os.path.join("data", "raw")


def get(url):
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.load(r)


def fetch_indicator(code):
    rows, page = [], 1
    while True:
        p = get(f"https://api.worldbank.org/v2/country/all/indicator/{code}?format=json&date={START}:{END}&per_page=20000&page={page}")
        if not isinstance(p, list) or len(p) < 2 or p[1] is None:
            raise RuntimeError(f"API 没有返回数据：{p}")
        rows += p[1]
        if page >= p[0].get("pages", 1):
            return rows
        page += 1


def main():
    os.makedirs(OUT, exist_ok=True)
    for fname, code in INDICATORS.items():
        recs = fetch_indicator(code)
        with open(os.path.join(OUT, fname), "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["iso3", "country", "year", "value"])
            for r in recs:
                w.writerow([r.get("countryiso3code"), r["country"]["value"], r["date"], r["value"]])
        print(f"已保存 data/raw/{fname}，{len(recs)} 行")

    meta = get("https://api.worldbank.org/v2/country?format=json&per_page=1000")
    with open(os.path.join(OUT, "wdi_countries.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["iso3", "name", "region", "income_group"])
        for c in meta[1]:
            w.writerow([c["id"], c["name"], c["region"]["value"], c["incomeLevel"]["value"]])
    print(f"已保存 data/raw/wdi_countries.csv，{len(meta[1])} 行")


if __name__ == "__main__":
    main()
