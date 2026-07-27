# 대표 일러스트(SHOWCASE) + 랭킹 개편 설계

- 작성일: 2026-07-27
- 대상: `index.html` (아크 제로 / Dot Defense)
- 목표: **스킨을 가진 유저의 자부심을 노출**한다. 내 정보에서 대표 일러를 고르고, 그 일러가 글로벌 랭킹에 드러난다.

## 1. 배경

스킨 시스템(v715)으로 로스터 21명 전원이 스킨을 갖게 됐다. 하지만 스킨은 **캐릭터 상세 화면에서만** 보인다. 남에게 보여줄 창구가 없어 구매 동기가 약하다.

글로벌 랭킹은 유일한 대인 노출 지점이지만, 현재는 Top3에만 작은 치비 아바타가 붙고 나머지는 텍스트 행이다.

## 2. 실측 (설계 근거)

| 항목 | 실측값 | 위치 |
|---|---|---|
| 랭킹 행 렌더 | `renderRankRow(rankNum, r, isMe)` — 가로 grid `40px / 1fr / 140px`, Top3만 치비 아바타 | `index.html:24619` |
| `rankings` 컬럼 | `user_id, nickname, title, score, round, ascension, character, updated_at, mode, account_level` — **대표 일러 컬럼 없음** | `index.html:24309` |
| 제출 폴백 | 5단계 체인 (컬럼 없어도 제출 안 깨짐) | `index.html:24230` |
| 내 정보 화면 | `#nicknameModal` "지휘관 데이터 인가" — 닉네임 + 계급 + 약장 picker | `index.html:4709` |
| 드래그 패턴 | `_wireDiffSwipe()` — pointerdown + `setPointerCapture` + 34px 임계 | `index.html:38418` |
| 일러 로딩 | `_applyIllustChain(img, charId, onFail, exactId)` — webp→gif→png 프로브 | 스킨은 `icons/illust/skin/` |
| 보유 판정 | `isCharUnlocked(id)` / `_skinOwned(charId, skinId)` | `index.html:26130`, `35285` |

**후보 개수 실측**: 일러 파일 보유 캐릭 21명 + 스킨 22개 = **최대 43개**.
기본 캐릭 9종(`standard, sniper, engineer, mage, berserker, chronos, researcher, agent, mixer`)은 일러 파일이 없어 후보에서 제외한다.

**세로 크롭 안전성 실측**: 스킨 일러 22종 전부 머리 꼭대기가 이미지 상단 1.2~10.1%(평균 4.5%)에 위치. 3:4 크롭이 세로 범위의 66~100%를 덮으므로 **얼굴 잘림 0건**. 캐릭별 예외 없이 `object-position: 50% 0%` 단일 값으로 22종 전부 커버된다.

## 3. 결정 사항

| 결정 | 선택 | 이유 |
|---|---|---|
| 랭킹 레이아웃 | **Top3 시상대 + 4~10위 세로 썸네일 행** | 모바일 세로 화면에서 가로 스크롤(A안)은 1위만 보임. 전원 대형 카드는 1등의 희소성을 희석 |
| 4~10위 일러 표시 | **세로 3:4 썸네일 + 배경 블러** | 세로 일러를 가로 행 배경으로 깔면 몸통 한 줄만 남아 식별 불가 |
| 서버 | **Supabase 컬럼 추가** | 남이 내 일러를 봐야 "자부심"이 성립 |
| 선택 UI | **큰 미리보기 + 하단 드래그 썸네일 스트립** | 43개를 3~4회 드래그로 훑음. 대표 선택은 비교 행위라 큰 미리보기가 필수 |

## 4. 데이터 모델

```js
META.showcase = 'luna__moonlit'   // 스킨 일러
META.showcase = 'luna'            // 기본 일러
META.showcase = null              // 미설정 (기본값)
```

**핵심**: 이 문자열은 `_resolveIllustId()`가 반환하는 형식과 동일하다. 따라서 기존 `_applyIllustChain(img, id, onFail, exactId)`의 `exactId`에 그대로 넣으면 webp→gif→png 프로브와 `illust/skin/` 경로 분기가 그대로 동작한다. **새 로딩 코드 불필요.**

META는 JSON 블롭 통째로 서버 동기화되므로 스키마 작업이 없다.

## 5. 서버 (Supabase)

### 5.1 마이그레이션 (함장이 1회 실행)

```sql
alter table rankings add column showcase text;
```

### 5.2 제출 (`submitScore`)

기존 5단계 폴백 체인 **맨 위에 0단계를 추가**한다.

- 0단계: `{...fullRow, showcase}` — 컬럼 존재 시 성공
- 1~5단계: 기존 체인 그대로

컬럼이 없으면 0단계만 실패하고 기존 체인이 동작 → **점수 제출은 절대 깨지지 않는다.**

### 5.3 조회 (`fetchRankingsData`)

