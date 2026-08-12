# 아크 제로 — 로비 UI 리소스 규격 (v809 기준)

> 메인 로비 버튼용. **라벨 판(배경) + 아이콘(글리프)을 분리**해서 받는다.
> 글자는 이미지에 넣지 않는다 — CSS 가 렌더한다(문구 수정·길이 대응 때문).
> 모든 수치는 실제 화면에서 잰 값이다(가로 폰 812×375 / 데스크톱 1280×800).

---

## 0. 한 줄 요약

```
라벨 판   icons/ui/plate/   3장   240×96 투명 WebP   9-slice(모서리 32px)
아이콘    icons/ui/menu/    10장  256×256 투명 WebP  표시 28~29px
```

⚠ **둘 다 투명 배경.** 이 게임의 *능력* 아이콘(`icons/abilities/`)만 **불투명 액자형**이다.
헷갈려서 액자형으로 만들면 판 위에 액자가 또 생긴다.

---

## 1. 라벨 판 — 3장

버튼의 배경이 되는 둥근 판. 글자와 아이콘이 이 위에 얹힌다.

| 파일 | 쓰이는 곳 | 색 방향 |
|---|---|---|
| `icons/ui/plate/normal.webp` | 하단 독 6개 · 코어관리 · 글로벌랭킹 | 반투명 하늘색 유리 |
| `icons/ui/plate/cta.webp` | **출격** (가장 중요한 버튼) | 진한 파랑, 가장 선명 |
| `icons/ui/plate/gold.webp` | 차원 스카우트(가챠) | 크림골드 |

### 규격

```
크기        240 × 96
모서리      각 변 32px 가 "늘어나지 않는 영역"  ← 9-slice 기준선
포맷        투명 WebP
```

### ⚠ 9-slice 를 반드시 지킬 것

버튼 폭이 화면마다 다르다(독 109~112px, 출격 171~200px). 이미지를 통째로 늘리면 모서리가
찌그러진다. 그래서 `border-image` 로 **모서리 32px 은 원본 그대로, 가운데만 늘린다.**

```
        32px          늘어남         32px
      ┌──────┬───────────────────┬──────┐
 32px │  ◜   │      상단 변       │   ◝  │
      ├──────┼───────────────────┼──────┤
 늘어 │ 좌변  │      가운데        │ 우변 │
      ├──────┼───────────────────┼──────┤
 32px │  ◟   │      하단 변       │   ◞  │
      └──────┴───────────────────┴──────┘
```

그리는 규칙:
- **모서리 32×32 안에 둥근 모서리와 테두리가 전부 들어가야 한다.** 넘치면 잘린다.
- **가운데 영역은 균일해야 한다.** 가로 그라디언트·무늬·로고를 넣으면 늘어날 때 뭉개진다.
  세로 방향 그라디언트(위 밝고 아래 어두운)는 괜찮다 — 가로로만 늘어나므로.
- 아이콘·글자를 판에 그려 넣지 말 것. 둘 다 따로 얹는다.

### 디자인 방향 — 말랑말랑

```
· 둥근 모서리(반경 14~18px 느낌). ⚠ 입체 렌더가 아니라 평면 패널이다
· 위쪽 밝고 아래쪽 살짝 어두운 세로 그라디언트 (2톤이면 충분)
· 아래 가장자리에 얇은 진한 띠 — "두께" 표현 (눌리면 사라지는 그 부분)
· 상단에 은은한 광택 하이라이트 한 줄
· 굵은 검정 외곽선 금지. 테두리는 밝은 반투명 흰빛으로 얇게
```

| 판 | 바탕 | 테두리 | 아래 두께띠 |
|---|---|---|---|
| `normal` | `rgba(238,248,255,.17)` → `rgba(150,190,235,.10)` 반투명 | `rgba(190,225,255,.34)` | `rgba(10,16,28,.42)` |
| `cta` | `#7fd4ff` → `#46a6f0` 불투명 | 없음 | `#2b6fae` |
| `gold` | `#ffe6a8` → `#f5c05a` 불투명 | 없음 | `#b8873a` |

`normal` 은 **반투명**이어야 한다 — 뒤의 캐릭터 일러가 비쳐야 로비 느낌이 산다.
`cta` 와 `gold` 는 불투명이어도 된다(가장 눈에 띄어야 하는 두 개).

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

```
Game UI button plate, 240x96, TRANSPARENT background, 9-slice safe.
A single rounded rectangle panel, {STYLE},
semi-flat vector panel (NOT a 3D render), rounded corners fully inside the outer 32 pixels,
vertical gradient only (lighter top, darker bottom), a thin darker band along
the bottom edge to suggest thickness, one subtle glossy highlight along the top.
The center area must be flat and uniform so it can stretch horizontally without artifacts.
No icon, no text, no numbers, no logo, no horizontal gradient, no pattern in the center,
no heavy black outline, no sharp corners.
```

`{STYLE}` 자리:
- `normal` → `translucent pale sky-blue frosted glass with a soft white rim`
- `cta` → `vivid sky-blue to azure (#7fd4ff to #46a6f0), opaque, the brightest of the set`
- `gold` → `warm cream to gold (#ffe6a8 to #f5c05a), opaque`

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
