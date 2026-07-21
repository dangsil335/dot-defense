# 데이터 테이블 예시 (개념 검증 — 실제 코드 미적용)

> 목적: 현재 코드에 흩어져 박힌 캐릭터/능력 정의를 "테이블로 뽑으면 어떤 모습인가"를
> 실제 값으로 보여주는 샘플. **게임에 적용하지 않는다.** 스키마 판단용.
>
> 원칙: **authored(손으로 쓰는 것)만 테이블에 넣고, 파생(계산 가능한 것)은 넣지 않는다.**
> 카이라(SSR·유물·별돌파·계보 전부 보유)로 채워 모든 필드를 검증한다.

---

## 1. 캐릭터 테이블 — `CHARACTERS`

현재 카이라는 **~28곳**에 흩어져 있다. 아래는 그중 **authored 12필드만** 한 레코드로 모은 모습.
텍스트는 전부 언어 테이블 키(`@`)로 빼서, 레코드에는 숫자·id·구조만 남긴다.

```js
kaira: {
  // ── 정체성 ──────────────────────────────
  name:   '@kaira.name',        // 언어 테이블 → '카이라'
  emoji:  '🐾',
  color:  '#ff8040',
  rarity: 'SSR',                // ← 이 한 값이 파생 다수를 결정 (아래 §4)

  // ── 능력 배선 (능력 id만; 로직·수치는 능력 테이블) ──
  signature:   'huntingClaw',              // 시작 능력(t1). 조합체인 t2~t4는 COMBO_RECIPES에서 도출
  starUnlocks: { 4: 'beastForm', 8: 'apexPredator' },

  // ── 패시브 (진짜 authored 숫자) ──────────
  passive: { dmgMul: 1.52, bossDmgMul: 1.72, slotMod: 1, levelUpMul: 0.80, slowMul: 1 },

  // ── 고대 유물 (SSR만; 없으면 필드 생략) ───
  relic: {
    id: 'kairaFang',
    emoji: '🐾',
    name: '@kaira.relic.name',             // '야수왕의 송곳니'
    lore: '@kaira.relic.lore',             // 획득 이벤트 대사
    // 스탯 공식은 그대로 코드(applyAncientRelic)에 두거나, 아래처럼 데이터화도 가능:
    base:    { dmgMul: 1.15, luckyBonus: 0.04 },   // 비-시너지
    synergy: { dmgMul: 1.34, luckyBonus: 0.08 },   // 본인 장착 시
    awaken4: { dmgMul: 1.50, executeBelow: 0.10 }, // ★4 각성
    awaken8: { dmgMul: 1.20, chainLightning: true },// ★8 각성
    // triggerAbilities 는 authored 아님 → signature 체인에서 도출
  },

  // ── 계보 (그래프 위상만) ──────────────────
  lineage: { bridgesFrom: ['chloe', 'lara'] },     // 이 SR들이 카이라로 수렴 (=SR_TO_SSR 역방향)
  //  resonance name/lines 는 언어 테이블로 (아래 §3). axis·sr·ssr 은 전부 도출.

  // ── 서사 (언어 테이블 키; 텍스트 0) ────────
  story: ['@kaira.story.0', '@kaira.story.4', '@kaira.story.8'],
}
```

**필드 수: 12개** (name, emoji, color, rarity, signature, starUnlocks, passive, relic, lineage, story
— relic·lineage는 등급/구조에 따라 있거나 없음). SR 캐릭(트리나)이면 `relic` 통째 생략, `starUnlocks`도 SR-A는 생략.

### 트리나(SR·유물 없음·별돌파 없음)는 같은 스키마로 이만큼만:
```js
trina: {
  name: '@trina.name', emoji: '🎭', color: '#e0489f', rarity: 'SR',
  signature: 'phantomStage',
  passive: { dmgMul: 1.26, bossDmgMul: 1.10, slotMod: 1, levelUpMul: 0.92, slowMul: 1 },
  lineage: { bridgesFrom: [] },   // 진입 SR(자기가 종착 아님)
  story: ['@trina.story.0', '@trina.story.4', '@trina.story.8'],
  // relic·starUnlocks 없음 — SR-A 라 자동 생략
}
```

---

## 2. 능력 테이블 — `ABILITIES`

