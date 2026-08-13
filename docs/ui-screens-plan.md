# 화면 UI 전면 개편 — 스텔라소라 문법으로

> 레퍼런스: 스텔라소라 5화면 (캐릭터 호감도 / 레코드 조합 / 난이도 선택 / 기록 상세 / 별의 탑)
> 로비(menu)는 v806~v823 에서 먼저 끝냈다. 이 문서는 **나머지 16화면**을 다룬다.

---

## 0. 핵심 발견 — 레퍼런스는 화면마다 새로 디자인하지 않는다

스텔라소라 5화면을 늘어놓으면 **같은 부품 8개를 재배치**하고 있을 뿐이다.
그래서 우리도 부품을 먼저 통일하면 화면 16개가 거의 따라온다.

| 부품 | 레퍼런스에서 보이는 곳 |
|---|---|
| **상단 바** | 전 화면. 원형 뒤로가기 + 위치 알약 + 홈, 우측에 필터/정렬 |
| **하단 탭** | 캐릭터 상세 (상세·스킬·잠재력·특성·호감도) |
| **패널** | 전 화면. 둥근 모서리 + 반투명 + 얇은 테두리 |
| **리스트 행** | 여행가 스토리 (썸네일 + 제목 + 쉐브론) |
| **카드 그리드** | 레코드 조합 (아트 + 모서리 배지 + 선택 테두리) |
| **칩/알약** | 전 화면. 탭·등급·비용·레벨 전부 알약 |
| **잠김 상태** | 난이도 선택 (흐림 + 자물쇠 + 해제 조건) |
| **하단 액션 바** | 레코드 조합 (좌: 정보 / 우: 확인) |

---

## 1. 우리 화면 17개 — 실측

`.screen` 17개. 그중 **13개가 이미 `.codex-header` 를 공유**한다.

| 공용 클래스 | 화면 수 | 화면 |
|---|---|---|
| `.codex-header` | **13** | globalRank, achievements, mode, character, evoTree, evoDetail, coreMgr, difficulty, shop, abilityPerma, records, recordDetail, codex |
| `.codex-tabs` | 6 | globalRank, achievements, character, shop, abilityPerma, codex |
| `.up-hero` `.up-dialog` `.up-list` `.up-tabs` | 4 | achievements, shop, abilityPerma, codex |
| 없음 | 4 | menu(완료), gachaScreen, gachaTuning, gachaResult |

**이미 "캐릭터 아트 + 우측 패널" 구조를 가진 화면이 4개** 있다(`.up-hero` + `.up-dialog`).
레퍼런스 1번(캐릭터 호감도)과 같은 골격이다.

---

## 2. 단계

### ✅ 1단계 — 공용 크롬 (v824~825, 완료)

한 블록으로 13화면 상단이 동시에 바뀐다. 스타일시트 맨 끝에 둬서 순서로 이긴다.

- `.codex-header` → 원형 뒤로가기(38px) + 제목 알약 + 우측 자원 칩
  - DOM 순서가 화면마다 달랐다(10개는 `h2+back`, 2개는 `h2+bar+back`, 1개는 `back+h2+hud`).
    `order` 로 시각 순서를 통일했다 → 13/13 뒤로가기가 좌측 2px 에 정렬
- `.codex-tabs > button` → 알약. 활성은 채워진 파랑
- 4화면이 밑줄·마름모 네온 탭을 **ID 2개짜리 선택자 + !important** 로 걸어놨다.
  클래스로는 못 이겨서 같은 특이도로 맞춰 무력화했다
  (`#achievementsScreen #ach-tabs .codex-tab` 등)
- 토큰: `--ss-panel` `--ss-edge` `--ss-ink` `--ss-accent` `--ss-r` `--ss-pill` `--ss-shadow`

### 2단계 — 리스트·패널 (4화면)

`.up-hero` `.up-dialog` `.up-list` 를 레퍼런스의 **캐릭터 아트 + 우측 패널 + 리스트 행**으로.

- 리스트 행 = 썸네일(둥근 사각) + 제목(굵게) + 부제(흐림) + 쉐브론 `›`
- 행 전체가 둥근 사각 카드. 잠김은 흐림 + 자물쇠 + 해제 조건 한 줄
- 대상: `achievementsScreen` `shop` `abilityPerma` `codex`

### 3단계 — 화면별 (레퍼런스 1:1 대응)

| 우리 화면 | 레퍼런스 | 할 일 |
|---|---|---|
| `characterScreen` | ① 캐릭터 호감도 | 좌 캐릭터 아트 + 우 패널 + 하단 탭 |
| `coreMgrScreen` | ② 레코드 조합 | 좌 장착 슬롯 + 우 카드 그리드 + 하단 액션 바 |
| `difficultyScreen` | ③ 난이도 선택 | 행 = 라벨칩 + 썸네일 + 이름, 잠김은 자물쇠+조건 |
| `records` `recordDetail` | ④ 기록 상세 | 좌 요약 패널 + 우 탭 + 타일 그리드 |
| `modeScreen` | ③ 응용 | 큰 카드 2~3장 |
| `evoTreeScreen` `evoDetailScreen` | ① 응용 | 트리는 유지, 크롬만 |
| `globalRankScreen` | ④ 응용 | 시상대 + 리스트 행 |
| 가챠 3화면 | ⑤ 별의 탑 | 배너 카드 + 비용 칩 + 보상 아이콘 행 |

---

## 3. 타이포 (미정 — 함장 선택 대기)

현재 (L15~17, Google Fonts CDN — **다운로드 없이** 쓰는 중):

```
Jua               body 기본. 이미 둥글고 말랑한 한글
Black Han Sans    로고
Rajdhani          --hud-font + 인게임 캔버스 93곳. SF 콘덴스드 = 우주 컨셉 잔재
IBM Plex Sans KR  Rajdhani 의 한글 폴백
```

⚠ Rajdhani 는 **라틴 전용**이라 한글은 실제로 IBM Plex Sans KR 로 떨어진다.
즉 지금 화면의 "SF 느낌"은 숫자·영문에서만 난다.

⚠ 93곳 중 대부분이 `ctx.font = '...Rajdhani...'` **하드코딩**이다.
`--hud-font` 변수는 8곳만 쓴다. 바꾸려면 문자열 일괄 치환이 필요하다(기계적).

⚠ PWA 오프라인: 지금은 폰트가 CDN 이라 오프라인이면 시스템 폰트로 떨어진다.
자체 호스팅하면 `sw.js` 에 넣어 오프라인에서도 유지된다(개선).
