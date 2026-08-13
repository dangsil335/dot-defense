# 화면 배경 일러 — 4장

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

## 1. ⚠ 가장 중요한 제약 — 좌측을 비워라

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

프롬프트에 이 문장을 반드시 넣을 것:

```
The LEFT THIRD of the image must stay simple and uncluttered — a character
illustration will stand there. Put the visual interest in the CENTER and RIGHT.
The BOTTOM QUARTER will be covered by UI panels, so keep it plain there too.
```

---

## 2. 공통 STYLE 블록 — 네 장 모두 동일하게 붙인다

```
Anime mobile game location background art, 2048x1152, 16:9, no characters, no people.

A quiet interior scene rendered in soft painterly anime style, like the location
backgrounds of Blue Archive or Stella Sora. Clean architecture, gentle perspective,
soft diffused daylight, calm and inviting.

Muted, slightly desaturated palette so that bright UI panels placed on top stay readable.
Soft ambient occlusion, no harsh contrast, no strong shadows.

The LEFT THIRD of the image must stay simple and uncluttered — a character
illustration will stand there. Put the visual interest in the CENTER and RIGHT.
The BOTTOM QUARTER will be covered by UI panels, so keep it plain there too.

No characters, no people, no text, no letters, no logo, no UI, no watermark, no frame.
```

---

## 3. 화면별 SCENE

| 파일 | 화면 | NPC | SCENE (위 STYLE 뒤에 붙일 것) |
|---|---|---|---|
| `achievements.webp` | 업적 | 크로니아 (`icons/npc/chronia.png`) | `A grand hall of records: tall arched windows on the right letting in warm afternoon light, rows of display plinths holding medals and trophies along the right wall, a high vaulted ceiling. Warm gold and cream tones with soft amber light.` |
| `shop.webp` | 강화소 | 세계·테라 (`icons/npc/world.png`) | `A bright workshop: a sturdy workbench on the right with neatly arranged tools and glowing crystals, shelves of parts behind it, a large round window letting in green-tinted daylight. Warm wood, brass, and soft mint-green tones.` |
| `perma.webp` | 능력 영구 강화 | 아리아 (일러 체인 `aria`) | `A quiet observatory concert hall: a curved balcony on the right overlooking a soft night sky, a grand piano silhouette in the middle distance, tall thin windows. Deep indigo and soft violet tones with gentle starlight. Calm, not flashy.` |
| `codex.webp` | 도감 | 비블리아 (`icons/npc/biblia.png`) | `A vast quiet library: towering bookshelves receding to the right, a tall window pouring pale blue light across a reading table in the center, floating dust motes. Cool blue and pale teal tones, scholarly and serene.` |

---

## 4. 네거티브 (공통)

```
characters, people, person, girl, boy, figure, silhouette of a person, hands,
text, letters, numbers, kanji, signage, logo, watermark, signature,
UI, interface, buttons, panels, frame, border, vignette overlay,
busy detail on the left, clutter on the left side, subject on the left,
harsh shadows, high contrast, neon, cyberpunk, sci-fi hologram, lens flare,
photorealistic, 3d render, fisheye, extreme perspective, tilted horizon
```

⚠ `characters, people` 를 반드시 넣을 것 — 배경에 사람이 그려지면 NPC 일러와 겹쳐서
두 명이 서 있는 것처럼 보인다.

⚠ `neon, cyberpunk, sci-fi hologram` — 지금 걷어내는 중인 우주 컨셉이다.

---

## 5. 통과 기준 — 내가 확인한다

1. 2048×1152 (16:9)
2. **좌측 3분의 1이 단순한가** — NPC 가 설 자리다. 여기가 복잡하면 실패
3. 사람이 그려져 있지 않은가
4. **하단 4분의 1이 단순한가** — UI 패널이 덮는다
5. 채도가 과하지 않은가 — 위에 밝은 패널이 올라간다
6. 글자·로고·UI 요소 없음

---

## 6. 넣은 뒤 (내가 하는 일)

파일만 `icons/ui/bg/` 에 넣으면 끝이다. CSS 는 이미 걸려 있다.

```css
#codex { background-image: url('./icons/ui/bg/codex.webp') !important; }
```

글자 가독용 스크림(위아래 어둡게)은 `::before` 하나로 이미 깔려 있다.
배경이 밝아서 글씨가 안 보이면 그 스크림의 알파만 올리면 된다.
