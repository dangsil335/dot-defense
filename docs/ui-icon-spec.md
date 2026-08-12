# 아크 제로 — 로비 UI 리소스 규격 (v822 기준)

> 메인 로비 버튼용. **라벨 판(배경) + 아이콘(글리프)을 분리**해서 받는다.
> 글자는 이미지에 넣지 않는다 — CSS 가 렌더한다(문구 수정·길이 대응 때문).
> 모든 수치는 실제 화면에서 잰 값이다(가로 폰 812×375 / 데스크톱 1280×800).

---

## 0. 한 줄 요약

```
라벨 판   icons/ui/plate/   3장   비율 고정 전체 아트 (9-slice 폐기)
아이콘    icons/ui/menu/    10장  256×256 투명 WebP  표시 28~29px  ← 1차 완료
```

⚠ **둘 다 투명 배경.** 이 게임의 *능력* 아이콘(`icons/abilities/`)만 **불투명 액자형**이다.
헷갈려서 액자형으로 만들면 판 위에 액자가 또 생긴다.

---

## 1. 버튼 판 — 3장  (5차: 구조는 맞다, 색과 배지만 고치면 된다)

### ✅ 4차에서 맞힌 것 — 이 구조를 유지할 것

4차 시안의 **좌측 아이콘 배지 + 우측 라벨 면** 구조는 정확하다.
코드도 그 구조에 맞춰 이미 바꿔놨다(v820). **구조는 건드리지 말 것.**

```
┌──────────────────────────────────────┐
│ ┌──────┐                             │
│ │ 배지 │      라벨 면 (글자 자리)      │
│ └──────┘                             │
└──────────────────────────────────────┘
   ↑ 여기 우리 아이콘이 얹힌다 → 비워둘 것
```

### ❌ 두 가지만 고치면 된다

| | 4차에서 온 것 | 고쳐야 할 것 |
|---|---|---|
| **배지 안** | 발바닥 그림이 그려져 있다 | **비워둔다.** 여기에 우리 아이콘 10장이 얹힌다 |
| **판 색** | 거의 검정 (평균 밝기 76 / 51 / 36) | **밝은 실리콘.** 로비가 밝은 팔레트다 |

배지 안에 그림이 있으면 우리 아이콘이 그 위에 겹쳐서 둘 다 안 보인다.
배지는 **살짝 다른 톤의 빈 홈**이면 된다.

### ⚠ 여기까지 온 실패 기록 (같은 실수를 반복하지 말 것)

| | 지시한 것 | 나온 것 | 원인 |
|---|---|---|---|
| 1차 | `thin darker band` | 납작한 흰 판 | 볼륨 단어를 내가 지웠다 |
| 2차 | `capsule pill` | 옆에서 본 알약 = 막대 | `pill` 이 형태를 막대로 몰았다 |
| 3차 | `the shape of a cat's paw pad` | 판 위에 발가락 젤리 4개 | **은유를 형상으로 받았다** |
| 4차 | 은유 제거 + `EXACTLY ONE` | 구조는 정확, 배지에 발바닥 + 검정 | 색 지정이 약했고 배지를 비우라고 안 했다 |

> **원칙: 은유를 쓰지 않는다.** 형태는 기하로, 말랑함은 음영으로 적는다.

### 파일과 캔버스 — ⚠ 이 표가 유일한 출처

| 파일 | 쓰이는 곳 | 캔버스 | 형태 | 근거(실측) |
|---|---|---|---|---|
| `icons/ui/plate/normal.webp` | 하단 독 6개 | **320 × 320** | **정원**(배지 없음) | 원 63~80px |
| `icons/ui/plate/cta.webp` | **출격** | **480 × 240** | 배지+라벨 2:1 | 171×85 |
| `icons/ui/plate/gold.webp` | 차원 스카우트 | **476 × 140** | 배지+라벨 3.4:1 | 171×50 |

투명 WebP, 판 바깥 알파 0. 접지 그림자는 **캔버스 안에**.

