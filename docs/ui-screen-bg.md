# 화면 배경 일러 — 4장  (2차: 서브컬쳐 게임 배경으로)

> 전에는 화면마다 `radial-gradient` 를 4~6겹 쌓고 성운 애니메이션까지 돌렸다.
> 이미지 한 장으로 바꿨다(v828). CSS 도 줄고 룩도 낫다.

---

## 0. 한 줄 요약

```
위치    icons/ui/bg/
파일    achievements.webp  shop.webp  perma.webp  codex.webp
크기    2048 × 1152  (16:9)   ← 로비 배경과 같은 규격
포맷    WebP, 불투명(투명 필요 없음)
```

⚠ **파일이 없으면 그냥 단색 배경이 된다.** 화면이 깨지지 않으니 한 장씩 넣어도 된다.

---

## 1. ⚠ 1차 스펙이 틀렸던 점 — 실사로 끌고 가는 단어들

내가 쓴 프롬프트에 **3D 렌더링·사진 용어**가 섞여 있었다. 그게 실사풍을 부른다.

| 1차에 쓴 말 | 왜 틀렸나 |
|---|---|
| `soft ambient occlusion` | **3D 렌더 용어.** 블렌더·언리얼 쪽으로 직행한다 |
| `soft diffused daylight` | 사진 조명 언어 |
| `Clean architecture`, `gentle perspective` | 건축 시각화(archviz)로 끌린다 |
| `Muted, slightly desaturated palette` | 서브컬쳐 배경은 **밝고 채도가 높다.** 정반대다 |

**우리가 원하는 건 애니메이션 배경화(背景美術)다.** 셀 채색, 밝은 하늘, 깔끔한 색면,
또렷한 그림자 모양. 사진처럼 정교한 게 아니라 **정리된 그림**이다.

> 가독성은 그림을 흐리게 해서 얻지 않는다. 코드에 스크림이 이미 깔려 있고(§6),
> 배경이 밝으면 **스크림 알파 숫자 하나만** 올리면 된다. 그림은 밝고 예쁘게 가는 게 맞다.

---

## 2. ⚠ 가장 중요한 제약 — 좌측을 비워라

각 화면에는 **NPC 일러가 좌측 아래에 서 있다** (`.up-hero-left`, 433×577).
그 위에 배경의 볼거리가 겹치면 둘 다 죽는다.

```
┌──────────────────────────────────────────────┐
│                                              │
│   ← 이 영역(좌 35%)은        볼거리는        │
│      단순하게.               여기(중앙~우측) │
│      NPC 가 선다                             │
│                                              │
└──────────────────────────────────────────────┘
        ↑ 화면 아래 25% 는 UI 패널이 덮는다
```

---

## 3. 공통 STYLE 블록 — 네 장 모두 글자 하나 안 바꾸고 붙인다

```
Anime game location background art, 2048x1152, 16:9 landscape.
Background scenery only — absolutely no characters, no people.

Style: hand-painted Japanese anime background art (背景美術), the kind used for
location screens in anime mobile games like Blue Archive and Stella Sora.
Cel-shaded: clean flat areas of color with crisp, clearly shaped shadows —
NOT smooth photographic gradients. Clean confident linework on key edges.
Detail is simplified and tidy, never photo-dense.

Bright, cheerful and saturated. Clear blue sky light, warm sunlight patches,
soft bounce light. High-key and inviting, not gloomy, not moody.

Straight-on or very gentle perspective, horizon level, nothing tilted or wide-angle.

The LEFT THIRD of the image must stay simple and uncluttered — a character
illustration will stand there. Put the visual interest in the CENTER and RIGHT.
The BOTTOM QUARTER will be covered by UI panels, so keep it plain there too.

No characters, no people, no text, no letters, no logo, no UI, no watermark, no frame.
```

---

## 4. 화면별 SCENE — 위 STYLE 뒤에 붙인다

