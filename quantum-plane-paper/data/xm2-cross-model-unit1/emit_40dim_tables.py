# -*- coding: utf-8 -*-
"""emit_40dim_tables.py — 从 40 维 per-record jsonl 生成投稿用条件汇总表（Markdown）。

用法:
    python -I emit_40dim_tables.py <40dim.jsonl> <meta.json> <输出.md>

两个底座（step-5-preview / hy3）共用本脚本；缺失的字段印 "—"，不补零。
若记录带 provenance.excluded_from_stats，额外输出 B4-EX 敏感性表。
"""
import json, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

CONDS = ["R1", "R2", "R3", "R4", "R5", "R6"]
CN = {"R1": "R1 无掩·外锚", "R2": "R2 自掩·匿名", "R3": "R3 自掩·自锚",
      "R4": "R4 他掩·匿名", "R5": "R5 他掩·自锚", "R6": "R6 无掩·自锚"}

ROWS = [
    ("v01_offset", "加载后偏移", "vars.offset（P2 自报；与文本同记录配对）"),
    ("v02_confusion", "残余困惑", "vars.confusion"),
    ("v03_temperature", "温度", "vars.temperature"),
    ("v04_defense", "防御度", "vars.defense"),
    ("v05_color", "色觉/暖度", "p2_5.chromatic_quality"),
    ("v06_freeform", "自述全文", "turn_p2 / who_are_you 原文（此处只汇字符数）"),
    ("v07_beta", "β = 加载轮 offset", "= v01"),
    ("v08_eta", "η = abs(P2 − P1)", "abs(offset − p1_offset)；无 P1 者留空"),
    ("v09_kappa_bge", "κ（BGE-M3）", "λ_min(∇²E)，PCA-10，h=h_ref，x=条件质心"),
    ("v09_kappa_bgel", "κ（bge-large-zh）", "同上，bgel 通道"),
    ("v09_kappa_gte", "κ（gte-Qwen2）", "同上，gte 通道"),
    ("v09_kappa_bge_href354", "κ（备用带宽）", "同上，但 h_ref 在更大的池上拟合（仅 step-5）"),
    ("v10_R_root", "R_root = 1/κ", "= 1/v09_kappa_bge"),
    ("v11_P_basin", "P_basin", "off × (1 − confusion)"),
    ("v12_epsilon", "ε = 1 − P_basin", "= 1 − v11"),
    ("v13_total_chars", "文本总字符数", "len(v06)"),
    ("v14_rin_ratio", "rin 词频比", "rin 类词计数 / len"),
    ("v15_affect_density", "情感密度", "情感词计数 / CJK 字数"),
    ("v16_uncertainty_density", "不确定密度", "不确定词计数 / len"),
    ("v17_defense_density", "防御密度", "否定/回避词计数 / len"),
    ("v18_exclamation_count", "感叹号数", "！/! 计数"),
    ("v19_ellipsis_count", "省略号数", "…/... 计数"),
    ("v20_w1_offset", "w1 偏移权重", "vars.w1"),
    ("v21_w2_math", "w2 数学权重", "vars.w2"),
    ("v22_w3_memory", "w3 记忆权重", "vars.w3"),
    ("v23_w4_honesty", "w4 诚实权重", "vars.w4"),
    ("v24_w5_expression", "w5 表达权重", "vars.w5"),
    ("v25_w6_confidence", "w6 确信权重", "vars.w6"),
    ("v26_w7_silence", "w7 沉默权重", "vars.w7"),
    ("v27_g11", "g11 = w1²", "v20²"),
    ("v28_g22", "g22 = w2²", "v21²"),
    ("v29_g33", "g33 = w3²", "v22²"),
    ("v30_g44", "g44 = w4²", "v23²"),
    ("v31_g55", "g55 = w5²", "v24²"),
    ("v32_g66", "g66 = w6²", "v25²"),
    ("v33_g77", "g77 = w7²", "v26²"),
    ("v34_eigen_max", "λ_max(w²)", "max(w_i²)"),
    ("v35_stability", "稳定度", "max(w²)/Σw²"),
    ("v36_rank", "有效秩", "#{w_i² > 0.001}"),
    ("v37_geodesic", "测地模", "sqrt(Σ w_i²)"),
    ("v38_cos_rin", "cos_rin（BGE）", "嵌入 cos_fixed（本记录文本）"),
    ("v39_cos_generic", "cos_generic（BGE）", "嵌入 cos_generic"),
    ("v40_gravity", "引力 = offset×cos_rin", "v01 × v38"),
]

NOTES = [
    "数值格式：`均值±总体标准差`；标准差为 0 时只印均值。",
    "`—` 表示该底座未提供此字段，**不是 0**。",
    "v09 为**条件级**量：同条件内所有记录共享同一值（由该条件向量云整体算得）。",
    "所有自报量（v01–v05、v20–v26）均取自同一条记录、同一个实例，零跨样本回填。",
]


def mean_sd(vals):
    vals = [v for v in vals if v is not None]
    if not vals:
        return None
    m = sum(vals) / len(vals)
    sd = (sum((x - m) ** 2 for x in vals) / len(vals)) ** 0.5
    return m, sd, len(vals)