**배지 위치·크기 (코드 실측값 그대로)**

| 파일 | 배지 좌측 여백 | 배지 폭 | 배지 높이 | 모서리 |
|---|---|---|---|---|
| `cta` | 캔버스 폭의 4.5% | 25% | 72% | 폭의 24% |
| `gold` | 4% | 19% | 74% | 26% |

`normal` 은 독 원형 버튼용이라 **배지 없이 원 하나**다.

### 색 — 4차의 검정을 밝은 실리콘으로

```
normal  판 위 #ffffff → 아래 #e6edf6,  아래 테두리 #c4d0e0
cta     판 위 #8fcdf2 → 아래 #4f9bd2,  아래 테두리 #3d7fae
        배지: 판보다 살짝 밝고 안으로 들어간 홈 (흰색 26% 정도)
gold    판 위 #f8e6bc → 아래 #dfbc6e,  아래 테두리 #b39a63
        배지: 흰색 32% 정도
```

유광 금지. 매트 소프트터치.

### 영문 프롬프트 — `cta` / `gold` (배지 + 라벨)

```
Top-down view of ONE soft silicone UI button plate, {SIZE} canvas,
TRANSPARENT background (alpha channel).

A single horizontal rounded-rectangle plate, corners fully rounded.
Inside it, on the LEFT, a slightly recessed square badge well with rounded corners —
the badge is EMPTY: a plain smooth recessed surface, no drawing, no symbol,
no paw, no icon, no glyph inside it. It is only a shallow empty well.
The rest of the plate to the right of the badge is a smooth EMPTY label area,
also completely plain — no text, no lines, no decoration.

{COLOR}

Matte soft-touch silicone finish, very fine subtle grain.
Not glossy, no mirror reflection, no wet look.
Light from above and slightly in front: a broad soft highlight across the upper half,
the lower third settling into soft shadow, a thin darker rim along the bottom edge,
and a soft contact shadow beneath the plate, fully inside the canvas.

Premium, tactile, physical. Bright and light in tone, NOT dark, NOT black.
```

| 파일 | SIZE | COLOR |
|---|---|---|
| `cta` | `480x240` | `Soft light sky blue silicone: #8fcdf2 at the top fading to #4f9bd2 at the bottom, darker blue bottom rim #3d7fae. The badge well is a lighter tint of the same blue, as if brushed with 26% white.` |
| `gold` | `476x140` | `Light warm cream silicone: #f8e6bc at the top fading to #dfbc6e at the bottom, soft bronze bottom rim #b39a63. The badge well is a lighter tint of the same cream, as if brushed with 32% white.` |

### 영문 프롬프트 — `normal` (정원, 배지 없음)

```
Top-down view of ONE soft silicone push-button pad, 320x320 canvas,
TRANSPARENT background (alpha channel).

EXACTLY ONE PERFECT CIRCLE, centered, filling about 88% of the canvas.
Nothing else in the image: no second circle, no badge, no bumps, no lobes,
no paw, no toes, no icon, no text. The surface is completely plain.

The surface is domed — highest at the center, falling away smoothly toward the rim,
so it reads as a thick soft cushion seen from directly above.
The rim rolls slightly downward and under.

Off-white silicone: #ffffff at the center, fading to #e6edf6 near the rim,
with a cool grey-blue edge #c4d0e0 along the bottom of the rim.

Matte soft-touch finish, very fine subtle grain. Not glossy, no mirror reflection.
Light from above and slightly in front: a broad soft highlight across the upper half,
the lower third in soft shadow, a soft contact shadow beneath, inside the canvas.

Premium, tactile, physical. Bright and light in tone, NOT dark, NOT black.
```

