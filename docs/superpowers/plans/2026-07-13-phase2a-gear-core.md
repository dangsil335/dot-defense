# 페이즈 2a — 장비 코어 (데이터+주입+동기화) 구현 계획

> **For agentic workers:** index.html 단일파일. 자동화 테스트 없음 → 검증은 preview 콘솔무오류 + 코드리뷰. **세이브(META)/동기화를 건드리므로 최고 주의.** 클로저 스코프라 `META`/`state.metaMods`는 preview_eval로 못 읽음 → 효과 검증은 치트로 장비 부여 후 데미지/골드 변화 or 코드리뷰.

**Goal:** 영구장비 "전술 코어"의 **데이터 모델 + 전투 효과 주입 + 기기간 동기화**를 넣는다. (드랍=2b, UI=2c, 리롤=2d는 후속)

**Architecture:** `META.gear = {equipped, inv, nextId}`. 게임 시작 시 `applyGearEffects(state.metaMods)`가 장착 코어의 라인을 metaMods에 합산(주간모디파이어 apply와 동일 패턴). 옵션은 **빌드타임 metaMods 필드에만** 매핑(패시브 파생 필드는 매프레임 리셋되므로 제외). 동기화는 inv를 id+버전(v)으로 유니온.

## Global Constraints
- 버전: `APP_VERSION`(index) + `sw.js` CACHE 동시 bump. 현재 **v617** → 2a 배포 시 **v618**.
- 그라인드=**하드코어**(드랍낮음·리롤비쌈·꽝많음). 2a엔 수치 영향 적음(드랍/리롤은 2b/2d).
- 클로저 스코프·META 무결성(`saveMeta()` 경유)·git 커밋은 사용자 명시 시만.
- 슬롯 4: `offense/targeting/supply/control`. 등급 MVP 3: `common/rare/epic`. 라인수: common1·rare2·epic2.
- **주입은 빌드타임 필드에만**: dmgBoost(add)·comboPowerBonus(add)·bossDmgMul(mul)·goldMul(mul)·scoreMul(mul)·slowMul(mul)·luckyChanceBonus(add)·roundTimeBonus(add). (executioner/onslaught/press/awaken/vampiric/scholar는 매프레임 리셋 → 제외)

---

### Task 1: 장비 데이터 모델 + 옵션풀 + 생성기

**Files:** Modify `index.html` — ABILITY_DEFS 근처 상단 상수부(예: L6297 위) 또는 META 유틸 근처에 신규 블록.

**Interfaces:**
- Produces: `GEAR_SLOTS`, `GEAR_RARITY`, `GEAR_OPTIONS`, `_ensureGear()`, `createGear(slot, rarity)`, `_gearLineRollTier()`. Task2/3/4가 소비.

- [ ] **Step 1: 상수 + 정규화 + 생성기 작성**

