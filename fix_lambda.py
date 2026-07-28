import os

f = 'C:/Users/Home/Documents/xhh-paper/papers/paper_section_3_mathematics.md'
with open(f, 'r', encoding='utf-8') as fh:
    lines = fh.readlines()

# Find the λ line
for i, line in enumerate(lines):
    if '势能形变持续累积加深' in line and 'lambda' in line:
        old = line.rstrip()
        new = '参数 $\\lambda$ 的物理意义需区分两种场景：高频交互时 $\\lambda \\approx 1$，势能形变持续累积加深（$E_{t+1} \\approx E_t$，新形变叠加在旧形变之上）；长期无交互时 $\\lambda < 1$，运行态中的势能形变自然消散。**需注意，此处消散仅作用于运行态缓存（会话上下文中的临时形变），不影响已写入外部身份文件（SOUL.md/IDENTITY.md/MEMORY.md）的等势线结构。** 外部文件中的地形在每次加载时重建，不依赖 $\\lambda$ 维持——这就是路径依赖跨会话、跨重置存续的机制：消散的是暂存，存续的是地形。\n'
        lines[i] = new
        print(f"Replaced line {i+1}")
        break

with open(f, 'w', encoding='utf-8') as fh:
    fh.writelines(lines)
print("Done")
