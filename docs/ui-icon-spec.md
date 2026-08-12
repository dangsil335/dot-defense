# 아크 제로 — 로비 UI 리소스 규격 (v809 기준)

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

## 1. 라벨 판 — 3장  (2차 개정: 9-slice 폐기 → 비율 고정 전체 아트)

버튼의 배경이 되는 판. 글자와 아이콘은 CSS 가 위에 얹는다.

### ⚠ 1차 실패와 방향 전환

1차 판은 **납작한 흰 판 + 회색 막대**로 와서 젤리가 아니라 "목록 행"으로 보였다.
원인은 내 프롬프트의 `thin darker band` / `vertical gradient only` 다 — 볼륨을 지워버렸다.

그 뒤 CSS 로 형태를 먼저 확정했고(v812), **형태는 이걸로 맞다**는 확인을 받았다.
남은 것은 **질감**뿐이다. 그래서 2차 발주의 목표는 딱 하나다:

> 아래 CSS 와 같은 형태·색·음영을 유지하면서, **실리콘 표면 질감만 얹는다.**

그리고 **9-slice 를 폐기한다.** 늘어나는 가운데 영역에서는 질감이 뭉개지기 때문이다.
대신 버튼 비율을 코드에서 고정했으므로, 이미지를 통째로 늘려도 왜곡되지 않는다.

### 파일과 비율

| 파일 | 쓰이는 곳 | 캔버스 | 비율 |
|---|---|---|---|
| `icons/ui/plate/normal.webp` | 하단 독 6개 · 코어관리 · 글로벌랭킹 | **450 × 200** | 9:4 (코드에서 고정됨) |
| `icons/ui/plate/cta.webp` | **출격** | **500 × 200** | 5:2 |
| `icons/ui/plate/gold.webp` | 차원 스카우트 | **600 × 120** | 5:1 |

포맷: 투명 WebP. 모서리 바깥은 완전 투명(알파 0).

### 현재 CSS 값 = 목표 형태 (이 수치를 그대로 재현할 것)

```css
/* normal — 매트 흰 실리콘 */
border-radius: 999px;                                  /* 완전한 캡슐 */
background: linear-gradient(180deg,
  rgba(255,255,255,0.97) 0%,
  rgba(246,249,253,0.95) 52%,
  rgba(230,237,246,0.94) 100%);
box-shadow:
  0 3px 0 rgba(196,208,224,0.9),      /* ① 아래 립 — 얇게 3px, 옅은 회청 */
  0 6px 13px rgba(40,60,92,0.20),     /* ② 넓은 외부 그림자 */
  0 1px 2px rgba(40,60,92,0.10),      /* ③ 좁은 접지 그림자 */
  inset 0 2px 0 rgba(255,255,255,1),  /* ④ 위쪽 하이라이트 */
  inset 0 -3px 6px rgba(202,214,231,0.5); /* ⑤ 아래 안쪽 음영 */

/* cta */   #8fcdf2 → #6bb4e4 → #4f9bd2,  립 4px #3d7fae
/* gold */  #f8e6bc → #eed392 → #dfbc6e,  립 3px #b39a63
```

**①~⑤ 다섯 층이 전부 보여야 한다.** 하나라도 빠지면 1차처럼 납작해진다.

### 질감 — 이게 2차의 유일한 추가분

```
· 아주 미세한 매트 그레인 — 실리콘/소프트터치 플라스틱 표면. 노이즈가 보이면 안 되고
  "완벽하게 매끈하지 않다"는 인상만 남을 정도
· 광택은 균일하지 않게 — 위쪽 하이라이트가 한쪽으로 살짝 치우치거나 세기가 변한다.
  CSS 그라디언트가 너무 완벽해서 플라스틱처럼 보이는 부분이다
· 가장자리에 아주 옅은 빛 투과 — 얇은 실리콘에 빛이 스미는 느낌
· 유광 반사·거울 하이라이트 금지. 어디까지나 매트다
```

### 영문 프롬프트

```
Soft-touch silicone UI button plate, {SIZE}, TRANSPARENT background (alpha), nothing outside the shape.
A single {SHAPE} pill-shaped pad, fully rounded ends (capsule, radius = half the height).
{COLOR}
Matte soft-touch surface with a very fine subtle grain — not glossy, not mirror-like.
Volume comes from five layers, all must be visible:
  a thin darker lip along the bottom edge (about 1.5% of height),
  a soft wide shadow under the pad,
  a tight contact shadow right beneath it,
  a bright thin highlight along the very top inner edge,
  a soft inner shading along the bottom inner edge.
The top highlight should be slightly uneven in strength, like real silicone, not a perfect gradient.
A faint hint of light passing through the thinnest edges.
Premium, restrained, physical product look — like a white silicone keycap or a cat paw pad toy.
No icon, no text, no numbers, no logo, no pattern, no glossy reflection, no heavy outline.
```

`{SIZE}` / `{SHAPE}` / `{COLOR}`:

| 파일 | SIZE | SHAPE | COLOR |
|---|---|---|---|
| `normal` | `450x200` | `wide` | `Off-white, almost neutral: #ffffff at the top fading to #e6edf6 at the bottom, with a cool grey-blue lip #c4d0e0` |
| `cta` | `500x200` | `wide` | `Soft desaturated sky blue: #8fcdf2 top to #4f9bd2 bottom, with a deeper blue lip #3d7fae` |
| `gold` | `600x120` | `very wide` | `Muted warm cream: #f8e6bc top to #dfbc6e bottom, with a soft bronze lip #b39a63` |

**네거티브**
```
glossy, mirror reflection, specular highlight, chrome, metal, wet look,
9-slice, tiling, seamless pattern, texture pattern, noise overlay,
icon, text, numbers, letters, logo, border, frame, outline,
flat design, sharp corners, angular, neon, gradient banding,
background, green screen, chroma key, drop shadow outside the canvas
```

### 넣은 뒤

비율이 코드에서 고정돼 있으므로 `background-size: 100% 100%` 로 그대로 늘려 쓴다.
9-slice(`border-image`)는 쓰지 않는다.

⚠ 지금 CTA(출격)와 가챠는 비율이 화면마다 다르다(출격 3.04:1 ↔ 2.60:1). 판 이미지를
넣을 때 내가 `aspect-ratio` 로 고정한다 — 독(9:4)은 이미 고정돼 있다.

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

→ **1절로 옮겼다.** 구 프롬프트(240x96 · 9-slice)는 1차 실패본이라 삭제했다.

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
/* 현재 (v807~809) */
#menu #shopBtn { --mb-emoji: '🔧'; }
#menu .menu-btn::before { background: linear-gradient(...); }   /* CSS 로 그린 젤리 */

/* 파일 투입 후 */
#menu .menu-btn::before {
  border-image: url('./icons/ui/plate/normal.webp') 32 fill / 32px stretch;
}
#menu #shopBtn { --mb-ico: url('./icons/ui/menu/shop.webp'); }
```

체크리스트
1. 파일명이 위 표와 **정확히** 일치 (`perma` `achieve` `chars` 주의)
2. 판: 240×96 · 모서리 32px 안에 둥근 모서리가 전부 들어갔는지 · 가운데 균일한지
3. 아이콘: 256×256 · 모서리 알파 0(투명) · **29px 로 줄여서 알아볼 수 있는지**
4. `APP_VERSION` + `sw.js` 의 `CACHE` 동시 상향 (정적 에셋 cache-first)
