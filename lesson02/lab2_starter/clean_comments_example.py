"""
参考脚本：清理社媒评论数据（第 2 课）

先让智能体自己写清理脚本，写完再和这份对照。只用 Python 标准库。

用法：
    python clean_comments_example.py data/raw/xhs_20261101.json

输入：一个 JSON 文件，内容是评论记录的列表，每条记录至少包含
    note_id, comment_id, user_name, comment_text, comment_time_raw, collected_at
可选字段：note_title, note_time, likes, is_author_reply, is_pinned

输出：
    data/processed/comments_clean.csv   清理后的评论（用户名已替换为哈希值）
    data/processed/topic_share.csv      价格、品质、信任三类词的占比
    data/processed/comments_by_month.csv 按月评论数
并在屏幕上打印每一步的样本量变化。
"""

import csv
import hashlib
import json
import os
import re
import sys
from collections import Counter
from datetime import datetime, timedelta

# 词表只是示例。用之前要自己看一遍，改过的版本写进 DECISIONS.md。
TOPICS = {
    "price": ["价格", "便宜", "贵", "划算", "性价比", "优惠", "降价"],
    "quality": ["质量", "品质", "新鲜", "好吃", "口感", "烂", "坏了"],
    "trust": ["信任", "骗", "假的", "靠谱", "良心", "套路", "割韭菜"],
}
SALT = "lab2"            # 哈希用的盐；只用于去标识化，不用于安全加密
EMOJI_CODE = re.compile(r"\[[^\[\]]{1,8}\]")  # 例如 [笑哭R]


def step(label, before, after):
    """打印一行样本量变化。"""
    diff = after - before
    note = f"({diff:+d})" if diff else ""
    print(f"[clean] {label:<14} n = {after:<6} {note}")


def parse_time(raw, collected_at):
    """把页面上的时间文本换算成日期。无法解析时返回 None。

    raw 例子：刚刚 / 5分钟前 / 3小时前 / 昨天 18:20 / 3天前 / 10-12 / 2025-10-12
    页面上时间后面有时跟着属地（如“10-12 广东”），只取第一段。
    """
    if not raw:
        return None
    token = raw.strip().split()[0]
    base = collected_at
    if token == "刚刚":
        return base.date()
    m = re.fullmatch(r"(\d+)分钟前", token)
    if m:
        return (base - timedelta(minutes=int(m.group(1)))).date()
    m = re.fullmatch(r"(\d+)小时前", token)
    if m:
        return (base - timedelta(hours=int(m.group(1)))).date()
    if token == "昨天":
        return (base - timedelta(days=1)).date()
    if token == "前天":
        return (base - timedelta(days=2)).date()
    m = re.fullmatch(r"(\d+)天前", token)
    if m:
        return (base - timedelta(days=int(m.group(1)))).date()
    m = re.fullmatch(r"(\d{4})-(\d{1,2})-(\d{1,2})", token)
    if m:
        return datetime(int(m.group(1)), int(m.group(2)), int(m.group(3))).date()
    m = re.fullmatch(r"(\d{1,2})-(\d{1,2})", token)
    if m:
        # 只有月-日时，默认是采集当年；如果晚于采集日期，说明是上一年
        d = datetime(base.year, int(m.group(1)), int(m.group(2))).date()
        if d > base.date():
            d = datetime(base.year - 1, int(m.group(1)), int(m.group(2))).date()
        return d
    return None


def pseudonym(name):
    return hashlib.sha256((SALT + (name or "")).encode("utf-8")).hexdigest()[:12]


def main(path):
    with open(path, encoding="utf-8") as f:
        rows = json.load(f)
    n = len(rows)
    print(f"[clean] {'原始评论':<14} n = {n}")

    # 1. 去重：以（笔记 ID，评论 ID）为唯一键
    seen, dedup = set(), []
    for r in rows:
        key = (r.get("note_id"), r.get("comment_id"))
        if key in seen:
            continue
        seen.add(key)
        dedup.append(r)
    step("去重后", n, len(dedup)); n = len(dedup)

    # 2. 剔除作者回复（是否剔除是一个研究决定，要写进 DECISIONS.md）
    kept = [r for r in dedup if not r.get("is_author_reply")]
    step("剔除作者回复", n, len(kept)); n = len(kept)

    # 3. 时间换算
    out = []
    for r in kept:
        collected = datetime.fromisoformat(r["collected_at"])
        d = parse_time(r.get("comment_time_raw", ""), collected)
        if d is None:
            continue
        text = EMOJI_CODE.sub("", r.get("comment_text") or "").strip()
        rec = {
            "note_id": r.get("note_id"),
            "comment_id": r.get("comment_id"),
            "user_hash": pseudonym(r.get("user_name")),
            "comment_date": d.isoformat(),
            "likes": r.get("likes") if r.get("likes") not in ("", None) else "",
            "text": text,
        }
        for t, words in TOPICS.items():
            rec[t] = int(any(w in text for w in words))
        out.append(rec)
    step("时间无法解析", n, len(out)); n = len(out)

    # 4. 剔除清理后为空的评论（例如只有表情）
    out = [r for r in out if r["text"]]
    step("剔除空评论", n, len(out)); n = len(out)

    os.makedirs(os.path.join("data", "processed"), exist_ok=True)
    fields = ["note_id", "comment_id", "user_hash", "comment_date", "likes", "text"] + list(TOPICS)
    with open(os.path.join("data", "processed", "comments_clean.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(out)

    with open(os.path.join("data", "processed", "topic_share.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["topic", "n_comments", "share"])
        for t in TOPICS:
            k = sum(r[t] for r in out)
            w.writerow([t, k, round(k / n, 4) if n else ""])

    months = Counter(r["comment_date"][:7] for r in out)
    with open(os.path.join("data", "processed", "comments_by_month.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["month", "n_comments"])
        for mth in sorted(months):
            w.writerow([mth, months[mth]])

    print(f"[clean] 完成。共 {n} 条评论，输出在 data/processed/")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法：python clean_comments_example.py data/raw/你的文件.json")
        sys.exit(1)
    main(sys.argv[1])