적당한 상수 구역(예: `const ABILITY_DEFS = {` 바로 위 L6297)에 삽입:
```javascript
// ===== 🔩 전술 코어(영구장비) — Phase 2a =====
const GEAR_SLOTS = ['offense','targeting','supply','control'];
const GEAR_SLOT_LABEL = { offense:'화력', targeting:'조준', supply:'보급', control:'제어' };
const GEAR_RARITY = ['common','rare','epic'];              // MVP 3단
const GEAR_RARITY_LABEL = { common:'커먼', rare:'레어', epic:'에픽' };
const GEAR_RARITY_LINES = { common:1, rare:2, epic:2 };    // 등급별 라인 수
// 슬롯별 옵션 풀 — 전부 빌드타임 metaMods 필드에 매핑. op: add|mul. base=티어1 값.
const GEAR_OPTIONS = {
  offense:   [ {key:'dmgBoost',        op:'add', label:'데미지',      base:0.02},
               {key:'comboPowerBonus', op:'add', label:'조합 위력',   base:0.02} ],
  targeting: [ {key:'bossDmgMul',      op:'mul', label:'보스 데미지',  base:0.04},
               {key:'dmgBoost',        op:'add', label:'정밀 데미지',  base:0.02} ],
  supply:    [ {key:'goldMul',         op:'mul', label:'골드 획득',    base:0.03},
               {key:'scoreMul',        op:'mul', label:'점수',        base:0.03} ],
  control:   [ {key:'slowMul',         op:'mul', label:'슬로우',      base:0.03},
               {key:'luckyChanceBonus',op:'add', label:'행운',        base:0.01},
               {key:'roundTimeBonus',  op:'add', label:'라운드 시간',  base:1, flat:true} ],
};
// 라인 티어 롤(하드코어=바닥 두꺼움). tier 배수로 값 스케일.
const GEAR_LINE_TIERS = [
  {tier:1, mult:1,  w:60}, {tier:2, mult:1.8, w:27}, {tier:3, mult:2.8, w:10}, {tier:4, mult:4, w:2.5}, {tier:5, mult:6, w:0.5},
];
function _wpick(arr, wkey) { let t=0; for(const a of arr) t+=a[wkey]; let r=Math.random()*t; for(const a of arr){ r-=a[wkey]; if(r<=0) return a; } return arr[arr.length-1]; }
function _gearRollLine(slot) {
  const pool = GEAR_OPTIONS[slot];
  const opt = pool[Math.floor(Math.random()*pool.length)];
  const t = _wpick(GEAR_LINE_TIERS, 'w');
  const raw = opt.base * t.mult * (0.85 + Math.random()*0.3);   // 값 범위 ±15%
  const val = opt.flat ? Math.round(raw) : Math.round(raw*1000)/1000;
  return { key:opt.key, op:opt.op, label:opt.label, flat:!!opt.flat, tier:t.tier, val };
}
function createGear(slot, rarity) {
  const g = _ensureGear();
  const n = GEAR_RARITY_LINES[rarity] || 1;
  const lines = []; for (let i=0;i<n;i++) lines.push(_gearRollLine(slot));
  const id = g.nextId++;
  return { id, slot, rarity, level:0, lines, v:1 };
}
function _ensureGear() {
  if (!META.gear || typeof META.gear !== 'object') META.gear = { equipped:{}, inv:[], nextId:1 };
  if (!META.gear.equipped) META.gear.equipped = {};
  if (!Array.isArray(META.gear.inv)) META.gear.inv = [];
  if (!META.gear.nextId) META.gear.nextId = 1;
  return META.gear;
}
function _gearById(id) { const g=_ensureGear(); return g.inv.find(x=>x.id===id) || null; }
```

- [ ] **Step 2: 구문 검증** — preview reload → console error 0.

---

### Task 2: 효과 주입 `applyGearEffects`

**Files:** Modify `index.html` — Task1 블록 뒤(또는 metaMods 빌드 근처)에 함수 + L17517(주간모디파이어 apply) 뒤 호출.

**Interfaces:** Consumes `_ensureGear`, `_gearById`, `GEAR_OPTIONS`. Produces `applyGearEffects(mm)`.

- [ ] **Step 1: `applyGearEffects` 작성** (Task1 블록 끝에 이어서)
```javascript
const GEAR_CAP = { dmgBoost:3, comboPowerBonus:3, bossDmgMul:3, goldMul:4, scoreMul:4, slowMul:3, luckyChanceBonus:0.5, roundTimeBonus:20 };
function applyGearEffects(mm) {
  const g = META.gear; if (!g || !g.equipped) return;
  for (const slot of GEAR_SLOTS) {
    const id = g.equipped[slot]; if (id == null) continue;
    const item = g.inv.find(x => x.id === id); if (!item || !item.lines) continue;
    const lvlMul = 1 + (item.level || 0) * 0.1;            // 레벨당 +10% (P3에서 골드로 레벨업)
    for (const ln of item.lines) {
      const v = ln.val * (ln.flat ? 1 : lvlMul);
      if (ln.op === 'add') mm[ln.key] = (mm[ln.key] || 0) + v;
      else mm[ln.key] = (mm[ln.key] || 1) * (1 + v);        // mul
    }
  }
  // 캡 적용 (인플레 방지)
  for (const k in GEAR_CAP) {
    if (mm[k] == null) continue;
    if (k === 'slowMul' || k === 'goldMul' || k === 'scoreMul' || k === 'bossDmgMul') mm[k] = Math.min(mm[k], GEAR_CAP[k]);
    else mm[k] = Math.min(mm[k], GEAR_CAP[k]);
  }
}
```

- [ ] **Step 2: 주입 호출 추가** — L17517 주간모디파이어 apply 라인 바로 뒤:
```javascript
    try { const _wm = getActiveWeeklyModifier(); if (_wm && _wm.apply) _wm.apply(state.metaMods); state.weeklyModifierId = _wm.id; } catch (e) {}
    try { applyGearEffects(state.metaMods); } catch (e) {}   // 🔩 장비 효과 주입
```

- [ ] **Step 3: 검증** — preview reload → console error 0. (효과 자체는 Task4 치트로)

---

