# 아크 제로 — SSR 알바 아트 생성 프롬프트

- 저장 위치: 일러 `icons/illust/alba.png` / 치비 `icons/characters/alba.png`
- 규격: **433 × 577**, RGBA **투명 배경**
- 원본은 `icons/illust/_orig/alba.png` 에 보관. 리사이즈는 `thumbnail((433,577), LANCZOS)`.
- ⚠ 배경 투명 처리는 함장 담당. 크로마키 초록 금지.

---

## 0. 캐릭터 정체

| 항목 | 값 |
|---|---|
| id | `alba` (충돌 0건 확인) |
| 표시명 | ⚔️ 알바 |
| 등급 | SSR |
| 컨셉 | 기사 — 참았다가 한 번에 내려친다 |
| 능력 축 | **적 밀도 충전 → 단일 초대형 일격** |
| 무기 | **양손 대검(츠바이핸더)** |
| 성격 | 과묵·절제. 웃지 않는다. |
| 테마색 | 은백 `#d5dbe6` + 은청 광휘 `#7fa8d4` |
| 배너 짝 | 🐈 플린타 (와인레드·리볼버) |
| 이름 어원 | `alba` = 새벽·흰빛 — 은백 테마 직결 + 「밤새 참고 기다린 끝에 오는 것」 |

**왜 이 축인가** — 이 게임엔 HP 가 없다(towerHP 는 폐기된 디펜스 전용).
클래식 패배는 오직 `state.enemies.length >= maxAlive` — **화면에 적이 쌓이는 것**뿐이다.
충전을 적 밀도에 걸면 위기가 곧 충전, 방출이 곧 해소가 되어 게임의 실제 위험 축과 맞물린다.

---

## 1. 겹침 회피 — 21종 전수 확인 결과

| 피할 것 | 이유 | 대체 |
|---|---|---|
| **판금 갑옷 전신** | 페리아가 이미 「부유 갑주」 | 예복 + **한쪽 견갑만** |
| **카타나·곡도** | 스미카(먹빛 도)·사쿠라(벚꽃도)가 둘 다 도 | **서양식 양손 대검** — 폭 넓은 직선 날 + 십자 가드로 실루엣이 완전히 갈린다 |
| **방사형 빛 폭발** | 솔라(12갈래 광선)·블랑슈(분광) | 날 중앙 홈을 따라 **아래에서 위로 차오르는 선형 게이지** |

**색**: 금(아리아)·보라(미사키)·청록(엘레미아)·먹(스미카)·연보라(블랑슈)·주황(카이라)·
강청(페리아)·하늘(솜니아)·와인레드(플린타). **은백은 비어 있다.**

**머리색**: 플린타가 플래티넘 블론드 → 알바는 **짙은 남흑발**. 나란히 놓았을 때 대비가 서야 한다.

---

## 2. 일러스트 (`icons/illust/alba.png`)

```
anime style character illustration, single female knight, vertical portrait composition,
transparent background, no background elements

FACE — HIGHEST PRIORITY:
face fully visible and completely unobstructed
NO helmet, NO visor, NO mask, NO hood — nothing covering or shadowing the face
calm expressionless stare directly at the viewer, silver-blue eyes, composed and severe
long straight dark blue-black hair, neatly tied back at the nape
a slim silver circlet resting on the forehead — the only headwear, sitting above the eyebrows,
it must not cross or cover any part of the face

OUTFIT — ceremonial, not battle plate:
long silver-white ceremonial coat with a high collar and dark navy underlayer,
fine silver-blue embroidery along the hem,
a single ornate pauldron on ONE shoulder only, with a heavy silver-white half-cape falling from it,
dark navy gloves and thigh-high boots
NOT full plate armor — refined ceremonial dress with exactly one armored piece

WEAPON — oversized two-handed greatsword (zweihander):
a very large straight double-edged greatsword, nearly as tall as she is,
broad flat blade, long cross-shaped guard, wrapped leather grip, heavy pommel
NOT a katana, NOT curved, NOT a halberd — a western straight greatsword
held point-down with the tip planted on the ground, both hands stacked on the pommel

STORED-POWER GAUGE (signature motif):
a narrow fuller (center groove) runs the length of the blade,
inside it a row of engraved tick marks glowing silver-blue,
filled from the guard upward to about two-thirds of the blade — a LINEAR charge gauge
faint silver-blue light bleeds only from the filled portion; the unfilled upper third stays dull steel
NOT a radial burst, NOT rays, NOT an aura

POSE:
standing perfectly straight, weight evenly on both feet, shoulders square,
chin level, both hands stacked on the pommel — a formal at-attention stance
she is waiting, not swinging

LIGHTING & RENDER:
cool silver-blue rim light from behind, restrained shading,
crisp anime cel style with clean confident linework,
high detail on the blade fuller and the glowing tick marks
the charge gauge is the single brightest element in the image

STRICT:
transparent background (alpha), full body edges must not touch the canvas border,
no text, no logos, no signature, no extra characters, no ground shadow baked in
```

