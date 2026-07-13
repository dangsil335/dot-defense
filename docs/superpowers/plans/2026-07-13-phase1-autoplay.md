# 페이즈 1 — 자동진행(AUTO) 구현 계획

> **For agentic workers:** 이 계획은 index.html 단일파일 게임에 대한 것이며, **자동화 테스트 하네스가 없다.** 게임 로직은 IIFE 클로저 스코프라 `preview_eval`로 접근 불가. 따라서 각 태스크의 검증은 **preview_start("dot-defense") + DOM 클릭/스냅샷 + 콘솔 확인 + 육안**으로 한다(pytest 없음). 체크박스(`- [ ]`)로 진행 추적.

**Goal:** 냥냥시노비식 완전 자동진행 토글 — ON이면 카드를 스마트 점수로 자동선택하고 라운드를 자동 시작, 게임오버 시 정지.

**Architecture:** 기존 실시간 `state.autoCardTimer` 메커니즘을 확장. 새 순수함수 `scoreCard(c)`가 카드 3장을 채점, `update()`의 자동선택 블록이 `autoPlay`일 때 argmax를 `applyLevelUpChoice`로 선택. 라운드 자동시작은 `tdPrepPhase` 가드에 훅. AoE 우선 규칙을 위해 광역 능력에 `aoe:true` 데이터 태깅.

**Tech Stack:** Vanilla JS(ES5-ish, IIFE), Canvas 2D, localStorage(META, obfuscated).

## Global Constraints

- 버전 규율: 배포 시 `index.html`의 `APP_VERSION`과 `sw.js`의 `CACHE='dot-defense-vNNN'`를 **동시에** bump. 현재 **v615** → 이 페이즈 완료 배포 시 **v616**.
- 클로저 스코프: `state`/`META`/`ABILITY_DEFS`/`COMBO_PARTNERS` 등은 preview_eval에서 접근 불가 → UI 검증은 DOM 클릭으로.
- META 무결성: `_packMeta`/checksum → localStorage 직접주입 불가. 영속은 `saveMeta()` 경유.
- git 커밋은 함장(사용자)이 명시할 때만. 태스크 체크포인트 = 육안/preview 검증 + (배포 태스크에서) 버전 bump.
- 카드 구조: `{action:'new'|'level'|'combo'|'ascendant'|'bonusScore'|'bonusStardust', id, tier?, lucky?, parts?}`.
- 조합 데이터: `COMBO_PARTNERS[id]` = `[{partner:abilityId, combo:comboId, tier:number}, ...]`(없으면 undefined).

---

### Task 1: 시너지 태깅 (`single` / `mobSynergy`)

> 정제(구현 중 확정): 이 게임은 액티브 대부분이 이미 광역이라 30개에 `aoe:true`를 다는 건 변별력이 없다. 대신 **단일표적 액티브(소수)**와 **몹 시너지 패시브(3개)**만 태깅 → 저비용·고정확.

**Files:**
- Modify: `index.html` (ABILITY_DEFS 정의부)

**Interfaces:**
- Produces: `ABILITY_DEFS[id].single === true`(단일표적 액티브), `ABILITY_DEFS[id].mobSynergy === true`(적수 비례 시너지 패시브). Task 2의 `scoreCard`/`_isAoeHeavyBuild`가 소비.

- [ ] **Step 1: 단일표적 액티브에 `single: true`**

단일 적만 때리는 액티브(desc "단발/단일/최강 적 저격")에 태깅:
- `샷`(L6299), `저격`(L9588), `먹빛 도`(L7235, 스미카 가챠) — 각 `name:` 라인에 `single: true,` 삽입.

- [ ] **Step 2: 몹 시너지 패시브에 `mobSynergy: true`**

적 수·비보스에 비례해 강해지는 = 광역(다굴) 플레이와 시너지 나는 패시브:
- `분노`(L10502, 적5마리당), `쇄도`(L11180, 화면적수당), `토벌`(L11170, 비보스뎀) — 각 `name:` 라인에 `mobSynergy: true,` 삽입.

- [ ] **Step 3: 태깅 개수 확인 (검증)**

```
Grep "single: true" count → 3 (샷/저격/먹빛도)
Grep "mobSynergy: true" count → 3 (분노/쇄도/토벌)
```

---

### Task 2: `scoreCard(c)` 스마트 점수 함수

**Files:**
- Modify: `index.html` — `getCardTier` 함수 근처(현행 L27115 부근)에 신규 함수 추가.

