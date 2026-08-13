# 아크 제로 — 로비 UI 리소스 규격 (v823 기준)

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

### 5차 결과 — 색은 잡혔다. 남은 두 가지

밝기 250 / 230 / 230 으로 밝아졌고 배지 안도 비었다. 남은 문제는 형태다.

| 문제 | 고칠 문장 |
|---|---|
| 흰 광택이 크고 불규칙한 얼룩처럼 번진다 | `The top highlight is a THIN EVEN BAND hugging the top edge of the plate, about 12% of the plate height. It must NOT be a large irregular patch, a blob, or a puddle.` |
| 배지가 판 밖으로 삐져나온다 | `The badge well is entirely INSIDE the plate outline, with a clear margin on all sides. It must never touch or cross the plate edge.` |

네거티브에 추가:
```
large white blob, glossy blob, wet highlight, melted highlight, puddle, liquid,
bubble, water droplet, shape sticking out, overlapping shapes, badge outside the plate
```
⚠ `flat` 은 **판에서만** 네거티브. 아이콘(§2)은 정반대이니 프롬프트를 섞지 말 것.

### 통과 기준

1. 캔버스가 위 표와 일치 (320×320 / 480×240 / 476×140)
2. **배지 안이 비어 있는가.** 그림이 하나라도 있으면 실패 — 우리 아이콘이 못 들어간다
3. **밝은가.** 불투명 픽셀 평균 밝기가 150 이상이어야 한다 (4차는 76/51/36 이었다)
4. 판 바깥 알파 0, 접지 그림자가 캔버스 안
5. 가운데를 세로로 자를 때 위쪽이 볼록 (직선이면 실패)
6. 유광 반사 없음, 글자·테두리 없음

---

## 2. 메뉴 아이콘 — 10장  (2차 발주)

⚠ 아이콘 관련 내용은 **전부 이 절에만** 둔다.
1차 때 §2·§3·§4·§5·§6 다섯 군데에 흩어져 있었고, 판이 2차에서 실패한 이유가
정확히 그거였다(뒤쪽에 남은 옛 사본을 보고 만들었다). 사본을 만들지 말 것.

### 1차 결과 — 10장 중 5장이 못 쓴다

40px 로 줄여서 무엇인지 알아볼 수 있는지로 판정했다.

| 파일 | 의도 | 실제로 보이는 것 | |
|---|---|---|---|
| `shop` | 렌치 + 상승 화살표 | 색 블록 덩어리 | ❌ |
| `perma` | 나선 | `OXO` 글자처럼 보임 | ❌ |
| `chars` | 인물 2명 | 그냥 원 3개 | ❌ |
| `scout` | 캡슐 | 정체불명의 고리 | ❌ |
| `achieve` | 트로피 | 왕관처럼 뭉개짐 | ❌ |
| `codex` `records` `core` `rank` `start` | | 읽힌다 | ✅ |

**원인 둘**

1. **주제를 이름으로만 줬다.** "a wrench crossed with an upgrade arrow" 라고 하면
   모델이 알아서 해석해 덩어리를 만든다. **기하로 묘사해야 한다** — 어느 방향으로
   몇 개의 덩어리가 어떻게 놓이는지.
2. **열 장을 따로 뽑았다.** 그래서 선 두께·채도·명암이 제각각이라 한 세트로 안 보인다.

### ⭐ 이번엔 한 장에 열 개를 함께 뽑는다

따로 열 번 뽑으면 반드시 그림체가 갈린다. **하나의 시트로 한 번에** 그리게 하면
모델이 열 개를 서로 보면서 그리므로 통일된다.

```
2행 5열, 셀 하나가 정사각, 전체 1280 x 512
배경 완전 투명, 셀 사이 여백 균일, 각 아이콘은 자기 셀 중앙
순서:  1행  shop  codex  perma  achieve  chars
       2행  records  core  rank  scout  start
```

받으면 내가 잘라서 256×256 으로 정규화한다 (`python tools/slice_icon_sheet.py <파일>`).
시트가 안 되면 낱장 10회로 가되, **아래 STYLE 블록을 글자 하나 바꾸지 말고** 매번
그대로 앞에 붙일 것. 그게 유일한 통일 장치다.

### STYLE 블록 — 열 장 모두 여기까지 동일