**네거티브**
```
helmet, visor, face mask, hood, covered face, obscured face, hidden eyes, shadowed face,
full plate armor, katana, curved blade, halberd, polearm, spear, axe,
radial light burst, sun rays, prism, rainbow, glowing aura around body,
smiling, smirking, cheerful, relaxed slouching pose, dynamic action pose,
background scenery, floor, wall, sky, watermark, text, multiple characters, chibi proportions
```

---

## 3. 치비 (`icons/characters/alba.png`)

인게임에서 **한 변 약 44px**. 그 크기에 남아야 하는 3요소:
**① 몸통보다 큰 직선 대검 실루엣 ② 은백 색면 ③ 날의 청색 게이지선**

```
chibi character sprite, single female knight, 2-3 head-tall super-deformed proportions,
front-facing standing pose, transparent background

face fully visible, NO helmet and NO visor, large silver-blue eyes, small flat mouth,
completely neutral expression, dark blue-black hair tied back,
thin silver circlet on the forehead that does not cover the face

silver-white ceremonial coat as a bold flat color block (the coat is the color anchor),
one silver pauldron on one shoulder, small silver-white half-cape, dark navy boots and gloves

holding an oversized straight greatsword planted point-down beside her,
the blade clearly taller than the character — this vertical blade is the silhouette read at 44px
broad straight blade with a cross guard (NOT a katana, NOT curved)
three or four silver-blue glowing tick marks along the blade's center groove — the charge gauge

pose: standing at attention, perfectly straight, both hands stacked on the pommel

STYLE:
clean thick outlines, flat cel shading with one shadow tone, high color contrast,
bold simple shapes that stay legible when scaled down to 44 pixels

STRICT:
transparent background (alpha), no background, no ground shadow, no text,
whole body inside frame with small margin, single character only
```

**네거티브**
```
helmet, visor, covered face, katana, curved blade, halberd, realistic proportions,
busy small details, background, ground shadow, text, multiple characters, smiling
```

---

## 4. 플린타와 나란히 놓았을 때

배너에 둘이 같이 뜬다. 대비가 서야 짝지은 의미가 있다.

| | 🐈 플린타 | ⚔️ 알바 |
|---|---|---|
| 실루엣 | 짧은 총, 흐트러진 자세 | **몸통보다 큰 직선 대검**, 곧은 정자세 |
| 색 | 와인레드 + 주황 불티 | 은백 + 은청 |
| 머리 | 플래티넘 블론드 | 짙은 남흑 |
| 표정 | 반쯤 감은 눈, 비웃음 | 무표정, 정면 응시 |
| 자원 | 6발 갖고 시작 → **줄어듦** | 0에서 → **차오름** |
| 감각 | 아껴 쓴다 | 참는다 |
| 44px 식별 | 고양이 귀 · 와인 색면 · 주황 점 | 세로 대검 · 은백 색면 · 청 게이지선 |

---

## 5. 넣은 뒤 할 일

1. `_orig/` 에 고해상도 원본 보관
2. `thumbnail((433,577), LANCZOS)` 규격화 — 투명도 실측(모서리 alpha 0 확인)
3. `APP_VERSION` + `sw.js` 의 `CACHE` **동시** 상향
4. 등록은 [`character-add-checklist.md`](character-add-checklist.md) 순서대로
   — 특히 §4-B 능력쪽 부속과 §3-3 `LINEAGE_RESONANCE` 를 빠뜨리지 말 것
5. 마지막 점검은 **부록 C 차분 감사** + 도감 탭 카운트