**Interfaces:**
- Consumes: `state.tower.abilities`(보유 배열), `ABILITY_DEFS`, `COMBO_PARTNERS`, `c.action/tier/lucky/id`.
- Produces: `scoreCard(c) -> number` (높을수록 우선). Task 4가 argmax로 사용.

- [ ] **Step 1: 헬퍼 — 보유 셋 & AoE 비율 계산 함수 작성**

`getCardTier` 정의 바로 위에 추가:
```javascript
// 🤖 자동진행 — 카드 스마트 점수. 높을수록 우선 선택.
function _ownedAbilitySet() {
  const s = new Set();
  if (state.tower && state.tower.abilities) for (const a of state.tower.abilities) s.add(a.id);
  return s;
}
function _isAoeHeavyBuild() {
  const abs = (state.tower && state.tower.abilities) || [];
  let act = 0, single = 0;
  for (const a of abs) {
    const d = ABILITY_DEFS[a.id];
    if (!d || d.isPassive) continue;                // 액티브만 카운트
    act++; if (d.single) single++;
  }
  if (act < 3) return false;                        // 초반엔 판단 보류
  return (act - single) / act >= 0.6;               // 액티브의 60%+ 가 광역 → 광역 위주
}
// 이 능력이 미완성 조합의 재료로 쓸모있는가? (트리플 경로 우선)
function _comboPathScore(id, owned) {
  const partners = COMBO_PARTNERS[id];
  if (!partners || !partners.length) return 0;
  const useful = partners.filter(p => !owned.has(p.combo));   // 이미 만든 조합 제외
  if (!useful.length) return 0;
  if (useful.some(p => p.tier === 3)) return 800;             // 트리플로 가는 재료
  return 700;                                                 // 일반 조합으로 가는 재료
}
```

- [ ] **Step 2: `scoreCard(c)` 본체 작성**

바로 이어서 추가:
```javascript
function scoreCard(c) {
  const owned = _ownedAbilitySet();
  if (c.action === 'combo') return c.tier === 3 ? 1000 : 900;   // 1·2: 트리플 > 일반조합
  if (c.action === 'new' || c.action === 'level') {
    const path = _comboPathScore(c.id, owned);                 // 3·4: 조합 재료 우선
    if (path) return path;
    const d = ABILITY_DEFS[c.id];
    if (d && d.isPassive && d.mobSynergy && _isAoeHeavyBuild()) return 650;  // 5: 광역 위주면 몹시너지 패시브(분노/쇄도/토벌)
    if (c.action === 'level') {                                // 6: 강화 (럭키 가점)
      return c.lucky === 2 ? 620 : (c.lucky === 1 ? 600 : 500);
    }
    return 400;                                                // 7: 신규 (조합 경로 없음)
  }
  if (c.action === 'ascendant') return 300;                    // 8
  if (c.action === 'bonusStardust') return 200;                // 9
  if (c.action === 'bonusScore') return 100;
  return 50;
}
// 카드 배열에서 최고점 인덱스 (동점이면 앞쪽)
function bestCardIndex(choices) {
  let bi = 0, bs = -Infinity;
  for (let i = 0; i < choices.length; i++) {
    const s = scoreCard(choices[i]);
    if (s > bs) { bs = s; bi = i; }
  }
  return bi;
}
```

- [ ] **Step 3: 구문 검증**

preview_start("dot-defense") 후 preview_console_logs(level:"error")로 **파싱/런타임 에러 없음** 확인(함수 선언만 추가했으므로 게임 정상 로드돼야 함).
Expected: 콘솔 에러 없음, 게임 메뉴 정상 표시.

---

### Task 3: AUTO 토글 (UI + 상태 + 영속)

**Files:**
- Modify: `index.html` — HUD 컨트롤 HTML(L5965 근처), 배속 핸들러부(L29672 근처), `_capHud` 노드목록(L29702), META 기본값.

**Interfaces:**
- Consumes: `saveMeta()`, `META`.
- Produces: 전역 `autoPlay`(bool), `#autoBtn` 토글, `META.prefAutoPlay` 영속. Task 4·5가 `autoPlay` 읽음.

- [ ] **Step 1: HUD에 AUTO 버튼 추가**