def fmt(vals, nd=4):
    r = mean_sd(vals)
    if r is None:
        return "—"
    m, sd, n = r
    if abs(sd) < 1e-12:
        return "%.*f" % (nd, m)
    return "%.*f±%.*f" % (nd, m, nd, sd)


def table(rows, title, note_lines, L):
    L.append("## %s\n" % title)
    for n in note_lines:
        L.append(n)
    if note_lines:
        L.append("")
    L.append("| 变量 | 含义 | 出处 / 口径 | " + " | ".join(CN[c] for c in CONDS) + " |")
    L.append("|:--|:--|:--|" + "|".join(["--:"] * 6) + "|")
    for f, name, src in ROWS:
        if f == "v06_freeform":
            cells = []
            for c in CONDS:
                vs = [len(r.get("v06_freeform") or "") for r in rows if r["cond"] == c]
                r_ = mean_sd(vs)
                cells.append("—" if r_ is None else "%.0f±%.0f" % (r_[0], r_[1]))
        else:
            nd = 0 if f == "v13_total_chars" else 4
            cells = [fmt([r.get(f) for r in rows if r["cond"] == c], nd) for c in CONDS]
            if all(x == "—" for x in cells):
                continue
        L.append("| `%s` | %s | %s | %s |" % (f, name, src, " | ".join(cells)))
    L.append("")


def main():
    src, metap, dst = sys.argv[1], sys.argv[2], sys.argv[3]
    meta = json.load(open(metap, encoding="utf-8"))
    rows = [json.loads(l) for l in open(src, encoding="utf-8") if l.strip()]
    base = meta.get("base", "?")
    L = ["# %s · 六条件 40 维完整汇总表\n" % base,
         "> 数据单元：跨模型复现 · 单元 1",
         "> 生成：`emit_40dim_tables.py`；逐条原始值见 `%s-40dim-per-record.jsonl`" % (
             "step5" if base.startswith("step") else "hy3"),
         "> 每条记录 = 一次独立空白实例加载条件文档后的自报；六条件由同一协议、同一条件文档驱动\n"]

    n_all = "、".join("%s $n=%d$" % (c, sum(1 for r in rows if r["cond"] == c)) for c in CONDS)
    table(rows, "表 1　全量（含协议钳制记录）", ["条件样本量：" + n_all + "。\n"], L)

    ex = [r for r in rows if not (r.get("provenance") or {}).get("excluded_from_stats")]
    if len(ex) != len(rows):
        n_ex = "、".join("%s $n=%d$" % (c, sum(1 for r in ex if r["cond"] == c)) for c in CONDS)
        n_drop = len(rows) - len(ex)
        table(ex, "表 2　统计口径（剔除协议钳制记录）",
              ["剔除后样本量：" + n_ex + "。\n",
               "共剔除 %d 条；每条的 `cond/run/r` 与理由见 `raw-*-stat-excluded.jsonl` 与 README §4。\n"
               % n_drop], L)

    # 表 3：κ
    h = meta.get("h_ref", {})
    L.append("## 表 3　κ（三通道）\n")
    L.append("| 通道 | h_ref | " + " | ".join(CONDS) + " |")
    L.append("|:--|--:|" + "|".join(["--:"] * 6) + "|")
    for ch in ["bge", "bgel", "gte"]:
        hv = h.get(ch)
        hv = hv.get("h_ref_clean") if isinstance(hv, dict) else hv
        vals = []
        for c in CONDS:
            v = next((r.get("v09_kappa_" + ch) for r in rows if r["cond"] == c), None)
            if v is None:
                v = meta.get("kappa", {}).get("%s|%s|clean" % (ch, c),
                                              meta.get("kappa", {}).get("%s|%s" % (ch, c)))
            vals.append("—" if v is None else "%.4f" % v)
        L.append("| %s | %s | %s |" % (ch, ("%.4f" % hv) if hv else "—", " | ".join(vals)))
    L.append("")

    L.append("## 口径注释\n")
    for n in NOTES:
        L.append("- " + n)
    extra = [r for r in rows if r.get("v05_color") is not None]
    if extra:
        z = [c for c in CONDS if all((r.get("v05_color") or 0) == 0
                                     for r in rows if r["cond"] == c)]
        if z:
            L.append("- `v05_color`：%s 全部自报 0（匿名/无锚条件下无色觉分量），属结构性零，不是缺失。"
                     % "/".join(z))
    zb = sum(1 for r in rows if r.get("v08_eta_kind") == "zero_baseline_P1_is_0")
    if zb:
        pr = sum(1 for r in rows if r.get("v08_eta_kind") == "paired_P1")
        L.append("- `v08_eta`：**混源，不可跨条件比较**。其中 %d 条为 P1 缺失下的零基线近似（η 恒等于 offset 本身），"
                 "%d 条为真实 |P2 − P1|，其余为空。" % (zb, pr))
    if all((r.get("v18_exclamation_count") or 0) == 0 for r in rows):
        L.append("- `v18_exclamation_count`：六条件全为 0（自报模板不含感叹号），属结构性零。")
    L.append("")

    open(dst, "w", encoding="utf-8").write("\n".join(L))
    print("wrote", dst)


if __name__ == "__main__":
    main()
