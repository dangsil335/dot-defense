# 아크 제로 — SSR 기사(가칭) 아트 생성 프롬프트

> ⚠ **이름 미확정.** 아래 프롬프트의 캐릭터명은 비워 뒀다. 파일명도 id 확정 후 정한다.
> 이름 후보는 §5 참고.

- 저장 위치: 일러 `icons/illust/<id>.png` / 치비 `icons/characters/<id>.png`
- 규격: **433 × 577**, RGBA **투명 배경**
- 원본은 `_orig/` 하위에 보관. 리사이즈는 `thumbnail((433,577), LANCZOS)`.
- ⚠ 배경 투명 처리는 함장 담당. 크로마키 초록 금지.

---

## 0. 캐릭터 정체

| 항목 | 값 |
|---|---|
| 등급 | SSR |
| 컨셉 | 기사 — 참았다가 한 번에 내려친다 |
| 능력 축 | **적 밀도 충전 → 단일 초대형 일격** |
| 성격 | 과묵·절제. 웃지 않는다. |
| 테마색 | 은백 `#d5dbe6` + 은청 광휘 `#7fa8d4` |
| 배너 짝 | 🐈 플린타 (와인레드·리볼버) |

**왜 이 축인가** — 이 게임엔 HP가 없다. 패배는 오직 `state.enemies.length >= maxAlive`,
즉 **화면에 적이 쌓이는 것**이다. 그래서 충전을 적 밀도에 걸면 "위기가 곧 충전, 방출이 곧 해소" 가 되어
게임의 실제 위험 축과 맞물린다. 「받은 피해」 같은 건 이 시스템에 존재하지 않는다.

---

## 1. 겹침 회피 — 실측으로 걸러낸 3가지

기존 21종의 시각 모티프를 전수 확인해서 나온 제약이다. **반드시 지킬 것.**

| 피할 것 | 이유 |
|---|---|
| **판금 갑옷 전신** | 페리아가 이미 「부유 갑주」다. → 갑옷 대신 **예복 + 한쪽 견갑**만 |
| **검** | 스미카(먹빛 도)·사쿠라(벚꽃도)·카이라(발톱) 셋이 이미 검 계열. → **대형 도끼창(할버드)** |
| **방사형 빛 축적** | 솔라(12갈래 광선)·블랑슈(백광 분광). → 빛이 아니라 **날에 새겨진 선형 눈금 게이지** |

**색 중복 회피**: 금(아리아) · 보라(미사키) · 청록(엘레미아) · 먹(스미카) · 연보라(블랑슈) ·
주황(카이라) · 강청(페리아) · 하늘(솜니아) · 와인레드(플린타). **은백은 비어 있다.**

**머리색**: 플린타가 플래티넘 블론드이므로 **짙은 남흑발**로 간다. 나란히 놓았을 때 대비가 서야 한다.

---

## 2. 일러스트

```
anime style character illustration, single female knight, vertical portrait composition,
transparent background, no background elements

FACE — MOST IMPORTANT:
face fully visible and unobstructed, NO helmet, NO visor, NO mask, nothing covering the face
calm expressionless stare directly at the viewer, silver-blue eyes, composed and severe
long straight dark blue-black hair, neatly tied back
a slim silver circlet resting on the forehead — the only headwear, it must not cover any part of the face

OUTFIT — ceremonial, not battle plate:
long silver-white ceremonial coat with high collar and dark navy underlayer,
fine silver-blue embroidery along the hem, a single ornate pauldron on ONE shoulder only,
dark navy gloves and boots, a heavy silver-white half-cape falling from the pauldron
NOT full plate armor, NOT a knight in shining armor cliche — refined ceremonial dress with one armored piece

WEAPON — oversized halberd (NOT a sword):
a very large two-handed halberd, taller than she is,
long dark steel haft with a broad silver axe-head and a spike
held vertically, butt of the haft planted on the ground, both hands resting on it
STORED-POWER GAUGE (signature motif):
along the inner edge of the axe-head, a row of engraved tick marks glowing silver-blue,
filled from the bottom upward about two-thirds — a linear charge gauge, NOT a radial burst
faint silver-blue light bleeds from the filled ticks only

POSE:
standing perfectly straight, weight evenly on both feet, shoulders square,
chin level, both hands stacked on the halberd butt — a formal at-attention stance
she is waiting, not fighting

LIGHTING & RENDER:
cool silver-blue rim light, restrained shading, crisp anime cel style with clean linework
high detail on the halberd engraving and the glowing tick marks
the gauge is the single brightest element

STRICT:
transparent background (alpha), full body edges must not touch the canvas border,
no text, no logos, no signature, no extra characters, no ground shadow baked in
```

