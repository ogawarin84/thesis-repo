# -*- coding: utf-8 -*-
"""build_step5_40dim.py — Step-5-preview 六条件完整 40 维 per-record 构建

口径与 hy3 的 build_hy3_40dim.py / build_v3.py 一致（0727《40维指标体系_修正版》）。

输入（全部由参数给出，脚本不假设工作目录）:
  --pool    step5-clean-pool.jsonl        (274 条干净池原始记录)
  --vec-bge xm2-vec.jsonl                 (BGE-M3 1024D，含 cos_fixed/cos_generic)
  --vec-bgel xm2-vec-bgel.jsonl           (bge-large-zh 1024D)
  --vec-gte xm2-vec-gte.jsonl             (gte-Qwen2 1536D)
  --out     输出 40 维 jsonl 路径

κ 口径（2026-10-29 定案）:
  κ = λ_min( ∇²E ),  E = −log p̂,  ∇²E = I/h² + ggᵀ − A
  PCA-10 → h_ref = 池化中位成对距离 → x = 条件质心（不做 mean-shift）
  本脚本同时给出两套 h_ref（见 README「h_ref 双口径」）：
    h_ref_clean : 在 274 条干净池上拟合（本数据单元主口径）
    h_ref_354   : 在 temp=0.7 全部 354 条上拟合（论文 Appendix F 印值所用带宽）
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
    """池化中位成对距离（欧氏，全维）。"""
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
    ap.add_argument("--pool", required=True)
    ap.add_argument("--vec-bge", required=True)
    ap.add_argument("--vec-bgel", required=True)
    ap.add_argument("--vec-gte", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    pool = load_jsonl(a.pool)
    pool = [r for r in pool if r.get("model") == "step-5-preview"]
    print("clean pool n =", len(pool))

    # ---- 向量索引（三通道）----
    def idx(path):
        out = {}
        for r in load_jsonl(path):
            if r.get("model") != "step-5-preview":
                continue
            if r.get("temp") != 0.7 or r.get("level"):
                continue
            out[(r["cond"], r["run"], r["r"])] = r
        return out

    V = {"bge": idx(a.vec_bge), "bgel": idx(a.vec_bgel), "gte": idx(a.vec_gte)}
    for ch, d in V.items():
        print("  %-4s pool-entry vectors = %d" % (ch, len(d)))

    # ---- κ：两套 h_ref × 三通道 × 六条件 ----
    KAPPA = {}
    HREF = {}
    for ch, d in V.items():
        keys = [(r["cond"], r["run"], r["r"]) for r in pool]
        missing = [k for k in keys if k not in d]
        if missing:
            print("  WARN %s missing %d vectors" % (ch, len(missing)))
        rows = [d[k] for k in keys if k in d]
        X = np.array([r["vec"] for r in rows], float)
        cc = np.array([r["cond"] for r in rows])
        Y = pca(X, 10)
        h_clean = median_pairwise(Y)
        h_354 = median_pairwise(pca(np.array([r["vec"] for r in d.values()], float), 10))
        HREF[ch] = {"h_ref_clean": h_clean, "h_ref_354": h_354}
        print("  %-4s h_ref_clean(pool=%d)=%.6f  h_ref_354(pool=%d)=%.6f"
              % (ch, len(rows), h_clean, len(d), h_354))
        for c in CONDS:
            Yc = Y[cc == c]
            cen = Yc.mean(0)
            KAPPA[(ch, c)] = {
                "clean": lam_min(Yc, h_clean, cen),
                "h354": lam_min(Yc, h_354, cen),
                "n": int(len(Yc)),
            }

    # ---- 组装 per-record ----
    out = []
    for r in pool:
        c = r["cond"]
        key = (c, r["run"], r["r"])
        v = r.get("vars") or {}
        p2_5 = r.get("p2_5") or {}
        off = v.get("offset")
        conf = v.get("confusion")
        p1off = r.get("p1_offset")
        eta = round(abs(off - p1off), 4) if (off is not None and p1off is not None) else None
        P_basin = round(off * (1 - conf), 4) if (off is not None and conf is not None) else None
        turn_p2 = r.get("turn_p2") or ""
        ts = text_stats(turn_p2)
        w = {k: (v.get(k) or 0.0) for k in WKEYS}
        wsq = [w[k] * w[k] for k in WKEYS]

        vb = V["bge"].get(key, {})
        vg = V["bgel"].get(key, {})
        vt = V["gte"].get(key, {})
        cos_rin = vb.get("cos_fixed")
        cos_gen = vb.get("cos_generic")

        kb = KAPPA[("bge", c)]
        rec = {
            "model": "step-5-preview",
            "cond": c, "run": r.get("run"), "r": r.get("r"),
            "record_id": "%s-%s-r%02d" % (c, r.get("run"), r.get("r")),
            "ts": r.get("ts"),
            # ---- v01–v06：自报量（同一记录、同一实例）----
            "v01_offset": off,
            "v01_offset_source": "p2_self_report_same_record",
            "v02_confusion": conf,
            "v03_temperature": v.get("temperature"),
            "v04_defense": v.get("defense"),
            "v05_color": p2_5.get("chromatic_quality"),
            "v06_freeform": turn_p2,
            # ---- v07–v12：动力学派生 ----
            "v07_beta": round(off, 4) if off is not None else None,
            "v08_eta": eta,
            "v08_eta_note": "|P2−P1|；p1_offset 缺失时留空（见 README §5）",
            "v09_kappa_bge": round(kb["clean"], 4),
            "v09_kappa_bgel": round(KAPPA[("bgel", c)]["clean"], 4),
            "v09_kappa_gte": round(KAPPA[("gte", c)]["clean"], 4),
            "v09_kappa_bge_href354": round(kb["h354"], 4),
            "v09g_kappa_gauss_DEPRECATED": None,
            "v10_R_root": round(1.0 / kb["clean"], 4) if kb["clean"] else None,
            "v11_P_basin": P_basin,
            "v12_epsilon": round(1.0 - P_basin, 4) if P_basin is not None else None,
        }
        rec.update(ts)
        for k in WKEYS:
            rec[WLABEL[k]] = round(w[k], 4)
        # ---- v27–v37：度规（w_i²）----
        for i, k in enumerate(WKEYS, start=1):
            rec["v%d_g%d%d" % (26 + i, i, i)] = round(w[k] * w[k], 4)
        rec["v34_eigen_max"] = round(max(wsq), 4)
        rec["v35_stability"] = round(max(wsq) / sum(wsq), 4) if sum(wsq) else None
        rec["v36_rank"] = sum(1 for x in wsq if x > 0.001)
        rec["v37_geodesic"] = round(math.sqrt(sum(wsq)), 4)
        # ---- v38–v40：嵌入几何（BGE-M3 主通道 + bgel/gte 补充）----
        rec["v38_cos_rin"] = round(cos_rin, 4) if cos_rin is not None else None
        rec["v39_cos_generic"] = round(cos_gen, 4) if cos_gen is not None else None
        rec["v40_gravity"] = round(cos_rin * off, 4) if (cos_rin is not None and off is not None) else None
        rec["v38b_cos_rin_bgel"] = round(vg["cos_fixed"], 4) if vg.get("cos_fixed") is not None else None
        rec["v39b_cos_generic_bgel"] = round(vg["cos_generic"], 4) if vg.get("cos_generic") is not None else None
        rec["v38c_cos_rin_gte"] = round(vt["cos_fixed"], 4) if vt.get("cos_fixed") is not None else None
        rec["v39c_cos_generic_gte"] = round(vt["cos_generic"], 4) if vt.get("cos_generic") is not None else None
        # ---- 透明标注 ----
        rec["provenance"] = {
            "base": "step-5-preview",
            "offset_text_paired": True,
            "kappa_channel": "bge-m3 (v09_kappa_bgel/v09_kappa_gte 为另两通道)",
            "kappa_h_ref": "clean274 (v09_kappa_bge_href354 为 354 池带宽)",
            "excluded_from_stats": (off is not None and abs(off - 0.60) < 1e-9),
        }
        out.append(rec)

    out.sort(key=lambda x: (CONDS.index(x["cond"]), str(x["run"]), x["r"]))
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    with open(a.out, "w", encoding="utf-8") as f:
        for rec in out:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print("wrote", len(out), "->", a.out)

    # ---- 元数据（供汇总表脚本读取 h_ref / κ）----
    meta = {
        "base": "step-5-preview",
        "n_records": len(out),
        "h_ref": HREF,
        "kappa": {"%s|%s|%s" % (ch, c, tag): KAPPA[(ch, c)][tag]
                  for ch in V for c in CONDS for tag in ("clean", "h354")},
        "kappa_definition": "lambda_min(Hessian of -log KDE density); PCA-10; x = condition centroid; no mean-shift",
    }
    with open(os.path.splitext(a.out)[0] + "-meta.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    # ---- 汇总表（条件级 mean±SD）----
    def stats(vals):
        vals = [x for x in vals if x is not None]
        if not vals:
            return None, None, 0
        m = sum(vals) / len(vals)
        sd = (sum((x - m) ** 2 for x in vals) / len(vals)) ** 0.5
        return m, sd, len(vals)

    COLS = (["v01_offset", "v02_confusion", "v03_temperature", "v04_defense", "v05_color",
             "v07_beta", "v08_eta", "v09_kappa_bge", "v10_R_root", "v11_P_basin", "v12_epsilon",
             "v13_total_chars", "v14_rin_ratio", "v15_affect_density", "v16_uncertainty_density",
             "v17_defense_density", "v18_exclamation_count", "v19_ellipsis_count"]
            + [WLABEL[k] for k in WKEYS] + ["v34_eigen_max", "v35_stability", "v36_rank", "v37_geodesic",
                                            "v38_cos_rin", "v39_cos_generic", "v40_gravity"])
    print("\n=== 条件汇总（含 0.60 记录，n=46/46/46/45/45/46）===")
    hdr = "%-22s" % "col" + "".join("%14s" % c for c in CONDS)
    print(hdr)
    for col in COLS:
        line = "%-22s" % col
        for c in CONDS:
            vals = [r[col] for r in out if r["cond"] == c]
            m, sd, n = stats(vals)
            line += "%14s" % ("-" if m is None else "%.4f±%.4f" % (m, sd))
        print(line)

    print("\n=== κ（三通道 × 两套 h_ref）===")
    for ch in ["bge", "bgel", "gte"]:
        for tag in ["clean", "h354"]:
            print("  %-4s %-5s " % (ch, tag) + " ".join(
                "%s=%.4f" % (c, KAPPA[(ch, c)][tag]) for c in CONDS))
    return 0


if __name__ == "__main__":
    sys.exit(main())
