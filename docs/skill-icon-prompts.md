# 아크 제로 — 스킬 아이콘 56종 생성 프롬프트

- 저장 위치: `icons/abilities/<id>.png`
- 규격: **256 × 256** RGBA
- ⚠ **투명 배경이 아니다.** 기존 아이콘은 전부 테두리 있는 액자형 카드다(어두운 배경 + 프레임).
  최초 작성 시 "투명 배경"이라고 적었으나 실제 에셋과 어긋난 잘못된 규격이었다.
- 게임 내 표시 크기 약 56px → **작아도 읽히는 실루엣** 필수

---

## 0. 공통 프리앰블 (GPT에 한 번만)

> 모바일 로그라이크 게임 "아크 제로(ARC ZERO)"의 **스킬 아이콘** 56종을 만들 거야.
> 기존 161개와 한 세트로 보여야 해. 아래 규격을 **모든 아이콘에 동일하게** 적용해줘.
>
> **규격**
> - 256 × 256 정사각형 PNG
> - **불투명 액자형 카드** — 어두운 배경판 + 얇은 테두리 프레임을 아이콘 안에 그린다
>   (⚠ 투명 배경 아님. 게임은 `ctx.drawImage` 한 번으로 그릴 뿐 배경판을 따로 깔지 않는다.
>    투명으로 뽑으면 어두운 UI 위에서 아이콘이 허공에 뜬 것처럼 보인다.)
> - 게임에서 약 56px로 축소 표시됨 → 실루엣이 뭉개지지 않게
>
> **스타일**
> - SF 판타지 게임 UI 아이콘. 굵고 명확한 형태, 강한 색 대비
> - 어두운 UI 위에 올라가므로 **밝고 채도 높게**, 발광(글로우) 강조
> - 요소는 1~2개만. 디테일 과다 금지
> - 원근 없는 **정면·평면 구성**
> - **텍스트·숫자 절대 금지**
>
> 각 아이콘마다 주색(HEX)을 지정할게. 그 색이 아이콘을 지배해야 해.

---

## 1. 영문 프롬프트 템플릿

`{CONCEPT}`와 `{HEX}`만 갈아끼우면 됩니다.

```
Game skill icon for a sci-fi fantasy mobile roguelike. {CONCEPT}.
Dominant color {HEX} with glowing accents. Bold readable silhouette that stays
legible at 56px. Flat front-facing composition, no perspective. Vibrant and
high-contrast for a dark UI. Minimal detail — one or two clear elements only.
No text, no numbers, no border, no background panel.
Fully transparent background. 256x256 square, ~8% padding from edges.
```

---

## 2. 캐릭터별 56종

### ⚗ 클로에 · `#a0e050`
| 파일 | 이름 | CONCEPT |
|---|---|---|
| `acidRain.png` | 산성비 | acid rain droplets falling from above onto a corrosive puddle |
| `omniSolvent.png` | 만상 용해 | an alchemy flask of universal solvent dissolving and melting everything it touches |

### ⚡ 레비나 · `#7cc8ff`
| 파일 | 이름 | CONCEPT |
|---|---|---|
| `thunderfall.png` | 뇌우낙하 | multiple lightning bolts striking straight down from a storm |
| `stormApex.png` | 폭풍정점 | a colossal chained lightning strike at the apex of a storm |

### 🌈 블랑슈 · `#c8b0ff`
| 파일 | 이름 | CONCEPT |
|---|---|---|
| `prismBolt.png` | 프리즘 볼트 | a refracting rainbow bolt splitting into prismatic beams |
| `spectrumBeam.png` | 스펙트럼 빔 | a rotating rainbow piercing beam |
| `chromaBurst.png` | 채도 폭발 | a burst of saturated color exploding outward in all directions |
| `refractionField.png` | 굴절의 장 | a hexagonal refraction barrier bending incoming light |
| `prismCataclysm.png` | 프리즘 종언 | many prismatic beams converging into a single devastating point |
| `whiteEclipse.png` | 백광의 일식 | a pure white supernova bursting through a black eclipse disc |

### 🎭 라라 · `#d070c0`
| 파일 | 이름 | CONCEPT |
|---|---|---|
| `stringWeb.png` | 실 그물 | a web of crossed marionette strings forming a trap |
| `grandGuignol.png` | 그랑 기뇰 | a giant menacing marionette puppet silhouette |

### 🎭 트리나 · `#e0489f`
| 파일 | 이름 | CONCEPT |
|---|---|---|
| `phantomStage.png` | 환영 무대 | a translucent phantom double standing before stage curtains |
| `chromaticSplit.png` | 색수차 분열 | a triple silhouette misaligned into cyan, magenta and yellow layers |
| `encore.png` | 앙코르 | phantom doubles repositioning for a repeat performance |
| `standingOvation.png` | 기립박수 | three phantoms with a burst of applause effect |
| `understudyCall.png` | 대역 소집 | understudy doubles emerging from a backstage door |
| `finalBow.png` | 마지막 인사 | a phantom bowing as it bursts apart in farewell |

