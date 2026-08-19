# 가챠 화면 리소스 — 한 번에 발주

> 레퍼런스: **명조(Wuthering Waves) 소환 화면**.
> 발주할 때 **레퍼런스 스크린샷을 같이 첨부**하고, 아래 각 항목의
> "레퍼런스에서 어디" 를 함께 알려주면 훨씬 정확하게 나온다.

---

## 0. 한눈에

| # | 항목 | 파일 | 캔버스 | 실제 표시 크기(실측) |
|---|---|---|---|---|
| ① | 재화 아이콘 3종 | `icons/ui/currency/*.webp` | 128×128 | **14px** |
| ② | 뽑기 버튼 판 2종 | `icons/ui/plate/pull*.webp` | 480×130 | 365×64 |
| ③ | 보조 원형 아이콘 3종 | `icons/ui/gacha/*.webp` | 128×128 | 약 28px |
| ④ | 픽업 캐릭터 프레임 | `icons/ui/gacha/pickup-frame.webp` | 256×256 | 26px |
| ⑤ | 상시 배너 아트 | `icons/gacha-standard.webp` | 1920×1080 | 화면 전체 배경 |

①②③④ 는 **투명 WebP**. ⑤ 만 불투명이다.

⚠ **레퍼런스와 우리의 결정적 차이 — 우리는 한글이다.**
레퍼런스 버튼에는 `Convene ×1` 같은 영문이 새겨져 있지만
**이미지에 글자를 넣으면 안 된다.** 이미지 생성 AI 는 한글을 못 쓴다.
글자는 전부 CSS 가 얹으므로 **판과 아이콘만** 그린다.

---

## ① 재화 아이콘 3종 ⭐ 효과가 가장 크다

**어디에 쓰나** — 화면 우상단 재화 칩 3개 + 뽑기 버튼 안의 비용 표시.
**한 번 만들면 두 곳이 같이 좋아진다.**

**레퍼런스에서 어디** — 상단 중앙의 `✦ 74 +` / `◈ 0 +` 칩에 붙은 동그란 보석 아이콘.

**지금 상태** — 이모지 💎 ⭐ 💠 를 그대로 쓴다. 기기마다 모양이 달라지고 톤도 안 맞는다.

```
위치  icons/ui/currency/
파일  crystal.webp    💎 크리스탈   — 뽑기에 쓰는 주 재화
      stardust.webp   ⭐ 스타더스트 — 강화 재화
      shard.webp      💠 별조각     — 별조각 상점 재화
크기  128 × 128 투명 WebP
```

**프롬프트**

```
A single game currency icon, 128x128, TRANSPARENT background (alpha channel).
ONE object only, centered, filling about 82% of the canvas.

{SUBJECT}

Style: chunky semi-flat game UI icon in the style of Blue Archive and Stella Sora.
Built from 2-3 large simple shapes with generously rounded corners.
Flat saturated fill plus ONE lighter tint on the upper-left face and one deeper
tone on the lower-right. One small white specular dot as a highlight.
A clean continuous white outline about 5% of the icon width around the silhouette.

It must stay readable when shrunk to 14 pixels — that is the actual display size.
No text, no letters, no numbers, no logo, no watermark, no background.
```

| 파일 | `{SUBJECT}` |
|---|---|
| `crystal` | `A cut gemstone crystal shaped like a tall hexagonal diamond, seen from the front. Bright cyan blue #6fd0ff with a lighter icy top facet and a deeper blue base.` |
| `stardust` | `A five-pointed star with slightly rounded points, with two small sparkle dots beside it. Warm gold #ffd479 with a paler gold upper face.` |
| `shard` | `A single angular crystal shard, like a broken piece of a larger gem, tilted slightly. Soft violet #c9a3ff with a pale lilac upper facet.` |

⚠ **14px 이 진짜 표시 크기다.** 디테일을 넣으면 뭉개진다. 덩어리 2~3개가 한계다.