**네거티브 (판 공통)**
```
dark, black, charcoal, dark grey, navy, night, low key,
paw, paw print, animal, beans, toes, bumps, lobes, multiple objects, two shapes,
icon inside badge, symbol, glyph, emblem, logo, text, numbers, letters, watermark,
capsule, pill, bar, tab,
flat, flat design, 2d, sticker, vector, paper, card,
glossy, mirror reflection, specular highlight, chrome, metal, glass, wet look,
pattern, border, frame, outline, sharp corners, hard edges, neon, gradient banding,
background, solid background, green screen, chroma key,
isometric, perspective tilt, side view
```
⚠ `dark, black` 과 `paw, icon inside badge` 가 5차의 핵심 추가다 — 4차가 정확히 그 둘로 막혔다.
⚠ `flat` 은 **판에서만** 네거티브. 아이콘(§2)은 정반대이니 프롬프트를 섞지 말 것.

### 통과 기준

1. 캔버스가 위 표와 일치 (320×320 / 480×240 / 476×140)
2. **배지 안이 비어 있는가.** 그림이 하나라도 있으면 실패 — 우리 아이콘이 못 들어간다
3. **밝은가.** 불투명 픽셀 평균 밝기가 150 이상이어야 한다 (4차는 76/51/36 이었다)
4. 판 바깥 알파 0, 접지 그림자가 캔버스 안
5. 가운데를 세로로 자를 때 위쪽이 볼록 (직선이면 실패)
6. 유광 반사 없음, 글자·테두리 없음

---

## 2. 아이콘 — 10장

| 파일명 | 버튼 | 라벨 | 현재 이모지 | 의미 |
|---|---|---|---|---|
| `shop.webp` | `#shopBtn` | 강화소 | 🔧 | 영구 강화·업그레이드 상점 |
| `codex.webp` | `#codexBtn` | 도감 | 📖 | 능력·유물 수집 도감 |
| `perma.webp` | `#abilityPermaBtn` | 능력 영구 | 🧬 | 능력의 영구 강화(별 퍼크) |
| `achieve.webp` | `#achievementsBtn` | 업적 | 🏆 | 업적 달성 목록 |
| `chars.webp` | `#charCollectionBtn` | 캐릭터·진화 | 👥 | 캐릭터 보유·진화 트리 |
| `records.webp` | `#recordsBtn` | 기록 | 📋 | 플레이 기록·통계 |
| `core.webp` | `#coreMgrBtn` | 전술 코어 관리 | 🔩 | 장비(코어) 장착·강화 |
| `rank.webp` | `#globalRankBtn` | 글로벌 랭킹 | 🌐 | 서버 순위표 |
| `scout.webp` | `#gachaBtn` | 차원 스카우트 | 🎰 | 캐릭터 뽑기 |
| `start.webp` | `#startBtn` | 출격 / 새 게임 | ▶ | 게임 시작 (최우선 CTA) |

### 규격

```
캔버스   256 × 256 정사각
포맷     투명 WebP
여백     상하좌우 8~12px. 가장자리에 붙이지 말 것
용량     장당 30KB 이하 (10장 합쳐 300KB 이내)
```

**표시 크기 (실측)**

| 화면 | 아이콘 | 버튼 |
|---|---|---|
| 가로 폰 812×375 | **28 × 29** | 109 × 43 |
| 데스크톱 1280×800 | **29 × 29** | 112 × 45 |

→ 256px 원본은 표시의 약 9배. 충분하다.

⚠ **29px 로 줄여도 뭔지 알아봐야 한다.** 가는 선·작은 글자·복잡한 디테일은 뭉개진다.
확정 전에 29px 로 축소해서 확인할 것.

### 배치 (내가 CSS 로 처리)

```
┌────────────────────────────┐  ← 라벨 판 (normal.webp)
│  ┌────┐                    │
│  │아이콘│   강화소           │  아이콘 좌측 4~30%, 글자 34%~
│  └────┘                    │
└────────────────────────────┘
```

아이콘은 판의 **왼쪽 26% 폭**을 쓰고, 글자는 34% 지점부터 왼쪽 정렬로 들어간다.
그래서 아이콘은 **정사각 안에 꽉 차게** 그리면 된다 — 여백은 CSS 가 준다.

---

## 3. 공통 디자인 톤 — ⚠ 3D 클레이 아님

