import os, re

papers_dir = 'C:/Users/Home/Documents/xhh-paper/papers'
files = [f for f in os.listdir(papers_dir) if f.endswith('.md') and f.startswith('paper_section_')]
files += [f for f in os.listdir(papers_dir) if f in ('paper_abstract.md', 'paper_references.md', 'paper_appendix.md')]

for fname in sorted(files):
    fpath = os.path.join(papers_dir, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content

    # 1. Visual metaphors → correct terms
    content = content.replace('凿刻力度', '势能修正步长')
    content = content.replace('凿刻', '势能修正')
    content = content.replace('冷雾基底', '中性网格基底')
    content = content.replace('冷雾', '中性')

    # 2. "刻痕" → contextual replacement
    # In visual descriptions: replace with 等势线偏移
    content = content.replace('刻痕不是记忆', '势能形变不是记忆')
    content = content.replace('刻痕结构', '势能形变结构')
    content = content.replace('刻痕地形', '势能形变地形')
    content = content.replace('刻痕累积', '势能形变累积')
    content = content.replace('刻痕深度', '等势线锐利度')
    content = content.replace('刻痕动力学', '势能形变动力学')
    content = content.replace('刻痕更新', '势能形变更新')
    content = content.replace('刻痕自然衰减', '势能形变自然衰减')
    content = content.replace('刻痕仍在', '势能形变仍在')

    # Remaining generic "刻痕" → "势能形变"
    content = content.replace('刻痕', '势能形变')

    # Fix double replacements
    content = content.replace('势能形变不是记忆', '势能形变不是记忆')
    content = content.replace('势能形变势能形变', '势能形变')

    if content != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        changes = sum(1 for a, b in zip(original, content) if a != b)
        print(f"  {fname}: updated")
    else:
        print(f"  {fname}: no changes")

print("Done!")
