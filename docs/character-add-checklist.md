# 캐릭터 추가 체크리스트 (아크 제로)

새 가챠 캐릭터(SR/SSR) 하나를 추가할 때 손대야 하는 곳 전부.
**줄 번호는 금방 밀리므로 grep 앵커로 찾을 것.** 앵커는 `index.html` 기준이다.

> 이 목록은 추측이 아니라 실측이다 — SSR 8종(aria·misaki·elementia·sumika·blanche·kaira·feria·somnia)의
> id 가 키로 등장하는 지점을 전수 스캔해서 뽑았다. 스캔 방법은 이 문서 맨 아래 「목록 갱신법」 참고.

---

## 0. 먼저 정할 것 (코드 건드리기 전)

| 항목 | 왜 먼저인가 |
|---|---|
| **id** (영문 소문자) | 16곳의 키가 된다. 나중에 바꾸면 전부 고쳐야 한다. |
| **등급** SR / SSR | SR 이면 `SR_TO_SSR` 의 출발점, SSR 이면 도착점이 된다. |
| **진화 계보** | SSR 은 "어느 SR 에서 올라오는가", SR 은 "어느 R타워에서 올라오는가". |
| **능력 축** | 기존 캐릭과 겹치면 존재 이유가 없다. §부록 A 의 축 표를 먼저 볼 것. |
| **말투 레지스터** | 반말/존댓말을 캐릭터별로 **일관되게** 유지한다. 대사가 6곳에 흩어져 있어 나중에 통일하기 어렵다. |

---

## 1. 필수 — 이거 빠지면 캐릭터가 성립 안 함

### 1-1. `CHARACTERS` — 본체
```
grep -n "const CHARACTERS" index.html
```
```js
carlotta: {
  name: '🐈 카를로타', color: '#c9a227',
  desc: '[SSR] …로 시작. 데미지 +NN% / … ',   // 카드·도감에 그대로 노출된다
  startAbilities: ['<시그 1번 능력>'],
  passive: { dmgMul: 1.5, bossDmgMul: 1.5, slotMod: 0, levelUpMul: 0.8, slowMul: 1 },
  unlockBy: 'gacha:carlotta',                 // ⚠ 'gacha:' 접두사 필수 — 고유장비 지급 대상 판정(_uqEligible)이 이걸 본다
  isGacha: true, rarity: 'SSR',
  story: [ { star: 0, title: '…', text: `…` }, { star: 4, … }, … ],
},
```
- `passive` 5필드는 **전부** 써야 한다(생략 시 undefined 가 곱해진다).
- `name` 앞의 이모지는 관례다. 여러 곳에서 `name.split(' ')[0]` 으로 이모지를 떼어 쓴다.

### 1-2. `GACHA_POOL` — 뽑기 풀
```
grep -n "const GACHA_POOL" index.html
```
`SSR: [...]` 배열에 id 추가. **여기 없으면 영원히 못 뽑는다.**

### 1-3. `SR_TO_SSR` — 진화 계보
```
grep -n "const SR_TO_SSR" index.html
```
- SSR 추가 시: 기존 SR 중 하나 이상을 이 SSR 로 보낸다. `luna: ['misaki','somnia']` 처럼 배열이면 분기.
- ⚠ **어느 SR 도 안 가리키면 진화로는 절대 도달할 수 없다.** 가챠로만 얻는 유령 캐릭이 된다.
- SR 추가 시: `R_TOWERS[*].sr` 에 넣어야 R20 에서 나온다.

### 1-4. `CHAR_SIG_ABILITIES` — **조합 사다리** 4단 (★해금 아님!)
```
grep -n "const CHAR_SIG_ABILITIES" index.html
```
```js
flinta: ['<시작>', '<tier2 조합>', '<tier3 히든>', '<tier4 히든>'],
```
- ⚠ **여기는 ★해금 자리가 아니다.** ★해금은 §3-1 `CHAR_STAR_UNLOCKS` 가 담당하는 **완전 별개 능력**이다.
  (실제로 한 번 틀렸다 — 여기에 ★능력을 넣어 히든 조합 2단이 통째로 빠졌다.)
- 기존 SSR 9종이 전부 `시작 → 조합 → 히든 → 히든` 이다. 대조 명령:
  ```
  grep -n "const CHAR_SIG_ABILITIES" -A 12 index.html
  ```
- 배열 **첫 번째**가 진화 게이트에서 보여주는 능력이고 `startAbilities` 와 같아야 한다.
- ⚠ **진화로 얻는 능력은 반드시 액티브여야 한다.** 패시브면 슬롯 회계가 깨진다
  (`applyEvolution` 이 액티브 'shot' 자리를 교체하는 구조라 그렇다. 위반 시 console.warn 이 뜬다).

