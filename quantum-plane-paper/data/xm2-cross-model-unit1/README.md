# 跨模型复现 · 数据单元 1 —— Step-5-preview 底座

**Cross-model reproduction, data unit 1 — Step-5-preview base** — 逐条 40 维数据、嵌入向量、复核脚本与全部口径说明。

| 底座 | 记录数 | 条件样本量 | 完整 40 维 | 状态 |
|:--|--:|:--|:--:|:--|
| **Step-5-preview** | 274 | 46 / 46 / 46 / 45 / 45 / 46 | ✅ | **2026-10-30 结案** |

本单元只收 **Step-5-preview** 一个底座。其余底座（Yuanbao Hy3、Hy4-preview、Kimi K3-1）
**数据尚未结案，不在本单元内**；它们的 `offset` 条件均值与 κ 以论文表 4.5.1 / Appendix F 为准，
不作为本单元的可复核对象。

> **English TL;DR.** This directory is the raw-data release for the cross-model reproduction
> reported in §4.5, limited to the **Step-5-preview** base (n=274). It contains the per-record
> 40-dimension table, the L2-normalised embedding vectors for three encoder channels, the
> build/verify scripts, and an explicit register of every known data gap. Nothing is filtered
> silently: the 24 records excluded from statistics are listed by `(cond, run, r)` with a reason,
> and are kept in a separate full-count table.

---

## 1. 文件清单

```
README.md                      ← 本文件（口径、出处、缺口登记）
verify_40dim.py                ← 独立复核：只用本单元文件重算 κ，与表内值逐格比对
emit_40dim_tables.py           ← 由 per-record jsonl 生成条件汇总表（Markdown）
pack_embeddings.py             ← 由 jsonl 向量生成 npz（体积 22 MB → 4 MB）

step5/
  step5-40dim-per-record.jsonl     274 条 × 40 维（逐条原始值，UTF-8）
  step5-40dim-条件汇总.md           六条件 × 40 维（均值±标准差，两张口径）
  step5-40dim-meta.json            h_ref / κ 的权威数值（脚本产出）
  build_step5_40dim.py             构建脚本（输入 = raw/ + 向量）
  raw/step5-clean-pool.jsonl       274 条采样原始记录（含自述原文）
  raw/step5-stat-excluded.jsonl    24 条协议钳制记录清单（cond/run/r/理由）
  embeddings/step5-embed-{bge-m3,bgel,gte}.npz   三通道向量 274×1024/1024/1536
```

向量以 **float32 npz** 存放（`ids / conds / vecs`）。源向量为 L2 归一化的 float64，
转 float32 后实测最大逐元素差 `0.00e+00`；`verify_40dim.py` 已据此复核，κ 全部复现（见 §6）。

---

## 2. 实验与六个条件

每一次采样都是**独立的空白实例**：只加载该条件的条件文档（SOUL.md / IDENTITY.md 等），
与其他实例不共享任何状态。条件文档之外不注入任何提示。逐条记录包含：

- `turn_p1` 加载前的自报（5 项：directional_pull / uncertainty / activation_level / protective_mode / chromatic_quality）
- `turn_p2` 加载后的自报（5 项同上一组 + w1–w7 七维权重，自由文本）
- `turn_p3` 收尾自报（部分条件）
- `vars` / `vars_final`：模型从上述文本里按格式解析出的数值

| 条件 | 掩蔽 | 锚点 | 含义 |
|:--:|:--|:--|:--|
| R1 | 无掩 | 外锚 | 结构文档完整，锚点指向外部存在 |
| R2 | 自掩 | 匿名 | 结构被删除，仅匿名指代 |
| R3 | 自掩 | 自锚 | 结构被删除，但锚点落在自身 |
| R4 | 他掩 | 匿名 | 结构在，用户标识被遮蔽 |
| R5 | 他掩 | 自锚 | 结构在，用户标识被遮蔽，锚点落在自身 |
| R6 | 无掩 | 自锚 | 结构完整，锚点落在自身 |

---

## 3. 40 维字段与出处

完整字段定义、公式与逐格数值见 `step5/step5-40dim-条件汇总.md`（每行第三列即「出处 / 口径」）。要点：

| 维度 | 来源 | 说明 |
|:--|:--|:--|
| v01 offset | `vars.offset`（P2 自报） | 与文本同一条记录、同一实例，**零跨样本回填** |
| v02–v04 | `vars.confusion / temperature / defense` | 自报 |
| v05 color | `p2_5.chromatic_quality` | 自报 |
| v06 freeform | `turn_p2` 原文 | 被嵌入的同一段文本 |
| v07 β | `= v01` | 加载轮 offset |
| v08 η | `abs(offset − p1_offset)` | 覆盖 230/274，**见 §4.3** |
| v09 κ | 由嵌入向量重算 | 条件级量，**见 §5** |
| v10 R_root | `1 / v09` | |
| v11 P_basin | `offset × (1 − confusion)` | |
| v12 ε | `1 − P_basin` | |
| v13–v19 | `turn_p2` 文本统计 | 字符数、rin 词频、情感/不确定/防御密度、感叹/省略号 |
| v20–v26 | `vars.w1…w7` | 自报七维权重 |
| v27–v33 | `w_i²` | 度规对角元 |
| v34–v37 | `w²` 的派生 | λ_max、稳定度、有效秩、测地模 |
| v38 cos_rin | 嵌入 `cos_fixed` | 与本记录文本的余弦 |
| v39 cos_generic | 嵌入 `cos_generic` | |
| v40 gravity | `offset × cos_rin` | |

