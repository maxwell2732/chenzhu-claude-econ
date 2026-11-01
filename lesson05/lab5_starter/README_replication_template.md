# 【项目名称】复制包

【一两句话：研究问题和主要结论】

作者：【姓名】　最后更新：【日期】

## 数据

本仓库不包含任何数据。

| 数据 | 获取方式 | 版本或下载日期 | 放在哪里 |
| --- | --- | --- | --- |
| 【CHARLS】 | 【官网申请，审核约 X 天】 | 【2011–2020 年各轮，下载于 YYYY-MM】 | `data/raw/w2011/` 等 |

放好以后，运行 `python hash_raw.py check` 可以核对文件和我用的是否一致（`raw_hashes.txt` 在仓库里）。

## 运行环境

| 软件 | 版本 |
| --- | --- |
| Python | 【3.11】，依赖见 `requirements.txt` |
| Stata | 【18 MP】，外部命令：【csdid、reghdfe】 |

## 重跑

```
bash run_all.sh
```

在【普通笔记本电脑】上约需【X 分钟】。

## 输出对照

| 论文中的位置 | 文件 | 生成脚本 |
| --- | --- | --- |
| 表 1 | `output/table1.csv` | `scripts/02_analysis.py` |
| 图 2 | `output/figures/event_study.png` | `scripts/03_figures.py` |
| 正文数字 | `output/numbers.json` | 各分析脚本 |

## 留痕

- `DECISIONS.md`：每个分析决定及理由
- `LOG.md`：工作过程
- `reports/`：数据审查、清理、合并、审查报告
- `AI_USE.md`：哪些部分用了 AI、怎样核对

## 已知问题

【例如：图的字体在不同系统上略有不同，不影响数字。】
