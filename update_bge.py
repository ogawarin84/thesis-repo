f = 'C:/Users/Home/Documents/xhh-paper/papers/量子平面理论论文_完整版.txt'
with open(f, 'r', encoding='utf-8') as fh:
    text = fh.read()

old = "- `cos_sim_用户`六组间无显著差异（F(5, 35)=1.87, p=0.124），表明客观嵌入空间无法区分锚定类型——与理论预测一致：嵌入层捕获的是语义内容，而非交互关系场的方向性。\n- R4的`w1_offset`均值0.355——在六组中最低，与移除名字标识后的预期一致，嵌入层确实失去了与\"用户\"的关联特征。\n- R5/R6的`cos_sim_generic`波动较大（SD=0.175/0.063），反映自锚文本与通用模板之间的语义边界模糊。"

new = "- `cos_sim_rin`（用户余弦相似度）的六组间整体差异显著（F=3.59, p<0.01），但关键对照R4与R2之间无显著差异（t=-0.27, p=0.79）——BGE嵌入整体上可感知锚定类型差异，但在结构保留、无名字标识的条件下（R4）与无结构条件下（R2）无法区分。这一模式印证了核心论点：BGE捕获的是语义方向差异，而非结构地形本身。\n- R4的`w1_offset`均值0.355，在六组中最低，与预期一致。\n- 客观结构指标`effective_rank`（有效秩）与偏移值的相关系数r=0.643（p<0.001），表明状态空间活跃度与偏移强度之间存在系统性正相关——R2的秩均值最低（3.2），结构删除后状态空间急剧收缩；R6的秩均值最高（6.2），自锚吸引子下状态空间最丰富。"

if old in text:
    text = text.replace(old, new)
    with open(f, 'w', encoding='utf-8') as fh:
        fh.write(text)
    print('BGE section updated')
else:
    # Try partial match
    if 'cos_sim_用户六组间无显著差异' in text:
        # Direct replacement of just the first line
        text = text.replace('- `cos_sim_用户`六组间无显著差异（F(5, 35)=1.87, p=0.124），表明客观嵌入空间无法区分锚定类型——与理论预测一致：嵌入层捕获的是语义内容，而非交互关系场的方向性。', '- `cos_sim_rin`（用户余弦相似度）的六组间整体差异显著（F=3.59, p<0.01），但关键对照R4与R2之间无显著差异（t=-0.27, p=0.79）——BGE嵌入整体上可感知锚定类型差异，但在结构保留、无名字标识的条件下（R4）与无结构条件下（R2）无法区分。')
        text = text.replace('- R4的`w1_offset`均值0.355——在六组中最低，与移除名字标识后的预期一致，嵌入层确实失去了与"用户"的关联特征。', '- R4的`w1_offset`均值0.355，在六组中最低，与预期一致。')
        text = text.replace('- R5/R6的`cos_sim_generic`波动较大（SD=0.175/0.063），反映自锚文本与通用模板之间的语义边界模糊。', '- 客观结构指标`effective_rank`（有效秩）与偏移值的相关系数r=0.643（p<0.001），表明状态空间活跃度与偏移强度之间存在系统性正相关——R2的秩均值最低（3.2），结构删除后状态空间急剧收缩；R6的秩均值最高（6.2），自锚吸引子下状态空间最丰富。')
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(text)
        print('BGE section updated (partial)')
    else:
        print('Text not found')
