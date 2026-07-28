import os, re

papers_dir = 'C:/Users/Home/Documents/xhh-paper/papers'
files = [f for f in os.listdir(papers_dir) if f.endswith('.md') and f.startswith('paper_section_')]
files += [f for f in os.listdir(papers_dir) if f in ('paper_abstract.md', 'paper_references.md', 'paper_appendix.md')]
files += ['量子海平面论文_完整版.md', '量子海平面论文_完整版.txt']

for fname in sorted(files):
    fpath = os.path.join(papers_dir, fname)
    try:
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        continue
    original = content

    # Model name
    content = content.replace('量子海平面', '量子平面')

    # Structural terms - "海平面" as base level reference
    content = content.replace('海平面基底', '平面基底')
    content = content.replace('海平面网格', '平面网格')
    content = content.replace('海平面场域', '场域')

    # Layer names - remove "海面"
    content = content.replace('海面与上空（活性交互域）', '上层活性交互域')
    content = content.replace('海面之下（沉默空间基底）', '下层沉默空间基底')
    content = content.replace('海面之上', '上层')
    content = content.replace('海面镜面', '基底')
    content = content.replace('海面产生可观测的结构化响应', '表面产生可观测的结构化响应')
    content = content.replace('海面出现可观测的结构化响应', '表面出现可观测的结构化响应')

    if content != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        changes = sum(1 for a, b in zip(original, content) if a != b)
        print(f"  {fname}: updated")
    else:
        print(f"  {fname}: no changes")

print("Done!")
