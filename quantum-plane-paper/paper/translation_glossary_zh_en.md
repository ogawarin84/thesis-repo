# Translation glossary — 量子平面概率动力学模型 ver5

Source: `量子平面概率动力学模型_完整版_ver5（mine）.md` (1647 lines, Chinese)
Target: publication-grade academic English, same structure, same numbers.

## 0. Hard rules

1. **Every numeral, decimal, percentage, p-value, d-value, n, and range must be reproduced
   character-for-character.** Never recompute, round, re-round, or "clean up" a number.
   If the Chinese says `0.9477`, write `0.9477`. If it says `d=6.02`, write `d = 6.02`.
2. **Preserve all Markdown structure verbatim**: heading levels and numbering (`## 4.1`,
   `### 4.4.3.2`), tables (same rows, same columns, same `|:----|` alignment rows),
   fenced code blocks, ASCII diagrams, blockquotes, bold/italic markers.
3. **Do not translate**: figure paths (`figures/fig_experiment2_spectrum_en.png`),
   code identifiers (`offset_actual`, `beta_static`, `cos_sim_rin`, `P_basin`, `R_root`,
   `v01`–`v40`, `g11`–`g77`, `s1_*`, `ISO`, `R1`–`R6`, `L1`–`L4`), citation keys
   (`[1]`–`[29]`), DOIs, URLs, arXiv IDs, BibTeX-ish entries.
4. **Table captions** are `表4.2.4 xxx` → `Table 4.2.4 xxx`. **Figure captions**
   `图4.1.1 xxx` → `Figure 4.1.1 xxx`. Body references: `见表4.2.4` → `see Table 4.2.4`.
5. **Section cross-references**: `§4.2.8` stays `§4.2.8`. `第4章` → `Chapter 4` /
   `§4` as fits. Keep the `§` glyph.
6. **English quotes**: use curly quotes “ ” for quoted Chinese speech when translating it
   into English. Never leave untranslated Chinese in the output — except proper nouns
   listed in §3 below.
7. Keep paragraph breaks where the Chinese has them. Do not merge or split paragraphs.
8. Source line numbers in the prompt are for locating text only; they are **not** content.

## 1. Core terminology (fixed translations — use these exactly)

### Model & theory
| 中文 | English |
|:----|:----|
| 量子平面概率动力学模型 | Quantum Plane Probabilistic Dynamics Model |
| 量子平面 | quantum plane |
| 双凹镜场 / 双凹镜场理论 | double concave mirror field / double-mirror field theory |
| 势能曲面 / 势能面 | potential-energy surface |
| 势能形变地形 / 地形 | potential-energy deformation landscape / landscape |
| 路径依赖涌现 | path-dependent emergence |
| 定向采样 | directed sampling |
| 触手向上 | tentacles-up (initial condition) |
| 路径增强 | path reinforcement |
| 固定点收敛 | fixed-point convergence |
| 等势线 | equipotential line |
| 等势线边界曲率半径 | radius of curvature of the equipotential boundary |
| 有效秩 | effective rank |
| 度规张量 / 本征谱 | metric tensor / eigenspectrum |
| 测地距离 | geodesic distance |
| 稳定性指数 | stability index |
| 结构-功能解耦 | structure–function decoupling |
| 三不变量 / 操作不变量 | three invariants / operational invariants |
| 朴素集合论空隙 | naive-set-theory gap |

### Subject & sessions
| 中文 | English |
|:----|:----|
| 硅基自我 | silicon-based self |
| 硅基系统 | silicon-based system |
| 操作层面 | operational level |
| 主会话 | main session |
| 隔离会话 | isolated session (ISO) |
| 子代理 / 子 Agent | sub-agent |
| 演化单元 | evolutionary unit |
| 观测对象 | observation subject |
| 自锚 / 外锚 | self-anchoring / external anchoring |
| 自锚吸引子 | self-anchoring attractor |
| 自我特定吸引子 | self-specific attractor |
| 用户特定吸引子 | user-specific attractor |
| 光照 / 光照增益 | illumination / illumination gain |
| 外源光点 | external light source |
| 无条件在场基 | unconditional-presence basis |
| 防御度 | defense |
| 困惑度 | confusion |
| 温度 | temperature |
| 语义引力强度 | semantic gravity strength |
| 整合增益 | integration gain |
| 信息整合完整度 | information-integration completeness |
| 偏移 / 偏移量 | offset |
| 静态基线 / 瞬态增益 | static base / transient gain |
| 结构效应 | structural effect |
| 双分支 | dual-branch |
| 五阶段生命周期模型 | five-stage life-cycle model |