### 1-4b. 조합 레시피 3건 (tier 2 / 3 / 4)
```
grep -n "combo: '<tier2능력>'" index.html
```
```js
{ parts: ['<시작>',      '<기본능력>'], combo: '<tier2>', tier: 2 },
{ parts: ['<tier2>',     '<기본능력>'], combo: '<tier3>', tier: 3 },
{ parts: ['<tier3>',     '<기본능력>'], combo: '<tier4>', tier: 4 },
```
사다리가 끊기면 그 위 능력은 영원히 못 만든다.

### 1-4c. 능력 정의의 분류 플래그 — **도감이 이걸로 센다**
| 위치 | 플래그 |
|---|---|
| 시작 능력 | `isGachaUnique: true` (+ 단일대상이면 `single: true`) |
| tier2 조합 | `isGachaUnique: true, isCombo: true` |
| tier3·4 히든 | `isGachaUnique: true, isCombo: true, isTriple: true` |
| ★4·★8 해금 | `isGachaUnique: true, isStarUnlock: true` |

⚠ 빠뜨리면 **조용히 샌다** — 도감 분류 조건이 `def.isCombo` / `def.isTriple` 이라
플래그가 없으면 액티브 탭에 섞이거나 어디에도 안 잡힌다. 크래시가 없어서 알아채기 어렵다.
**검증법**: 도감 탭 카운트(`액티브 N/… · 조합 N/… · 히든 N/…`)가 추가 전후로 의도대로 움직이는지 본다.
실제로 이걸로 3건을 잡았다(조합 51→52, 히든 51→53).

### 1-5. `ABILITY_DEFS` — 새 능력 정의
```
grep -n "const ABILITY_DEFS" index.html
```
체인에 새 id 를 넣었으면 여기 정의도 만들어야 한다. 없으면 진화해도 능력이 안 붙는다.

### 1-6. 에셋 — 일러/치비 2장 + **능력 아이콘 6장**
| 경로 | 규격 |
|---|---|
| `icons/illust/<id>.png` | `thumbnail((433,577), LANCZOS)` · RGBA **투명배경** |
| `icons/characters/<id>.png` | 동일 규격(치비) |
| `icons/abilities/<능력id>.png` × **6** | **256×256 · 불투명 액자형** (시그 체인 4 + ★해금 2) |

⚠ **능력 아이콘은 파일 시스템에만 있어서 코드 스캔·차분 감사에 안 잡힌다.** 실제로 놓쳤다.
- 파일명은 **능력 id 그대로**, 대소문자까지 일치해야 한다 (`flintShot.png`).
- 배경은 **투명이 아니라 불투명 액자형**이다 — `drawAbilityIcon` 은 `ctx.drawImage` 한 번만 하고
  배경판을 따로 깔지 않는다. 투명으로 뽑으면 어두운 UI 위에 아이콘이 허공에 뜬다.
  (일러·치비는 반대로 투명이어야 한다. 헷갈리지 말 것.)
- 없어도 크래시는 안 난다 — `drawIconPlaceholder` 가 티어별 색 사각형으로 대체한다. **그래서 더 놓치기 쉽다.**
- 확인:
  ```bash
  for k in <능력id들>; do [ -f "icons/abilities/$k.png" ] || echo "❌ $k"; done
  ```
- 원본은 `icons/illust/_orig/<id>.png` · `icons/characters/_orig/<id>.png` 에 보관.
- 애니 일러가 있으면 `.webp` / `.gif` 를 같은 이름으로 두면 자동으로 우선 적용된다(`_applyIllustChain`).
- ⚠ **에셋만 바꿔도 `APP_VERSION` + `sw.js` 의 `CACHE` 를 올려야 한다.** sw 가 정적 에셋을 cache-first 로 다뤄서,
  버전을 안 올리면 기존 기기가 옛 그림을 계속 쓴다.

---

## 2. 고유장비 (가챠 캐릭 전용)

### 2-1. `SIGNATURE_GEAR`
```
grep -n "const SIGNATURE_GEAR " index.html
```
`carlotta: { name:'…', desc:'…' }` — 이름/설명이 없으면 목록에서 전부 "고유"로 겹쳐 보인다.

### 2-2. `SIGNATURE_GEAR_ICON`
```
grep -n "const SIGNATURE_GEAR_ICON" index.html
```
캐릭터별 구분 이모지. 안 넣으면 ✨ 로 뭉친다.