### 🎴 카르타 · `#e0b13a`
| 파일 | 이름 | CONCEPT |
|---|---|---|
| `wildDeal.png` | 와일드딜 | spinning playing cards scattered in a fan spray |
| `jackpotRoyale.png` | 잭팟로얄 | an exploding jackpot of gold coins and slot symbols |

### 🐾 카이라 · `#ff8040`
| 파일 | 이름 | CONCEPT |
|---|---|---|
| `huntingClaw.png` | 사냥꾼의 발톱 | three steel claw slash waves flying forward |
| `savageRend.png` | 야수의 참격 | a close-range beast claw arc tearing through |
| `beastCyclone.png` | 야수 선풍 | a spinning cyclone formed of whirling claws |
| `beastForm.png` | 야수 변신 | a half-human half-beast transformation silhouette |
| `primalRampage.png` | 태초의 광란 | trails of repeated leaping beast assaults |
| `apexPredator.png` | 정점의 포식자 | a crowned beast fang marking the apex predator |

### 💤 솜니아 · `#8fd8ff`
| 파일 | 이름 | CONCEPT |
|---|---|---|
| `lullaby.png` | 자장가 | floating music notes with drowsy sleep bubbles |
| `pillowThrow.png` | 베개 던지기 | a pillow hurled forward with feathers scattering |
| `dreamland.png` | 꿈나라 | a dreamy cloud zone of drifting sleep |
| `daydream.png` | 백일몽 | a peaceful nap interrupted by an awakening flash |
| `countingSheep.png` | 양 세기 | cartoon sheep leaping in a line |
| `somnambulism.png` | 몽유 | a sleepwalking silhouette staggering forward |

### 📷 아이리스 · `#c0392b`
| 파일 | 이름 | CONCEPT |
|---|---|---|
| `longExposure.png` | 장노출 | a camera shutter aperture with long light trails |
| `overexposed.png` | 과노출 | a blown-out white monochrome afterimage |
| `contactSheet.png` | 컨택트시트 | a film contact sheet grid of frames |
| `developingTray.png` | 현상액 | a darkroom developing tray with a photo surfacing |
| `flashbulb.png` | 플래시 | a bursting camera flashbulb |
| `darkroomVault.png` | 암실 금고 | a red darkroom lamp over stored ghost afterimages |

### 🔮 엘레미아 · `#4fd6c2`
| 파일 | 이름 | CONCEPT |
|---|---|---|
| `elementCycle.png` | 원소 순환 | wind, fire and ice cycling in a triangular loop |
| `elementalMonarch.png` | 정령왕 강림 | a crowned elemental monarch with three orbiting spirits |

### 🖌️ 스미카 · `#3a3a3a` ※ 먹빛 + **붉은 인장** 포인트
| 파일 | 이름 | CONCEPT |
|---|---|---|
| `inkBlot.png` | 묵점 | spreading black ink blots on paper, with a red accent |
| `finalSeal.png` | 낙관 | a red seal stamp pressing down onto black ink |

### 🗿 갈라테아 · `#c8b890`
| 파일 | 이름 | CONCEPT |
|---|---|---|
| `petrifyGaze.png` | 석화의 응시 | an eye turning to stone as it gazes |
| `petraShatter.png` | 석화 파쇄 | stone spikes erupting then shattering |
| `medusaGaze.png` | 메두사의 시선 | a fan-shaped petrifying gaze sweeping outward |
| `stoneGarden.png` | 석상 정원 | a row of standing stone statues |
| `gorgonRealm.png` | 고르곤의 영역 | a gorgon serpent head over a petrifying field |
| `eternalPetrify.png` | 영겁의 조각상 | a colossal cracking statue collapsing |

### 🛰 에이미 · `#FFB703`
| 파일 | 이름 | CONCEPT |
|---|---|---|
| `droneSwarm.png` | 드론 군집 | a swarm of small drones flying in formation |
| `skyDominion.png` | 제공권 | multi-point precision bombardment raining from the sky |

### 🧲 페리아 · `#3b7fe0` ※ N극 `#ff6b6b` / S극 `#6ba8ff` 이색 대비 활용
| 파일 | 이름 | CONCEPT |
|---|---|---|
| `polarField.png` | 극성장 | a magnetic field of N and S polarity lines |
| `reversePolarity.png` | 역극전환 | polarity arrows flipping and reversing |
| `magRail.png` | 자기 레일건 | a railgun round between two charged rails |
| `magnetStorm.png` | 자기폭풍 | a spiral magnetic pull erupting into a shrapnel blast |
| `ferroShard.png` | 강자성 파편 | a floating cloud of ferromagnetic iron filings |
| `monopole.png` | 단극자 | a single-pole sphere with an inward suction vortex |

---

## 3. 완성 후

`icons/abilities/` 에 파일명 그대로 넣어주시면 전부 로드되는지 실측하고 누락분을 알려드립니다.
