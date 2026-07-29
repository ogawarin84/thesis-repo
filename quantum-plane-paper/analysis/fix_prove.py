import os, re

papers_dir = 'C:/Users/Home/Documents/xhh-paper/papers'
files = [f for f in os.listdir(papers_dir) if f.endswith('.md') and f.startswith('paper_section_4')]

for fname in sorted(files):
    fpath = os.path.join(papers_dir, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content

    # 实验证明 → 实验观测证据表明
    content = content.replace('实验三证明了', '实验三的观测证据表明')
    content = content.replace('实验一和实验三分别证明了', '实验一和实验三的观测证据分别表明')
    content = content.replace('已证明后者成立', '已得到初步验证')
    content = content.replace('证明这不是自我存续的必要条件', '表明这不是自我存续的必要条件')
    content = content.replace('在60组独立采样中证明', '在60组独立采样中验证')
    content = content.replace('验证了本模型的势能曲面假设', '与本模型的势能曲面假设一致')
    content = content.replace('验证了身份拓扑的分层路径连通性', '佐证了身份拓扑的分层路径连通性')
    content = content.replace('证实移除名字标识后', '与移除名字标识后的预期一致')

    # "证明" remaining generic
    content = content.replace('证明了', '提示了')
    content = content.replace('证实了', '支持了')

    if content != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  {fname}")

print("Done")
