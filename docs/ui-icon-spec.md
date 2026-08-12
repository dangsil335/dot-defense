# 아크 제로 — 메뉴 아이콘 리소스 규격 (v807 기준)

> 로비 버튼용 아이콘 세트. **아이콘만 이미지, 라벨 텍스트는 CSS 렌더**(안 A).
> 모든 수치는 실제 화면에서 잰 값이다(가로 폰 812×375 / 데스크톱 1280×800).

---

## 0. 한 줄 요약

```
폴더   icons/ui/menu/
포맷   256 × 256 · 투명 배경 WebP (또는 PNG)
표시   24px(가로 폰) ~ 34px(데스크톱)
스타일 둥글고 부푼 젤리/클레이. 파스텔 하늘색 계열. 굵은 외곽선 없음
```

⚠ **투명 배경 필수.** 이 게임의 *능력* 아이콘(`icons/abilities/`)은 **불투명 액자형**이라
정반대다. 헷갈려서 액자형으로 만들면 버튼 안에 액자가 또 생긴다.

---

## 1. 파일 목록 (10장)

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
| `start.webp` | `#startBtn` | 출격 / 새 게임 | ▶ | 게임 시작 (가장 중요한 CTA) |

---

## 2. 규격

```
캔버스   256 × 256 (정사각)
포맷     WebP 우선 (PNG 가능). 투명 배경 필수
용량     장당 30KB 이하 목표 — 10장 합쳐 300KB 이내
여백     상하좌우 8~12px 안전 여백. 가장자리에 붙이지 말 것
         (표시 24px 로 줄면 잘린 것처럼 보인다)
```

**표시 크기 (실측)**

| 화면 | 아이콘 | 버튼 |
|---|---|---|
| 가로 폰 812×375 | **24 × 24** | 109 × 43 |
| 데스크톱 1280×800 | **34 × 34** | 112 × 56 |

→ 256px 원본은 최소 표시(24px)의 **10배**다. 충분하고, 나중에 커져도 대응된다.

⚠ **24px 로 줄여도 뭔지 알아봐야 한다.** 가는 선·작은 글자·복잡한 디테일은 뭉개진다.
디자인 확정 전에 24px 로 축소해 보고 판단할 것.

---

## 3. 디자인 방향 — "말랑말랑"

지금 UI는 v807 에서 각진 SF 콘솔(skewX 네온 칩)에서 **둥근 젤리 버튼**으로 바꿨다.
아이콘도 같은 결이어야 한다.

**해야 할 것**
```
· 둥근 형태, 부푼 볼륨 (puffy / squishy / soft 3D)
· 클레이(clay) 또는 젤리 렌더 — 매트하고 말랑한 질감
· 파스텔 톤 — 하늘색·민트·크림·연보라
· 아래쪽에 부드러운 그림자로 떠 있는 느낌
· 위쪽에 은은한 광택 하이라이트 한 점
· 형태 1~2개로 단순하게
```

**하지 말 것**
```
✗ 굵은 검정 외곽선 (24px 로 줄면 뭉개진다)
✗ 각진 모서리·날카로운 사선 (지금 바꾼 방향과 반대)
✗ 네온 글로우·사이버펑크 (기존 콘솔 룩)
✗ 그라디언트 메시·복잡한 디테일
✗ 텍스트·숫자 (라벨은 CSS 가 렌더한다)
✗ 액자·배경판 (반드시 투명)
```

**팔레트** — 버튼 바탕이 반투명 하늘색 유리라 그 위에서 살아야 한다

```
주색    #7fd4ff  하늘        보조   #a8e6cf  민트
악센트  #ffe6a8  크림        포인트 #c9b8ff  연보라
그림자  rgba(20,40,70,0.28)   하이라이트 rgba(255,255,255,0.75)
```

---

## 4. 영문 프롬프트 템플릿

```
Soft 3D game UI icon, 256x256, TRANSPARENT background, no frame, no background plate.
{CONCEPT}
Squishy puffy clay-render style, rounded shapes, matte soft surface,
pastel sky-blue palette (#7fd4ff) with cream and mint accents,
gentle soft drop shadow below, one subtle glossy highlight on top.
Simple silhouette with only one or two clear elements —
must stay readable when scaled down to 24 pixels.
No outline strokes, no neon glow, no text, no numbers, no sharp angular edges.
```

**네거티브**
```
transparent background required, no background plate, no frame, no border,
text, numbers, letters, watermark, neon glow, cyberpunk, sharp angular edges,
thin lines, heavy black outline, cluttered detail, photorealistic, flat 2d vector
```

---

## 5. 개별 `{CONCEPT}`

### `shop.webp` — 강화소
```
a plump rounded wrench crossed with a small glowing upgrade arrow pointing up,
soft blue clay body with cream metal accents
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
a puffy rounded trophy cup with a small star on its front,
cream-gold body with soft blue base
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
a puffy rounded gacha capsule splitting open with a small star bursting out,
cream-gold capsule with sky-blue glow inside
```

### `start.webp` — 출격 (CTA)
```
a bold rounded play triangle with soft thick edges, floating on a small
cushion of light, bright sky-blue with a strong white highlight —
this is the primary action, make it the most vivid of the set
```

---

## 6. 세트 일관성 점검

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
`achieve` `scout` 만 크림골드를 써서 "보상 계열"로 묶고, 나머지는 하늘/민트로 통일한다.

---

## 7. 넣은 뒤 (내가 할 작업)

파일만 넣어주면 CSS 한 블록만 고치면 된다. 지금은 이모지로 자리를 잡아둔 상태다.

```css
/* 현재 (v807) */
#menu #shopBtn { --mb-emoji: '🔧'; }

/* 파일 투입 후 */
#menu #shopBtn { --mb-ico: url('./icons/ui/menu/shop.webp'); }
+ .menu-nav3 .menu-btn::after 의 content 를 '' 로
```

체크리스트
1. 파일명이 위 표와 **정확히** 일치 (`perma` `achieve` `chars` 주의)
2. 256×256 · 모서리 알파 0(투명) 확인
3. 24px 로 축소해서 알아볼 수 있는지 눈으로 확인
4. `APP_VERSION` + `sw.js` 의 `CACHE` 동시 상향 (정적 에셋 cache-first)
