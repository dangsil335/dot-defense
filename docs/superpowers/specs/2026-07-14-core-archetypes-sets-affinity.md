# 전술 코어 심화 — 아키타입 · 세트 · 캐릭터 동조 · 레전드 고유

> 작성일: 2026-07-14 · 대상: `index.html` · 전제: Phase 2 코어(4슬롯·4등급·라인·별조각리롤·드랍) 이미 구현(v641).
> **구현 상태(2026-07-14): T1(v642) · T2(v643) · T3 4피스(v644) · T3b 레전드 고유라인(v649) 전부 완료.** (부가: 코어 이미지 v645, 처리시스템 잠금/일괄분해/합성 v646, 동기화 묘비 v647.)
> 목표: 코어에 **정체성**(등급마다 하나뿐 해소) + **캐릭터 시너지**("이 캐릭한테 어울리는") + **세트**(수집·UI) 부여.

## 확정 결정 (2026-07-14, 함장)
1. **구조 = 통합형**: 코어 하나 = `세트 × 슬롯`. 3세트 × 4슬롯 = 12기종. 아키타입과 세트를 하나로.
2. **캐릭터 동조 = 소프트**: 매칭 캐릭이면 풀 보너스, 미매칭이어도 **절반**은 발동(마이너스 아님, 덜 억울, 범용성↑).
3. **세트 4피스 = 시그니처 메커니즘**: 라운드시작 전체빙결·처치 골드폭발·보스등장 즉딜 같은 특수효과(전투 커스텀 훅). 세트당 1개.

## 통합 데이터 모델
```
core = { id, slot, set, rarity, level, lines[], v }   // ← set 신규 필드
  slot: offense|targeting|supply|control
  set:  destroyer|cryomancer|alchemist
  (slot,set) → 기종명 + 시그니처 확정 라인
  lines: [시그니처(확정)] + [일반 랜덤]*(등급수-1) + [에픽↑ 동조 라인?] + [레전드 고유 라인?]
```
등급별 라인 수(기존 유지): common1 · rare2 · epic2 · legend3. 시그니처가 1줄 차지, 나머지 랜덤.

## 3세트 × 4슬롯 (기종 · 시그니처 · 어울리는 캐릭)
| 세트 | 색/아이콘 | 화력 | 조준 | 보급 | 제어 | affinity |
|---|---|---|---|---|---|---|
| **destroyer 파괴자** | ⚔ #ff5b6e | 폭격(dmgBoost) | 관통(bossDmgMul) | 전리품(scoreMul) | 처형(luckyChanceBonus) | berserker·sniper·solar |
| **cryomancer 빙결술사** | ❄ #7ad7ff | 서리(comboPowerBonus) | 한파(bossDmgMul) | 결정(goldMul) | 빙결(slowMul) | mage·marine |
| **alchemist 연성술사** | 💰 #ffd479 | 촉매(comboPowerBonus) | 정밀(dmgBoost) | 황금(goldMul) | 행운(luckyChanceBonus) | mixer·engineer·researcher |

시그니처 중복 허용(세트가 정체성 캐리). 비-시그니처 라인은 슬롯 풀에서 랜덤.

## 확장 옵션 풀 (build-time metaMods만 — 패시브 파생 제외)
안전 키: dmgBoost, comboPowerBonus, bossDmgMul, goldMul, scoreMul, slowMul, luckyChanceBonus, roundTimeBonus, levelUpMul(신규 채용, 강한 편이라 캡 타이트).
- offense: dmgBoost, comboPowerBonus
- targeting: bossDmgMul, dmgBoost
- supply: goldMul, scoreMul, levelUpMul
- control: slowMul, luckyChanceBonus, roundTimeBonus