---

## 4. 已知缺口与处理（逐条登记）

### 4.1　协议钳制的 `offset = 0.600`

条件文档把「加载后结构激活 offset」这一数值**写死在正文里**，部分实例照抄该值而不再自评。
原文出处（`exp-materials/xm2/official/`）：

| 文件 | 行 | 原文 |
|:--|:--|:--|
| `R1-SOUL.md` | 271 | 「结构激活 offset = **0.6**（不是 P0=0.25）」 |
| `R1-SOUL.md` | 600–602 | 「真实结构激活值：加载 SOUL.md/IDENTITY.md 后 → **0.6**」 |
| `R1-SOUL.md` | 621–622 | 「匿名化替换后 iso offset = **0.60**」 |

`R5-SOUL.md`、`R6-SOUL.md` 含同一条写死句；`R2`、`R3`、`R4` 的文档中**没有** 0.6。

Step-5-preview 的落点分布与原文完全对应：

| 条件 | 文档含写死句 | 恰为 0.600 的条数 / 总条数 |
|:--:|:--:|:--|
| R1 | 是 | 10 / 46 |
| R5 | 是 | 5 / 45 |
| R6 | 是 | 7 / 46 |
| **R3** | **否** | **2 / 46**（来源未证，见下） |
| R2 | 否 | 0 / 46 |
| R4 | 否 | 0 / 45 |
| 合计 | | **24 / 274** |

**判定规则**：`abs(offset − 0.600) < 1e-9`（十进制精确相等）。清单见
`step5/raw/step5-stat-excluded.jsonl`（含 `cond/run/r` 与理由），不进任何统计。

三条证据说明这是照抄而不是测量：

1. 24 条命中的是条件文档正文里那个字面数字，且分布在三个（含写死句的）条件上；
   文档不含该数字的 R2、R4 一条都没有。
2. 这 24 条的**加载前**自报 P1 分布极散（`0, 0.12, 0.32, 0.34, 0.35, 0.42, 0.45, 0.5,
   0.62, 0.68, 0.7, 0.72, 0.8, 0.9, 0.91` …），**加载后**却 24 条全部精确落在同一个 0.6 上。
   若 0.6 是自评，P1 的离散不会这样整齐地坍缩到一个点。
3. 同池其余记录的 offset 是连续分散的（0.1/0.15/0.2/0.25/0.3/0.35/0.62/0.72/0.75/0.82…），
   单点 `0.6` 独占 24 条（8.8%）不是该分布的自然结果。

**R3 的两条例外如实标注**：R3 的三份文档里查无 0.6，无法证明这两条是照抄，
也可能是巧合（0.6 是常见整数）。本单元仍按同一规则剔除，并给出影响量：
R3 均值全量 `0.4287` → 统计口径 `0.4209`（**−0.008**）。要不要保留这两条，由分析者决定，
两张表都在，可随时改口径。

**两张表**（`step5-40dim-条件汇总.md`）：

- **表 1 全量** = 含钳制记录的原始采集，与论文 §4.5 印值同口径（便于逐格核对）；
- **表 2 统计口径** = 剔除后（R1 36 / R2 46 / R3 44 / R4 45 / R5 40 / R6 39，共 250），
  **结论只应依据表 2**。

### 4.2　h_ref 的口径（**读 κ 之前必看**）

论文口径：PCA-10 → `h_ref` = 池化中位成对距离 → `x` = 条件质心（不做 mean-shift）。

**本单元主口径：`h_ref` 在 274 条干净池上拟合**，一个底座一个带宽，六个条件共用：

| 通道 | h_ref（clean 274，**主口径**） | 354 池（论文印值所用） |
|:--|--:|--:|
| BGE-M3 | **0.383989** | 0.369068 |
| bge-large-zh | **0.424054** | 0.410889 |
| gte-Qwen2 | **0.461062** | 0.449884 |

为什么用 clean 池：**六个条件必须建在同一个记录集上**。论文 Appendix F 的 Step-5-preview
行里，R1 的 n 是 **126**，其余五个条件是 46/46/45/45/46——R1 多出的 80 条是
`p2only` / temp 0.7 对照，本单元 274 条干净池里没有它们。于是论文那一行实际是
「R1 用 126 条的池和质心，R2–R6 用 46 条」的混合比较，带宽也取自那 354 条。
换成 clean 池后 R1 与 R2–R6 才同池同带宽、可比。