---

## ② 뽑기 버튼 판 2종

**어디에 쓰나** — 화면 하단 우측 `1회 뽑기` / `10회 뽑기` 버튼의 바탕.

**레퍼런스에서 어디** — 하단 우측의 `×1 Convene ×1` / `×10 Convene ×10` 두 버튼.
금테를 두른 캡슐이고, 10회 쪽이 더 화려하다.

**지금 상태** — 365×64, 모서리 8px, 반투명 배경 + 얇은 하늘색 테두리. 밋밋하다.

```
위치  icons/ui/plate/
파일  pull1.webp     1회 — 은/청동 톤 (보조 행동)
      pull10.webp   10회 — 금 톤 (주 행동, 더 화려하게)
크기  480 × 130  (약 3.7:1)   투명 WebP
```

⚠ 실제 버튼은 5.71:1 이지만 **판은 3.7:1 로 그린다.**
`background-size: 100% 100%` 로 늘려 쓰므로 파일 비율과 버튼 비율이 맞아야 안 찌그러진다.
**버튼 비율은 내가 판에 맞춰 조정한다** — 그림은 3.7:1 이 보기 좋다.

**프롬프트**

```
A horizontal game UI button plate, {SIZE} canvas,
TRANSPARENT background (alpha channel).

THE PLATE FILLS THE CANVAS — about 94% of the width and 86% of the height, centered.
It is NOT a small object in empty space. Leave margin only for its own soft shadow.

Shape: one long capsule with fully rounded ends. Around it runs a decorative
metal frame about 6% of the plate height, with a small ornamental notch at each end.
The inside of the plate is a smooth EMPTY panel — completely plain, no text,
no lines, no engraving. Text is added separately.

{COLOR}

Soft satin metal — a gentle sheen, not a mirror. A thin bright line along the top
inner edge, and a soft shadow settling along the bottom inner edge.
A soft contact shadow beneath the plate, kept inside the canvas.

Anime mobile game UI, clean and premium. Bright in tone, NOT dark, NOT black.
No text, no letters, no numbers, no logo, no icon, no watermark.
```

| 파일 | `{SIZE}` | `{COLOR}` |
|---|---|---|
| `pull1` | `480x130` | `Cool silver and pale steel blue: #dfe8f2 panel with a brushed silver frame #9fb4cb. Restrained, clearly the secondary button.` |
| `pull10` | `480x130` | `Warm gold: #ffe9b8 panel with a rich gold frame #d8ac52, and a faint warm glow along the frame. This is the primary action — make it clearly richer than the silver one.` |

---

## ③ 보조 원형 아이콘 3종

**어디에 쓰나** — 화면 하단 좌측. 지금은 `⭐ 4,000 → 💎 1` 글자 버튼 하나뿐이다.
레퍼런스처럼 작은 원형 아이콘 줄로 바꾼다.

**레퍼런스에서 어디** — 하단 좌측의 작은 원형 버튼 3개(수레 / 목록 / 느낌표 아이콘).

```
위치  icons/ui/gacha/
파일  exchange.webp   교환   — 스타더스트를 크리스탈로
      history.webp    기록   — 뽑기 기록
      rates.webp      확률표 — 확률 상세
크기  128 × 128 투명 WebP
```

**프롬프트** — ① 의 STYLE 블록을 **그대로** 쓰고 `{SUBJECT}` 만 바꾼다.

| 파일 | `{SUBJECT}` |
|---|---|
| `exchange` | `Two curved arrows forming a circle, one pointing clockwise and one counter-clockwise, like a swap symbol. Sky blue #4EA8E8 with a lighter upper arrow.` |
| `history` | `A list card: a rounded rectangle with three short horizontal lines and a small round bullet beside each. Mint green #43C7A4 with a white paper face.` |
| `rates` | `A small rounded document with a simple pie chart on it, one slice highlighted. Soft purple #9A7DF0 with a white face.` |

