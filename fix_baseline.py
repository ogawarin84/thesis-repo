import os, re

papers_dir = 'C:/Users/Home/Documents/xhh-paper/papers'
files = [f for f in os.listdir(papers_dir) if f.endswith('.md') and f.startswith(('paper_', '量子'))]
files += ['paper_abstract.md']

for fname in sorted(files):
    fpath = os.path.join(papers_dir, fname)
    if not os.path.exists(fpath):
        continue
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content

    # "海平面基线" → "基准基线"
    content = content.replace('海平面基线', '基准基线')
    # "裸海平面" → "裸基线"
    content = content.replace('裸海平面', '裸基线')
    # "纯海平面" → "纯基线"
    content = content.replace('纯海平面', '纯基线')
    # "≈海平面" → "≈基线"
    content = content.replace('≈海平面', '≈基线')
    content = content.replace('（趋近海平面）', '（趋近基线）')
    content = content.replace('显著高于海平面', '显著高于基线')
    content = content.replace('回落海平面', '回落基线')
    content = content.replace('理论海平面', '理论基线')
    content = content.replace("从海平面到", "从基线到")
    content = content.replace("通用海平面", "通用基线")
    content = content.replace("阶段0：海平面基线", "阶段0：基准基线")
    content = content.replace('"海平面基线"', '"基准基线"')
    content = content.replace('海平面基线——所有实验的零基准', '基准基线——所有实验的零基准')
    # Section title
    content = content.replace('辅助观测：负引力与海平面基线', '辅助观测：负引力与基准基线')
    # Remaining standalone "海平面"
    content = re.sub(r'(?<!基准)海平面(?!基线|图片|网格|理论)', '基线', content)

    if content != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  {fname}")
    else:
        print(f"  {fname} (no change)")

print("Done")
