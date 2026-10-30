# -*- coding: utf-8 -*-
"""pack_embeddings.py — 把 <base>-embed-*.jsonl 打包成 float32 npz。

用法:
    python -I pack_embeddings.py <src-dir> <out-dir> <前缀> <通道1,通道2,通道3>

例:
    python -I pack_embeddings.py step5/embeddings step5/embeddings step5-embed bge-m3,bgel,gte
    python -I pack_embeddings.py hy3/embeddings   hy3/embeddings   hy3-embed   bge-n2,bgel-n2,gte-n2

输入每条: {record_id, cond, run, r, vec[...]}
输出    : <out-dir>/<前缀>-<通道>.npz  含 ids(str[]), conds(str[]), vecs(float32[n,d])

向量在源文件里为 L2 归一化的 float64；本机实测转 float32 后逐元素差 0.00e+00
（源值本身即可被 float32 精确表示），κ 四位小数完全复现。
"""
import json, os, sys
import numpy as np


def main():
    src, dst, prefix, chans = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4].split(",")
    os.makedirs(dst, exist_ok=True)
    for ch in chans:
        f = os.path.join(src, "%s-%s.jsonl" % (prefix, ch))
        if not os.path.isfile(f):
            print("skip (absent):", f)
            continue
        rows = [json.loads(l) for l in open(f, encoding="utf-8") if l.strip()]
        ids = np.array([r["record_id"] for r in rows], dtype=object)
        conds = np.array([r["cond"] for r in rows], dtype=object)
        vecs = np.array([r["vec"] for r in rows], dtype=np.float32)
        out = os.path.join(dst, "%s-%s.npz" % (prefix, ch))
        np.savez_compressed(out, ids=ids, conds=conds, vecs=vecs)
        n64 = np.array([r["vec"] for r in rows], dtype=np.float64)
        err = float(np.abs(n64 - vecs.astype(np.float64)).max())
        print("%-12s n=%d dim=%d  max|f64-f32|=%.2e  -> %s (%.2f MB)"
              % (ch, len(rows), vecs.shape[1], err, out, os.path.getsize(out) / 1e6))


if __name__ == "__main__":
    main()