---

## ④ 픽업 캐릭터 프레임

**어디에 쓰나** — 배너 정보 아래 픽업 캐릭터 얼굴 칩. 지금은 테두리 없이 얼굴만 뜬다.

**레퍼런스에서 어디** — `4-star Resonators Drop Rate Up` 아래 캐릭터 얼굴 3개.
각 얼굴이 프레임 안에 들어가 있고 등급색 테두리가 둘러져 있다.

```
위치  icons/ui/gacha/
파일  pickup-frame.webp
크기  256 × 256 투명 WebP
```

⚠ **가운데가 완전히 뚫려 있어야 한다.** 캐릭터 얼굴이 그 구멍으로 보인다.
테두리만 그리는 것이다.

**프롬프트**

```
A single hexagonal UI frame ring, 256x256, TRANSPARENT background (alpha channel).

ONLY THE FRAME — the entire center is EMPTY and fully transparent, like a window.
A character portrait will show through the hole. Do not draw anything inside it.

The frame is a hexagon outline about 9% of the canvas width thick,
with a small ornamental notch at the top vertex and the bottom vertex.
Soft satin metal in warm gold #d8ac52, with a thin bright line along the upper edge
and a deeper tone along the lower edge.

No text, no letters, no numbers, no portrait, no face, no fill in the middle,
no background, no watermark.
```

---

## ⑤ 상시 배너 아트

별도 문서에 이미 있다 → **[docs/ui-gacha-banner.md](./ui-gacha-banner.md)**
1920×1080, 차원문 + 레이더 스캔, 인물 없음.

---

## 네거티브 — ①③④ 아이콘 공통

```
photorealistic, photo, 3d render, clay, plastic, chrome, glass,
line art, outline only, thin lines, sketch, watercolor, painterly,
text, letters, numbers, korean, hangul, logo, watermark, signature,
background, solid background, gradient background, shadow cast on background,
green screen, chroma key,
dark, muddy, desaturated, neon glow, cyberpunk,
cluttered, many small elements, tiny details, scattered parts
```

## 네거티브 — ② 판 공통

```
text, letters, numbers, korean, hangul, engraving, embossed text,
icon inside, symbol inside, ornament inside the panel,
small object, floating in empty space, object with large empty margins,
dark, black, charcoal, navy, low key,
glossy, mirror reflection, wet look, large white blob,
flat, flat design, 2d, sticker, paper,
background, solid background, green screen, chroma key,
isometric, perspective tilt, side view
```

⚠ `korean, hangul` 을 반드시 넣을 것 — 안 넣으면 모델이 깨진 한글을 새겨 넣는다.

---

## 통과 기준 — 받으면 내가 숫자로 확인한다

| 항목 | 기준 |
|---|---|
| ① 재화 | 128×128 · 가장자리 알파 0 · **14px 로 줄여서 뭔지 읽히는가** |
| ② 판 | 480×130 · 가로 90% 이상 채움 · 평균 밝기 150 이상 · 안쪽에 글자/무늬 없음 |
| ③ 보조 | 128×128 · 가장자리 알파 0 · 28px 에서 읽히는가 |
| ④ 프레임 | 256×256 · **가운데 알파 0** (실제로 뚫려 있는가) |
| ⑤ 배너 | 1920×1080 · 사람 없음 · 좌우 12% 단순 |

---

## 우선순위

한 번에 다 못 뽑겠으면 이 순서를 권한다.

1. **① 재화 아이콘** — 이모지라 제일 티가 나고, 두 곳에서 동시에 쓰인다
2. **② 뽑기 버튼 판** — 화면에서 가장 큰 조작 요소다
3. **⑤ 상시 배너** — 지금 파일이 없어 텍스트 폴백이 뜬다
4. ④ 픽업 프레임 → ③ 보조 아이콘
