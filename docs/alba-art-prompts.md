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
| 무기 | **양손 대검** — 한 손으로 **세워** 든다 (칼끝 아래) |
| 복장 | **경장** — 한쪽 견갑 · 양팔 건틀릿 · 허리 파울드. 다리 판금 없음, 민소매 |
| 머리 | **은백**, 어깨 길이 + 뒤로 땋아 올린 번(bun) |
| 성격 | 과묵·절제. 웃지 않는다. |
| 테마색 | **은백 + 감청 + 금** · 게이지는 청백 · `CHARACTERS.color` = `#dfe6f2` |
| 배너 짝 | 🐈 플린타 (와인레드·리볼버) |
| 이름 어원 | `alba` = 새벽·흰빛 — 은백 테마 직결 + 「밤새 참고 기다린 끝에 오는 것」 |

**왜 이 축인가** — 이 게임엔 HP 가 없다(towerHP 는 폐기된 디펜스 전용).
클래식 패배는 오직 `state.enemies.length >= maxAlive` — **화면에 적이 쌓이는 것**뿐이다.
충전을 적 밀도에 걸면 위기가 곧 충전, 방출이 곧 해소가 되어 게임의 실제 위험 축과 맞물린다.

---

## 1. 겹침 회피 — 21종 전수 확인 결과

| 피할 것 | 이유 | 대체 |
|---|---|---|
| ~~판금 갑옷~~ | **겹치지 않는다.** 페리아는 「몸이 아닌 **허공을 맴도는** 강철 파편」이라 부유물이지 착용 판금이 아니다 — 처음에 과하게 피했다 | **경장 판금** 착용 OK |
| **카타나·곡도** | 스미카(먹빛 도)·사쿠라(벚꽃도)가 둘 다 도 | **서양식 양손 대검** — 폭 넓은 직선 날 + 십자 가드로 실루엣이 완전히 갈린다 |
| **방사형 빛 폭발** | 솔라(12갈래 광선)·블랑슈(분광) | 날 중앙 홈을 따라 **아래에서 위로 차오르는 선형 게이지** |

**색**: 금(아리아)·보라(미사키)·청록(엘레미아)·먹(스미카)·연보라(블랑슈)·주황(카이라)·
강청(페리아)·하늘(솜니아)·와인레드(플린타). **은백은 비어 있다.**

**머리색**: 플린타가 플래티넘 **블론드**(노란 기미)라면 알바는 **완전 무채색 은백**이다.
머리만 보면 가깝지만 화면을 지배하는 색이 와인레드 ↔ 순백으로 정반대라 실루엣 인상은 확실히 갈린다.
프롬프트에 `no yellow, no gold, no platinum-blonde tint` 를 박아 노란 기미가 섞이는 걸 막았다.

---

## 2. 일러스트 — ✅ **확정·투입 완료** (`icons/illust/alba.png`, 433×577)

아래 프롬프트는 **치비·스킨을 뽑을 때 톤을 맞추기 위한 기록**이다.
실제 채택본은 프롬프트와 일부 다르며, **어긋나면 채택본이 기준**이다:

| 항목 | 프롬프트 | **채택본(기준)** |
|---|---|---|
| 색 구성 | 순백·은 무채색, 금 최소 | **은백 + 감청 서코트 + 금 장식** |
| 노출 | 언급 없음 | **민소매·어깨 노출**, 다리 판금 없음 |
| 파지 | 옆으로 늘어뜨림 | **한 손으로 세워 듦** (칼끝 아래) |
| 게이지 | 눈금(tick) | **날 중앙의 청백 룬 라인 + 화살촉 문양** |
| 머리 | 단발~어깨 + 사이드 땋기 | **어깨 길이 + 뒤로 땋아 올린 번** |


