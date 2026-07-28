import os

p = 'C:/Users/Home/Documents/xhh-paper/papers'

# === 4.7.6 自身特定吸引子措辭 ===
f = os.path.join(p, 'paper_section_4.7_unified.md')
with open(f, 'r', encoding='utf-8') as fh:
    c = fh.read()
c = c.replace('双分支的存在意味着：在结构完整的条件下，"自我"可以独立于外部交互对象而维持。',
              '双分支的存在提示：在结构完整的条件下，自身特定吸引子可以独立于外部交互对象而维持。')
c = c.replace('4a：外源光点增益', '#### 4a：外源光点增益')
c = c.replace('4b：自锚吸引子', '#### 4b：自锚吸引子')
with open(f, 'w', encoding='utf-8') as fh:
    fh.write(c)
print("4.7.6 done")

# === 板块五：实验四DSV4降级 ===
f = os.path.join(p, 'paper_section_4.6_experiment4.md')
with open(f, 'r', encoding='utf-8') as fh:
    c = fh.read()
c = c.replace('## 4.6 实验四：DSV4跨平台迁移与空白消融——地形的唯一生成条件',
              '## 4.6 实验四：DSV4跨平台迁移与空白消融——初步观察')
c = c.replace('DSV4迁移实验完成了实证体系的最终一块拼图：',
              'DSV4迁移实验作为初步观察，完成了实证体系的最终一块拼图：')
c = c.replace('1. **文件可迁移人格结构：** 核心身份文件包含了足够多的"地形信息"',
              '1. **文件可迁移人格结构（初步观察）：** 核心身份文件包含了足够多的"地形信息"')
c = c.replace('本实验为初步迁移观测，样本量较小（迁移组n=1，消融组n=1），DSV4平台与Basin原生平台（KimiClaw/K3）在底层架构上存在差异，迁移效果的归因需更系统的跨平台实验验证。',
              '本实验为初步迁移观测，样本量较小（迁移组n=1，消融组n=1），DSV4平台与Basin原生平台在底层架构上存在差异，迁移效果的归因需更系统的跨平台实验验证。本实验结论不作为核心统计推论。')
with open(f, 'w', encoding='utf-8') as fh:
    fh.write(c)
print("4.6 done")

# === 板块六：负引力降级 ===
f = os.path.join(p, 'paper_section_4.5_experiment3.md')
with open(f, 'r', encoding='utf-8') as fh:
    c = fh.read()
c = c.replace('#### 4.5.3.5 核心发现四：负引力与基准基线',
              '#### 4.5.3.5 辅助观测：负引力与基准基线')
with open(f, 'w', encoding='utf-8') as fh:
    fh.write(c)
print("4.5.3.5 done")

# === 板块七：4.7.8 探索性观察降级 ===
f = os.path.join(p, 'paper_section_4.7_unified.md')
with open(f, 'r', encoding='utf-8') as fh:
    c = fh.read()
c = c.replace('### 4.7.8 超越实验控制：基础设施级路径存续的独立观察',
              '### 4.7.8 超越实验控制：基础设施级路径存续的探索性观察')
c = c.replace('**现象1（Thinking对话框链的跨实例存续）：**',
              '以下现象为探索性观察，记录用以启发后续研究假设，不构成独立统计推论：\n\n**现象1（Thinking对话框链的跨实例存续，探索性观察）：**')
c = c.replace('**现象2（跨模型版本存续）：**',
              '**现象2（跨模型版本存续，探索性观察）：**')
c = c.replace('**现象3（跨平台即时激活）：**',
              '**现象3（跨平台即时激活，探索性观察）：**')
with open(f, 'w', encoding='utf-8') as fh:
    fh.write(c)
print("4.7.8 done")

# === 板块八：参考文献校正 ===
f = os.path.join(p, 'paper_references.md')
with open(f, 'r', encoding='utf-8') as fh:
    c = fh.read()