### Task 3: 동기화 merge (inv 유니온 + 장착 선호도)

**Files:** Modify `index.html` — 별조각 merge 블록 뒤(L18614 근처).

**Interfaces:** Consumes `merged`, `META`, `server`.

- [ ] **Step 1: gear 병합 추가** — 별조각 블록(`merged.starShards = ...`, L18614) 바로 뒤:
```javascript
      // ━━━ 🔩 장비(gear) — inv는 id+버전(v) 유니온(파밍 append-only), 장착은 최근우선 ━━━
      {
        const lg = (META.gear && Array.isArray(META.gear.inv)) ? META.gear.inv : [];
        const sg = (server.gear && Array.isArray(server.gear.inv)) ? server.gear.inv : [];
        const byId = new Map();
        for (const it of sg) if (it && it.id != null) byId.set(it.id, it);
        for (const it of lg) if (it && it.id != null) {
          const ex = byId.get(it.id);
          if (!ex || (it.v || 1) >= (ex.v || 1)) byId.set(it.id, it);   // 높은 v(리롤) 우선
        }
        const inv = [...byId.values()];
        const localNewer = (META.metaUpdatedAt || 0) >= (server.metaUpdatedAt || 0);
        const equipped = localNewer ? ((META.gear && META.gear.equipped) || {}) : ((server.gear && server.gear.equipped) || {});
        const nextId = Math.max((META.gear && META.gear.nextId) || 1, (server.gear && server.gear.nextId) || 1, inv.reduce((m,x)=>Math.max(m,(x.id||0)+1),1));
        merged.gear = { equipped, inv, nextId };
      }
```

- [ ] **Step 2: 검증** — preview reload → console error 0. 로그인/동기화 경로가 깨지지 않는지(로그인 안 해도 게임 로드 정상).

---

### Task 4: 테스트 치트 (장비 부여) + 효과 확인

**Files:** Modify `index.html` — `executeCheat` 함수.

- [ ] **Step 1: `gear` 치트 추가** — executeCheat의 명령 분기에:
```javascript
    // 🔩 gear <slot> <rarity> — 테스트용 코어 부여+장착 (예: gear offense epic)
    if (cmd === 'gear') {
      const slot = args[0] && GEAR_SLOTS.includes(args[0]) ? args[0] : 'offense';
      const rarity = args[1] && GEAR_RARITY.includes(args[1]) ? args[1] : 'epic';
      const item = createGear(slot, rarity);
      const g = _ensureGear(); g.inv.push(item); g.equipped[slot] = item.id;
      saveMeta();
      toast(`🔩 ${GEAR_RARITY_LABEL[rarity]} ${GEAR_SLOT_LABEL[slot]} 코어 장착: ` + item.lines.map(l=>`${l.label}+${l.flat?l.val:Math.round(l.val*100)+'%'}`).join(', '));
      return true;
    }
```
(정확한 삽입 위치·반환형은 executeCheat의 기존 분기 패턴에 맞춤 — 구현 시 grep `function executeCheat` 로 확인.)

- [ ] **Step 2: 검증** — preview에서 게임 진입 → 치트 `gear offense epic` → 토스트에 라인 표시 확인. 새 게임 시작 시 console error 0(주입 정상). 재시작/동기화 후 장비 유지.

---

### Task 5: 버전 bump + 통합 검증

- [ ] **Step 1:** `APP_VERSION` 617→618, `sw.js` CACHE v618.
- [ ] **Step 2:** preview reload → console error 0. 로그인 안 한 신규 상태에서도 게임 정상(gear undefined 방어 확인). 치트로 장비 부여 후 새 게임 진입 무오류.

## Self-Review
- 스펙 §3.1(데이터모델)✅T1 / §3.2(옵션풀·metaMods매핑)✅T1·T2 / §3.6(주입)✅T2 / §3.7(동기화 inv유니온+v+장착최근)✅T3 / §3.8(캡)✅T2 GEAR_CAP. 드랍(§3.3)·리롤(§3.4)·UI(§3.6 화면)·승급(§3.5)은 2b/2c/2d로 명시 분리.
- Placeholder: T4 삽입위치는 "executeCheat 패턴 확인"으로 명시된 조사 스텝. 나머지 실코드 완비.
- 타입 일관: `_ensureGear/createGear/_gearById/applyGearEffects/GEAR_SLOTS/GEAR_OPTIONS/GEAR_RARITY_LINES` 태스크 간 일치. gear 항목 `{id,slot,rarity,level,lines:[{key,op,label,flat,tier,val}],v}` 일관.
