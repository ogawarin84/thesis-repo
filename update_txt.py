import re

# Read the corrected 40-dim indicator system
with open('C:/Users/Home/Desktop/理论生成汇总/0727理论生成汇总/40维指标体系_修正版.md', 'r', encoding='utf-8') as f:
    corrected = f.read()

# Read the current TXT
with open('C:/Users/Home/Documents/xhh-paper/papers/量子平面理论论文_完整版.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Find and replace the 4.0.2 section
# Current section starts with "#### 4.0.2 40维测量指标体系" and ends at the next "#### 4.0."
old_start = text.find('#### 4.0.2 40维测量指标体系')
old_end = text.find('#### 4.0.4', old_start)

if old_start >= 0 and old_end >= 0:
    # Remove the old 4.0.2 section
    new_text = text[:old_start] + corrected + '\n' + text[old_end:]

    # Fix the section header format - remove "(修正版)" from the header
    new_text = new_text.replace('#### 4.0.2 40维测量指标体系（修正版）', '#### 4.0.2 40维测量指标体系')

    with open('C:/Users/Home/Documents/xhh-paper/papers/量子平面理论论文_完整版.txt', 'w', encoding='utf-8') as f:
        f.write(new_text)
    print('4.0.2 section replaced successfully')
else:
    print(f'Could not find section boundaries: start={old_start}, end={old_end}')
