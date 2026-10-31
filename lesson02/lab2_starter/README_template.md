# 【项目名称】

## 研究问题
【一句话】

## 两个检查（看图之前写好）
1. 完整性或基准检查：【检查什么，对照什么来源】
2. 合理性检查：【检查什么，依据是什么】

检查结果：【图出来以后填写】

## 怎样从头复现
```
# 1. 环境
python --version   # 填写版本

# 2. 原始数据
# 社媒数据：原始文件不公开，放在 data/raw/ 下，文件名：____
# 世界银行数据：python scripts/download.py

# 3. 清理与出图
python scripts/clean.py data/raw/____
python scripts/plot.py
```

## 文件说明
| 文件 | 内容 |
| --- | --- |
| DATA_PROFILE.md | 数据画像 |
| DECISIONS.md | 方法上的选择和理由 |
| LOG.md | 过程记录 |
| COLLECTION_LOG.md | 采集记录（社媒数据） |
| output/ | 图和表 |