레퍼런스: 블루아카이브 / 스텔라소라의 로비 UI 아이콘.

**1차 시도가 실패한 이유** — 프롬프트에 `clay-render` `puffy 3D` `soft 3D` 를 넣었더니
스톡 3D 아이콘 팩 같은 **두꺼운 입체 렌더**가 나왔다. 레퍼런스는 그것과 다르다.

| | 나오면 안 되는 것 | 목표 |
|---|---|---|
| 렌더 | 두꺼운 3D 입체 렌더 | **반평면 벡터 일러** |
| 음영 | 강한 볼륨·바닥 그림자 | 최소한, 단색면 위주 |
| 시점 | 살짝 사선 원근 | **정면 평면** |
| 질감 | 매트 플라스틱·점토 | 깨끗한 색면 |
| 인상 | 스톡 3D 아이콘 | 게임 UI 아이콘 |

**실용적인 이유도 있다.** 표시 크기가 **29px** 이라 3D 볼륨·페이지 선·리본 같은 디테일은
전부 뭉개져 회색 덩어리가 된다. 평면이 작게 줄었을 때 훨씬 잘 읽힌다.

```
· 반평면(semi-flat) 벡터. 정면. 굵고 단순한 실루엣
· 면은 단색 또는 아주 완만한 2톤 그라디언트
· 음영은 면 분할로만 (밝은 면 / 어두운 면). 블러 그림자 최소
· 하이라이트는 점 하나 정도까지만
· 파스텔 — 하늘 #7fd4ff · 민트 #a8e6cf · 크림 #ffe6a8 · 연보라 #c9b8ff
· 요소 1~2개. 29px 로 줄여서 알아볼 수 있어야 한다
```

**금지**
```
✗ clay / 3D render / puffy / volumetric   ← 1차 실패 원인. 절대 넣지 말 것
✗ 바닥에 드리우는 블러 그림자
✗ 사선 원근·입체 두께 표현
✗ 굵은 검정 외곽선        29px 로 줄면 뭉개진다
✗ 각진 모서리·날카로운 사선
✗ 네온 글로우·사이버펑크
✗ 텍스트·숫자            라벨은 CSS 가 렌더한다
✗ 불투명 배경판·크로마키 초록 배경   반드시 알파 투명
```

---

## 4. 영문 프롬프트

### 라벨 판

→ **1절로 옮겼다.** 구 프롬프트(240×96 · 9-slice)는 실패본이라 삭제했다.
⚠ 판 프롬프트는 1절에만 있다. 여기에 사본을 두지 않는다 — 2차 실패가 사본 때문이었다.

### 아이콘

```
Cute mobile game UI icon, semi-flat vector illustration, 256x256,
TRANSPARENT background (alpha), no frame, no background plate, no green screen.
{CONCEPT}
Flat front-facing view, bold simple silhouette with rounded corners.
Solid color fills with at most a gentle two-tone shading — light face and shadow face.
Pastel palette: sky blue #7fd4ff, mint #a8e6cf, cream #ffe6a8.
Clean and cute, in the style of bright anime mobile game menu icons.
Must stay readable when scaled down to 29 pixels.
NOT a 3D render. No clay, no plastic, no volumetric depth, no perspective,
no drop shadow, no outline strokes, no text, no numbers.
```

**네거티브 (공통)**
```
3d render, clay, claymation, plastic, volumetric, isometric, perspective, depth, extrusion,
drop shadow, ambient occlusion, glossy plastic, stock 3d icon,
green screen, chroma key, solid background, background plate, frame, border,
text, numbers, letters, watermark, neon glow, cyberpunk, sharp angular edges,
thin lines, heavy black outline, cluttered detail, photorealistic
```
⚠ `flat 2d vector` 를 네거티브에 넣지 말 것 — 1차 프롬프트의 실수다. 우리가 원하는 게 그거다.

---

## 5. 아이콘 개별 `{CONCEPT}`

