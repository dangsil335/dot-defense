import sys, io, os, re
from collections import defaultdict
sys.stdout.reconfigure(encoding='utf-8')
os.chdir(r'C:\Users\solid\Desktop\dot-defense')
h = io.open('index.html', encoding='utf-8').read()

# 🎭 캐릭터별 기대 말투 — 전역 다수결이 아니라 이 표를 기준으로 검사한다.
#    (전역 다수결로 판정하면 존댓말 캐릭터가 반말로 뭉개진다 — v754 에서 실제로 그랬다)
EXPECT = defaultdict(lambda: '반말', {
    'aria': '존대',      # 🌟 팬에게 존댓말 하는 무대 위 아이돌
    'misaki': '존대',    # 🦋 조용하고 정중한 초연체
    'sumika': '존대',    # 🖌️ 과묵하되 정중한 살수
})

POL = re.compile(r'(요[.?!…]|요$|습니다|세요|어요|아요|예요|이에요|게요|드릴|드려|드리|셨|십니|나요|가요|시죠|시겠|으세요)')
def kind(s): return '존대' if POL.search(s) else '반말'

data = defaultdict(list)
def simple(name):
    m = re.search(r'const ' + name + r' = \{[\s\S]*?\n  \};', h)
    if not m: return
    for k, s in re.findall(r"^\s{4}(\w+):\s*'((?:[^'\\]|\\.)*)'", m.group(0), re.M):
        data[k].append((name, s))
simple('EVO_CHAR_LINES'); simple('CHAR_AMBUSH_LINES')

b = re.search(r'const PET_LINES = \{[\s\S]*?\n  \};', h).group(0)
for k, body in re.findall(r"^\s{4}(\w+):\s*\[(.*)\],\s*$", b, re.M):
    for s in re.findall(r"'((?:[^'\\]|\\.)*)'", body):
        data[k].append(('PET_LINES', s))

b = re.search(r'const SKIN_LINES = \{[\s\S]*?\n  \};', h).group(0)
for key, body in re.findall(r"^\s{4}'(\w+__\w+)':\s*\{(.*)\},\s*$", b, re.M):
    for fld, s in re.findall(r"(evo|amb):\s*'((?:[^'\\]|\\.)*)'", body):
        data[key.split('__')[0]].append((f'SKIN:{key}.{fld}', s))

b2 = re.search(r'const SSR_REVEAL_LINES = \{[\s\S]*?\n  \};', h)
if b2:
    for k, body in re.findall(r"^\s{4}(\w+):\s*\{(.*?)\},", b2.group(0), re.M | re.S):
        for s in re.findall(r"'((?:[^'\\]|\\.)*)'", body):
            data[k].append(('SSR_REVEAL', s))

print(f'{"캐릭터":12}{"기대":>5}{"총":>4}{"어긋남":>6}   판정')
print('-' * 62)
bad_total = 0
offenders = []
for ch in sorted(data):
    exp = EXPECT[ch]
    bad = [(src, s) for src, s in data[ch] if kind(s) != exp]
    bad_total += len(bad)
    if bad: offenders.append((ch, exp, bad))
    print(f'  {ch:12}{exp:>5}{len(data[ch]):>4}{len(bad):>6}   {"OK" if not bad else "⚠ 어긋남"}')

print(f'\n총 대사 {sum(len(v) for v in data.values())}줄  |  기대 말투와 어긋난 줄 {bad_total}개')
for ch, exp, bad in offenders:
    print(f'\n  [{ch}] 기대={exp}')
    for src, s in bad:
        print(f'    {src:<32} {s}')
if not offenders:
    print('\n전 캐릭터 자기 말투 일관 — 어긋남 0')
