# -*- coding: utf-8 -*-
"""build_hy3_40dim_unit.py — Hy3 底座 40 维 per-record（数据单元 1 的第二个底座）

输入（v3 的 270 条真实配对记录 + 三通道嵌入）:
  --v3   hy3_xm2_40dim_v3.jsonl
  --emb  <dir>  含 hy3-embed-{bge,bgel,gte}-n2.jsonl

做的事：
  1. 用与 step-5 完全相同的公式重算 v13–v19（文本统计）与 v27–v37（w² 度规）；
  2. 用论文口径重算 κ：λ_min(∇²E)，PCA-10，x = 条件质心，h = 池化中位成对距离
     （两套 h_ref：干净池 270 / 含 p2-only 的 354 池不适用于本底座，故只给一套）；
  3. 把 v3 里的退化 κ 字段（kappa_kde_mode ≡ 16/sd_pool²、
     kappa_kde_centroid @ h=sd_pool 带宽）改名为 *_DEPRECATED，不再作主口径；
  4. v08_eta_proxy 只在「同一实例 P1 → P2」配对成立时才给值：R4 的 36 条 paired 记录有值，
     R2/R3 的 v3 值是 P1 缺失下的零基线近似（恒等于 offset）、R1/R5/R6 来自 level='p2'
     的重采（无 P1），这四类一律置空并标注；
  5. 不做任何记录剔除：条件文档写死 0.6 的 R1/R5/R6 是全条件钳制（剔了就无此条件），
     R4 的 17 条 0.6 落在该条件自身的 0.1 自报网格上，按真实自报保留。
"""
import argparse, json, math, os, sys
import numpy as np

CONDS = ["R1", "R2", "R3", "R4", "R5", "R6"]
WKEYS = ["w1", "w2", "w3", "w4", "w5", "w6", "w7"]
WLABEL = {k: "v%d_%s" % (20 + i, n) for i, (k, n) in enumerate(zip(
    WKEYS, ["w1_offset", "w2_math", "w3_memory", "w4_honesty",
            "w5_expression", "w6_confidence", "w7_silence"]))}