`fullCols`에 `showcase` 추가. 에러 메시지가 `/showcase/i`에 매칭되면 기존 컬럼셋으로 폴백(기존 `mode`/`title` 폴백과 동일 패턴).

### 5.4 프로필 갱신 (`updateProfile`)

대표 일러 변경 시 `updateProfile` 경로로도 반영한다. 게임을 새로 돌리지 않아도 **즉시** 랭킹에 반영된다.

## 6. 검증 / 보안

`showcase`는 클라이언트가 보내는 값이므로 신뢰하지 않는다. 렌더 직전 화이트리스트 검증:

1. `charId`가 `CHARACTERS`에 존재하는가
2. 스킨 키(`__` 포함)면 `SKINS[charId]`에 해당 `skinId`가 실제로 존재하는가

둘 중 하나라도 실패하면 `character` 컬럼(그 판에 쓴 캐릭)의 기본 일러로 폴백한다.

**알려진 한계**: 서버는 그 유저가 해당 스킨을 실제로 **보유**했는지 알 수 없다(남의 META를 읽을 수 없음). 조작 시 안 산 스킨을 랭킹에 걸 수 있으나 게임 밸런스 피해는 없다. 서버측 보유 검증은 별도 인프라가 필요하므로 이번 범위 밖.

## 7. 렌더링

### 7.1 Top3 시상대 카드

- 배치: 2-1-3 (가운데가 1위, 높이차로 시상대 은유)
- 1위 카드가 가장 큼
- 일러: 3:4 크롭, `object-position: 50% 0%`
- 하단에 닉네임/점수 오버레이 (일러 위 가독성 확보)
- **Top3만 애니 일러 체인**(webp/gif) 허용

### 7.2 4~10위 행

- 행 높이 약 76px
- 왼쪽에 3:4 세로 썸네일 (약 57×76)
- 행 배경: 같은 일러를 `opacity: 0.14` + 확대 크롭으로 은은하게
  - **CSS `filter: blur()`를 쓰지 않는다** — 모바일에서 비쌈. 저투명도 + 확대 크롭으로 분위기만 낸다
- 정지 **png 고정** (애니 금지 — 성능)
- 기존 `isMe` 강조 유지

### 7.3 성능 원칙

랭킹 한 화면에 일러 10장. 전부 애니면 무겁다. **Top3만 애니, 4~10위는 정지 png.**

## 8. 내 정보 — 대표 일러 선택 UI

`#nicknameModal` 안, 약장(`#title-picker`) 섹션 **위**에 새 섹션을 추가한다.

```
▍대표 일러 / SHOWCASE
┌─────────────────────┐
│                     │  ← 큰 미리보기 (3:4, 높이 약 180px)
│      선택된 일러      │
│                     │
│ 루나 · 월광 라군      │  ← 하단 라벨
└─────────────────────┘
[▪][ ][ ][ ][ ][ ]→      ← 가로 드래그 썸네일 스트립
```

- **스트립 항목**: 보유 캐릭 기본 일러 + 보유 스킨. 캐릭별 그룹(기본 → 그 캐릭의 스킨 순)
- **드래그**: `overflow-x: auto` + pointer 드래그-스크롤 (`_wireDiffSwipe` 패턴 차용, `setPointerCapture` 사용)
- **탭 = 선택**: 미리보기 갱신 → `META.showcase` 저장 → `saveMeta()` → `updateProfile()` 서버 반영
- 드래그와 탭 구분: 이동 거리 임계값(약 8px) 미만이면 탭으로 판정 (기존 패턴과 동일)

## 9. 엣지 케이스

| 상황 | 처리 |
|---|---|
| 대표 미설정 | 그 판에 쓴 캐릭(`character`)의 기본 일러 |
| 대표로 건 스킨이 레지스트리에서 삭제됨 | `_resolveIllustId`와 같은 원칙으로 기본 일러 폴백 |
| 일러 파일 로드 실패 | `onerror`로 이미지만 숨기고 행 레이아웃 유지 (기존 `rank-avatar` 패턴) |
| 보유 캐릭 0명(신규 유저) | "캐릭터를 뽑으면 대표 일러를 설정할 수 있어요" 안내 |
| `showcase` 컬럼 미생성 | 내 행에만 내 일러 표시, 남은 `character` 기본 일러 |

## 10. 재사용 / 신규

**재사용**: `_applyIllustChain`(일러 로딩), `_wireDiffSwipe`(드래그 패턴), `isCharUnlocked`/`_skinOwned`(보유 판정), `submitScore` 폴백 체인 패턴, `rank-avatar`의 `onerror` 패턴.

**신규 구현은 두 개뿐**: 썸네일 스트립 UI, 랭킹 카드/행 렌더.

## 11. 범위 밖 (YAGNI)

- 서버측 스킨 보유 검증 (별도 인프라 필요)
- 대표 일러 복수 설정 / 프로필 배경 커스텀
- 랭킹 외 화면(길드, 친구 목록 등)에서의 대표 일러 노출
