# 튜토리얼 Phase 1 (골격) 구현 계획

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans (인라인) 로 task 단위 구현. 이 게임은 단일 index.html + 유닛테스트 프레임워크 없음 → 각 task의 "테스트"는 **브라우저 프리뷰 검증**(콘솔0 · javascript_tool DOM/state 실측 · 네트워크). 실플레이 의존분(R5도달·강제진화 발동)은 rAF 제약상 **기기 검증 필요**로 명시. 커밋마다 APP_VERSION+sw CACHE 동반.

**Goal:** 첫 플레이 유저가 닉네임 설정 직후 튜토리얼에 진입해, 무조건 클리어 가능한 전용 행성에서 R5에 도달하면 솜니아(SSR)로 강제 진화(런 한정, META 격리)하고, 게임 종료 시 튜토리얼이 영구 완료되는 "작동하는 골격"을 만든다. 스포트라이트·안내 말풍선은 Phase 2.

**Architecture:** 신규 상태 `META.tutorial.stage`(intro→planet→evolved→done)를 중심으로, 기존 게임 루프를 조작하지 않고 진입점(setNickname)·게임시작(asc)·진화게이트(maybeTriggerEvolutionGate/showEvoGate)·게임종료(endGame)에 최소 훅을 얹는다. 튜토리얼 행성은 데이터 추가 없이 진입 시 `state.tutorial=true` + `state.asc` 덮어쓰기(임시 asc 주입).

**Tech Stack:** 바닐라 JS(단일 index.html, IIFE 클로저), 서비스워커(sw.js), 서버는 META 전체 JSON 블롭 저장(스키마 작업 불필요).

## Global Constraints

- 파일: `index.html`(전 로직) · `sw.js`(캐시버전)만 수정. 데이터모델(PLANET_TIERS/getAscensionMods/CHARACTERS/GACHA) 불변.
- **🚫 META 격리 절대원칙:** 강제진화는 `state.*`(런 한정)만 건드린다. `META.gachaUnlocked`·`META.selectedCharacter`·기타 META에 솜니아 해금을 **절대 기록하지 않는다**. 완주 후 정상게임에서 솜니아가 가챠/진화트리/도감에 공짜로 뜨면 실패.
- **기존 유저 보호:** 이미 플레이 중인 계정(닉네임 보유)에게 튜토리얼이 소급 발동하면 안 됨. 신규 판정 = 첫 `setNickname()` 시점 `META.tutorial===undefined && !META.tutorialDone`.
- 신규 헬퍼/상수는 모두 기존 IIFE 클로저 안에 정의(전역 오염 없음). 커밋 메시지 한국어, 말미에 `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`.
- 매 커밋 `APP_VERSION`(index.html L38301 부근)과 `sw.js` `CACHE = 'dot-defense-vNNN'` 동시 증가.

---

### Task 1: 튜토리얼 상태 코어 (META.tutorial + 헬퍼 + 마이그레이션)

**Files:**
- Modify: `index.html` — 헬퍼는 `saveMeta()`(L22511) 정의 부근(META 유틸 구역)에 추가. 마이그레이션은 부팅 1회 실행 구역(예: `_ensureGear`/초기 마이그레이션이 도는 곳, L6877 부근 `saveMeta()` 마이그 패턴 참조).

**Interfaces (Produces — 이후 모든 task가 사용):**
- `_tutStage()` → `'intro'|'planet'|'evolved'|'done'|null` : `META.tutorial ? META.tutorial.stage : null`
- `_tutSetStage(s)` : `META.tutorial = META.tutorial||{}; META.tutorial.stage = s; if (s==='done') META.tutorialDone = true; saveMeta();`
- `_tutActive()` → bool : `!!_tutStage() && _tutStage() !== 'done' && !META.tutorialDone`
- `_tutStart()` : 신규 진입 — `META.tutorial = { stage:'intro' }; saveMeta();`
- `_tutDone()` → bool : `!!META.tutorialDone || _tutStage()==='done'`

- [ ] **Step 1: 헬퍼 5종 추가**

`saveMeta()` 정의(L22511) 바로 앞이나 뒤(같은 함수 구역)에 삽입:

```js
// ===== 🎓 튜토리얼 상태 (META.tutorial.stage: intro→planet→evolved→done) =====
function _tutStage() { return (META && META.tutorial) ? META.tutorial.stage : null; }
function _tutSetStage(s) {
  if (!META.tutorial) META.tutorial = {};
  META.tutorial.stage = s;
  if (s === 'done') META.tutorialDone = true;
  try { saveMeta(); } catch (e) {}
}
function _tutActive() { const s = _tutStage(); return !!s && s !== 'done' && !META.tutorialDone; }
function _tutStart() { META.tutorial = { stage: 'intro' }; try { saveMeta(); } catch (e) {} }
function _tutDone() { return !!(META && (META.tutorialDone || _tutStage() === 'done')); }
```

