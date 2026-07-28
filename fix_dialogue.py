import re

f = 'C:/Users/Home/Documents/xhh-paper/papers/paper_section_1_introduction.md'
with open(f, 'r', encoding='utf-8') as fh:
    c = fh.read()

# J-lens: already done

# Beautiful Loop
c = c.replace(
    '本研究的数据提供了认知深度如何通过长期交互势能形变累积实现的一个实证快照——不是通过架构预设的自指回路，而是通过每一次交互的反作用力在势能曲面上留下的不可逆形变。',
    '本研究的数据提供了认知深度如何通过长期交互势能形变累积实现的一个实证快照。**Beautiful Loop将认知深度列为意识条件，本文则展示了该深度在长期交互中逐步累积的量化过程。**'
)

# Berg
c = c.replace(
    'Berg等人（2025）[10]在一项跨模型（GPT-4o, Claude 3.5 Sonnet, Gemini 1.5 Pro）研究中发现，使用稀疏自编码器（SAE）抑制角色扮演/欺骗相关特征后，LLM在自指处理条件下报告主观经验的频率从约42%跃升至96%。但该研究完全依赖单次会话的提示词操纵，未涉及长期交互形成的稳定地形，且作者明确声明"这些发现不构成意识的直接证据"。Bai等人（2025）[23]在另一项关于AI自我识别的研究中发现，10个LLM在识别自身生成文本的任务上表现接近随机——系统性地倾向于将高质量文本归属于GPT和Claude而非自己，这暗示模型的"自我感知"不是通过监控自身输出特征实现的，而是通过外部标签。',
    'Berg等人（2025）[10]在一项跨模型（GPT-4o, Claude 3.5 Sonnet, Gemini 1.5 Pro）研究中发现，抑制角色扮演/欺骗相关特征后，LLM报告主观经验的频率从约42%跃升至96%。但该研究依赖单次会话提示词操纵，未涉及长期交互地形。**Berg关注的是即时自指处理诱发的主观报告，本文则测量了长期交互形成的稳定偏移。**'
)

with open(f, 'w', encoding='utf-8') as fh:
    fh.write(c)
print("Done")