```
anime style character illustration, single female knight, vertical portrait composition,
transparent background, no background elements

AGE & FACE — HIGHEST PRIORITY:
a YOUNG girl, looks about 16-17 years old, youthful and delicate
small rounded face with a soft jawline and small chin, smooth cheeks
LARGE round anime eyes (not narrow, not sharp), clear pale blue-grey irises, long lashes
face fully visible and completely unobstructed
NO helmet, NO visor, NO mask, NO hood — nothing covering or shadowing the face
quiet reserved expression, lips closed in a small neutral line, looking straight at the viewer
— she is calm and self-contained, NOT stern, NOT angry, NOT a mature adult woman

HAIR:
pure achromatic silver-white hair (no yellow, no gold, no platinum-blonde tint — desaturated silver),
short to shoulder length, slightly tousled, with a small braid running along one side above the ear
a slim silver circlet on the forehead sitting above the eyebrows — must not cross the face

OUTFIT — LIGHT armor, white and silver:
polished silver-white plate on the key points ONLY: a fitted breastplate, both pauldrons,
gauntlets, and greaves. everything else is cloth — keep it light and mobile
flowing white tabard / surcoat over a pale grey underlayer, soft cloth sleeves and skirt,
a long white half-cape with a faint silver lining, thin leather belt
minimal gold filigree on the breastplate edge only — sparse, not ornate
NOT full plate armor, NOT heavy knight-in-shining-armor bulk, NOT a long formal coat
the overall read is WHITE AND SILVER — desaturated, almost monochrome

WEAPON — oversized two-handed greatsword (zweihander):
a very large straight double-edged greatsword, nearly as tall as she is,
broad flat blade, long cross-shaped guard, wrapped leather grip, heavy pommel
NOT a katana, NOT curved, NOT a halberd — a western straight greatsword
held loosely in ONE hand, arm relaxed at her side, blade angled down toward the ground
(not planted, not raised, not swinging) — the other hand hangs free

STORED-POWER GAUGE (signature motif):
a narrow fuller (center groove) runs the length of the blade,
inside it a row of engraved tick marks glowing silver-blue,
filled from the guard upward to about two-thirds of the blade — a LINEAR charge gauge
faint silver-blue light bleeds only from the filled portion; the unfilled upper third stays dull steel
NOT a radial burst, NOT rays, NOT an aura

BODY & FRAMING:
petite slender build, youthful proportions — roughly 6.5 heads tall (anime proportions,
head slightly large relative to the body), NOT a tall realistic 8-head figure
CROP: full body is fine — but the character must FILL the frame vertically,
head near the top edge and feet near the bottom. no empty margin, no distant framing.
(youth comes from the face and proportions, not from cropping)

POSE:
standing at ease, weight settled evenly, shoulders relaxed but square, chin level,
sword hanging from one hand at her side — quiet and unhurried
she is waiting, not fighting

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
full plate armor, heavy bulky armor, long formal coat, katana, curved blade, halberd, polearm, spear, axe,
blonde hair, golden hair, warm-toned hair, dark hair, black hair,
radial light burst, sun rays, prism, rainbow, glowing aura around body,
mature adult woman, older woman, 20s, 30s, sharp angular jawline, long narrow face,
narrow slanted eyes, hooded eyes, stern glare, severe expression, tall realistic proportions,
full body shot at small scale, distant framing,
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

face fully visible, NO helmet and NO visor, large pale blue eyes, small flat mouth,
completely neutral expression,
silver-white hair, shoulder length, tied into a small braided bun at the back

white corset-style bodice with gold trim over a DARK NAVY skirt and half-cape
(white + navy is the color anchor — both must read as flat blocks at 44px)
one large silver pauldron on one shoulder, dark navy gloves, silver forearm gauntlets,
gold fleur-de-lis accent on the cape

holding an oversized straight greatsword UPRIGHT in one hand beside her, point down,
the blade clearly taller than the character — this vertical blade is the silhouette read at 44px
broad straight blade with an ornate cross guard (NOT a katana, NOT curved)
a glowing pale blue-white line running down the center of the blade — the charge gauge

pose: standing straight, one hand gripping the sword upright, the other relaxed at her side

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
| 실루엣 | 짧은 총, 흐트러진 자세 | **긴 대검을 옆으로 늘어뜨린** 편히 선 자세 |
| 색 | 와인레드 + 주황 불티 | **은백 + 감청 + 금** |
| 머리 | 플래티넘 블론드(노란 기미) | **무채색 은백** |
| 표정 | 반쯤 감은 눈, 비웃음 | 무표정, 정면 응시 |
| 자원 | 6발 갖고 시작 → **줄어듦** | 0에서 → **차오름** |
| 감각 | 아껴 쓴다 | 참는다 |
| 44px 식별 | 고양이 귀 · 와인 색면 · 주황 점 | **세로 대검** · 흰+감청 색면 · 청백 게이지선 |

---

## 5. 넣은 뒤 할 일

1. `_orig/` 에 고해상도 원본 보관
2. `thumbnail((433,577), LANCZOS)` 규격화 — 투명도 실측(모서리 alpha 0 확인)
3. `APP_VERSION` + `sw.js` 의 `CACHE` **동시** 상향
4. 등록은 [`character-add-checklist.md`](character-add-checklist.md) 순서대로
   — 특히 §4-B 능력쪽 부속과 §3-3 `LINEAGE_RESONANCE` 를 빠뜨리지 말 것
5. 마지막 점검은 **부록 C 차분 감사** + 도감 탭 카운트