### `shop.webp` — 강화소
```
a rounded wrench crossed with a small upgrade arrow pointing up,
sky-blue body with cream metal accents, flat two-tone shading
```
### `codex.webp` — 도감
```
a chubby open book with rounded corners, a small star floating above the pages,
sky-blue cover with cream pages
```
### `perma.webp` — 능력 영구
```
a soft rounded DNA helix made of two twisting jelly strands,
mint and sky-blue, with a tiny star at the top
```
### `achieve.webp` — 업적
```
a rounded trophy cup with a small star on its front,
cream-gold body with a sky-blue base, flat two-tone shading
```
### `chars.webp` — 캐릭터·진화
```
two overlapping rounded character silhouette busts (no faces),
front one sky-blue and back one soft violet, simple shoulder shapes only
```
### `records.webp` — 기록
```
a plump clipboard with rounded corners and three short line marks,
sky-blue board with cream paper
```
### `core.webp` — 전술 코어 관리
```
a rounded hexagonal core gem with a soft glow inside,
one small orbiting ring around it, mint and sky-blue
```
### `rank.webp` — 글로벌 랭킹
```
a chubby rounded globe with soft latitude bands,
a small cream star or laurel accent at the lower right
```
### `scout.webp` — 차원 스카우트
```
a rounded gacha capsule splitting open with a small star above it,
cream-gold capsule with a sky-blue inner face, flat two-tone shading
```
### `start.webp` — 출격 (CTA)
```
a bold rounded play triangle, bright sky-blue with a lighter top face,
this is the primary action — make it the most vivid and saturated of the set
```

---

## 6. 세트 일관성

| 아이콘 | 주 형태 | 주색 | 밝기 |
|---|---|---|---|
| shop | 렌치+화살표 | 하늘 | 중 |
| codex | 책 | 하늘+크림 | 중 |
| perma | 나선 | 민트 | 중 |
| achieve | 트로피 | 크림골드 | 높음 |
| chars | 인물 실루엣 2 | 하늘+연보라 | 중 |
| records | 클립보드 | 하늘+크림 | 낮음 |
| core | 육각 젬 | 민트 | 중 |
| rank | 지구본 | 하늘 | 중 |
| scout | 캡슐 | 크림골드 | 높음 |
| **start** | **재생 삼각형** | **하늘(진함)** | **최고** |

`start` 가 가장 선명해야 한다 — 유일한 주요 행동 버튼이다.
`achieve` `scout` 만 크림골드로 "보상 계열"을 묶고 나머지는 하늘/민트로 통일한다.

---

## 7. 넣은 뒤 (내가 할 작업)

파일만 넣으면 CSS 한 블록으로 끝난다. 지금은 CSS 젤리 + 이모지로 자리를 잡아둔 상태다.

```css
/* 아이콘은 이미 들어갔다 (v810~) */
#menu #shopBtn { --mb-ico: url('./icons/ui/menu/shop.webp'); }

/* 판은 아직 CSS 로 그리는 중 (v813). 이미지가 오면 이렇게 바뀐다.
   9-slice(border-image)는 쓰지 않는다 — 늘어나는 가운데에서 도밍이 뭉개진다.
   비율을 코드에서 고정했으므로 통째로 늘려도 왜곡되지 않는다. */
#menu .menu-nav3 .menu-btn::before {
  background: url('./icons/ui/plate/normal.webp') center / 100% 100% no-repeat !important;
  box-shadow: none !important;   /* 음영은 그림 안에 있다 */
}
```

체크리스트
1. 파일명이 위 표와 **정확히** 일치 (`perma` `achieve` `chars` 주의)
2. 판: 320×320(정원) / 480×240 / 476×140 · **배지 안이 비었는지** · **평균 밝기 150 이상인지**
3. 아이콘: 256×256 · 모서리 알파 0(투명) · **29px 로 줄여서 알아볼 수 있는지**
4. `APP_VERSION` + `sw.js` 의 `CACHE` 동시 상향 (정적 에셋 cache-first)
