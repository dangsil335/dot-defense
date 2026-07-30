# 아크 제로 — R타워(타로) 치비 13종 생성 프롬프트

- 저장 위치: `icons/characters/<id>.png` — 기존 치비들과 **같은 폴더**
- 규격: **433 × 577**, RGBA **투명 배경** (기본 9종과 완전 동일)
- 게임 내 표시: 캔버스 중앙, 한 변 약 44px로 축소 → **작아도 읽히는 실루엣** 필수
- 파일명은 아래 표의 `파일` 열 그대로. 넣으면 코드 수정 없이 바로 붙습니다(v741).

---

## 0. 왜 이 13종이 필요한가

진화 사다리는 **기본 → R(5라운드) → SR(20) → SSR(40)** 입니다.

| 단계 | 대상 | 성격 |
|---|---|---|
| 시작 | 기본 9종 (표준·저격수·요원 등) | 무명 오퍼레이티브 |
| **R5** | **R타워 13종 (타로)** | **각인을 얻은 오퍼레이티브 ← 지금 만드는 것** |
| R20 | SR 캐릭터 (레비나 등) | 실제 인물 |
| R40 | SSR 캐릭터 | 실제 인물 |

R타워는 **사람이 아니라 "타로 각인을 받은 상태"** 입니다. 그래서 가챠 캐릭터(애니풍 미소녀)가 아니라
**기본 9종과 같은 계열** — 얼굴 안 보이는 어두운 남색 장비/로브 실루엣 — 로 가고,
거기에 타로 문양과 고유색을 얹습니다. 이러면 R5는 "같은 요원이 각인을 얻었다",
R20은 "사람이 된다" 로 읽혀 단계가 자연스럽게 이어집니다.

---

## 1. 공통 프리앰블 (GPT에 한 번만)

> 모바일 로그라이크 "아크 제로(ARC ZERO)"의 **치비 캐릭터** 13종을 만들 거야.
> 기존 기본 캐릭터 9종(표준·저격수·요원 등)과 **한 세트로 보여야** 해.
>
> **기존 9종의 화풍 (반드시 맞출 것)**
> - 전신 직립, **정면**, 치비 비율(머리 크게, 3~4등신)
> - **얼굴이 보이지 않는다** — 바이저·후드·마스크로 가림. 눈은 발광 슬릿 하나 정도만
> - 베이스는 **어두운 남색~검정 전술 장비/로브**, 거기에 **고유색 발광 액센트**
> - 굵고 깔끔한 라인아트, 평면적 셰이딩 + 발광부만 강조
> - 장식 과다 금지. 실루엣이 먼저 읽혀야 함
>
> **규격**
> - 433 × 577 세로 캔버스, **완전 투명 배경 PNG** (배경·바닥그림자·프레임 없음)
> - 인물은 캔버스 **아래쪽에 정렬**, 머리 위 여백 약 5%
> - 게임에서 한 변 44px로 축소됨 → 작게 봐도 형태가 구분돼야 함
> - **텍스트·숫자 절대 금지**
>
> 각 캐릭터마다 타로 아르카나 하나와 주색(HEX)을 지정할게.
> 그 아르카나의 상징물을 **1~2개만** 쓰고, 주색이 발광 액센트를 지배해야 해.

---

## 2. 영문 프롬프트 템플릿

`{ARCANA}` · `{MOTIF}` · `{HEX}` 만 갈아끼우면 됩니다.

```
Chibi full-body character for a sci-fi tarot roguelike, front-facing, standing.
A faceless operative in dark navy tactical gear with a visor/hood — no visible face,
only a single glowing eye slit. Marked by the tarot arcanum {ARCANA}: {MOTIF}.
Dominant glowing accent color {HEX} on an almost-black navy base.
Chibi proportions (large head, 3-4 heads tall). Bold clean lineart, flat shading with
glowing accents only. Minimal detail — silhouette must read clearly when scaled to 44px.
No text, no numbers, no background, no ground shadow, no frame.
Fully transparent background. 433x577 vertical canvas, figure bottom-aligned,
about 5% headroom above the head.
```

---

## 3. 13종 표

능력색은 게임 코드의 실제 값입니다 — 그대로 쓰면 인게임 이펙트와 색이 맞습니다.

| 파일 | 타로 | 능력 | HEX | ARCANA | MOTIF |
|---|---|---|---|---|---|
| `wheel.png` | 운명의 수레 | 벼락 | `#ffe070` | The Wheel of Fortune | a spoked golden wheel hovering behind the shoulders, crackling with lightning |
| `devil.png` | 탐욕의 인장 | 체인 | `#88e0ff` | The Devil | heavy binding chains coiled around both arms, glowing sigil on the chest |
| `star.png` | 예지의 별 | 별빛 | `#ffe070` | The Star | a single bright star above the head, falling starlight motes around the body |
| `sun.png` | 백열의 태양 | 운석 | `#dd6633` | The Sun | a blazing white-hot solar disc behind the head like a halo, molten embers rising |
| `fool.png` | 방랑의 바보 | 부메랑 | `#ffaa44` | The Fool | a wanderer's bindle staff over the shoulder and a curved boomerang blade in hand |
| `magician.png` | 변성의 마법사 | 플라즈마호 | `#ff66ff` | The Magician | one hand raised with a plasma arc arcing between the fingers, infinity sigil floating |
| `hierophant.png` | 신성의 교황 | 광선 | `#ff66bb` | The Hierophant | a tall papal staff emitting a vertical pillar of light, layered ceremonial robe |
| `justice.png` | 심판의 정의 | 빙결 | `#88ddff` | Justice | frost-coated scales floating at one side, an ice blade in the other hand |
| `empress.png` | 풍요의 여황제 | 분신 | `#ffaaff` | The Empress | a crowned silhouette with two faint translucent duplicates flanking it |
| `world.png` | 완성의 세계 | 오비탈 | `#52e07a` | The World | a closed laurel ring orbiting the body, small orbital spheres circling it |
| `lovers.png` | 결속의 연인 | 미사일 | `#bb88ff` | The Lovers | twin bound silhouettes sharing one cloak, paired missile pods on the back |
| `strength.png` | 야수의 힘 | 회전검 | `#cccccc` | Strength | a beast-jaw pauldron on one shoulder and a large spinning blade held low |
| `chariot.png` | 돌격의 전차 | 돌진로켓 | `#ff8866` | The Chariot | heavy charging armor with a forward-tilted stance, rocket thrusters on the back |

> `strength` 의 코드 색이 `#cccccc`(무채색 회색)입니다. 그대로 쓰면 13종 중 유일하게
> 발광 액센트가 죽습니다. **은백색 금속 광택 + 붉은 짐승 눈** 정도로 포인트를 주시거나,
> 능력색을 바꾸고 싶으시면 말씀해 주시면 코드 쪽도 같이 맞추겠습니다.

---

## 4. 완성 후

`icons/characters/` 에 파일명 그대로 넣어주시면:

1. 규격(433×577) 실측 + 초과분 리사이즈
2. 13종 전부 로드되는지 감사 (누락분 보고)
3. R5 진화 시 실제로 치비가 바뀌는지 검증
4. 버전업 + 배포

**부분 납품도 됩니다.** v741 코드는 에셋이 없는 타로는 자동으로 현재 캐릭터 치비로
폴백하므로, 13종 중 몇 개만 넣어도 게임이 깨지지 않습니다.