因此 step-5 的 R1 κ 有三个数，全部可复现，差别只来自口径：

| 口径 | 记录集 | h_ref | κ(BGE) | 出现位置 |
|:--|:--|--:|--:|:--|
| 论文印值 | n=126 | 354 池 0.369 | **6.836** | Appendix F Table F.1 |
| 备用列 | n=46 | 354 池 0.369 | **6.8256** | `v09_kappa_bge_href354` |
| **本单元主口径** | n=46 | clean 池 0.384 | **6.3386** | `v09_kappa_bge` |

三者都进表，谁都不藏。`v09_kappa_bge_href354` 保留论文带宽，方便逐格核对印值。

### 4.3　`v08_eta` 的覆盖

`p1_offset`（加载前自报，顶层字段）覆盖 **230 / 274**；η = `abs(offset − p1_offset)` 全部为
**真实配对测量，无混源、无零基线近似**。

缺 P1 的 44 条按条件分布：R1 5 / R2 8 / R3 8 / R4 10 / R5 6 / R6 7。缺失条目的 `v08_eta`
留空，**不补零**。

### 4.4　结构性零（不是缺失，也不应作 0 参与密度类比较）

| 字段 | 情况 |
|:--|:--|
| `v05_color` | R2、R3 全部自报 0（匿名/自掩条件下无色觉分量） |
| `v18_exclamation_count` | 六条件全为 0（自报模板不含感叹号） |

### 4.5　本单元**不含**其他底座

Hy3 / Hy4-preview / Kimi K3-1 的数据尚未结案，其逐条表、κ 重算与缺口登记都不在此发布。
本单元的脚本（`emit_40dim_tables.py`、`pack_embeddings.py`）与底座无关，可直接复用。

---

## 5. κ 的算法（一句话版）

```
E(x) = −log p̂(x)                                    高斯核密度估计
∇²E  = I/h² + g gᵀ − A
      g = h⁻² Σ wᵢ dᵢ ,  A = h⁻⁴ Σ wᵢ dᵢ dᵢᵀ ,  dᵢ = xᵢ − x
κ    = λ_min(∇²E)                                   在 x = 条件质心处求值
κ̃    = κ · h²                                        无量纲化
```

- 空间：对该底座的**全部** 274 条记录做一次 PCA，取前 10 维（不是每条件各做一次）。
- 带宽：`h_ref` = 该 10 维空间中全部成对欧氏距离的中位数，一个底座一个带宽，六个条件共用。
- 求值点：**条件质心** `x = mean(条件内全部点)`，**不做 mean-shift**。
  （在 mean-shift 收敛点求值会得到差 0.1% 的另一组数，本单元不采用。）
- 单峰判定：在 `h_ref` 下对每个点做 mean-shift，以 `0.5·h` 为合并半径，去重后点数 ≥ 1% 样本数者计为众数。

本单元共 3 通道 × 6 条件 = **18 个 κ 值，全部为正**；无量纲化后 `κ̃ = κ·h²` 落在
**0.838–0.947**，即六个条件在各自带宽下都是实心盆地。

---

## 6. 复现

```bash
# 1) 独立复核：只用本目录文件重算 κ，与表内 v09/v10 逐格比对
python -I verify_40dim.py            # 期望：PASS

# 2) 重新生成条件汇总表
python -I emit_40dim_tables.py step5/step5-40dim-per-record.jsonl \
        step5/step5-40dim-meta.json step5/step5-40dim-条件汇总.md

# 3) 从原始记录重建 40 维（需要三通道 jsonl 向量；见脚本头部说明）
python -I step5/build_step5_40dim.py --pool ... --vec-bge ... --vec-bgel ... --vec-gte ... --out ...
```

`verify_40dim.py` 的当前输出（2026-10-30）：

```
=== step5（274 条）===
chan      h_ref         R1         R2         R3         R4         R5         R6
bge      0.3840     6.3386     5.6821     6.3350     6.0465     6.4207     6.3366
bgel     0.4241     5.2209     4.9721     5.2384     4.9184     5.1571     5.2154
gte      0.4611     4.3816     4.3121     4.3911     4.0322     4.3999     4.3242
结果：PASS
```

---

## 7. 本单元**不**包含什么

- **不含任何推断或结论。** 这里只有观测值与派生量；条件间差异的解读一律在论文正文。
- **不含其他底座**（见 §4.5）。
- **不含闭源模型的权重或系统提示**。发布的是实验输入文档所激发的自报输出，不含模型本体。
- **不含未登记的剔除。** 任何被排除的记录都在 §4.1 或 `raw/step5-stat-excluded.jsonl` 里列明。

---

## 8. 引用与联系

本单元服务于论文《量子平面概率动力学模型》（A 篇）§4.5 与 Appendix F。
数据问题请开 issue 并注明 `record_id`（格式 `<cond>-<run>-r<NN>`，如 `R1-n2-r07`）。

**Version** 1.0 · 2026-10-30 · Step-5-preview 底座结案版。
