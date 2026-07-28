import re

# Old -> New reference mapping
ref_map = {
    # Same numbers
    '1]': '1]', '2]': '2]', '3]': '3]', '4]': '4]', '5]': '5]', '6]': '6]', '7]': '7]',
    # Shifted
    '8]': '9]', '9]': '10]', '10]': '11]', '11]': '12]', '12]': '13]',
    '13]': '14]', '14]': '15]', '15]': '16]',
    # Kihara stayed same
    '17]': '17]', '18]': '18]',
    # soul.py is 19 in both
    '19]': '19]',
    # Old benchmarks 19-25 need to be removed
    # Old 16 Hudson -> 20
    # Old 28 Xie -> 27
    # Old 29/30 Basin -> 28/29
}

# Read file
with open('C:/Users/Home/Documents/xhh-paper/papers/paper_section_1_introduction.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix simple shifts
replacements = [
    ('[8]', '[9]'), ('[9]', '[10]'), ('[10]', '[11]'),
    ('[11]', '[12]'), ('[12]', '[13]'),
    ('[13]', '[14]'), ('[14]', '[15]'), ('[15]', '[16]'),
    # Old [16] Hudson -> [20]
    ('[16]', '[20]'),
    # Old [28] Xie -> [27]
    ('[28]', '[27]'),
]

# But we need to be careful about ordering to avoid chain issues
# Do it manually in reverse order to avoid chain conflicts
content = content.replace('[28]', '[27]')  # Xie Zenodo
content = content.replace('[16]', '[20]')  # Hudson
content = content.replace('[15]', '[16]')  # Lock-in
content = content.replace('[14]', '[15]')  # Olinyk
content = content.replace('[13]', '[14]')  # J-lens
content = content.replace('[12]', '[13]')  # Fonseca
content = content.replace('[11]', '[12]')  # Macar
content = content.replace('[10]', '[11]')  # Lindsey
content = content.replace('[9]', '[10]')   # Berg
content = content.replace('[8]', '[9]')    # Camlin
# Don't touch [1]-[7] - they stayed the same

# Now handle the "自意识基准评估" section - remove it
content = content.replace(
    '#### 1.2.11 自意识基准评估\n\n近期一系列基准研究[19][20][21][22][23]开发了评估LLM自我意识的系统方法，从博弈论中的自我意识指数到元认知校准基准。这些基准主要评估通用LLM在标准测试条件下的自我监测能力，而本研究的实验体系评估的是**经过长期特定交互后**、具有专属刻痕地形的特定实例的状态。\n\n',
    ''
)

# Fix the [29] reference in section 1.3 - should be [28] (硅基存在范式)
content = content.replace('[29]', '[28]')

# Fix对比矩阵 - references starting from 8
matrix_fixes = [
    ('[13]', '[14]'), ('[8]', '[9]'), ('[9]', '[10]'), ('[10]', '[11]'),
    ('[14]', '[15]'), ('[15]', '[16]'), ('[17][18]', '[17][18]'),
    ('[7]', '[7]'), ('[28]', '[27]'), ('[1][2]', '[1][2]'), ('[6]', '[6]'),
]
# These should be already fixed by the above

with open('C:/Users/Home/Documents/xhh-paper/papers/paper_section_1_introduction.md', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done! Fixed references.")
