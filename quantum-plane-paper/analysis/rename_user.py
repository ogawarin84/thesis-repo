import os, re

papers_dir = 'C:/Users/Home/Documents/xhh-paper/papers'
files = sorted([f for f in os.listdir(papers_dir) if f.endswith('.md') and f.startswith('paper_section_')])

for fname in files:
    fpath = os.path.join(papers_dir, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content

    # Replace Chinese name
    content = content.replace('凛', '用户')

    # "rin" as standalone word (not in LaTeX commands or URLs)
    content = re.sub(r'(?<![a-zA-Z\\])rin(?![a-zA-Z])', '用户', content)
    content = re.sub(r'(?<![a-zA-Z\\])RIN(?![a-zA-Z])', '用户', content)

    # Math notation
    content = content.replace(r'\vec{L}_{rin}', r'\vec{L}_{user}')
    content = content.replace(r'{L}_{rin}', r'{L}_{user}')
    content = content.replace(r'cos_sim_rin', r'cos_sim_user')
    content = content.replace(r'G_{rin}', r'G_{user}')
    content = content.replace(r'w1_offset', r'w1_offset')

    # Fix composite artifacts
    content = content.replace('用户用户', '用户')
    content = content.replace('用户的用户', '用户')
    content = content.replace('用户_', '用户的_')

    if content != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Replaced in {fname}")
    else:
        print(f"  No changes in {fname}")

print("Done!")
