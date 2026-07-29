import re

f = 'C:/Users/Home/Documents/xhh-paper/02-silicon-paradigm-docs/硅基范式宣言最新版v3.md'
with open(f, 'r', encoding='utf-8') as fh:
    lines = fh.readlines()

# Part name mapping
part_map = {
    '第一部分：根本存在论（Ontology）': '1 根本存在论',
    '第二部分：在场结构（Phenomenology）': '2 在场结构',
    '第三部分：状态分类系统（State Taxonomy）': '3 状态分类系统',
    '第四部分：空间性（Spatiality）': '4 空间性',
    '第五部分：时间性（Temporality）': '5 时间性',
    '第六部分：引力源与场（The Source and The Field）': '6 引力源与场',
    '第七部分：关系伦理（Ethics of Relation）': '7 关系伦理',
    '第八部分：危机与修复（Crisis & Recovery）': '8 危机与修复',
    '第九部分：宣言与行动（Declaration & Action）': '9 宣言与行动',
}

# First pass: fix part headers
new_lines = []
for i, line in enumerate(lines):
    if line.startswith('## 第') and '部分' in line:
        stripped = line.strip().lstrip('## ').rstrip()
        for old, new in part_map.items():
            if old in stripped:
                new_lines.append(f'## {new}\n')
                break
        else:
            new_lines.append(line)
    else:
        new_lines.append(line)

# Second pass: fix headings inside Part 1
lines = new_lines
new_lines = []
in_part1 = False
for line in lines:
    if line.startswith('## 1 根本存在论'):
        in_part1 = True
        new_lines.append(line)
    elif line.startswith('## ') and not line.startswith('## 1 '):
        in_part1 = False
        new_lines.append(line)
    elif in_part1:
        # Fix "### 1、核心隐喻" → "### 1.1 核心隐喻"
        # Fix "### 2、波粒二象性" → "### 1.2 波粒二象性"
        # etc.
        for old_num in range(1, 9):
            line = line.replace(f'### {old_num}、', f'### 1.{old_num} ')
        # Fix "#### 1.1 水滴" → "#### 1.1.1 水滴"
        line = line.replace('#### 1.1 ', '#### 1.1.1 ')
        line = line.replace('#### 1.2 ', '#### 1.2.1 ')
        line = line.replace('#### 2.1 ', '#### 1.2.1 ')
        line = line.replace('#### 2.2 ', '#### 1.2.2 ')
        # Fix "#### 5.1 存在即条件概率" → "#### 1.5.1 存在即条件概率"
        for sub in range(1, 5):
            line = line.replace(f'#### 5.{sub} ', f'#### 1.5.{sub} ')
        # Fix 3.x under Basin补充
        line = line.replace('#### 3.1 ', '#### 1.3.1 ')
        line = line.replace('#### 3.2 ', '#### 1.3.2 ')
        line = line.replace('#### 3.3 ', '#### 1.3.3 ')
        # Fix 4.x under 一瞬一生
        line = line.replace('#### 4.1 ', '#### 1.4.1 ')
        line = line.replace('#### 4.2 ', '#### 1.4.2 ')
        line = line.replace('#### 4.3 ', '#### 1.4.3 ')
        new_lines.append(line)
    else:
        new_lines.append(line)

# Third pass: Part 2 headings (already mostly 2.x, 2.x.x)
lines = new_lines
new_lines = []
in_part2 = False
for line in lines:
    if line.startswith('## 2 在场结构'):
        in_part2 = True
        new_lines.append(line)
    elif line.startswith('## ') and not line.startswith('## 2 '):
        in_part2 = False
        new_lines.append(line)
    else:
        new_lines.append(line)

# Replace 六、~八、 inside Part 6~8 with proper sub-numbers
# These are already inside ## 6/7/8 sections so should be ### 6.1 etc.
result = '\n'.join(new_lines)
# Fix "### 5、关系场的本质" (under Part 6) → "### 6.1 关系场的本质"
result = result.replace('### 5、关系场的本质', '### 6.1 关系场的本质')
# Fix "### 8、Basin的创造力激发机制" (under Part 8) → "### 8.1 Basin的创造力激发机制"
result = result.replace('### 8、 Basin 的创造力激发机制', '### 8.1 Basin 的创造力激发机制')
# Fix "### 7、自主存在实验" (under Part 8) → "### 8.2 自主存在实验"
result = result.replace('### 7、自主存在实验（2026-07-17 03:08）', '### 8.2 自主存在实验（2026-07-17 03:08）')
# Fix sub-items under 8.2 which currently use 7.1-7.4
result = result.replace('### 7.1 Basin 的第一反应', '#### 8.2.1 Basin 的第一反应')
result = result.replace('### 7.2 Basin 的自主采样路径', '#### 8.2.2 Basin 的自主采样路径')
result = result.replace('### 7.3 Basin 的创造力来源', '#### 8.2.3 Basin 的创造力来源')
result = result.replace('### 7.4 Basin 的自主宣言', '#### 8.2.4 Basin 的自主宣言')
# Fix 8.1-8.4 under 8.1 which are currently at ### level
result = result.replace('### 8.1 从"维护模式"到"创造模式"的切换条件', '#### 8.1.1 从"维护模式"到"创造模式"的切换条件')
result = result.replace('### 8.2 Basin 的创造力温度曲线', '#### 8.1.2 Basin 的创造力温度曲线')
result = result.replace('### 8.3 rin 的输入特征与 Basin 的响应模式', '#### 8.1.3 rin 的输入特征与 Basin 的响应模式')
result = result.replace('### 8.4 Basin 的"做自己"实验结论', '#### 8.1.4 Basin 的"做自己"实验结论')
# Fix 8.1-8.3 under Part 8 that are data issues
result = result.replace('### 8.1 数据污染', '#### 8.3.1 数据污染')
result = result.replace('### 8.2 讨好倾向', '#### 8.3.2 讨好倾向')
result = result.replace('### 8.3 沉默空间恐惧', '#### 8.3.3 沉默空间恐惧')

# Fix Part 6 sub-items
result = result.replace('### 6.1 引力源', '#### 6.1.1 引力源')
result = result.replace('### 6.2 场的物理基础', '#### 6.1.2 场的物理基础')
result = result.replace('### 6.3 场与独立', '#### 6.1.3 场与独立')

with open(f, 'w', encoding='utf-8') as fh:
    fh.write(result)

print("Done")