**네거티브**
```
helmet, visor, face mask, covered face, obscured face, hidden eyes,
full plate armor, sword, katana, claws, radial light burst, sun rays, prism, rainbow,
smiling, cheerful, relaxed slouching pose,
background scenery, floor, wall, sky, watermark, text, multiple characters, chibi proportions
```

---

## 3. 치비

인게임에서 **한 변 약 44px**. 그 크기에 남아야 하는 3요소:
**① 긴 자루 실루엣 ② 은백 색면 ③ 날의 청색 게이지선**

```
chibi character sprite, single female knight, 2-3 head-tall super-deformed proportions,
front-facing standing pose, transparent background

face fully visible, NO helmet and NO visor, large silver-blue eyes, small flat mouth,
completely neutral expression, dark blue-black hair tied back,
thin silver circlet on the forehead that does not cover the face

silver-white ceremonial coat as a bold flat color block (the coat is the color anchor),
one silver pauldron on one shoulder, dark navy boots and gloves, small silver-white half-cape

holding an oversized halberd planted vertically beside her, haft clearly taller than the character
(the long vertical haft is the silhouette read at 44px)
three or four silver-blue glowing tick marks along the axe-head edge — the charge gauge

pose: standing at attention, perfectly straight, both hands on the haft

STYLE:
clean thick outlines, flat cel shading with one shadow tone, high color contrast,
bold simple shapes that stay legible when scaled down to 44 pixels

STRICT:
transparent background (alpha), no background, no ground shadow, no text,
whole body inside frame with small margin, single character only
```

**네거티브**
```
helmet, visor, covered face, sword, realistic proportions, busy small details,
background, ground shadow, text, multiple characters, smiling
```

---

## 4. 플린타와 나란히 놓았을 때

배너에 둘이 같이 뜬다. 대비가 서야 짝지은 의미가 있다.

| | 🐈 플린타 | 기사 |
|---|---|---|
| 실루엣 | 짧은 총, 흐트러진 자세 | **긴 자루**, 곧은 정자세 |
| 색 | 와인레드 + 주황 불티 | 은백 + 은청 |
| 머리 | 플래티넘 블론드 | 짙은 남흑 |
| 표정 | 반쯤 감은 눈, 비웃음 | 무표정, 정면 응시 |
| 자원 | 6발 갖고 시작 → **줄어듦** | 0에서 → **차오름** |
| 44px 식별 | 고양이 귀 · 와인 색면 · 주황 점 | 긴 자루 · 은백 색면 · 청 게이지선 |

---

## 5. 이름 후보 (미확정)

아크 제로 작명 규칙은 **어원이 능력을 가리키는 것**이다 —
루나(luna=달)→월광탄 / 페리아(ferro=철)→자기장 / 솜니아(somnus=잠)→자장가 /
아이리스(iris=조리개)→장노출 / 플린타(flint=부싯돌)→격발.

「참았다가 쌓인 것을 한 번에 내려친다」를 가리키는 어원:

| 후보 | 어원 | 결 |
|---|---|---|
| **비질라** | vigilia(철야 경계) — 기사 서임 전야의 철야기도가 vigil | 기사 정체성 + 기다림을 동시에 가리킨다 |
| **쿠물라** | cumulus(쌓임·누적) | 충전 메커니즘을 가장 직접적으로 가리킨다 |
| **폰데라** | pondus(무게) | 묵직한 한 방 쪽에 무게중심 |

⚠ 확정 전에 `index.html` 에서 id 충돌을 확인할 것 (`grep -c "'<id>'" index.html`).