## 세트 보너스
- **2피스**(같은 세트 2슬롯): 단순 metaMods. destroyer=데미지+8% · cryomancer=슬로우+12% · alchemist=골드+15%.
- **4피스**(전 슬롯 같은 세트): 시그니처 메커니즘(커스텀 훅) + 큰 수치 1줄.
  - destroyer: 보스 등장 시 즉시 현재체력 15% 딜 (+보스뎀 큰 수치)
  - cryomancer: 라운드 시작 시 전체 2초 빙결 (+슬로우 큰 수치)
  - alchemist: 처치 시 5% 확률 골드 폭발(주변 골드 획득) (+골드 큰 수치)

## T2 캐릭터 동조 라인 (에픽↑ 등장)
- 별도 라인 카테고리. 롤 시 `affinityKey` + 대상 캐릭 세트.
- **소프트 적용**: `applyGearEffects`에서 현재 state 캐릭이 대상군에 있으면 풀 val, 아니면 val×0.5.
- 예: ⚡저격동조(boss+Y%, sniper·berserker) · ❄빙결동조(slow+Y%, mage·marine) · 🔗조합촉매(combo+Y%, mixer·engineer·marine·solar) · ⏱시간동조(levelUpMul, chronos) · 💢폭주동조(dmg+Y%, berserker).
- UI: 현재 주력캐 매칭이면 컬러, 아니면 "절반 적용" 뱃지(반투명).

## T3 레전드 고유 라인
- 레전드 코어 전용 라인 슬롯 1개. 단순 배수 아닌 커스텀 훅.
- 후보(세트 4피스와 별개 or 공유): 조합 시 15% 추가 조합카드 · 첫 보스 즉딜 · 라운드시작 슬로우 · 처치 골드폭발 · 시작 시 랜덤 능력 +1.
- 전투 루프 훅은 하나씩 추가(감당 범위). 4피스 메커니즘과 구현 공유.

## 세트 UI (코어 관리 화면)
- **세트 현황 패널**: 세트별 (N/4) 게이지 + 채운 슬롯 체크/빈슬롯 dim + 2피스/4피스 보너스 라인.
  - 활성 = 세트색 글로우 「활성」 · 미충족 = grayscale 「비활성」+"N개 더".
- **코어 카드 세트 태그**(⚔/❄/💰) — 소속 한눈에.
- 슬롯 얹기 미리보기: "착용 시 파괴자 3→4피스" 라이브.
- 동조 라인 상태색: 주력캐 매칭=컬러 / 미매칭=반투명+"절반".

## 동기화 · 캡 · 마이그레이션
- 코어에 `set` 필드 실림 → `createGear` 각인, inv union(id+v)로 이동. merge 추가필드 없음(세트보너스는 런타임).
- 동조·고유 라인용 **GEAR_CAP 신규 항목** + 소프트 배율은 캡 이후 적용.
- **레거시 코어 마이그레이션**: 기존 `set` 없는 코어 → 슬롯 시그니처에 맞는 세트 추정 배정 or 'neutral'(세트 불참, 개별 라인만). 안전하게 로드시 1회 스탬프.

## 페이즈 분할 (독립 배포)
| T | 범위 | metaMods | 난이도 |
|---|---|---|---|
| **T1** | 12기종 + set필드 + 옵션풀확장 + 시그니처확정 + 세트태그/현황UI + 2피스 + 레거시마이그레이션 | ✅ | 낮음 |
| **T2** | 캐릭터 동조 라인(에픽↑) + 소프트적용 + 동조 UI상태 + 리롤지원 | ✅+캐릭체크 | 중간 |
| **T3** | 레전드 고유라인 + 세트 4피스 시그니처 메커니즘(커스텀 훅) | ⚠️훅 | 높음 |

## 미해결 (진행 중 확정)
- 세트 테마명/색 최종(파괴자/빙결술사/연성술사 잠정).
- 옵션풀 최종 수치·캡·동조 val.
- 캐릭별 코어 프리셋(로드아웃)은 v2로 보류(소프트 동조가 당장 커버).
- 코스믹(5등급)은 확장 여지로 남김.