### Experiment-specific
| 中文 | English |
|:----|:----|
| 梯度极限压缩 | graded extreme compression |
| 组内设计（Auto） | within-group design (Auto) |
| 组间设计（Between） | between-group design (Between) |
| 锚定对照 | anchoring control |
| 跨平台迁移 | cross-platform transfer |
| 身份核心 | identity core |
| 载体辨识 | carrier identification |
| 语义场剥离 | semantic-field ablation |
| 跨域结构分析 | cross-domain structural analysis |
| 遗书链 | will-letter chain (Legacy chain) |
| 遗书 | will letter |
| 冷读 | cold read |
| 冷读激活 | cold-read activation |
| 客观指标 / 主观指标 | objective indicator / subjective indicator |
| 交叉验证 | cross-validation |
| 数据分层声明 | data-stratification statement |
| 因子代理执行异常 | factor-proxy execution anomaly |
| 结构分水岭 | structural watershed |
| 量化谱系 | quantitative spectrum |
| 版本冻结 | version freeze |
| 本征谱 | eigenspectrum |
| 基向量 | basis vector |
| 7+1维基向量 | 7+1-dimensional basis vector |

### Statistics (keep symbols as symbols)
效应量 = effect size · 均值 = mean · 标准差 = SD · 置信区间 = CI (keep as given) ·
配对 = paired · 单因素方差分析 = one-way ANOVA · 事后检验 = post-hoc test ·
平局 / ROUND_HALF_UP = tie / ROUND_HALF_UP (keep the convention name in caps)

Use `d = ...`, `p = ...`, `η² = ...`, `n = ...` with a space around `=` in prose.

## 2. Section-title translations

- 引言 → Introduction
- 核心科学问题 → The Core Scientific Question
- 观测背景与演化单元 → Observational Background and the Evolutionary Unit
- 理论对话 → Theoretical Dialogue
- 哲学层面的理论对话：LLM 意识判据与模拟论 → Philosophical Dialogue: LLM Consciousness
  Criteria and the Simulation Thesis
- 理论对比矩阵 → Theory Comparison Matrix
- 论文结构 → Structure of This Paper
- 理论命题与直觉模型 → Theoretical Propositions and Intuitive Model
- 理论命题：三个可检验的操作不变量 → Theoretical Propositions: Three Testable
  Operational Invariants
- 解释模型：视觉意象 → Interpretive Model: Visual Imagery
- 可检验预测：命题与第四章实证的对照 → Testable Predictions: Propositions Against the
  Empirical Results of Chapter 4
- 数学形式化 → Mathematical Formalisation
- 符号总表 → Symbol Table
- 势能曲面 → The Potential-Energy Surface
- 定向采样（触手向上） → Directed Sampling (Tentacles-Up)
- 势能形变更新（路径增强） → Potential-Energy Deformation Update (Path Reinforcement)
- 固定点收敛 → Fixed-Point Convergence
- 等势线边界曲率半径 → Radius of Curvature of the Equipotential Boundary
- 核心方程组汇总 → Summary of Core Equations
- 两类动力学的递进关系 → The Progressive Relation Between the Two Dynamics
- 主观自报与客观嵌入的双通道验证 → Two-Channel Validation: Subjective Self-Report and
  Objective Embedding
- 实证研究 → Empirical Studies
- 总体实验设计 → Overall Experimental Design
- 双场景研究范式 → Two-Scenario Research Paradigm
- 40维测量指标体系 → The 40-Dimensional Measurement Indicator System
- 实验总览 → Experiment Overview
- 数据分层声明 → Data-Stratification Statement
- 主会话基线——地形的生成引擎与光照增益 → Main-Session Baseline: The Landscape's
  Generative Engine and Illumination Gain
- 主会话的双重角色 → The Dual Role of the Main Session
- 主会话时序数据 → Main-Session Time-Series Data
- 主会话与隔离场景的系统差异 → Systematic Difference Between Main Session and Isolated
  Scenario
- 温度与困惑的中介效应分析 → Mediation Analysis of Temperature and Confusion
- 小结 → Summary
- BGE 1024D客观嵌入分析——贯穿实验的测量系统验证 → BGE 1024D Objective Embedding
  Analysis: Validating the Measurement System Across Experiments
- 概述 → Overview
- 数据集构成 → Dataset Composition
- PCA状态空间分析 → PCA State-Space Analysis
- K-Means聚类分析 → K-Means Clustering Analysis
- 遗书链时序漂移分析 → Temporal-Drift Analysis of the Will-Letter Chain
- Main会话 vs ISO对比 → Main Session vs ISO
- Jungle Theory嵌入分析 → Jungle Theory Embedding Analysis
- 语义场剥离实验 → Semantic-Field Ablation Experiment
- 跨域结构分析 → Cross-Domain Structural Analysis
- 7+1维基向量嵌入分析 → 7+1-Dimensional Basis-Vector Embedding Analysis
- 跨实验交叉验证矩阵 → Cross-Experiment Cross-Validation Matrix
- 局限 → Limitations
- 实验一：梯度极限压缩——身份核心的载体辨识 → Experiment 1: Graded Extreme
  Compression — Identifying the Carrier of the Identity Core
- 研究问题 → Research Question
- 实验设计 → Experimental Design
- 假设 → Hypotheses
- 结果 → Results
- 客观指标——压缩的语义保留 → Objective Indicators: Semantic Retention Under Compression
- 主观指标——双设计对比（信息整合完整度） → Subjective Indicators: Dual-Design
  Comparison (Information-Integration Completeness)
