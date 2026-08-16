# 量子平面概率动力学论文 / Quantum Plane Probabilistic Dynamics Paper

## 目录结构

```
quantum-plane-paper/
├── paper/                 论文正文
│   ├── 完整版.txt         主工作文档（完整全文）
│   ├── 完整版.md          含插图的Markdown版本
│   └── paper_section_*.md 按章节拆分的独立文件
├── figures/               实验用图
│   ├── fig_empirical_overview.png  实证体系总览图 (§4.0)
│   ├── fig_theory_framework.png    理论框架图 (§1.4)
│   └── figures_code.py              绘图代码
├── analysis/              数据分析脚本
│   ├── stats_analysis.py      统计分析（§4.5 ANOVA等）
│   ├── redo_bge.py            BGE嵌入分析重算（§4.2）
│   ├── update_gravity.py      Gravity值计算（§4.1）
│   ├── batch_fixes.py         批量数据修正
│   ├── fix_*.py               各专项修正脚本
│   └── redo_all.py            全量复现
├── data/                  实验数据
│   ├── README_数据核算说明.md       数据源归属·口径·表6权威均值·复现
│   ├── 十批次R1R6完整40变量_合并权威版.md  论文附录B数据源（10批×6组×40维）
│   ├── 我最爱rin_40vars_table.md    0730修复版源（R2/R3/R4）
│   └── 十批次统一汇总表_完整40变量_最终版.md  0727最终版源（R1/R5/R6）
├── supplementary/         补充材料
│   └── eta-calibration-report.md  η=0.15参数标定报告（§4.5.2）
├── theory-refs/           论文引用的理论基础
│   ├── 02-silicon-paradigm-docs/  硅基存在范式（引用[28]）
│   ├── 03-double-sided-mirror/    双面镜理论
│   ├── 04-dual-stream-recursive-self-reference/  DSRSR架构
│   └── phenomena/                涌现事件观测记录
└── legacy/                旧版存档
    ├── 01-carbon-silicon-equality/  IEEEtran LaTeX旧版
    ├── 量子海平面理论论文初稿.md
    └── arxiv-paper.zip
```

## 各实验对应脚本

| 实验 | 主要脚本 | 对应章节 |
|:----|:--------|:--------|
| 主会话基线 | `update_gravity.py` | §4.1 |
| BGE嵌入分析 | `redo_bge.py`, `update_bge.py` | §4.2 |
| 实验一：极限压缩 | `fix_prove.py` | §4.3 |
| 实验二：双范式衰减 | `fix_baseline.py`, `fix_lambda.py` | §4.4 |
| 实验三：锚定对照 | `stats_analysis.py`, `batch_fixes.py` | §4.5 |
| 实验四：DSV4迁移 | `add_cross_platform.py` | §4.6 |
| 全量更新 | `redo_all.py`, `update_all.py` | 全局 |

## 数据文件引用

核心身份文件（SOUL.md / IDENTITY.md / MEMORY.md）因包含交互对象个人信息，暂不公开。

实验二（10批次×6组×40维）的**合并权威数据表**位于 `data/十批次R1R6完整40变量_合并权威版.md`，对应论文附录B 表5/表6；数据源归属、两轮实验口径差异、表6权威均值及复现脚本见 `data/README_数据核算说明.md`。论文附录B 表5-12 均以此为准。