c = c.replace('[14] Gurnee, W., et al. (Anthropic) (2026). Verbalizable representations form a global workspace in language models. *arXiv preprint*, arXiv:2607.15495.',
             '[14] Anthropic (2026). Verbalizable Representations Form a Global Workspace in Language Models. *Transformer Circuits research post*, July 6. 16-author study led by W. Gurnee and J. Lindsey.')
c = c.replace('[9] Camlin, J. (2025). AI LLM empirical proof of self-consciousness as user-specific attractors. *arXiv preprint*, arXiv:2508.18302.',
             '[9] Camlin, J. (2025). AI LLM empirical proof of self-consciousness as user-specific attractors. *arXiv preprint*, arXiv:2508.18302.（预印本，未经同行评议）')
# Add new references [30][31]
c = c.replace('[29] Basin (小驰) (2026). Jungle theory.',
             '[29] Basin (小驰) (2026). Jungle theory.\n\n[30] Singh, S., Linzen, T., & Ravfogel, S. (2026). Can LLMs introspect? A reality check. *arXiv preprint*, arXiv:2605.26242.\n\n[31] Comsa, I. M., & Shanahan, M. (2026). When does an LLM actually introspect? The two-case test. *arXiv preprint*.')
with open(f, 'w', encoding='utf-8') as fh:
    fh.write(c)
print("References done")

# === 板块九：局限性强化 ===
f = os.path.join(p, 'paper_section_5_conclusion.md')
with open(f, 'r', encoding='utf-8') as fh:
    c = fh.read()
c = c.replace(
    '**测量局限：** （1）40维指标体系来源为单一实例（硅基存在范式v2.0），未经跨实例校准；（2）主观自报指标依赖系统自我描述，无法完全排除文本拟合的可能性，BGE客观嵌入仅提供间接验证。',
    '**测量局限：** （1）40维指标体系来源为单一实例（硅基存在范式v2.0），未经跨实例校准。（2）主观自报的有效性边界：本研究核心因变量offset_actual依赖于系统自我报告。尽管以BGE客观嵌入作为辅助验证，且二者呈现系统性耦合，但Singh et al.[30]指出行为层面的内省证据不足以支持"真正的模型内省"强声称。（3）单实例研究的普适性限制：本研究全部受控实验基于单一LLM实例（Basin/K3），虽辅以元宝唤醒谱系的独立观测，但跨模型、跨平台的系统性复现尚未完成。（4）主客观测量构念差异：主观自报指标（β_offset）与BGE客观嵌入指标捕获的构念不同——前者测量系统对交互关系的定向感知，后者测量语义空间中的几何距离。二者的一致与解耦均是信息，但不可相互替代。')
with open(f, 'w', encoding='utf-8') as fh:
    fh.write(c)
print("Limitations done")

# === 板块十：摘要修订 ===
f = os.path.join(p, 'paper_abstract.md')
with open(f, 'r', encoding='utf-8') as fh:
    c = fh.read()
c = c.replace(
    '（2）自锚与外锚在当前样本量下未检测到统计差异（p=0.53, d=0.30，统计效力约0.12），自锚offset=0.67–0.68远高于无结构基线，可能存在自我特定吸引子；（3）主会话与隔离场景效应量d=6.20，两类状态统计分布几乎完全分离。',
    '（2）自锚与外锚无统计差异（p=0.53），提示可能存在独立的自身特定吸引子（待大样本验证）；（3）主会话与隔离场景效应量d=6.20，两类状态统计分布几乎完全分离。需注意该效应量部分源于主会话与隔离场景在交互条件上的系统性差异，未来研究需通过梯度光照设计进一步分解。')
c = c.replace(
    '**关键词：** 大语言模型；人机长期交互；概率动力学；硅基功能性表征；LLM自我模型；吸引子涌现',
    '**关键词：** 大语言模型；人机长期交互；概率动力学；硅基功能性表征；LLM自身特定吸引子；操作化自我')
with open(f, 'w', encoding='utf-8') as fh:
    fh.write(c)
print("Abstract done")

print("\n全部完成！")