`index.html` L5965 `speedCycle` 버튼 바로 뒤에 추가:
```html
        <button id="speedCycle" class="speed-btn" title="배속 순환">⏩ ×1</button>
        <button id="autoBtn" class="speed-btn" title="자동진행 (카드 자동선택+라운드 자동시작)">🤖 AUTO</button>
```
핫키 힌트(L5967)도 갱신:
```html
      <div class="hotkey-hint">Space: 일시정지 · R: 리셋 · ⏩: 배속 · A: 자동</div>
```

- [ ] **Step 2: `autoPlay` 상태 + 토글 핸들러 + 영속**

배속 핸들러(L29682 `speedCycle.onclick` 블록) 바로 뒤에 추가:
```javascript
// 🤖 자동진행 토글
let autoPlay = false;
function setAutoPlay(on) {
  autoPlay = !!on;
  const b = document.getElementById('autoBtn');
  if (b) { b.classList.toggle('active', autoPlay); b.textContent = autoPlay ? '🤖 AUTO ON' : '🤖 AUTO'; }
  try { META.prefAutoPlay = autoPlay; saveMeta(); } catch (e) {}
}
const _autoBtn = document.getElementById('autoBtn');
if (_autoBtn) _autoBtn.onclick = () => setAutoPlay(!autoPlay);
```

- [ ] **Step 3: 시작 시 선호도 복원 + 배속 옆 이동 대상에 포함**

`_capHud`의 nodes 목록(L29702)에 `'autoBtn'` 추가(가로/세로 전환 시 함께 이동):
```javascript
      nodes: ['s-round','s-gold','s-enemies','s-enemybar','s-time','s-timebar','pauseBtn','resetBtn','menuBtn','speedCycle','autoBtn'].map(g).map(mk).filter(Boolean),
```
그리고 setSpeed 초기화가 있는 init 부근(L29756 `try { setSpeed(gameSpeed); }` 근처)에 복원 호출 추가:
```javascript
    try { setSpeed(gameSpeed); } catch (e) {}
    try { setAutoPlay(!!(META && META.prefAutoPlay)); } catch (e) {}
```
키보드 'A' 핫키(선택) — keydown 핸들러(L29824 Digit1 근처)에 추가:
```javascript
    if (e.code === 'KeyA' && !e.repeat) setAutoPlay(!autoPlay);
```

- [ ] **Step 4: 검증 (토글 동작)**

preview_start 후 게임 진입 → preview_click("#autoBtn") → preview_inspect("#autoBtn", ["className"])로 `active` 포함 확인, 텍스트 'AUTO ON' 확인. 재클릭 시 해제 확인. 새로고침 후에도 상태 유지(META 영속) 확인.

---

### Task 4: 자동 카드선택 훅

**Files:**
- Modify: `index.html` — `update()` 자동선택 블록(L23073~L23080), 카운트다운 라벨(L27533 근처).

**Interfaces:**
- Consumes: `autoPlay`, `bestCardIndex`(Task 2), `applyLevelUpChoice`, `state.autoCardTimer`, `state.levelUpChoices`.

- [ ] **Step 1: 모든 모달 경로에서 autoPlay 타이머 자동 세팅 + argmax 선택**

`update()` 상단 자동선택 블록(현행)을 아래로 교체:
```javascript
    // 자동 카드 선택 타이머 — 실시간 deadline 방식 (게임 속도 배율 영향 X)
    if (state.levelUpChoices && !paused) {
      // 🤖 autoPlay: 모달이 뜬 어떤 경로든 타이머가 0이면 짧게(0.6s) 세팅 → 스마트 선택
      if (autoPlay && state.autoCardTimer === 0) {
        state.autoCardTimer = performance.now() + 600;
      }
      if (state.autoCardTimer > 0 && performance.now() >= state.autoCardTimer) {
        let idx;
        if (autoPlay) {
          idx = bestCardIndex(state.levelUpChoices);            // 스마트 최고점
        } else {
          idx = state.levelUpChoices.findIndex(c => c.action === 'bonusStardust');  // 기존 로직
          if (idx < 0) idx = 0;
        }
        applyLevelUpChoice(idx);
        return;
      }
    }
```

- [ ] **Step 2: 카운트다운 라벨을 autoPlay일 때 문구 변경**

카드 모달 카운트다운 라벨(현행 L27533 `'스타더스트 자동 선택'`)을:
```javascript
      ctx.fillText(autoPlay ? '🤖 자동 선택' : '스타더스트 자동 선택', CX, countY);
```

- [ ] **Step 3: 검증 (자동선택 동작)**

