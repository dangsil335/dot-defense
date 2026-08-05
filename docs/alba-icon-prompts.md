# 아크 제로 — 알바 능력 아이콘 6종 생성 프롬프트

- 저장 위치: `icons/abilities/<능력id>.png` — 파일명은 **능력 id 그대로** (대소문자까지)
- 규격: **256 × 256** PNG, **불투명 액자형 카드**
  - ⚠ 투명 배경 아님. `drawAbilityIcon` 은 `ctx.drawImage` 한 번만 하고 **배경판을 따로 깔지 않는다.**
    투명으로 뽑으면 어두운 UI 위에서 아이콘이 허공에 뜬 것처럼 보인다.
  - 실측 근거: 최근 추가분(플린타 킷 6종, 8-05)이 전부 액자형 · 모서리 alpha 255.
- 게임 표시 크기 약 **56px** → 작아도 읽히는 실루엣 필수
- 넣은 뒤 `APP_VERSION` + `sw.js` 의 `CACHE` 동시 상향 (정적 에셋 cache-first)
- 현재 `icons/abilities` 에 **223장** 있고, 알바 6종만 비어 있다(2026-08-05 실측).

---

## 0. 공통 프리앰블 (한 번만)

> 모바일 로그라이크 "아크 제로(ARC ZERO)"의 **스킬 아이콘** 6종을 만든다.
> 기존 223장과 한 세트로 보여야 한다.
>
> **규격**
> - 256 × 256 정사각형 PNG
> - **불투명 액자형 카드** — 어두운 배경판 + 얇은 테두리 프레임을 아이콘 안에 그린다
> - 게임에서 약 56px로 축소 → 실루엣이 뭉개지면 안 된다
>
> **스타일**
> - SF 판타지 게임 UI 아이콘. 굵고 명확한 형태, 강한 색 대비
> - 어두운 UI 위에 올라가므로 밝고 채도 높게, 발광 강조
> - 요소는 1~2개만. 디테일 과다 금지
> - 원근 없는 **정면·평면 구성**
> - **텍스트·숫자 절대 금지**
>
> 이 6종은 한 캐릭터(대검 기사 「알바」)의 킷이다. **6장이 한 세트로 보여야 한다** —
> 공통 색은 순백 은색 `#dfe6f2`, 공통 악센트는 푸른 미광 `#7fa8d4`, 금속은 백은.
> 반복 상징은 **양날 대검**, 특히 **날 한복판을 지나는 홈(fuller)** 이다.

---

## 1. 영문 템플릿

```
Game skill icon for a sci-fi fantasy mobile roguelike, 256x256 square card.
OPAQUE framed card: dark background plate with a thin ornate border frame — NOT transparent.
{CONCEPT}
Dominant color {HEX} with cool blue glow accents (#7fa8d4) and white-silver metal.
Bold readable silhouette that stays legible at 56px. Flat front-facing composition,
no perspective. Vibrant and high-contrast for a dark UI. One or two clear elements only.
No text, no numbers, no letters.
```

**네거티브**
```
transparent background, no background, floating element, text, numbers, letters, watermark,
photorealistic, cluttered detail, perspective, 3d render, character face, full character,
warm orange tint, fire, flames
```

> ⚠ 네거티브에 **주황/불꽃을 넣었다.** 플린타(불티·황동)와 팔레트가 섞이면 두 SSR 킷이 구분되지 않는다.

---

## 2. 6종 개별 `{CONCEPT}` / `{HEX}`

플린타는 「티어가 올라갈수록 뜨거워지는」 사다리였다. 알바는 **밤 → 새벽 → 일출**로 간다.
알바 팔레트는 원래 밝은 흰색이라 단순히 "위로 갈수록 밝게"를 쓰면 층이 안 갈린다.
그래서 **하위 티어는 날을 어둡게 두고 홈(fuller)만 빛나게** 하고, 상위 티어에서 빛이 터져나오게 잡았다.
이건 고유장비 설명과도 그대로 맞는다 — *"밤새 빛을 삼켰다가, 해가 뜨는 순간 한 줄기로 쏟아낸다."*

### ① `dawnEdge` — 여명의 칼날 (시작)
```
HEX: #dfe6f2
CONCEPT: a large double-edged greatsword standing upright point-up, blade in shadow,
the central fuller groove filled with cool blue light only about HALF WAY up from the guard,
a thin cross guard and a round pommel, night-dark background behind the blade.
```
> 킷의 얼굴. **홈이 절반만 차 있는** 게 이 캐릭의 규칙(충전)을 아이콘 하나로 설명한다.