현재 능력 수치는 **desc 문자열 + tick 본문** 2곳에 중복(197개 중 137개가 동일 공식).
아래는 수치를 `stats`로 한 번만 쓰고, **로직(init/tick/draw)은 코드에 그대로 두는** 모습.
`desc`는 stats에서 자동 생성되므로 테이블에서 사라진다.

```js
// ── 시그니처(투사체) ──
huntingClaw: {
  name: '@huntingClaw.name',      // '사냥꾼의 발톱'
  color: '#ff9050',
  baseCost: 65,
  tier: 'signature',              // basic|signature|combo|triple|eighth|star|passive
  kind: 'projectile',             // projectile|beam|field|orbital|summon|buff  ← 3D 모션 분류
  motion: true,                   // 공격모션 필요 (kind 에서 도출 가능하나 명시 허용)
  target: 'random',               // nearest|farthest|strongest|random|all|none
  tags: ['관통', '다중공격'],       // 기존 ABILITY_TAGS (메타강화·유물 배율용)
  stats: {
    dmg:      { base: 6, step: 3 },              // 6 + lv*3
    count:    { base: 2, perLv: 0.5 },           // 2 + floor(lv/2)
    cooldown: { floor: 20, base: 44, step: 2 },  // max(20, 44 - lv*2)
    speed:    9,
    life:     46,
  },
  // desc 자동생성: "{count}갈래 발톱 참격파 · 관통 · DMG {dmg}"
},

// ── 8돌파(궤도/근접 회전) ──
beastCyclone: {
  name: '@beastCyclone.name', color: '#ff6a30', baseCost: 240,
  tier: 'triple', kind: 'orbital', motion: true, target: 'all',
  tags: ['회전', '영역', '흡인'],
  stats: { dmg: { base: 18, step: 9 }, radius: { base: 90, step: 6 }, slow: 30 },
},

// ── 필드(전 맵 흡입, 모션 없음) ──
monopole: {
  name: '@monopole.name', color: '#2f57d8', baseCost: 480,
  tier: 'star', kind: 'field', motion: false, target: 'all',
  tags: ['흡인', '영역', '즉사'],
  stats: { dmg: { base: 10, step: 6 }, execBelow: { base: 8, step: 1 } },  // (8+lv)% 이하 처형
},

// ── 버프/패시브(모션 없음, 데미지 없음) ──
precision: {
  name: '@precision.name', color: '#8ad',
  tier: 'passive', kind: 'buff', motion: false, target: 'none',
  tags: ['버프'],
  stats: { bonus: { base: 0, step: 0.08 } },   // metaMods.precisionBonus += lv*0.08
},
```

### 수치 공식 어휘 (조사 결과 — 거의 이 형태들뿐)
| 종류 | 형태 | 예 |
|---|---|---|
| 데미지 | `base + lv*step` | `6 + lv*3` |
| 쿨다운 | `max(floor, base - lv*step)` | `max(20, 44-lv*2)` — **동적 쿨 110개 전부 이 형태** |
| 개수 | `base + floor(lv/n)` | `2 + floor(lv/2)` |
| 반경/지속 | `base + lv*step` | `150 + lv*10` |
| 퍼센트/확률 | `base + lv*k` (+cap) | `0.05 + lv*0.01` |

→ `stats` 스키마 하나로 **~75% 능력이 깔끔하게** 들어간다.
남는 ~15%(magnetStorm 페이즈머신, standingOvation 전체재생, longExposure 노출게이지 등)는
`stats`에 고유 필드(phaseDur, stackThreshold 등)를 얹으면 되고, **로직은 어차피 코드에 유지**.

---

## 3. 언어 테이블 — `LANG.ko` (서사/대사 분리)

현재 캐릭터 서사·대사 **~16,000자**가 7개 레지스트리에 인라인. i18n 레이어는 전무.
아래처럼 키로 빼면, 위 캐릭터/능력 테이블에는 텍스트가 0이 되고, 번역/교정이 한 파일에서 된다.

