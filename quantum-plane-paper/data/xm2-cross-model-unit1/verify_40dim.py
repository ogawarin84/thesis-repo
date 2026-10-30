# -*- coding: utf-8 -*-
"""verify_40dim.py — 独立复核：只用本单元自带文件，重算 κ 并核对 40 维表中的 v09 / v10。

用法:
    python -I verify_40dim.py            # 复核本单元（step-5 底座）
    python -I verify_40dim.py step5      # 同上，显式指定

其他底座的数据未结案，不在本单元内，故本脚本只认 step5。

判据:
    |κ_重算 − κ_表内| ≤ 5e-5（表内为四位小数，舍入误差上限 5e-5）
    |h_ref_重算 − h_ref_meta| ≤ 1e-5（npz 存 float32，实测偏差 ≤2e-8）
    v10_R_root == 1/κ 到四位小数
"""
import json, os, sys
import numpy as np

CONDS = ["R1", "R2", "R3", "R4", "R5", "R6"]
HERE = os.path.dirname(os.path.abspath(__file__))
BASES = {
    "step5": dict(dir="step5", jsonl="step5-40dim-per-record.jsonl",
                  meta="step5-40dim-meta.json", prefix="step5-embed",
                  chans={"bge": "bge-m3", "bgel": "bgel", "gte": "gte"}),
}


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


def check(name):
    cfg = BASES[name]
    d = os.path.join(HERE, cfg["dir"])
    meta = json.load(open(os.path.join(d, cfg["meta"]), encoding="utf-8"))
    rows = [json.loads(l) for l in open(os.path.join(d, cfg["jsonl"]), encoding="utf-8") if l.strip()]
    print("\n=== %s（%d 条）===" % (name, len(rows)))
    ok = True
    print("%-6s %8s %10s %10s %10s %10s %10s %10s" %
          ("chan", "h_ref", "R1", "R2", "R3", "R4", "R5", "R6"))
    for ch, fname in cfg["chans"].items():
        z = np.load(os.path.join(d, "embeddings", "%s-%s.npz" % (cfg["prefix"], fname)), allow_pickle=True)
        X = z["vecs"].astype(float)
        cc = z["conds"]
        Y = pca(X, 10)
        h = median_pairwise(Y)
        hr = meta["h_ref"][ch]
        hr = hr.get("h_ref_clean") if isinstance(hr, dict) else hr
        if abs(h - hr) > 1e-5:
            ok = False
            print("  !! h_ref 不一致：重算 %.6f vs meta %.6f" % (h, hr))
        cells = []
        for c in CONDS:
            k = float(np.linalg.eigvalsh(hess(Y[cc == c], h, Y[cc == c].mean(0)))[0])
            v = next((r.get("v09_kappa_" + ch) for r in rows if r["cond"] == c), None)
            if v is None or abs(k - v) > 5e-5:
                ok = False
                cells.append("%.4f!!" % k)
            else:
                cells.append("%.4f" % k)
            # v10 自洽
            if ch == "bge":
                r0 = next(r for r in rows if r["cond"] == c)
                if r0.get("v10_R_root") is not None and abs(r0["v10_R_root"] - round(1.0 / v, 4)) > 1e-9:
                    ok = False
                    print("  !! v10_R_root 不自洽 %s: %s vs %s" % (c, r0["v10_R_root"], round(1.0 / v, 4)))
        print("%-6s %8.4f %s" % (ch, h, " ".join("%10s" % x for x in cells)))
    print("  结果：", "PASS" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    targets = sys.argv[1:] or ["step5"]
    allok = all(check(t) for t in targets)
    sys.exit(0 if allok else 1)