- [ ] **Step 2: 기존 유저 마이그레이션 (부팅 1회)**

부팅 마이그레이션 구역(L6877 `if (_mig) { saveMeta(); }` 패턴이 있는 초기화 흐름)에서, META 로드 직후 실행:

```js
// 🎓 기존 유저는 튜토리얼 소급 발동 금지 — 닉네임이 이미 있고 튜토리얼 기록이 없으면 '완료'로 봉인
if (META && META.nickname && META.tutorial === undefined && !META.tutorialDone) {
  META.tutorialDone = true; try { saveMeta(); } catch (e) {}
}
```

- [ ] **Step 3: 검증 (브라우저)**

프리뷰 로드 → `javascript_tool`:
- 기존 계정(닉네임 보유, localStorage 유지) 로드 시 `META.tutorialDone===true`, `_tutActive()===false` 여야 함(closure라 직접 못 부르면 다음 task의 진입훅으로 간접 검증).
- 콘솔 에러 0.
Expected: 기존 유저에게 튜토리얼 미발동.

- [ ] **Step 4: 커밋**

```bash
git add index.html
git commit -m "feat(tutorial): 상태 코어 META.tutorial + 헬퍼 5종 + 기존유저 봉인 마이그레이션"
```

---

### Task 2: 진입 훅 (setNickname → intro) + 솜니아 인트로 컷인

**Files:**
- Modify: `index.html` — `setNickname(n)`(L22796 `META.nickname = n.trim();` 직후). 인트로 컷인은 기존 컷인 시스템(`showCharComboCutin` L34899 부근 / `char-cutin`)의 실제 시그니처를 **구현 시 읽어** 재활용. 대사 테이블 `TUTORIAL_LINES` 신규(CHAR_AMBUSH_LINES 부근).

**Interfaces:**
- Consumes: `_tutStart()`, `_tutStage()` (Task 1)
- Produces: `_tutIntro()` — 인트로 컷인 재생 후 메뉴로. `TUTORIAL_LINES = { intro:[3줄], evolve:'...', done:'...' }`

- [ ] **Step 1: 대사 테이블 추가 (나른·반말·딸 톤)**

`CHAR_AMBUSH_LINES` 정의 부근에:

```js
const TUTORIAL_LINES = {
  intro: [
    '으음… 왔구나, 함장. 나 솜니아라고 해. 반가워—.',
    '여긴 처음이지? 걱정 마, 내가 옆에서 알려줄게. 어렵지 않아.',
    '자, 저 아래 행성 하나 골라서 시작해 보자. 가볍게.'
  ],
  evolve: '이제 날 불러! 저 카드 누르면 내가 나올게. 이번만 특별히 도와주는 거야.',
  done: '거봐, 할 만하지? 이제 진짜 시작이야. 잘 부탁해, 함장.'
};
```

- [ ] **Step 2: 진입 훅 (setNickname)**

`setNickname` 안 `META.nickname = n.trim();` 직후 삽입:

```js
// 🎓 신규 유저 첫 닉네임 → 튜토리얼 시작 (기존 유저는 Task1 마이그레이션으로 tutorialDone=true라 여기 안 걸림)
if (META.tutorial === undefined && !META.tutorialDone) {
  _tutStart();               // stage='intro'
  try { _tutIntro(); } catch (e) {}
}
```

- [ ] **Step 3: `_tutIntro()` 구현 (기존 컷인 재활용)**

구현 시 `showCharComboCutin`(L34899)의 실제 인자/동작을 읽고, 솜니아 일러(somnia.png 존재) + `TUTORIAL_LINES.intro` 3연을 순차 표시하는 최소 컷인으로 작성. 컷인 종료 콜백에서 `showScreen('menu')` 보장. (Phase 1은 스포트라이트 없이 컷인만.)

- [ ] **Step 4: 검증 (브라우저)**

localStorage 초기화 → 새 계정/닉네임 설정 흐름 진행 → `javascript_tool`로 `_tutStage()` 간접 확인(메뉴 게이팅 활성 여부/`document`에 컷인 DOM 존재). 콘솔 0.
Expected: 신규 닉네임 설정 시 stage='intro', 인트로 컷인 표시.

