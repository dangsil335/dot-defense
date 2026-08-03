# 아크 제로 — SSR 카를로타 아트 생성 프롬프트

- 저장 위치: 일러 `icons/illust/carlotta.png` / 치비 `icons/characters/carlotta.png`
- 규격: **433 × 577**, RGBA **투명 배경** (기존 캐릭터와 완전 동일)
- 원본(고해상도)은 각각 `_orig/` 하위에 보관. 리사이즈는 `thumbnail((433,577), LANCZOS)`.
- ⚠ 배경 투명 처리는 함장 담당. 크로마키 초록 금지.

---

## 0. 캐릭터 정체

| 항목 | 값 |
|---|---|
| id | `carlotta` |
| 표시명 | 🐈 카를로타 |
| 등급 | SSR |
| 능력 축 | **탄창·재장전** — 6발 쏘고 재장전, 마지막 한 발이 극대 위력 |
| 성격 | 도도한 츤데레. 관심 없는 척하다 결정적일 때 한 발. |
| 말투 | **반말** (6곳 대사 전부 반말로 통일) |
| 테마색 | 와인레드 + 금장 `#b0324a` |

**색 중복 회피**: aria 금색 / kaira 주황 / feria 강청 / misaki 보라 / somnia 하늘 / elementia 청록 /
blanche 무지개 / sumika 먹. **레드 계열은 비어 있어** 카를로타가 가져간다.

**카이라와의 구분** — 카이라(🐾)는 이미 야수·발톱·맹수다. 카를로타는 **집고양이** 쪽이다:
발톱으로 찢는 게 아니라 **총으로 쏘고**, 사납지 않고 **도도하다**. 프롬프트에서 이 구분을 반드시 지킬 것.

---

## 1. 일러스트 (`icons/illust/carlotta.png`)

세로 초상. 얼굴~허벅지 정도가 화면에 들어오는 구도. 배경 투명.

```
anime style character illustration, single female gunslinger, vertical portrait composition,
transparent background, no background elements

CHARACTER:
young woman, aloof and haughty expression, half-lidded eyes looking slightly down at the viewer,
faint smug smirk — proud tsundere, "I'm not doing this for you"
long straight platinum-blonde hair with a wine-red inner layer, hair swept over one shoulder
sharp amber cat-like eyes with vertical slit pupils
small black cat ears sitting naturally in the hair (elegant house-cat, NOT beast/feral)
slender black cat tail curling lazily behind her

OUTFIT:
aristocratic gunslinger — deep wine-red tailored longcoat with gold trim and gold buttons,
black high-collar shirt, black gloves, thigh-high black boots
a slim leather bandolier across the chest holding six brass cartridges — the cartridges must read
clearly as SIX, evenly spaced (this is her mechanic: a six-round cylinder)
gold filigree accents, no armor plating — refined, not military

WEAPON:
an ornate long-barreled revolver held casually in one hand, pointed down or resting on her shoulder,
NOT aimed at the viewer — she can't be bothered yet
brass and wine-red enamel, engraved gold scrollwork on the barrel and cylinder
the cylinder is visible and slightly rotated open, one chamber glowing faint gold (the last bullet)

POSE:
relaxed contrapposto, weight on one hip, free hand on hip or idly examining her gloved fingertips
chin slightly raised — looking down at whoever she's talking to

LIGHTING & RENDER:
soft rim light from behind in warm gold, cool shadow on the front — dramatic but clean
crisp anime cel shading with painterly highlights, high detail on the revolver engraving
subtle floating gold dust motes near the glowing chamber

STRICT:
transparent background (alpha), full body edges must not touch the canvas border,
no text, no logos, no signature, no extra characters, no ground shadow baked in
```

**네거티브**
```
beast form, monster, claws, fangs, feral, aggressive snarl, gun aimed at viewer,
background scenery, floor, wall, sky, watermark, text, multiple characters, chibi proportions
```

---

## 2. 치비 (`icons/characters/carlotta.png`)

인게임 캔버스에서 **한 변 약 44px** 로 축소된다. 작아도 읽히는 실루엣이 필수다.
44px 로 줄였을 때 남아야 하는 3요소: **① 고양이 귀 실루엣 ② 와인레드 코트 색면 ③ 리볼버 금색 점**.

```
chibi character sprite, single female gunslinger, 2-3 head-tall super-deformed proportions,
front-facing standing pose, transparent background

oversized round head, large sharp amber cat eyes with slit pupils, tiny smug smirk,
small black cat ears clearly silhouetted above the head (must stay readable at 44px),
platinum-blonde hair with wine-red inner layer, short black cat tail curled to one side

deep wine-red longcoat with gold trim as a bold flat color block (the coat is the color anchor),
black boots, black gloves
holding a small ornate revolver in one hand, barrel pointed down,
one gold glowing dot on the cylinder — the last bullet

pose: standing, chin up, one hand on hip — aloof and pleased with herself

STYLE:
clean thick outlines, flat cel shading with one shadow tone, high color contrast,
bold simple shapes that stay legible when scaled down to 44 pixels

STRICT:
transparent background (alpha), no background, no ground shadow, no text,
whole body inside frame with small margin, single character only
```

**네거티브**
```
realistic proportions, detailed rendering, busy small details, background, ground shadow,
text, multiple characters, beast form, claws
```

---

## 3. 넣은 뒤 할 일

1. `_orig/` 에 고해상도 원본 보관
2. `thumbnail((433,577), LANCZOS)` 로 규격화 — 투명도 실측(모서리 alpha 0 확인)
3. `APP_VERSION` + `sw.js` 의 `CACHE` **동시** 상향 (정적 에셋 cache-first라 안 올리면 안 바뀐다)
4. 나머지 등록 16곳은 [`character-add-checklist.md`](character-add-checklist.md) 순서대로

---

## 4. (참고) 확정된 진화 계보

```
iris     → [feria, carlotta]     장노출: "모았다가 한 번에 터뜨린다" → 장전·격발
cardista → [sumika, carlotta]    요행·한 방·골드 → 서부극 도박사 총잡이
```

둘 다 기존 1-way 라 2-way 가 된다. 기존 2-way 를 3-way 로 희석하지 않고,
sumika 는 sakura, feria 는 trina 라는 보장 경로를 그대로 유지한다.

루나(월광**탄** · 달 · 밤 = 고양이)도 잘 맞지만 이미 2-way(misaki·somnia)라
3-way 가 되면 솜니아 확률이 1/2 → 1/3 으로 깎인다. 솜니아는 튜토리얼 캐릭이라 뺐다.
