import re

with open('main.tex') as f:
    t = f.read()

# Strip LaTeX
t = re.sub(r'\\[a-zA-Z]+(\[[^]]*\])?\{[^}]*\}', '', t)
t = re.sub(r'\$[^$]*\$', '', t)
t = re.sub(r'\\[a-zA-Z]+', '', t)
t = re.sub(r'[{}]', '', t)
t = re.sub(r'[0-9]', '', t)

words = re.findall(r'\b[a-z]{3,}\b', t.lower())

# Common words
with open('/usr/share/dict/words' if False else None) as fw:
    pass

# Manual common list
common = set('the and for are not but all any can had her him his its may per she was yet about after again almost along among anger angle angry apart argue aside avoid based basic basis began begin being below bench birth block bound bread break breed bring bring broad broke build built bunch burst cabin carry cases catch cause chain chair chant chase cheap check cheek cheer chest chief child chill chunk claim class clean clear clerk click cliff climb cling clock close cloth cloud coach coast color comma could count court cover crack craft crash crawl cream creek crime crisp cross crowd crown cruel crush curve cycle daily dance death debug depth diary dirty doubt draft draft drain drake drama drank drawn dread dream dress dried drift drink drive drove dying eager early earth eight either elect elite email empty enemy enjoy enter entry equal equip error essay event every exact excel faint faith false fault feast fence ferry fetus fiber field fifth fifty fight filed final fined first fixed flame flash flesh flies float flood floor flour fluid flush flyer focal focus force forge forth forum fossil found frame frank fraud fresh front frost froze fruit fully fungi funny ghost giant given glass gleam glide globe gloom glory glove grace grade graft grain grand grant graph grasp grave great greed green greet grief grill grind gross group grove growl grown guard guess guest guide guilt guitar hairs hairy harsh haven heart heavy hedge heist hence hoist honor hook horse hotel house hover human humor hurry ideal image imply incur index inner input intro issue ivory jelly joint judge juice knock label labor large later laugh layer learn leave legal level lever light limit linen liver lobby local logic loose lover lower lucky lunch magic mains major maker manor maple march marry marsh match mayor media mercy merge merit metal meter midst might mildly minor minus mixed model moist moral mount mouse mouth movie muddy music naive noble noise novel nurse occur ocean offer often onset opera orbit order organ other outer oxide paint panel panic paper party paste patch pause peace peach pearl pedal penny phase phone photo piece pilot pinch pitch pixel place plain plane plant plate plaza plead pluck plumb plume plunge point polar polka porch porte posse pound power press price pride prime print prior probe proof prose proud prove prune psalm punch purge purse quest queue quick quiet quota quote race rack rage rally ranch range rapid ratio reach ready realm rebel reign render ridge rifle rigid rinse risky rival river roast robin robot rocky rogue roman rough round route royal rural saint salad sauce scale scare scene scent scope score scout screw seize sense serve seven shade shaft shake shall shame shape share sharp shave shear sheen sheep sheet shelf shell shift shine shirt shock shore short shout shown siege sight since sixth sixty skill skull slave sleek sleep slice slide slope smart smell smile smoke snack snake solar solid solve sonic sorry sound south space spare spark speak speed spell spend spice spike spill spine split spoke spoon sport spray squad stack staff stage stain stairs stake stale stalk stall stamp stand stare start state steam steel steep steer stern stick stiff still stink stock stone stool store storm story stove strap straw stray strip stuck study stuff style sugar suite super surge swamp swear sweat sweep sweet swept swift swing swirl sword swore sworn table taste teach tempo theme there these thick thief thing think third thorn those three throw thumb tiger tight timer title toast today token total touch tough towel tower trace track trade trail train trait trash treat trees trend trial tribe trick tripe troop truck truly trump trust truth tumor twice twine twist ultra under union unite unity until upper upset urban usage usual utter valid valor value vapor verse vigor villa vinyl viola viral virtue visit vista vital vocal voice voter vowel waist waste watch water weave wedge weigh weird whale wheat wheel where which while whilst white whole whose width witch woman world worry worse worst worth would wound woven wrong wrote yacht yield young youth zebra zoom'.split())

potential = []
for w in sorted(set(words)):
    if len(w) < 4:
        continue
    if w in common:
        continue
    if w.endswith('s') and w[:-1] in common:
        continue
    if w.endswith('ed') and w[:-2] in common:
        continue
    if w.endswith('ing') and w[:-3] in common:
        continue
    if w.endswith('ly') and w[:-2] in common:
        continue
    if w.endswith('er') and w[:-2] in common:
        continue
    if w.endswith('tion') or w.endswith('sion') or w.endswith('ment'):
        continue
    potential.append(w)

for w in potential:
    print(w)

print(f'\n=== {len(potential)} words to check ===')
