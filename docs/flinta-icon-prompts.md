# 아크 제로 — 플린타 능력 아이콘 6종 생성 프롬프트

- 저장 위치: `icons/abilities/<능력id>.png` — 파일명은 **능력 id 그대로**
- 규격: **256 × 256** PNG, **불투명 액자형 카드**
  - ⚠ 투명 배경 아님. `drawAbilityIcon` 은 `ctx.drawImage` 한 번만 하고 **배경판을 따로 깔지 않는다.**
    투명으로 뽑으면 어두운 UI 위에서 아이콘이 허공에 뜬 것처럼 보인다.
  - 실측 근거: 최근 추가분(페리아 킷 6종, 7-30)이 전부 액자형 · 모서리 alpha 255.
- 게임 표시 크기 약 **56px** → 작아도 읽히는 실루엣 필수
- 넣은 뒤 `APP_VERSION` + `sw.js` 의 `CACHE` 동시 상향 (정적 에셋 cache-first)

---

## 0. 공통 프리앰블 (한 번만)

> 모바일 로그라이크 "아크 제로(ARC ZERO)"의 **스킬 아이콘** 6종을 만든다.
> 기존 219개와 한 세트로 보여야 한다.
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
> 이 6종은 한 캐릭터(총잡이 「플린타」)의 킷이다. **6장이 한 세트로 보여야 한다** —
> 공통 색은 와인레드 `#b0324a`, 공통 악센트는 주황 불티 `#ff8a3d`, 금속은 황동.

---

## 1. 영문 템플릿

```
Game skill icon for a sci-fi fantasy mobile roguelike, 256x256 square card.
OPAQUE framed card: dark background plate with a thin ornate border frame — NOT transparent.
{CONCEPT}
Dominant color {HEX} with glowing orange ember accents (#ff8a3d) and brass metal.
Bold readable silhouette that stays legible at 56px. Flat front-facing composition,
no perspective. Vibrant and high-contrast for a dark UI. One or two clear elements only.
No text, no numbers, no letters.
```

**네거티브**
```
transparent background, no background, floating element, text, numbers, letters, watermark,
photorealistic, cluttered detail, perspective, 3d render, character face, full character
```

---

## 2. 6종 개별 `{CONCEPT}` / `{HEX}`

세트로 보이게 하되 **티어가 올라갈수록 화면이 뜨겁고 복잡**해지도록 잡았다.

### ① `flintShot` — 부싯돌 사격 (시작)
```
HEX: #b0324a
CONCEPT: a single ornate revolver cylinder seen face-on, six chambers arranged in a circle,
five chambers dark and empty, ONE chamber glowing hot orange — the last bullet.
a few small orange sparks struck from a flint-and-steel striker at the top.
```
> 킷의 얼굴. **여섯 칸 중 한 칸만 발광** — 이 캐릭의 규칙이 아이콘 하나로 설명된다.

### ② `hammerFall` — 공이 낙하 (tier2 조합)
```
HEX: #ff8a3d
CONCEPT: a heavy revolver hammer striking down onto a flint plate,
the impact point bursting into a sharp radial spray of orange sparks,
a brass cartridge base visible beneath the strike.
```
> 조합 티어. 「내려친다 → 불티가 터진다」가 한눈에.

### ③ `fanTheHammer` — 연속 격발 (tier3 히든)
```
HEX: #ff8a3d
CONCEPT: a revolver seen from the side with a gloved hand fanning the hammer,
SIX overlapping muzzle flashes fanned out in an arc from the barrel,
dense orange sparks trailing, brass casings ejecting.
```
> 히든 티어. **여섯 갈래 총구 화염**이 「잔탄 전부」를 시각화한다.

### ④ `finalChamber` — 최후의 약실 (tier4 히든)
```
HEX: #b0324a
CONCEPT: a single massive brass cartridge standing upright, cracked open and
overflowing with concentrated white-hot light, a wide shockwave ring blowing outward,
the revolver cylinder shattering apart behind it.
```
> 최상위 티어. 가장 밝고 가장 큼. **흰빛**을 써서 나머지 5종과 격을 벌린다.

### ⑤ `quickdraw` — 속사 (★4)
```
HEX: #ffb15c
CONCEPT: a revolver cylinder snapping shut with a speed-blur arc,
six fresh brass cartridges sliding into place simultaneously,
motion streaks and a bright flash at the closing seam.
```
> ★해금. 「즉시 재장전」 — **닫히는 실린더 + 속도선**.

### ⑥ `deadeye` — 데드아이 (★8)
```
HEX: #b0324a
CONCEPT: a glowing crosshair reticle burned over a revolver cylinder where
ALL SIX chambers glow hot orange at once, converging aim lines pulling into the center,
a faint eye shape formed by the reticle.
```
> ★8 돌파. ①의 「한 칸만 발광」을 뒤집어 **여섯 칸 전부 발광** — 능력 설명(전탄이 마지막 한 발)과 일치.

---

## 3. 세트 일관성 점검

| 아이콘 | 주색 | 핵심 형태 | 밝기 |
|---|---|---|---|
| flintShot | `#b0324a` | 실린더 정면, **1칸 발광** | 낮음 |
| hammerFall | `#ff8a3d` | 공이 + 방사 불티 | 중간 |
| fanTheHammer | `#ff8a3d` | 6갈래 총구 화염 | 높음 |
| finalChamber | `#b0324a` | 갈라진 탄피 + 충격파 | **최고(흰빛)** |
| quickdraw | `#ffb15c` | 닫히는 실린더 + 속도선 | 중간 |
| deadeye | `#b0324a` | 조준선 + **6칸 전부 발광** | 높음 |

**실린더가 4번 반복**된다(①④⑤⑥). 그게 이 캐릭의 상징이므로 의도한 반복이고,
①과 ⑥이 「1칸 ↔ 6칸」으로 대구를 이룬다.

---

## 4. 넣은 뒤

1. 파일명이 능력 id와 정확히 일치하는지 확인 — `flintShot.png` 처럼 **대소문자까지** 같아야 한다
2. 256×256 · 모서리 alpha 255(불투명) 확인
3. `APP_VERSION` + `sw.js` `CACHE` 동시 상향
4. 게임에서 확인: 능력 카드 · 도감 · 진화 게이트 컷인에 뜨는지
   (없으면 `drawIconPlaceholder` 가 티어별 색 사각형으로 대체하므로 크래시는 안 난다)