| 파일 | 화면 | NPC | SCENE |
|---|---|---|---|
| `achievements.webp` | 업적 | 크로니아 (`icons/npc/chronia.png`) | `A bright trophy hall. Tall arched windows along the right wall with clear blue sky beyond, sunlight falling in clean warm patches across a polished floor. A row of low display stands on the right holding medals and cups. Cream walls, warm gold accents, red carpet runner.` |
| `shop.webp` | 강화소 | 세계·테라 (`icons/npc/world.png`) | `A cheerful craft workshop. A wooden workbench on the right with tools hung tidily on a pegboard above it and a few glowing crystals in a tray. A big round window behind pouring bright daylight and green leaves visible outside. Warm wood, brass fittings, fresh mint-green accents.` |
| `perma.webp` | 능력 영구 강화 | 아리아 (일러 체인 `aria`) | `A music room at dusk. A curved balcony railing on the right opening onto a clear evening sky with the first stars, an upright piano and a music stand in the middle distance, tall narrow windows. Soft indigo and violet with warm lamp light. Calm and pretty, gently lit — still clearly daylight-readable, not dark.` |
| `codex.webp` | 도감 | 비블리아 (`icons/npc/biblia.png`) | `A bright library. Tall wooden bookshelves receding toward the right, a large window in the center pouring clean pale-blue daylight onto an open reading table with a few stacked books. Warm wood, cream pages, cool blue light. Calm and scholarly but bright and airy.` |

---

## 5. 네거티브 (공통)

```
3d render, unreal engine, octane, blender, cgi, ray tracing, ambient occlusion,
architectural visualization, archviz, interior design render,
photograph, photorealistic, realistic lighting, hdr, depth of field, bokeh, lens flare,
characters, people, person, girl, boy, figure, silhouette of a person, hands,
text, letters, numbers, kanji, signage, logo, watermark, signature,
UI, interface, buttons, panels, frame, border, vignette overlay,
busy detail on the left, clutter on the left side, subject on the left,
dark, gloomy, moody, desaturated, muted, washed out, grayscale,
neon, cyberpunk, sci-fi hologram, fisheye, wide angle, tilted horizon,
sketch, unfinished, rough
```

⚠ `3d render` 계열과 `ambient occlusion` 을 넣은 게 2차의 핵심이다 — 1차가 그걸로 실사가 됐다.
⚠ `characters, people` 는 반드시 넣을 것. 배경에 사람이 그려지면 NPC 일러와 겹쳐
   두 명이 서 있는 것처럼 보인다.
⚠ `desaturated, muted` 도 네거티브다. 1차엔 내가 프롬프트 본문에 그걸 넣었었다.

---

## 6. 통과 기준 — 내가 확인한다

1. 2048×1152 (16:9)
2. **셀 채색인가** — 색면이 또렷하고 그림자 모양이 잡혀 있는가.
   부드러운 사진 그라디언트면 실패다
3. **좌측 3분의 1이 단순한가** — NPC 가 설 자리다
4. 사람이 그려져 있지 않은가
5. **하단 4분의 1이 단순한가** — UI 패널이 덮는다
6. 밝고 채도가 살아 있는가 (어둡고 탁하면 실패)
7. 글자·로고·UI 요소 없음

---

## 7. 넣은 뒤 (내가 하는 일)

파일만 `icons/ui/bg/` 에 넣으면 끝이다. CSS 는 이미 걸려 있다.

```css
#codex { background-image: url('./icons/ui/bg/codex.webp') !important; }
```

글자 가독용 스크림은 `::before` 하나로 이미 깔려 있다(위아래 어둡게).
배경이 밝아서 글씨가 안 보이면 **그 알파 숫자만** 올리면 된다 — 그림을 어둡게 뽑을 필요 없다.

```css
background: linear-gradient(180deg,
  rgba(6,12,22,0.62) 0%, rgba(6,12,22,0.30) 34%,
  rgba(6,12,22,0.42) 72%, rgba(6,12,22,0.74) 100%);
```