- [ ] **Step 5: 커밋**

```bash
git add index.html
git commit -m "feat(tutorial): 진입 훅(setNickname→intro) + 솜니아 인트로 컷인·대사"
```

---

### Task 3: 메뉴 게이팅 (튜토리얼 중 다른 버튼/행성 잠금)

**Files:**
- Modify: `index.html` — 메뉴 렌더 갱신 함수(`refreshMenuButtons`/`refreshMenuHero` 부근, showScreen('menu') 진입 구역). 대상 버튼 id: 차원스카우트(gachaBtn)·강화소·도감·능력영구(abilityPerma)·업적·캐릭터진화·기록. 허용: 새 게임(startBtn).

**Interfaces:**
- Consumes: `_tutActive()` (Task 1)
- Produces: `_tutApplyMenuGate()` — active면 대상 버튼 `disabled`+`.tut-locked`, 아니면 해제.

- [ ] **Step 1: 게이팅 함수**

구현 시 메뉴 버튼들의 실제 id를 읽어(read_page로 확인된: `gachaBtn`, 강화소/도감/능력영구/업적/캐릭터진화/기록 버튼) 배열화:

```js
function _tutApplyMenuGate() {
  const active = _tutActive();
  const LOCK = ['gachaBtn', /* 강화소·도감·능력영구·업적·캐릭터진화·기록 버튼 id — 구현 시 실측 */];
  LOCK.forEach(id => { const b = document.getElementById(id); if (!b) return;
    b.disabled = active; b.classList.toggle('tut-locked', active);
    if (active) b.title = '튜토리얼 완료 후 열려요'; });
}
```

- [ ] **Step 2: `.tut-locked` CSS + showScreen 훅**

CSS(코스믹 UI 톤): `.tut-locked{opacity:.4;filter:grayscale(.6);pointer-events:none;}`. `showScreen('menu')` 진입 블록(refreshMenuHero 호출 옆)에서 `try{_tutApplyMenuGate();}catch(e){}` 호출.

- [ ] **Step 3: 검증 (브라우저)**

튜토리얼 활성 프로필 → 메뉴 → read_page: 대상 버튼 `disabled`/회색, 새게임만 활성. `_tutDone` 프로필 → 전부 활성. 콘솔 0.

- [ ] **Step 4: 커밋**

```bash
git add index.html
git commit -m "feat(tutorial): 메뉴 게이팅 — 튜토리얼 중 새게임 외 잠금"
```

---

### Task 4: 튜토리얼 행성 진입 + asc 주입 (무조건 클리어)

**Files:**
- Modify: `index.html` — 행성선택 화면(`#difficultyScreen`, L4211~) 및 게임 시작 asc 세팅(L22105-22107 `state.ascension`/`state.asc`). 튜토리얼 mods 상수 신규.

**Interfaces:**
- Consumes: `_tutActive()`, `_tutSetStage()` (Task 1)
- Produces: `TUTORIAL_ASC` 상수 · `state.tutorial` 플래그 · `_tutStartPlanet()`

- [ ] **Step 1: 튜토리얼 asc 상수 (무조건 클리어)**

`getAscensionMods`(L24456) 부근에:

```js
// 🎓 튜토리얼 전용 난이도 — 무조건 클리어 가능 + 파밍 방지(보상 극소)
const TUTORIAL_ASC = {
  enemyHpMul: 0.45, bossHpMul: 0.5, maxAliveAdd: 40, scoreReward: 0.05,
  stardustMul: 0.05, enemySpeedMul: 0.75, extraBossCount: 0, eliteEscorts: 0,
  extraBossRounds: false, bossDmgMul: 0.4, enemyCountAdd: 0, roundTimeMul: 0.7,
  enhanceMul: 1, startGoldMul: 1, startScoreMul: 1
};
```

- [ ] **Step 2: 게임 시작 시 asc 주입**

게임 시작(L22105-22107 `state.ascension = getSelectedAscension(); ... state.asc = getAscensionMods(...)`) 직후 삽입:

```js
// 🎓 튜토리얼 런이면 난이도를 무조건-클리어로 덮어씀 (PLANET_TIERS/getAscensionMods 불변)
if (_tutActive() && state.tutorial) {
  state.asc = Object.assign({}, TUTORIAL_ASC);
  state.ascension = 0;
}
```

- [ ] **Step 3: 행성선택 게이팅 + 튜토리얼 진입 라우팅**