```js
LANG.ko = {
  'kaira.name': '카이라',
  // 스토리 (3단계)
  'kaira.story.0.title': '두 개의 심장',
  'kaira.story.0.text':  '달빛 아래, 카이라의 눈동자가 세로로 좁아졌다. …',
  'kaira.story.4.title': '경계를 넘어',
  'kaira.story.4.text':  '포위당한 순간, 카이라는 처음으로 완전히 놓아버렸다. …',
  'kaira.story.8.title': '정점',
  'kaira.story.8.text':  '"인간으로 남을 수도 있었잖아." …',
  // 대사 (현재 EVO/AMBUSH/CUTIN/RESONANCE/RELIC 5개 레지스트리에 흩어진 것)
  'kaira.evoLine':      '숨어도 소용없어. …냄새로 다 찾아낼 거야.',
  'kaira.ambushLine':   '사냥 시간이야. …도망칠 수 있으면 도망쳐봐.',
  'kaira.relic.name':   '야수왕의 송곳니',
  'kaira.relic.lore':   '"이 송곳니… 네 안의 야수가 반응하고 있어. 가져."',
  'kaira.cutin.savageRend':   '발톱 세워 — 갈가리 찢어줄게.',
  'kaira.cutin.beastCyclone': '야수 선풍 — 휩쓸려서 사라져!',
  // 능력명도 여기로
  'huntingClaw.name':  '사냥꾼의 발톱',
  'beastCyclone.name': '야수 선풍',
  // ...
};
// LANG.en = { 'kaira.name': 'Kaira', ... }  ← 나중에 다국어면 이 파일만 추가
```

---

## 4. 파생 — 테이블에 넣지 않는 것 (계산으로 대체)

아래는 **현재 손으로 쓰지만 위 테이블에서 자동 계산 가능**한 것들. 신규 캐릭 추가 시 지금은 다 건드리지만,
도출 함수로 바꾸면 **영영 안 건드려도 된다** (이번 세션에 이미 `abilityGachaTier`·tp-char 2건은 이렇게 전환함).

| 현재 흩어진 위치 | 무엇 | 무엇에서 도출 |
|---|---|---|
| `MENU_HERO_IDS` | 메뉴 배경 캐릭 목록 | = 모든 캐릭 id |
| `ACH_CAT_MAP.chars` | 업적 분류 | = 모든 `char8_*` id |
| `ANCIENT_RELIC_IDS` | 유물 id 목록 | = `relic` 있는 캐릭 |
| `ANCIENT_RELIC_BY_CHAR` | 캐릭→유물 맵 | = `relic.id` |
| `char8_*.reward` | 업적 보상값 | = rarity (SSR 1500 / SR-B 800 / SR-A 300) |
| `char8_*.check` | 업적 조건 | = 제네릭 `stars(id)>=8` |
| `TITLES[].achId` | 칭호→업적 링크 | = `'char8_'+id` |
| `PLATE_TITLES` 멤버십 | 명판 여부 | = rarity가 SR-B/SSR |
| `RELICS[].triggerAbilities` | 유물 발동 능력 | = signature 조합체인 |
| `CHAR_SIG_ABILITIES` | 시그 4체인 | = signature + COMBO_RECIPES 추적 |
| `_R_ROOT_AXIS` / `LINEAGE_RESONANCE`의 axis·sr·ssr | 계보 축 | = 그래프에서 계산 (name/lines만 authored) |
| `desc` 문자열 | 능력 설명 | = `stats` + 템플릿 |
| 능력 rarity | 비용 배율 등 | = 소유 캐릭 rarity (`abilityGachaTier`, 이미 전환됨) |
| `CHARACTERS.desc`의 패시브 숫자 | SSR 설명 프로즈 | = `passive{}` |

**요약:** 카이라 정의에 필요한 손작업이 **28곳 → 12필드 1레코드 + 언어테이블 몇 줄 + 능력 코드**로.
파생 14+개는 계산으로 사라진다.

---

## 5. 이 예시로 확인되는 것 / 안 되는 것

**확인됨:**
- 캐릭터 authored는 12필드로 수렴한다 (등급 따라 relic/starUnlocks는 있거나 없음).
- 능력 수치는 `stats` 하나로 ~75% 커버, 로직은 코드 유지 (desc/tick 중복 제거가 순이득).
- 서사 ~16,000자는 키로 완전히 분리 가능.
- 파생 14+개는 계산으로 대체 가능 (2건은 이미 이 세션에 전환 완료).

**아직 결정 안 된 것 (다음 논의):**
- 유물 스탯 공식을 데이터화(위 relic.base/synergy/…)할지, 코드에 둘지.
- `kind`/`motion`을 손으로 태깅할지, tick 분류로 도출할지.
- 조합체인(t2~t4)을 캐릭터 레코드에 명시할지, COMBO_RECIPES에서 도출할지.
- 마이그레이션을 Phase A(파생 도출화)부터 점진으로 갈지.