preview_start → 게임 시작 → AUTO ON → 레벨업/카드 모달이 뜨면 ~0.6s 후 자동 사라짐 확인(preview_snapshot 반복 or preview_screenshot). 조합 카드가 있는 상황에서 조합이 선택되는지 육안 확인(도크에 조합 능력 등장). 콘솔 에러 없음.

---

### Task 5: 자동 라운드시작 훅

**Files:**
- Modify: `index.html` — `update()`의 `tdPrepPhase` 가드(L23089 근처).

**Interfaces:**
- Consumes: `autoPlay`, `state.tdPrepPhase`, 라운드 시작 함수(prep 해제).

- [ ] **Step 1: prep phase 자동 해제**

먼저 라운드 시작(Start) 함수명을 확인:
```
Grep pattern: "tdPrepPhase\s*=\s*false|function startRound|function tdStart|startWave"
```
`tdPrepPhase` 가드(현행 `if (state.tdPrepPhase) return;`)를 아래로 교체(실시간 딜레이 0.8s 후 자동시작):
```javascript
    if (state.tdPrepPhase) {
      if (autoPlay) {
        if (!state._autoPrepAt) state._autoPrepAt = performance.now() + 800;
        else if (performance.now() >= state._autoPrepAt) { state._autoPrepAt = 0; startRoundFn(); }  // ← Step에서 확인한 실제 시작 함수/로직
      }
      return;
    }
```
※ `startRoundFn()` 자리에 Step 1 grep으로 찾은 **실제 라운드 시작 트리거**(예: prep 해제 + 스폰 시작을 담당하는 함수 호출, 또는 Start 버튼의 onclick 핸들러 로직)를 넣는다. prep 해제가 단순히 `state.tdPrepPhase=false`라면 그 라인 + 기존 Start 버튼이 하던 초기화를 동일 호출.
그리고 prep 재진입 시 타이머 리셋을 위해, prep가 새로 켜지는 지점에서 `state._autoPrepAt = 0;`을 함께 세팅(라운드 종료→다음 prep 전환부).

- [ ] **Step 2: 검증 (자동 진행)**

preview_start → AUTO ON → 라운드 클리어 후 prep 화면에서 ~0.8s 뒤 자동으로 다음 라운드 시작되는지 확인. AUTO OFF면 수동 Start 대기(회귀 없음) 확인.

---

### Task 6: 버전 bump + 통합 검증 + (선택)커밋

**Files:**
- Modify: `index.html`(`APP_VERSION` → v616), `sw.js`(`CACHE='dot-defense-v616'`).

- [ ] **Step 1: 버전 동시 bump**

`index.html`의 `APP_VERSION` 상수를 616으로, `sw.js` L4 `const CACHE = 'dot-defense-v616';`로.
```
Grep pattern: "APP_VERSION" → 값 615→616
```

- [ ] **Step 2: 통합 플레이 검증**

preview_start("dot-defense") → 한 판 전체:
- AUTO ON → 카드 자동선택(조합 우선 육안) + 라운드 자동시작 + 게임오버까지 무개입 → **오버 시 정지**(재시작 안 함) 확인.
- AUTO OFF → 기존처럼 수동(회귀 없음).
- preview_console_logs(level:"error") 에러 없음.
- 세로/가로 전환 시 AUTO 버튼이 배속과 함께 이동하는지 확인.

- [ ] **Step 3: (선택) 커밋** — 함장이 요청 시에만:
```bash
git add index.html sw.js docs/superpowers
git commit -m "feat(dot-defense): 자동진행(AUTO) — 스마트 카드 자동선택 + 라운드 자동시작 (v616)"
```

---

## Self-Review

- **스펙 커버리지(§2 자동진행):** 범위(완전자동·오버시정지) ✅Task4/5/6, 토글+영속 ✅Task3, scoreCard 점수표 ✅Task2, AoE 태깅 ✅Task1, 라운드 자동시작 ✅Task5, 기존 타이머 재활용 ✅Task4. 갭 없음.
- **Placeholder:** Task1 대상 id·Task5 startRoundFn은 "실행 중 grep으로 확정"으로 명시된 조사 스텝(플레이스홀더 아님, 판정기준·grep 제공). 나머지 실코드 완비.
- **타입 일관성:** `scoreCard`/`bestCardIndex`/`_ownedAbilitySet`/`_isAoeHeavyBuild`/`_comboPathScore`/`setAutoPlay`/`autoPlay` 명칭 태스크 간 일치. `COMBO_PARTNERS[id]` 항목 `{partner,combo,tier}` 일관.
