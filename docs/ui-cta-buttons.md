# 메인 원형 버튼 — 2장 (차원 스카우트 · 새 게임)

> 지금은 가로 판 + 좌측 배지 + 글자다. 그걸 **원형 버튼 이미지**로 바꾼다.
> 하단 독의 발바닥 버튼과 같은 문법이 된다 — 원 + 아래 글자.

---

## 0. ⚠ 먼저: 글자는 그림에 넣지 않는다

> **이미지 생성 AI 는 한글을 못 쓴다.** "차원 스카우트"를 그림 안에 넣으라고 하면
> 한글처럼 생긴 깨진 글자가 나온다. 영어도 자주 틀린다.

그래서 **그림에는 아이콘만** 넣고, 글자는 지금처럼 CSS 가 원 아래에 얹는다.
독의 발바닥 버튼이 이미 그 구조이고 잘 읽힌다.

```
   ╭─────────╮
   │  레이더  │   ← 이미지 (원형 버튼 + 아이콘)
   ╰─────────╯
   차원 스카우트   ← CSS 글자 (낙서체)
```

글자를 아예 빼고 아이콘만 둘 수도 있지만, 함장이 예전에
"어떤 버튼인지도 모르겠고"라고 했던 게 글자가 없어서였다. 아래 글자는 남기는 걸 권한다.

---

## 1. 파일과 규격

```
위치    icons/ui/cta/
파일    scout.webp   (차원 스카우트)
        start.webp   (새 게임)
크기    512 × 512
포맷    투명 WebP. 원 바깥은 알파 0
```

⚠ `icons/ui/menu/` 의 같은 이름 파일과 **다른 폴더**다. 덮어쓰지 말 것.

---

## 2. 공통 STYLE — 두 장 모두 글자 하나 안 바꾸고 붙인다

```
A single round game UI button, 512x512, TRANSPARENT background (alpha channel).

ONE PERFECT CIRCLE, centered, filling about 88% of the canvas.
Nothing outside the circle except its own soft contact shadow.

The button is a soft matte silicone dome: the center rises slightly and falls away
toward the rim, with a thin darker rim along the bottom edge and a broad soft
highlight across the upper half. Not glossy, no mirror reflection, no wet look.

In the middle of the circle sits ONE simple bold icon, drawn as a chunky
semi-flat shape with rounded corners and a clean white outline, in the style of
Blue Archive and Stella Sora UI icons. The icon fills about 52% of the circle.
It must stay readable when the whole button is shrunk to 70 pixels.

{ICON}

{COLOR}

No text, no letters, no numbers, no logo, no watermark.
Bright and light in tone, NOT dark, NOT black.
```

---

## 3. 두 버튼

| 파일 | 버튼 | `{ICON}` | `{COLOR}` |
|---|---|---|---|
| `scout.webp` | 차원 스카우트 | `The icon is a RADAR: a quarter-circle sweep fan with two or three concentric arcs, and one small round blip dot on the outer arc.` | `Warm cream gold silicone: #ffe9b8 at the top of the dome fading to #e0b463 near the rim, with a soft bronze bottom rim #b39a63. The radar icon is deep warm brown #5c3e12 with a white outline, so it stays readable on the gold.` |
| `start.webp` | 새 게임 | `The icon is a SPACESHIP seen from the side, nose pointing to the upper right: one rounded hull, one swept fin, and a short flame or thruster trail behind it.` | `Soft sky blue silicone: #8fcdf2 at the top of the dome fading to #4f9bd2 near the rim, with a deeper blue bottom rim #3d7fae. The spaceship icon is white with a light cream highlight face, so it stays readable on the blue.` |

⚠ **아이콘 색을 판 색과 다르게 지정한 게 핵심이다.**
지금 버튼이 "배지가 텅 빈 것처럼" 보이던 이유가 정확히 이거다 —
크림골드 아이콘을 크림골드 판에 얹으니 사라졌다.

---

## 4. 네거티브 (공통)

```
text, letters, numbers, korean, hangul, japanese, chinese, watermark, signature, logo,
dark, black, charcoal, navy, low key,
glossy, mirror reflection, specular highlight, wet look, large white blob, puddle,
chrome, metal, glass,
multiple objects, two shapes, second circle, square, rectangle, badge, frame, border,
photorealistic, 3d render, clay, cgi,
busy detail, tiny details, thin lines, cluttered,
background, solid background, green screen, chroma key, drop shadow outside the canvas
```

⚠ `korean, hangul` 을 반드시 넣을 것 — 안 넣으면 모델이 알아서 깨진 한글을 그려 넣는다.

---

## 5. 통과 기준 — 내가 숫자와 눈으로 확인한다

1. 512×512, 원 바깥 알파 0
2. **아이콘이 판 색과 대비되는가** — 회색조로 바꿔도 아이콘이 보여야 한다
3. **70px 로 줄여서 레이더/우주선인지 알아볼 수 있는가**
4. 불투명 픽셀 평균 밝기 150 이상 (어두우면 실패)
5. 글자 없음 (한글 비슷한 것도 없어야 함)
6. 물체가 하나 — 원 하나 + 그 안의 아이콘 하나

---

## 6. 넣은 뒤 (내가 하는 일)

```css
#menu .menu-btn-primary::before { background: url('./icons/ui/cta/start.webp') center / contain no-repeat; }
#menu #gachaBtn::before        { background: url('./icons/ui/cta/scout.webp') center / contain no-repeat; }
```

- 버튼을 정사각(1:1)으로 바꾸고 글자를 원 아래로 내린다 — 독 발바닥과 같은 구조
- 우측 컬럼 폭·위치는 `--cta-w` 하나로 잡혀 있어 같이 따라온다
- 현재 배지·라벨 면 관련 CSS 는 지운다