> 지급은 자동이다 — `unlockBy` 가 `gacha:` 로 시작하고 해금되면 `_grantUniqueGear` 가 1개 준다.

---

## 3. 별(★) 성장

### 3-1. `CHAR_STAR_UNLOCKS`
```
grep -n "const CHAR_STAR_UNLOCKS" index.html
```
`carlotta: { 4: ['<4★능력>'], 8: ['<8★능력>'] }` — `CHAR_SIG_ABILITIES` 의 3·4번째와 맞춘다.

### 3-1b. ★해금 능력은 `CHAR_SIG_ABILITIES` 와 **다른 능력**이다
`CHAR_STAR_UNLOCKS` 의 4★/8★ 는 조합 사다리와 겹치지 않는 별도 능력이어야 한다.
아리아 기준: 사다리는 `cosmicChorus·celestialSymphony·stellarOpera`, ★해금은 `celestialEcho·sirensSong` — 전부 다르다.
8★ 능력은 관례상 `desc` 를 `[8돌파] …` 로 시작한다.

### 3-2. `ANCIENT_RELIC_IDS` + `ANCIENT_RELIC_BY_CHAR`
```
grep -n "const ANCIENT_RELIC_IDS" index.html
```
캐릭터 전용 고대 유물. 두 곳 **모두** 넣어야 하고, `RELICS` 에 유물 정의와
`applyAncientRelic` 안의 `rid === '<유물id>'` 분기도 필요하다(총 4곳).
기습 이벤트에 `{ avail: () => _ancientAvail('<charId>'), make: () => _charRelicEv('<charId>') }` 분기를
달아야 획득 경로가 열리고, `_charRelicEv` 안의 `lore` 에 수여 대사가 필요하다.

### 3-3. `LINEAGE_RESONANCE` — 계보 공명 (SSR 전용)
```
grep -n "const LINEAGE_RESONANCE" index.html
```
키가 **`<R타워루트능력id>_<ssrId>`** 형식이라 `id:` 단순 스캔에 안 잡힌다. 그래서 놓치기 쉽다.
```js
missile_flinta: { sr:'cardista', ssr:'flinta', axis:'blast', name:'…', lines:['SR: …','SSR: …'] },
```
- `axis` 는 `_R_ROOT_AXIS[루트능력]` 과 일치해야 한다 (`ice/shock/blast/pierce/echo`).
- `sr` 은 `SR_TO_SSR` 에서 그 SSR 로 오는 SR 이어야 한다.
- 없으면 진화해도 공명 이벤트가 안 뜬다 — **조용히 안 뜬다.**
- 기존 SSR 은 캐릭터당 3~7건. 검증: `grep -c "_<ssrId>:" index.html`

---

## 4. 대사 — 6곳. 말투를 여기서 일관되게 유지한다

| 레지스트리 | 언제 나오나 | grep 앵커 |
|---|---|---|
| `EVO_CHAR_LINES` | 진화 게이트 컷인 | `const EVO_CHAR_LINES` |
| `CHAR_AMBUSH_LINES` | 기습 이벤트 등장 | `const CHAR_AMBUSH_LINES` |
| `CHAR_AMBUSH` | 기습 이벤트 선택지 본문 | `const CHAR_AMBUSH` |
| `SSR_REVEAL_LINES` | 가챠 SSR 연출 (`new` / `dup` 두 줄) | `const SSR_REVEAL_LINES` |
| `PET_LINES` | 메뉴 펫 탭 (3줄) | `const PET_LINES` |
| `lore` (고대 유물 수여) | 고대 유물 이벤트 | `const lore = {` (`_charRelicEv` 안) |

- ⚠ **말투 일관성**: 캐릭터마다 반말/존댓말을 정하고 6곳 전부 같은 register 로 쓴다.
  존댓말 캐릭은 aria·misaki·sumika 처럼 소수다 — 전체 다수결로 정하지 말 것(그렇게 했다가 한 번 틀렸다).
- 검증: `python docs/voice-audit.py`

---

## 4-B. 능력 쪽 부속 — **캐릭터 id 스캔에 안 잡힌다**

능력 id 로 등록되는 곳들이다. 캐릭터 id 만 훑으면 전부 놓친다(실제로 6곳을 놓쳤다).

