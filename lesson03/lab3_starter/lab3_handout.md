# 第 3 课作业：审查、清理、合并你的调查数据

预计用时约 2 小时。

## 两条路线

| 路线 | 数据 | 产出 |
| --- | --- | --- |
| 主路线 | 你自己申请到的 CHNS 或 CHARLS，至少三轮 | 个人-年份面板、审查报告、清理报告、合并报告、codebook |
| 备选路线 | 世界银行：三个指标文件 + 国家信息表（`download_wdi_modules.py`） | 国家-年份面板、审查报告、合并报告、codebook |

还没拿到调查数据的同学先走备选路线，拿到以后补做主路线。

## 步骤

1. 克隆 research harness 仓库作为项目文件夹：

   ```
   cd ~
   git clone https://github.com/maxwell2732/claudecode-research-harness-workflow.git lab3
   cd lab3
   mkdir -p data/raw .claude
   ```

2. 把原始数据放进 `data/raw/`，按轮次建子文件夹（例如 `data/raw/w2011/`）。备选路线运行 `python ~/lab3_starter/download_wdi_modules.py`。
3. 加上保护：

   ```
   cp ~/lab3_starter/settings.json.template .claude/settings.json
   cat ~/lab3_starter/data_rules_for_CLAUDE.md >> CLAUDE.md
   git check-ignore data/raw          # 应输出 data/raw
   python ~/lab3_starter/hash_raw.py save
   ```

4. 启动 `claude`，输入 `/permissions`，确认 deny 规则里有 `Edit(./data/raw/**)`。
5. 按 `prompts.md` 的顺序：可行性 → setup → audit → 清理计划 → clean。
6. 审查报告和清理计划都要自己读一遍，编码含义对照问卷核对。
7. 开一个新会话，只读 codebook 回答五个变量的含义。
8. 运行 `python ~/lab3_starter/hash_raw.py check`，确认原始数据全部一致。

## 完成之后

1. 对照 `lab3_verify_checklist.md` 自查。
2. 填写 `exit_ticket.md`。
3. 清理好的面板留在本地，第 4 课还要用。