### ② `risingArc` — 떠오르는 호 (tier2 조합)
```
HEX: #c8d8ea
CONCEPT: a wide upward-sweeping crescent slash arc rising from the bottom edge,
a greatsword blade at the end of the sweep, the arc trail brightening toward its top,
faint silver motes lifting along the curve.
```
> 조합 티어. 「아래에서 위로 솟는다」 — 실제 연출(`risingArc.draw`)의 호와 같은 모양.

### ③ `firstLight` — 첫 빛 (tier3 히든)
```
HEX: #eef3fa
CONCEPT: a flat horizon line of light stretching edge to edge across the middle,
a greatsword silhouette standing behind it, the light band blooming softly outward
above and below the line, dark sky above and dark ground below.
```
> 히든 티어. **가로 빛 띠** — 풀스크린 백광이 아니라 지평선이다(연출·설명과 일치, 눈 부담 규칙 준수).

### ④ `daybreak` — 일출 (tier4 히든)
```
HEX: #ffffff
CONCEPT: two greatsword slashes crossing in an X at the center, a blinding white light
pillar erupting upward from the crossing point, the blade's fuller now fully overflowing
with light, a wide shockwave ring blowing outward.
```
> 최상위 티어. 가장 밝고 가장 큼. **홈이 완전히 넘쳐흐른다** — ①의 「절반」과 대구.

### ⑤ `nightWatch` — 불침번 (★4)
```
HEX: #7fa8d4
CONCEPT: a greatsword planted point-down in the ground with a small hanging lantern
beside it, one single warm point of light in deep darkness, the blade's fuller
faintly glowing as it slowly charges, a crescent moon shape above.
```
> ★해금. 「충전 속도 ↑」를 **밤을 지키는 등불**로 — 스킨 '졸린 불침번'과 같은 모티프.

### ⑥ `whiteNight` — 백야 (★8)
```
HEX: #ffffff
CONCEPT: a greatsword whose fuller stays fully lit with steady white light that does not
fade, the surrounding night sky itself turned pale and bright, no darkness left in the
frame corners, a faint sun that never sets low on the horizon behind the blade.
```
> ★8 돌파. ⑤의 「어둠 속 한 점」을 뒤집어 **어둠이 사라진 화면** — 8★ 스토리(*"해가 지지 않는 밤"*)와 일치.

---

## 3. 세트 일관성 점검

| 아이콘 | 주색 | 핵심 형태 | 밝기 | 시간대 |
|---|---|---|---|---|
| dawnEdge | `#dfe6f2` | 세운 대검, **홈 절반 발광** | 낮음 | 밤 |
| risingArc | `#c8d8ea` | 위로 솟는 호 | 중간 | 여명 전 |
| firstLight | `#eef3fa` | **가로 지평선 빛 띠** | 중상 | 첫 빛 |
| daybreak | `#ffffff` | X자 참격 + 빛기둥 | **최고** | 일출 |
| nightWatch | `#7fa8d4` | 대검 + 등불, 초승달 | **최저** | 한밤 |
| whiteNight | `#ffffff` | 꺼지지 않는 홈, 밝은 밤 | 높음 | 백야 |

**대검이 5번 반복**된다(②만 호가 주인공). 그게 이 캐릭의 상징이므로 의도한 반복이다.
대구가 두 쌍 있다 — ①「홈 절반」↔ ④「홈 넘침」, ⑤「어둠 속 한 점」↔ ⑥「어둠이 없음」.

플린타 세트와 겹치지 않는지: 플린타는 **원형 실린더 + 주황 불티 + 황동**,
알바는 **세로 대검 + 푸른 미광 + 백은**. 형태축(원 ↔ 세로선)과 색축(따뜻 ↔ 차가움)이 모두 갈린다.

---

## 4. 넣은 뒤

1. 파일명이 능력 id와 정확히 일치하는지 확인 — `dawnEdge.png` 처럼 **대소문자까지** 같아야 한다
   (`nightWatch`, `whiteNight`, `firstLight` 는 카멜케이스 주의)
2. 256×256 · 모서리 alpha 255(불투명) 확인
3. `APP_VERSION` + `sw.js` `CACHE` 동시 상향
4. 게임에서 확인: 능력 카드 · 도감 · 진화 게이트 컷인에 뜨는지
   (없으면 `drawIconPlaceholder` 가 티어별 색 사각형으로 대체하므로 크래시는 안 난다)