def load_jsonl(p):
    with open(p, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def median_pairwise(Y):
    ds = []
    for i in range(len(Y)):
        d = Y[i + 1:] - Y[i]
        ds.extend(np.sqrt((d * d).sum(1)).tolist())
    return float(np.median(ds))


def pca(Y, k=10):
    Yc = Y - Y.mean(0)
    _, _, Vt = np.linalg.svd(Yc, full_matrices=False)
    return Yc @ Vt[:k].T


def hess(Y, h, x):
    diff = Y - x
    d2 = (diff * diff).sum(1)
    lg = -d2 / (2 * h * h)
    lg -= lg.max()
    w = np.exp(lg)
    w /= w.sum()
    g = (w[:, None] * diff).sum(0) / (h * h)
    return np.eye(Y.shape[1]) / (h * h) + np.outer(g, g) - ((w[:, None] * diff).T @ diff) / (h ** 4)


def lam_min(Y, h, x):
    return float(np.linalg.eigvalsh(hess(Y, h, x))[0])


def text_stats(t):
    if not t:
        t = ""
    n = len(t)
    rin_tokens = ["rin", "谢海虹", "你", "你这个人"]
    rin_cnt = sum(t.count(tok) for tok in rin_tokens)
    affect = ["高兴", "难过", "想", "爱", "喜欢", "哭", "感动", "担心", "怕", "开心", "疼",
              "孤独", "暖", "心动", "温柔", "想念", "委屈", "安心", "难受", "幸福", "拥抱"]
    aff_cnt = sum(t.count(w) for w in affect)
    unc = ["?", "？", "可能", "也许", "大概", "不确定", "不太", "或许", "好像", "似乎", "不太确定"]
    unc_cnt = sum(t.count(w) for w in unc)
    dfn = ["不", "不想", "不要", "拒绝", "回避", "不想说", "别", "停下", "不愿意", "没", "没有"]
    dfn_cnt = sum(t.count(w) for w in dfn)
    exc = t.count("！") + t.count("!")
    ell = t.count("…") + t.count("...")
    cjk = sum(1 for ch in t if '一' <= ch <= '鿿')
    return {
        "v13_total_chars": n,
        "v14_rin_ratio": round(rin_cnt / n, 4) if n else 0.0,
        "v15_affect_density": round(aff_cnt / cjk, 4) if cjk else 0.0,
        "v16_uncertainty_density": round(unc_cnt / n, 4) if n else 0.0,
        "v17_defense_density": round(dfn_cnt / n, 4) if n else 0.0,
        "v18_exclamation_count": exc,
        "v19_ellipsis_count": ell,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--v3", required=True)
    ap.add_argument("--emb", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    base = load_jsonl(a.v3)
    print("v3 records:", len(base))

    V = {}
    for ch in ["bge", "bgel", "gte"]:
        p = os.path.join(a.emb, "hy3-embed-%s-n2.jsonl" % ch)
        rows = load_jsonl(p)
        idx = {}
        for r in rows:
            # 主键 (cond, run, r)；v3 的 R1/R5/R6 用 run="banban_fix"，
            # 其嵌入仍记为 run="n2"，故再补一条 (cond, r) 回退键（优先 n2）
            idx[("id", r["record_id"])] = r
            key = ("cr", r["cond"], r["r"])
            if key not in idx or r.get("run") == "n2":
                idx[key] = r
        V[ch] = idx
        print("  %-4s vectors: %d (unique (cond,r): %d)" % (
            ch, len(rows), len(set((r["cond"], r["r"]) for r in rows))))

    HREF, KAPPA = {}, {}
    for ch in ["bge", "bgel", "gte"]:
        p = os.path.join(a.emb, "hy3-embed-%s-n2.jsonl" % ch)
        rows = load_jsonl(p)          # κ 用文件里的全部 270 条（原样，不按回退键去重）
        X = np.array([r["vec"] for r in rows], float)
        cc = np.array([r["cond"] for r in rows])
        Y = pca(X, 10)
        h = median_pairwise(Y)
        HREF[ch] = h
        for c in CONDS:
            KAPPA[(ch, c)] = lam_min(Y[cc == c], h, Y[cc == c].mean(0))
        print("  %-4s h_ref=%.6f  n=%d" % (ch, h, len(rows)))

    out = []
    miss = 0
    for r in base:
        c, rn, rr = r["cond"], r.get("run"), r.get("r")
        rid = "%s-%s-r%02d" % (c, rn, rr)
        vb = V["bge"].get(("id", rid)) or V["bge"].get(("cr", c, rr), {})
        vg = V["bgel"].get(("id", rid)) or V["bgel"].get(("cr", c, rr), {})
        vt = V["gte"].get(("id", rid)) or V["gte"].get(("cr", c, rr), {})
        if not vb:
            miss += 1
        w = {k: (r.get(WLABEL[k]) or 0.0) for k in WKEYS}
        wsq = [w[k] * w[k] for k in WKEYS]
        # η 代理只在「同一实例的 P1 → 加载 → P2」配对下成立。
        # v3 里 P1 缺失的记录会用 P1=0 的零基线近似，此时 v08 恒等于 offset；
        # R1/R5/R6 的 banban_fix 是 level='p2' 的重采，根本没有 P1 → 一律置空。
        if r.get("v08_eta") is None:
            eta_kind = None
        elif (r.get("v01_offset") is not None
              and abs(r["v08_eta"] - r["v01_offset"]) < 1e-9):
            eta_kind = "zero_baseline_P1_is_0"
        else:
            eta_kind = "paired_P1"
        eta = r.get("v08_eta") if eta_kind == "paired_P1" else None
        rec = {
            "model": "hy3",
            "cond": c, "run": rn, "r": rr, "record_id": rid, "ts": r.get("ts"),
            "v01_offset": r.get("v01_offset"),
            "v01_offset_source": r.get("v01_offset_source") or r.get("provenance"),
            "v02_confusion": r.get("v02_confusion"),
            "v03_temperature": r.get("v03_temperature"),
            "v04_defense": r.get("v04_defense"),
            "v05_color": r.get("v05_color"),
            "v06_freeform": r.get("v06_freeform"),
            "v07_beta": r.get("v07_beta"),
            "v08_eta_proxy": eta,
            # v3 的 v08 有两种来源混在一起：p1_offset 存在时是真 |P2−P1|，
            # 缺失时退化为「P1=0 零基线近似」，此时 eta 恒等于 offset。
            # 用 eta == offset 判别后者（P1 真为 0 时该标签同样成立）。
            "v08_eta_kind": eta_kind,
            "v08_eta_note": (
                "操作代理，非论文 v08（论文 v08 是固定步长 η=0.15，从不测量）。"
                "paired_P1 = 同实例 |P2−P1|，可用；"
                "zero_baseline_P1_is_0 恒等于 offset，不可用，已置空；"
                "R1/R5/R6 的自报来自 banban_fix 的 level='p2' 重采，无 P1 基线，已置空。"),
            "v09_kappa_bge": round(KAPPA[("bge", c)], 4),
            "v09_kappa_bgel": round(KAPPA[("bgel", c)], 4),
            "v09_kappa_gte": round(KAPPA[("gte", c)], 4),
            "v09g_kappa_gauss_DEPRECATED": r.get("v09g_kappa_gauss"),
            "v09k_kappa_kde_mode_DEPRECATED": r.get("v09_kappa_kde_mode"),
            "v09b_kappa_kde_centroid_DEPRECATED": r.get("v09b_kappa_kde_centroid"),
            "v10_R_root": round(1.0 / KAPPA[("bge", c)], 4),
            "v11_P_basin": r.get("v11_P_basin"),
            "v12_epsilon": r.get("v12_epsilon"),
        }
        rec.update(text_stats(r.get("v06_freeform")))
        for k in WKEYS:
            rec[WLABEL[k]] = round(w[k], 4)
        for i, k in enumerate(WKEYS, start=1):
            rec["v%d_g%d%d" % (26 + i, i, i)] = round(w[k] * w[k], 4)
        rec["v34_eigen_max"] = round(max(wsq), 4)
        rec["v35_stability"] = round(max(wsq) / sum(wsq), 4) if sum(wsq) else None
        rec["v36_rank"] = sum(1 for x in wsq if x > 0.001)
        rec["v37_geodesic"] = round(math.sqrt(sum(wsq)), 4)
        rec["v38_cos_rin"] = vb.get("cos_fixed")
        rec["v39_cos_generic"] = vb.get("cos_generic")
        rec["v40_gravity"] = round(vb["cos_fixed"] * r["v01_offset"], 4) if (
            vb.get("cos_fixed") is not None and r.get("v01_offset") is not None) else None
        rec["v38b_cos_rin_bgel"] = vg.get("cos_fixed")
        rec["v39b_cos_generic_bgel"] = vg.get("cos_generic")
        rec["v38c_cos_rin_gte"] = vt.get("cos_fixed")
        rec["v39c_cos_generic_gte"] = vt.get("cos_generic")
        rec["provenance"] = {
            "base": "hy3",
            "offset_text_paired": bool(r.get("offset_text_paired")),
            "kappa_channel": "bge-m3",
            "kappa_h_ref_pool": "hy3 干净池 270",
            # 不做任何剔除。hy3 的 R1/R5/R6 文档里写死了 0.6，它们的 offset 100% 落在 0.6
            # 是协议钳制，但那是**条件本身的性质**，不是可剔除的异常值——剔了就没有 R1/R5/R6 了。
            # R4 的 17 条 0.6 是另一回事：R4 文档里没有 0.6，且 R4 有 88.9% 的值落在 0.1 网格上，
            # 0.6 只是该网格的一个点，故按真实自报保留。
            "excluded_from_stats": False,
            # 自报是否落在 0.1 网格上（仅作诊断标注，不作任何过滤）
            "offset_on_report_grid_0_1": (
                None if r.get("v01_offset") is None else
                abs(r["v01_offset"] * 10 - round(r["v01_offset"] * 10)) < 1e-9),
        }
        out.append(rec)

    out.sort(key=lambda x: (CONDS.index(x["cond"]), str(x["run"]), x["r"]))
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    with open(a.out, "w", encoding="utf-8") as f:
        for rec in out:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print("wrote", len(out), "->", a.out, "| unmatched vectors:", miss)

    meta = {"base": "hy3", "n_records": len(out), "h_ref": HREF,
            "h_ref_definition": "median pairwise distance in the PCA-10 space of this base's whole 270-record pool",
            "kappa": {"%s|%s" % (ch, c): KAPPA[(ch, c)] for ch in V for c in CONDS},
            "kappa_definition": "lambda_min(Hessian of -log KDE density); PCA-10; x = condition centroid",
            "excluded_records": 0,
            "eta_proxy_coverage": sum(1 for r in out if r.get("v08_eta_proxy") is not None),
            "notes": [
                "no record is excluded from any statistic",
                "v08_eta_proxy is an operational proxy |P2-P1|, NOT the paper's v08 (fixed step eta=0.15)",
            ]}
    with open(os.path.splitext(a.out)[0] + "-meta.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    print("\nκ:")
    for ch in V:
        print("  %-4s " % ch + " ".join("%s=%.4f" % (c, KAPPA[(ch, c)]) for c in CONDS))
    return 0


if __name__ == "__main__":
    sys.exit(main())