```
Cute mobile game menu icon, in the style of Blue Archive / Stella Sora lobby UI.

Drawn as a DIE-CUT STICKER: the entire icon is wrapped by ONE continuous clean
WHITE BORDER about 6% of the icon width, following only the outer silhouette.
Inside that border the icon is built from 2 to 4 large chunky shapes with
generously rounded corners. No thin lines anywhere. No small details.

Each shape is filled with one flat saturated color, plus ONE lighter tint over its
upper-left portion to suggest a single soft light from the upper left, and one
slightly deeper tone on the lower-right. Shading is flat color areas, not blur,
not airbrush, not gradient mesh.

Bright, cheerful, high contrast, clean and confident.
Fully TRANSPARENT background (alpha) — nothing behind the icon.
Centered, filling about 84% of its square cell.
It must stay instantly recognizable when shrunk to 40 pixels.
```

### 팔레트 — 열 장이 공유한다

```
sky blue    #4EA8E8   밝은 면 #9FD9F8
warm gold   #F2B33C   밝은 면 #FFDE93
mint green  #43C7A4   밝은 면 #96E8D0
soft purple #9A7DF0   밝은 면 #C9B8FB
white       #FFFFFF
```

### 주제 — 이름이 아니라 기하로 적는다

| 파일 | 쓰임 | SUBJECT (영문 그대로 붙일 것) |
|---|---|---|
| `shop` | 강화소 | `A thick upward-pointing arrow with a wide head and a short wide shaft, rising from a small rounded platform beneath it. Arrow in sky blue, platform in warm gold.` |
| `codex` | 도감 | `An open book seen straight from the front, symmetric, two pages spread flat, three short horizontal lines on each page. Sky blue cover, cream-white pages.` |
| `perma` | 능력 영구 | `A simple skill tree: one large round node at the bottom center and two smaller round nodes above it to the left and right, joined by two thick straight branches. Mint green.` |
| `achieve` | 업적 | `A trophy cup with two curved side handles standing on a short square base, and one five-pointed white star on the front of the cup. Warm gold.` |
| `chars` | 캐릭터·진화 | `Two simple person figures side by side, each a round head above a rounded shoulder shape. The front figure is larger and sky blue, the back figure is smaller, soft purple, and partly hidden behind it.` |
| `records` | 기록 | `A clipboard seen straight from the front with a small clip at the top center and three list rows, each row one round bullet and one short bar. Sky blue board, white paper.` |
| `core` | 코어 관리 | `A hexagonal gem seen flat from the front with one bright round core at its center, the upper-left facets lighter. Mint green.` |
| `rank` | 글로벌 랭킹 | `A globe: a circle with one horizontal band across the middle and one vertical oval meridian, wearing a small three-point crown on top. Sky blue globe, warm gold crown.` |
| `scout` | 차원 스카우트 | `A gacha capsule: a sphere split across its middle by a thin white band, the top half lighter and the bottom half deeper, with two four-pointed sparkles floating beside it. Warm gold.` |
| `start` | 출격 | `A bold right-pointing play triangle with softly rounded corners, with a short rounded vertical bar just to its left. Vivid sky blue — this is the primary action, make it the most saturated icon of the set.` |

`achieve` `scout` 만 골드로 "보상 계열"을 묶고, 나머지는 하늘·민트·보라로 간다.
`start` 가 세트에서 가장 선명해야 한다 — 유일한 주요 행동 버튼이다.

### 네거티브 (아이콘 공통)

```
photorealistic, photo, 3d render, clay, claymation, plastic, metal, chrome, glass,
line art, outline only, thin lines, sketch, pencil, watercolor, painterly, brush texture,
abstract, geometric abstraction, random shapes, unrecognizable blob,
text, letters, numbers, logo, watermark, signature, button, panel, frame, badge,
background, solid background, gradient background, shadow cast on background,
green screen, chroma key,
dark, muddy, desaturated, neon glow, cyberpunk, sci-fi,
cluttered, many small elements, scattered parts
```

⚠ `flat 2d vector` 를 네거티브에 넣지 말 것 — 우리가 원하는 게 그거다.
⚠ 판(§1)과 정반대다. 판은 입체가 필요하고 `flat` 이 네거티브다. 프롬프트를 섞지 말 것.

### 규격

```
파일 위치   icons/ui/menu/
파일명      shop codex perma achieve chars records core rank scout start  (.webp)
캔버스      256 x 256
배경        완전 투명 (알파). ⚠ 능력 아이콘(icons/abilities/)만 불투명 액자형이다
표시 크기   독에서 약 40px
```

### 통과 기준 — 내가 숫자와 눈으로 확인한다

1. 256×256, 가장자리 알파 0
2. **40px 로 줄였을 때 무엇인지 읽히는가** — 어두운 띠 위에 얹어서 본다. 1차는 5장이 여기서 죽었다
3. 흰 외곽 테두리가 하나로 이어져 있는가
4. 팔레트가 위 표 안에 있는가 (열 장이 한 세트로 보이는가)
5. 글자·배경·액자 없음

---

## 3. 넣은 뒤 (내가 할 작업)

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