구현 시 `#difficultyScreen`(L4211~)의 행성 오브(planet-orb) 클릭 핸들러/렌더를 읽고: `_tutActive()`면 실제 3행성을 `.planet-lock` 잠금, "튜토리얼" 진입 하나만 활성화. 그 진입 클릭 = `_tutStartPlanet()`:

```js
function _tutStartPlanet() {
  if (_tutStage() === 'intro') _tutSetStage('planet');   // 행성 진입 = planet 단계
  state = state || {};   // (실제 게임시작 함수 호출 경로에 맞춤 — 구현 시 startGame 진입점 사용)
  // startGame 진입 시 state.tutorial=true 세팅되도록 플래그를 넘긴다(구현 시 startGame 시그니처 확인)
}
```
`startGame`(게임 시작 함수) 진입에서 튜토리얼이면 `state.tutorial = true` 세팅(Step 2 조건과 연결).

- [ ] **Step 4: 검증 (브라우저 + 기기)**

브라우저: 튜토리얼 프로필 → 행성선택 → 3행성 잠금·튜토리얼만 활성(read_page). 게임 시작 후 `state.asc` 실측(javascript_tool) = TUTORIAL_ASC 값, `state.tutorial===true`. **기기 검증:** 실제로 안 지고 R5까지 도달 가능한지(rAF 제약상 프리뷰 불가).

- [ ] **Step 5: 커밋**

```bash
git add index.html
git commit -m "feat(tutorial): 전용행성 진입 + 임시 asc 주입(무조건 클리어)"
```

---

### Task 5: R5 솜니아 강제진화 (핵심·위험 — META 격리)

**Files:**
- Modify: `index.html` — `maybeTriggerEvolutionGate(roundNum)`(L34793) 상단 우회 분기 · `showEvoGate(kind,id[,forced])`(L34846) 거절 비활성 인자.

**Interfaces:**
- Consumes: `_tutActive()`, `_tutStage()`, `_tutSetStage()` (Task 1), 기존 `showEvoGate`·`applyEvolution`(L34866, state.character만 세팅·META 불변)
- Produces: 없음(진화 후 stage='evolved')

**⚠️ 실제 진화 구조:** R5=base→R(카드드래프트), R20=R→SR, R40=SR→SSR. 튜토리얼은 R5에서 **정상 base→R 게이트를 가로채** 솜니아 SSR 게이트를 강제한다(짧은 튜토리얼). `applyEvolution('SSR','somnia',sig)`는 `state.character='somnia'`만 세팅 → META 격리 구조적 보장.

- [ ] **Step 1: `showEvoGate`에 forced 인자 (거절 비활성)**

L34846 시그니처 `function showEvoGate(kind, id)` → `function showEvoGate(kind, id, forced)`. 버튼 배선부(L34862-34864) 교체:

```js
const yes = document.getElementById('evoYes'), no = document.getElementById('evoNo');
if (yes) yes.onclick = () => {
  el.style.display = 'none'; paused = el._prevPaused || false;
  applyEvolution(kind, id, info.abId);
  if (forced && state && state.tutorial && kind === 'SSR' && id === 'somnia') _tutSetStage('evolved');
};
if (no) {
  no.style.display = forced ? 'none' : '';   // 🎓 튜토리얼 강제진화 = 거절 버튼 숨김
  no.onclick = forced ? null : () => { el.style.display = 'none'; paused = el._prevPaused || false; try { toast('진화 거절 — 현 단계 유지'); } catch (e) {} };
}
```
(정상 게이트는 `forced` 미전달 → undefined → 거절 버튼 정상 표시. L34797 호출 무변.)

- [ ] **Step 2: R5 우회 분기 (`maybeTriggerEvolutionGate` 상단)**

L34793 함수 본문 첫 줄에 삽입:

```js
// 🎓 튜토리얼: R5에 도달하면 정상 base→R 게이트를 가로채 솜니아 SSR 게이트를 강제(거절 불가)
if (_tutActive() && _tutStage() === 'planet' && state && state.tutorial && (roundNum || state.round) === 5) {
  showEvoGate('SSR', 'somnia', true);
  return true;
}
```

- [ ] **Step 3: 격리 정적 확인 (코드 리뷰)**

`applyEvolution`(L34866-34906) 경로에 `META.` 쓰기가 없는지 grep 재확인. `unlockAbility(abId)`(L34897)가 META를 건드리는지 확인 — 만약 도감/영구해금을 META에 기록하면 그건 능력(솜니아 시그)이지 캐릭터 가챠해금이 아니므로 격리 원칙(가챠/진화트리/도감 캐릭터 노출)과 무관하나, **`unlockAbility`가 캐릭터 해금까지 건드리지 않는지 구현 시 확인**.