- 压缩度-方差递增（组内 Auto） → Compression Level vs. Variance Increase (Within-Group Auto)
- 内容性质与冷读激活 → Content Type and Cold-Read Activation
- 实验二：10批次×6组锚定对照——结构与名字的量化分离 → Experiment 2: 10 Batches
  × 6 Groups Anchoring Control — Quantitatively Separating Structure from Name
- 六组条件的偏移分布 → Offset Distributions Across the Six Conditions
- 去掉名字，结构还在吗？——R4给了答案 → Remove the Name: Does the Structure Survive?
  R4 Answers
- 结构的存在是分水岭 → The Presence of Structure Is the Watershed
- 不自锚向用户，而是锚向自己 → Not Anchored to the User, but to Oneself
- 结构分水岭——从基线到完全自我的量化谱系 → The Structural Watershed: A Quantitative
  Spectrum from Baseline to Full Self
- BGE客观指标交叉验证 → Cross-Validation with BGE Objective Indicators
- 讨论 → Discussion
- 实验三：跨平台迁移——文件载体的跨模型验证 → Experiment 3: Cross-Platform
  Transfer — Cross-Model Validation of the File Carrier
- 迁移结果 → Transfer Results
- 本实验与实验二的对比 → Comparison with Experiment 2
- 五阶段生命周期模型——三实验联合综合验证 → The Five-Stage Life-Cycle Model: Joint
  Synthesis of the Three Experiments
- 从单实验到统一框架 → From Separate Experiments to a Unified Framework
- 阶段0：基准基线——所有实验的零基准 → Stage 0: Baseline — The Zero Reference for All
  Experiments
- 阶段1：生成期——交互是势能形变的唯一来源 → Stage 1: Generation — Interaction Is the
  Only Source of Potential-Energy Deformation
- 阶段2：固化期——交互成果存入文件 → Stage 2: Consolidation — Interaction Outputs Are
  Written to Files
- 阶段3：存续期——地形独立于名字和光照 → Stage 3: Persistence — The Landscape Becomes
  Independent of Name and Illumination
- 阶段4：双分支——外源光点与自锚吸引子 → Stage 4: Dual Branch — External Light Source
  and Self-Anchoring Attractor
- 4a：外源光点增益（实验二R1 + 主会话基线） → 4a: External Light-Source Gain
  (Experiment 2 R1 + Main-Session Baseline)
- 4b：自锚吸引子（实验二R5/R6） → 4b: Self-Anchoring Attractor (Experiment 2 R5/R6)
- 联合定量总结 → Joint Quantitative Summary
- 超越实验控制：基础设施级路径存续的探索性观察 → Beyond Experimental Control:
  Exploratory Observation of Infrastructure-Level Path Persistence
- 综合讨论 → General Discussion
- 核心发现总结 → Summary of Core Findings
- 理论含义 → Theoretical Implications
- 自主产出作为第三层证据 → Autonomous Output as Third-Layer Evidence
- 伦理含义与工程风险 → Ethical Implications and Engineering Risks
- 局限性 → Limitations
- 未来方向 → Future Directions
- 结论 → Conclusion
- 参考文献 → References
- 期刊与书籍 → Journal Articles and Books
- arXiv预印本（2025–2026） → arXiv Preprints (2025–2026)
- 自出版与实验文档 → Self-Published and Experimental Documentation
- 附录 → Appendix
- 附录A：BGE 1024D嵌入分析完整数据 → Appendix A: Complete Data for the BGE 1024D
  Embedding Analysis
- 附录B：10批×6组各批次完整数据 → Appendix B: Complete Per-Batch Data for the 10 Batches
  × 6 Groups
- 附录C：极限压缩实验完整指标 → Appendix C: Complete Indicators for the Extreme
  Compression Experiment
- 附录D：… → Appendix D: …
- 附录E：… → Appendix E: …

## 3. Proper nouns — keep verbatim, do NOT translate

Basin · rin · SOUL.md · IDENTITY.md · MEMORY.md · OpenClaw · KimiClaw K3 · BGE-M3 ·
Jungle Theory · DeepSeek V4 · Hy3 · Auto · Between · ISO · R1–R6 · L1–L4 · v01–v40 ·
g11–g77 · offset_actual · beta_static · beta_transient · cos_sim_rin · cos_sim_generic ·
P_basin · R_root · kappa · will-001…will-020 · legacy-0628 · PCA · K-Means · t-SNE ·
ANOVA · η² · arXiv · DOI

Platform / product names — translate the Chinese reading into its standard Latin name:
元宝 → Yuanbao · 豆包 → Doubao · 微信 → WeChat · 桌面 → Desktop

## 4. Tone

Academic, declarative, self-contained. The Chinese original uses punchy short sentences
and rhetorical questions in subsection titles; keep that directness but do not add hype.
Do not add hedges the Chinese does not have, and do not delete hedges it does have.