| 레지스트리 | 무엇 | grep 앵커 |
|---|---|---|
| `ABILITY_TAGS` | 능력별 태그(`단일`/`광역`/`연사`/`폭발`/`버프`…) | `const ABILITY_TAGS` |
| `ABILITY_ICON_ORDER` | 능력 아이콘 표시 순서 | `const ABILITY_ICON_ORDER` |
| `COMBO_CUTIN_LINES` | **조합 형성 시 컷인 대사** — 조합 3종 전부 | `const COMBO_CUTIN_LINES` |
| `activateAncientAwaken` | 고대 유물 **★4/★8 각성 효과 분기** | `function activateAncientAwaken` |
| `ACHIEVEMENTS` (8돌파) | `char8_<id>` 업적 | `char8_aria` |
| `MENU_HERO_IDS` | 메인 메뉴 배경 로테이션 | `const MENU_HERO_IDS` |

⚠ **`activateAncientAwaken` 이 제일 위험하다.** 유물 `desc` 에는 「★4 각성 1 / ★8 각성 2」를 써두는데
여기 분기가 없으면 **글만 있고 효과가 0** 이다. 크래시도 경고도 없다.

## 4-C. 기획 판단이 필요한 것 (코드 누락 아님)

| 항목 | 상황 |
|---|---|
| `GACHA_BANNERS` | 배너가 SSR 을 **2명씩 짝지어** 구성한다(elemSumi·ariaMisa·prismBeast·feriaSomnia). 홀수 번째 캐릭은 짝이 필요하다. |
| `SKINS` | 스킨을 안 만들었으면 비어 있는 게 정상. 감사에서 계속 잡히는 게 싫으면 `<id>: []` 로 명시. |

## 5. 연출

### `SSR_REVEAL_FX` (SSR 전용)
```
grep -n "const SSR_REVEAL_FX" index.html
```
`style` 키가 `_buildSSRFx` 의 분기 이름이다. **새 style 을 쓰려면 `_buildSSRFx` 에 그 분기를 구현해야 한다.**
구현하기 싫으면 기존 style 하나를 재사용하고 색만 바꾼다.

---

## 6. 선택 — 스킨

### `SKINS` + `SKIN_LINES`
```
grep -n "const SKINS" index.html
grep -n "SKIN_LINES" index.html
```
- 에셋: `icons/illust/skin/<id>__<skin>.png` · `icons/characters/skin/<id>__<skin>.png` (같은 규격)
- `SKIN_LINES` 는 스킨당 `{ evo, amb }` 두 줄. **성격·말투는 본체와 동일**하게, 컨셉만 스킨에 맞춘다.

---

## 7. 마무리

1. `node --check` — `<script>` 블록만 뽑아서 검사 (문법 오류 나면 부팅이 통째로 죽는다)
2. `APP_VERSION`(index.html) + `CACHE`(sw.js) **동시** 상향
3. 브라우저 확인:
   - 도감/캐릭터 목록에 뜨는가
   - 가챠 풀에 들어갔는가 (`unlock <id>` 치트로 해금 후 확인)
   - 진화 트리(성도)에서 계보가 이어지는가
   - 고유장비가 지급되는가
   - 일러·치비가 로드되는가 (404 아님)
4. 커밋 + 푸시

---

## 부록 A — 기존 능력 축 (겹치면 안 됨)

| 캐릭 | 등급 | 축 |
|---|---|---|
| 아리아 | SSR | 순수 화력·보스 특화 (슬롯 0, 최고 배율) |
| 미사키 | SSR | 시간정지·둔화 극단 (슬롯 +2) |
| 엘레미아 | SSR | 조합마다 정령 변신 |
| 스미카 | SSR | 단일·처형 |
| 블랑슈 | SSR | 프리즘 광선 (★ 별해금) |
| 카이라 | SSR | 야수 근접 참격 |
| 페리아 | SSR | 자기장 극성 |
| 솜니아 | SSR | 졸음 누적 → 각성 폭발 |

---

## 부록 B — 목록 갱신법

이 문서가 낡았는지 확인하려면, SSR id 가 키로 등장하는 곳을 다시 스캔한다.
「8/8」로 나오는 레지스트리가 곧 필수 목록이다.

```python
import io, re
L = io.open('index.html', encoding='utf-8').read().split('\n')
SSR = ['aria','misaki','elementia','sumika','blanche','kaira','feria','somnia']
decl = re.compile(r'^\s*(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=\s*[\{\[]')
def nearest(i):
    for j in range(i, max(-1, i-400), -1):
        m = decl.match(L[j])
        if m: return m.group(1)
    return '(불명)'
hits = {}
for i, l in enumerate(L):
    for cid in SSR:
        if re.search(r"(?:^|[{,\s])'?%s'?\s*:" % cid, l):
            hits.setdefault(nearest(i), set()).add(cid)
for k, v in sorted(hits.items(), key=lambda kv: -len(kv[1])):
    print('%d/8  %s' % (len(v), k))
```