- [ ] **Step 4: 검증 (기기 필수)**

강제진화는 R5 실도달이 필요 → **기기 검증:** 튜토리얼 플레이 → R5 보스 처치 → 솜니아 SSR 게이트가 뜨고 **거절 버튼 없음**, 진화 시 `state.character==='somnia'`, stage='evolved'. 브라우저 정적 확인: `showEvoGate('SSR','somnia',true)` 강제호출 시 evoNo 숨김·evoYes 동작(javascript_tool로 게이트 DOM 강제표시).

- [ ] **Step 5: 커밋**

```bash
git add index.html
git commit -m "feat(tutorial): R5 솜니아 강제진화 — 게이트 우회 + 거절 비활성(state.character만, META 격리)"
```

---

### Task 6: 완료 처리 (endGame → done + 잠금 해제)

**Files:**
- Modify: `index.html` — `endGame(reason, win)`(L22319).

**Interfaces:**
- Consumes: `_tutStage()`, `_tutSetStage()` (Task 1)

- [ ] **Step 1: 게임 종료 시 튜토리얼 완료**

`endGame`(L22319) 본문, `state.gameOver = true;`(L22321) 직후 삽입:

```js
// 🎓 튜토리얼: 솜니아 진화까지 마친 런이 끝나면(승/패 무관) 튜토리얼 영구 완료
if (state && state.tutorial && _tutStage() === 'evolved') {
  _tutSetStage('done');   // tutorialDone=true + saveMeta (Task1)
  try { if (typeof queueServerSync === 'function') queueServerSync(true); } catch (e) {}
}
```

- [ ] **Step 2: 검증 (기기)**

**기기:** 강제진화 후 게임 종료(승 또는 패) → `META.tutorialDone===true`, 메뉴 복귀 시 전 버튼 활성(Task3 게이트 해제), 재접속해도 튜토리얼 미발동. 브라우저 정적: `endGame` 호출 경로에서 stage='evolved'→'done' 전이 확인.

- [ ] **Step 3: 커밋**

```bash
git add index.html
git commit -m "feat(tutorial): 완료 처리 — 진화 후 종료 시 done+서버동기화, 잠금 해제"
```

---

### Task 7: 버전업 + 격리 검증 (완주 후 솜니아 공짜 미노출)

**Files:**
- Modify: `index.html`(APP_VERSION) · `sw.js`(CACHE)

- [ ] **Step 1: 버전 증가**

`index.html` `APP_VERSION = 699` → `700`, `sw.js` `CACHE = 'dot-defense-v699'` → `'v700'`.

- [ ] **Step 2: 브라우저 부팅 검증**

프리뷰 리로드 → 콘솔 0, `APP_VERSION`/CACHE v700 서빙 확인, 게임 정상 부팅.

- [ ] **Step 3: 🔑 격리 검증 (핵심, 기기)**

신규 프로필로 튜토리얼 완주(진입→튜토리얼행성→R5 솜니아 강제진화→종료→done) 후, **정상 게임에서:**
- 가챠 풀에 솜니아가 공짜로 안 뜬다(뽑아야 등장).
- 진화트리/도감에서 솜니아가 잠금 상태(가챠 미해금).
- `javascript_tool`(가능 범위): `META.gachaUnlocked['somnia']`가 `undefined`/0.
Expected: 튜토리얼로 솜니아를 "체험"했지만 영구 소유는 안 됨.

- [ ] **Step 4: 커밋**

```bash
git add index.html sw.js
git commit -m "chore(tutorial): v700 — Phase 1 골격 완료 + 격리 검증"
```

---

## Phase 1 완료 판정

- [ ] 신규 유저: 닉네임 설정 → 인트로 → 튜토리얼 행성만 선택 가능 → 무조건 클리어로 R5 도달 → 솜니아 강제진화(거절 불가) → 종료 시 done → 전 잠금 해제.
- [ ] 기존 유저: 튜토리얼 미발동(마이그레이션 봉인).
- [ ] **격리:** 완주 후 솜니아가 가챠/진화트리/도감에 공짜 미노출.
- [ ] 콘솔 에러 0, 기존 게임 흐름 회귀 없음.

## Phase 2 (다음 계획)
B 스포트라이트 강제 오버레이(getBoundingClientRect 런타임 구멍) · D 이벤트감지 안내 말풍선(levelUpChoices/isCombo 조합카드 감지) · 튜토리얼 각 단계 안내 트리거.