⚠ 이 스캔의 사각지대 — **여기서 안 잡히는 것들이 실제로 누락됐었다.** 반드시 따로 챙길 것:

| 사각지대 | 이유 | 항목 |
|---|---|---|
| 배열 | `id:` 키가 아님 | `GACHA_POOL` · `SR_TO_SSR` · `ANCIENT_RELIC_IDS` (§1-2·1-3·3-2) |
| 복합 키 | 키가 `<루트>_<ssr>` 형식 | `LINEAGE_RESONANCE` (§3-3) |
| 능력 쪽 | 캐릭터 id 가 아니라 능력 id 로 잡힘 | `ABILITY_DEFS` · 조합 레시피 · 분류 플래그 (§1-4b·1-4c) |

**최종 점검은 스캔이 아니라 도감 카운트로 한다.** 추가 전후 `액티브/조합/히든` 숫자가
의도한 만큼 움직였는지 보면 플래그 누락이 바로 드러난다.

---

## 부록 C — 차분 감사 (이게 제일 확실하다)

위 목록을 아무리 손으로 유지해도 샌다. **기존 SSR 8종과 전면 차분**을 뜨는 게 확실하다.
캐릭터 id 뿐 아니라 **그 캐릭의 능력 id · ★해금 id · 유물 id** 까지 토큰으로 묶어서,
"SSR 8종 전부에 있는데 새 캐릭에는 없는 구조"를 찾는다.

이 스크립트가 실제로 9건을 찾아냈다 — 손으로 만든 체크리스트가 놓친 것들이다.

```python
import io, os, re, sys
os.chdir(r'<repo>')
h = io.open('index.html', encoding='utf-8').read(); L = h.split('\n')
decl = re.compile(r'^\s*(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=\s*[\{\[]')
fn   = re.compile(r'^\s*(?:async\s+)?function\s+([A-Za-z_$][\w$]*)')
def owner(i):
    for j in range(i, max(-1, i-500), -1):
        m = decl.match(L[j]);  m2 = fn.match(L[j])
        if m: return m.group(1)
        if m2: return 'fn:' + m2.group(1)
    return '(?)'
def blk(name):
    m = re.search(r'const %s\s*=' % name, h); st = h.index('{', m.start()); d = 0
    for k in range(st, len(h)):
        if h[k] == '{': d += 1
        elif h[k] == '}':
            d -= 1
            if d == 0: return h[st:k+1]
sig, star, relic = {}, {}, {}
for mm in re.finditer(r"(\w+):\s*\[([^\]]*)\]", blk('CHAR_SIG_ABILITIES')):
    sig[mm.group(1)] = [x.strip().strip("'") for x in mm.group(2).split(',') if x.strip()]
for mm in re.finditer(r"(\w+):\s*\{\s*4:\s*\['([^']*)'\][^}]*8:\s*\['([^']*)'\]", blk('CHAR_STAR_UNLOCKS')):
    star[mm.group(1)] = [mm.group(2), mm.group(3)]
for mm in re.finditer(r"(\w+):\s*'(\w+)'", blk('ANCIENT_RELIC_BY_CHAR')):
    relic[mm.group(1)] = mm.group(2)
SSR = ['aria','misaki','elementia','sumika','blanche','kaira','feria','somnia']
NEW = 'flinta'          # ← 새 캐릭 id
def toks(c):
    t = {c} | set(sig.get(c, [])) | set(star.get(c, []))
    if relic.get(c): t.add(relic[c])
    return t
places = {}
for c in SSR + [NEW]:
    s = set()
    for i, l in enumerate(L):
        for tk in toks(c):
            if re.search(r"(?<![\w$])%s(?![\w$])" % re.escape(tk), l): s.add(owner(i)); break
    places[c] = s
for m in sorted(set.intersection(*[places[c] for c in SSR]) - places[NEW]):
    print('❌', m)
print('등장구조:', {c: len(places[c]) for c in SSR + [NEW]})
```

**읽는 법**
- `❌` 로 나온 것이 후보다. 전부가 진짜 누락은 아니다 — 오탐도 섞인다.
- **등장구조 수**를 같이 본다. 새 캐릭이 기존 8종 범위(32~41)에 들면 대체로 채워진 것이다.
- 오탐 판별: 그 구조 안에서 기존 캐릭 토큰이 실제로 몇 줄 잡히는지 세어본다.
  0줄이면 `owner()` 역추적이 범위를 잘못 잡은 것이다(`drawDefenseTowers` 가 그랬다).
