# Dot Defense 신규 3캐릭 구현 계획

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 페리아(SSR 자력) · 트리나(SR 환영타워) · 아이리스(SR 사진) 3인을 가챠·진화트리·유물·업적까지 전 계통에 배선한다.

**Architecture:** 단일 파일 `index.html`(~35,000줄)의 기존 레지스트리에 항목을 **추가만** 한다. 진화 트리 기존 항목은 수정하지 않는다. 유일한 신규 인프라는 `damageEnemy`의 환영 피해 게이트 1곳이다.

**Tech Stack:** 바닐라 JS IIFE, Canvas 2D, 서비스워커 PWA. **빌드 없음. 테스트 프레임워크 없음.**

**설계 스펙:** `docs/superpowers/specs/2026-07-20-dot-defense-3chars-design.md`

---

## Global Constraints

- **버전 규율:** 변경 시 `index.html`의 `APP_VERSION`과 `sw.js`의 `CACHE='dot-defense-vNNN'`를 **둘 다** 올린다. 현재 v672 → 이 계획 완료 시 v673.
- **테스트 프레임워크가 없다.** 검증은 (a) 브라우저 로드 후 콘솔 에러 0, (b) `grep`으로 배선 확인, (c) 치트 `unlock all` 후 캐릭터 수. 자동 테스트를 새로 만들지 않는다.
- **로컬 서버:** `.claude/launch.json`에 `python -m http.server 8777` 설정이 있다. 검증은 `http://localhost:8777`로 한다.
- **밸런스 상한은 협상 대상이 아니다.** 환영 40/28/18% · 합산 +90% 하드캡 · T4 25% · 극성 최대 20체 · 충돌 개체당 20프레임 쿨 · 쇳가루 상한 40. 구현 중 임의 완화 금지.
- **환영 피해는 판정을 굴리지 않는다.** 즉사(`executeBelow`) · 계보 각인 · 별보너스 · 영구강화 전부 skip.
- **desc에 캡과 판정 미발동을 명시한다.** 이 게임에는 부동 데미지 숫자가 없어 `desc`가 유일한 문자 채널이다.
- **id 충돌 주의:** `railgun`은 기존 콤보 재료다. 페리아 t3는 반드시 `magRail`.
- **`ABILITY_TAGS`는 건드리지 않는다.** 최신 6캐릭 전원이 미등록 상태이고 조회가 null-safe다. 신규 3인도 동일하게 생략한다(선례 일치).
- **신규 SR은 별해금을 받지 않는다.** 에이미·클로에·라라·갈라테아 선례를 따른다. `CHAR_STAR_UNLOCKS`에는 페리아만 추가.

### 신규 id 전체 목록

| 캐릭터 | 등급 | 능력 id (시그→t2→t3→t4) | 별해금 | 유물 |
|---|---|---|---|---|
| `feria` | SSR | `polarField` `reversePolarity` `magRail` `magnetStorm` | `ferroShard`(4★) `monopole`(8★) | `ferroCore` |
| `trina` | SR | `phantomStage` `chromaticSplit` `encore` `standingOvation` | — | — |
| `iris` | SR | `longExposure` `overexposed` `contactSheet` `developingTray` | — | — |

---

## File Structure

| 파일 | 책임 | 변경 |
|---|---|---|
| `index.html` | 게임 전체 | 수정 (전 태스크) |
| `sw.js` | SW 캐시 | 수정 (Task 8) |
| `icons/illust/{feria,trina,iris}.png` | 일러 | **배치 완료** |
| `icons/characters/{feria,trina,iris}.png` | 치비 | **배치 완료** |
| `icons/abilities/*.png` | 능력 아이콘 14종 | **미제작 — 없어도 색상박스+첫글자 폴백으로 동작** |
| `icons/gacha-ferroPole.*` | 4번째 배너 | **미제작 — Task 8에서 폴백 처리** |

---

## Task 1: `damageEnemy` 환영 피해 게이트

트리나의 모든 능력이 이것에 의존한다. 반드시 먼저 만든다.

**Files:**
- Modify: `index.html` — `damageEnemy` 함수 (선언 23423 부근)

**Interfaces:**
- Produces: 모듈 스코프 `let _phantomDmg` (boolean), `let _phantomScale` (number). 트리나 능력이 환영 발사 직전 `_phantomDmg = true; _phantomScale = <비율>` 로 켜고 `finally`로 되돌린다.

- [ ] **Step 1: 게이트 변수 선언**

`damageEnemy` 함수 선언 바로 앞에 추가한다. 현재 그 자리는 이렇게 생겼다:

```js
  function damageEnemy(e, dmg) {
    if (e.hp <= 0) return;
```

앞에 다음을 삽입:

```js
  // 👻 v673 — 환영(트리나) 피해 게이트.
  //   환영은 "피해만 주고 판정은 하지 않는다": 즉사·계보각인·별보너스·영구강화를 전부 건너뛴다.
  //   damageEnemy 는 곱연산 사슬이 매우 길어서, 게이트 없이 환영을 태우면
  //   "피해 2배"가 아니라 "즉사 판정 4배"가 되어 밸런스가 붕괴한다.
  //   트리나 능력이 발사 직전에 켜고 finally 로 반드시 되돌린다.
  let _phantomDmg = false;
  let _phantomScale = 1;
```

- [ ] **Step 2: 피해 배율 적용 + 최상단 진입**

`damageEnemy` 본문 최상단의 무적/보호막 분기 **뒤**, `if (state.metaMods) {` **앞**에 삽입한다. 현재:

```js
    if (e.shieldPhaseUntil && e.shieldPhaseUntil > state.t) dmg *= 0.18;
    // 모든 데미지 멀티 (캐릭터 + 모든 패시브 + 메타 효과)
    if (state.metaMods) {
```

→ 사이에 삽입:

```js
    if (e.shieldPhaseUntil && e.shieldPhaseUntil > state.t) dmg *= 0.18;
    // 👻 환영 피해 — 배율만 먹고 판정류는 아래에서 전부 skip
    if (_phantomDmg) dmg *= _phantomScale;
    // 모든 데미지 멀티 (캐릭터 + 모든 패시브 + 메타 효과)
    if (state.metaMods) {
```

- [ ] **Step 3: 별보너스 / 영구강화 skip**

현재 (23441–23446 부근):

```js
      // ⭐ 캐릭터 별 보너스 — 가챠 캐릭터 고유 능력에만 적용 (해당 캐릭터 별 수만큼 데미지 ↑)
      const starBonus = getCharStarBonusForAbility(state.currentAbilityId);
      if (starBonus > 0) mul *= (1 + starBonus);
      // 🌟 능력별 영구 강화 (스타더스트 강화) — 모든 능력
      const permaBonus = getAbilityPermaBonus(state.currentAbilityId);
      if (permaBonus > 0) mul *= (1 + permaBonus);
```

→ 교체:

```js
      // ⭐ 캐릭터 별 보너스 — 가챠 캐릭터 고유 능력에만 적용 (해당 캐릭터 별 수만큼 데미지 ↑)
      //    👻 환영은 제외 — 실체가 이미 받은 보너스를 환영이 또 받으면 이중 적용
      const starBonus = _phantomDmg ? 0 : getCharStarBonusForAbility(state.currentAbilityId);
      if (starBonus > 0) mul *= (1 + starBonus);
      // 🌟 능력별 영구 강화 (스타더스트 강화) — 모든 능력
      const permaBonus = _phantomDmg ? 0 : getAbilityPermaBonus(state.currentAbilityId);
      if (permaBonus > 0) mul *= (1 + permaBonus);
```

- [ ] **Step 4: 유물 즉사 skip — 가장 중요한 한 줄**

현재 (23475–23479 부근):

```js
      // 💎 유물 처형 (즉사) — 저체력 비-보스 적
      const exBelow = (state.relicEffects && state.relicEffects.executeBelow) || 0;
      if (!e.isBoss && exBelow > 0 && e.maxHp > 0 && e.hp / e.maxHp <= exBelow) {
        dmg = e.hp + 1; // 즉사
      }
```

→ 교체:

```js
      // 💎 유물 처형 (즉사) — 저체력 비-보스 적
      //    👻 환영은 즉사를 굴리지 않는다. 환영 3기 = 즉사 판정 4배가 되는 것을 막는다.
      const exBelow = (state.relicEffects && state.relicEffects.executeBelow) || 0;
      if (!_phantomDmg && !e.isBoss && exBelow > 0 && e.maxHp > 0 && e.hp / e.maxHp <= exBelow) {
        dmg = e.hp + 1; // 즉사
      }
```

- [ ] **Step 5: 계보 각인 skip**

현재 (23501–23505):

```js
    e.hp -= dmg;
    // 🧬 ② 계보 자동 각인 — 현재 능력이 내 계보 SSR 시그면 축 효과 부착 (재귀 가드)
    if (!state._inLineageHit && state._lineageAxis && state._lineageSigSet && state._lineageSigSet.has(state.currentAbilityId)) {
      state._inLineageHit = true; try { _lineageOnHit(e); } catch (err) {} state._inLineageHit = false;
    }
```

→ 교체 (조건에 `!_phantomDmg` 추가):

```js
    e.hp -= dmg;
    // 🧬 ② 계보 자동 각인 — 현재 능력이 내 계보 SSR 시그면 축 효과 부착 (재귀 가드)
    //    👻 환영 제외 — 각인은 실체 타격에만 붙는다
    if (!_phantomDmg && !state._inLineageHit && state._lineageAxis && state._lineageSigSet && state._lineageSigSet.has(state.currentAbilityId)) {
      state._inLineageHit = true; try { _lineageOnHit(e); } catch (err) {} state._inLineageHit = false;
    }
```

- [ ] **Step 6: 배선 확인**

Run:
```bash
grep -n "_phantomDmg" index.html
```
Expected: **6줄** — 선언 1 + 배율 1 + 별보너스 1 + 영구강화 1 + 즉사 1 + 계보 1.

- [ ] **Step 7: 파싱 검증**

`python -m http.server 8777` 를 띄우고 `http://localhost:8777` 접속. 브라우저 콘솔에 에러가 0건이어야 하고 메뉴 화면이 떠야 한다.
Expected: 콘솔 에러 없음. 에러가 있으면 문법 오류이므로 다음 태스크로 넘어가지 않는다.

- [ ] **Step 8: 커밋**

```bash
git add index.html
git commit -m "feat: damageEnemy 환영 피해 게이트 추가

환영(트리나)은 피해만 주고 판정은 굴리지 않는다.
즉사/계보각인/별보너스/영구강화 4곳을 _phantomDmg 로 차단.

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 2: 페리아 능력 6종 (`ABILITY_DEFS`)

**Files:**
- Modify: `index.html` — `ABILITY_DEFS` 끝부분. 현재 마지막 항목은 카이라의 `apexPredator`(~17206)이고 객체는 **17479의 `  };`** 로 닫힌다. 그 닫는 줄 **바로 앞**에 삽입한다.

**Interfaces:**
- Consumes: `permaCount(id)`, `damageEnemy(e,dmg)`, `enemyXY(e)`, `spawnParticles(x,y,color,n)`, `compactInPlace(arr,pred)`, `CX/CY`, `state.t`, `state.enemies`, `ARENA_R`, `ctx`
- Produces: 능력 id 6종 — `polarField` `reversePolarity` `magRail` `magnetStorm` `ferroShard` `monopole`
- Produces: 적 객체에 붙는 필드 `e._pol`(+1/-1 극성), `e._polUntil`(만료 프레임), `e._magHitUntil`(충돌 피해 쿨), `state._ferroShards`(쇳가루 배열)

- [ ] **Step 1: 6종 삽입**

`ABILITY_DEFS` 닫는 `  };` 앞에 다음을 통째로 삽입한다.

```js
    // 🧲 페리아(SSR) — 자력 킷 (쌍극자장 · 곡선 역선 · 견인/반발) + 별해금 2종
    //   밸런스: 극성 부여를 최대 20체로 캡 → 쌍 충돌 스캔이 20×20/2=200회로 상한이 걸린다.
    //   개체당 20프레임 충돌 쿨로 N² 데미지를 N 으로 내린다.
    polarField: {
      name: '극성장', baseCost: 65, color: '#3b7fe0', isGachaUnique: true,
      desc: lv => `적 ${Math.min(20, 4 + lv * 2)}체에 N/S 극성 부여 · 역선 견인 · 같은 극 충돌 파편 DMG ${8 + lv * 4}(개체당 0.33s 쿨)`,
      init(ab) { ab.cooldown = 0; ab.rot = 0; ab.nx = CX; ab.ny = CY; ab.sx = CX; ab.sy = CY; },
      tick(ab) {
        ab.rot += 0.012;
        const pd = 44 + ab.level * 2;
        ab.nx = CX + Math.cos(ab.rot) * pd; ab.ny = CY + Math.sin(ab.rot) * pd;
        ab.sx = CX - Math.cos(ab.rot) * pd; ab.sy = CY - Math.sin(ab.rot) * pd;
        // 극성 부여 (상한 20체)
        if (--ab.cooldown <= 0) {
          const cap = Math.min(20, 4 + ab.level * 2 + permaCount('polarField'));
          let n = 0;
          for (const e of state.enemies) {
            if (e.hp <= 0) continue;
            if (e._pol && e._polUntil > state.t) { n++; continue; }
            if (n >= cap) break;
            e._pol = (n % 2 === 0) ? 1 : -1; e._polUntil = state.t + 300; n++;
          }
          ab.cooldown = 34;
        }
        // 견인 — 극성별로 반경을 밀거나 당긴다
        const charged = [];
        for (const e of state.enemies) {
          if (e.hp <= 0 || !e._pol) continue;
          if (e._polUntil <= state.t) { e._pol = 0; continue; }
          e.radius = Math.max(34, e.radius + (e._pol > 0 ? 0.55 : -0.35));
          if (e.targetRadius !== undefined) e.targetRadius = e.radius;
          e._xyT = -1;
          charged.push(e);
        }
        // 같은 극 충돌 — charged 가 20체 이하라 스캔 상한이 잡혀 있다
        const dmg = 8 + ab.level * 4;
        let events = 0;
        for (let i = 0; i < charged.length && events < 12; i++) {
          const a = charged[i]; const [ax, ay] = enemyXY(a);
          for (let j = i + 1; j < charged.length && events < 12; j++) {
            const b = charged[j];
            if (a._pol !== b._pol) continue;
            const [bx, by] = enemyXY(b);
            const dx = ax - bx, dy = ay - by;
            if (dx * dx + dy * dy > 26 * 26) continue;
            for (const t of [a, b]) {
              if (t._magHitUntil && t._magHitUntil > state.t) continue;
              t._magHitUntil = state.t + 20;
              damageEnemy(t, dmg);
            }
            spawnParticles((ax + bx) / 2, (ay + by) / 2, '#b8c0cc', 4);
            events++;
          }
        }
      },
      draw(ab) {
        ctx.save(); ctx.globalCompositeOperation = 'lighter';
        // 쌍극자 역선 — 두 극을 잇는 대칭 베지어 16가닥
        for (let i = 0; i < 16; i++) {
          const t = (i / 15) - 0.5, bow = t * 150;
          const mx = (ab.nx + ab.sx) / 2 - Math.sin(ab.rot) * bow;
          const my = (ab.ny + ab.sy) / 2 + Math.cos(ab.rot) * bow;
          const g = ctx.createLinearGradient(ab.nx, ab.ny, ab.sx, ab.sy);
          g.addColorStop(0, '#3b7fe0'); g.addColorStop(1, '#e04b4b');
          ctx.strokeStyle = g; ctx.globalAlpha = 0.30 - Math.abs(t) * 0.28; ctx.lineWidth = 1.4;
          ctx.beginPath(); ctx.moveTo(ab.nx, ab.ny); ctx.quadraticCurveTo(mx, my, ab.sx, ab.sy); ctx.stroke();
        }
        // 극
        ctx.globalAlpha = 0.9;
        for (const [px, py, c] of [[ab.nx, ab.ny, '#3b7fe0'], [ab.sx, ab.sy, '#e04b4b']]) {
          ctx.fillStyle = c; ctx.beginPath(); ctx.arc(px, py, 5, 0, Math.PI * 2); ctx.fill();
        }
        // 극성 표시 — 충돌 쿨 중이면 회색으로 죽여서 왜 지금 안 아픈지 보이게 한다
        ctx.lineWidth = 1.6;
        for (const e of state.enemies) {
          if (e.hp <= 0 || !e._pol) continue;
          const [ex, ey] = enemyXY(e);
          const cooling = e._magHitUntil && e._magHitUntil > state.t;
          ctx.globalAlpha = cooling ? 0.25 : 0.85;
          ctx.strokeStyle = cooling ? '#8a8f98' : (e._pol > 0 ? '#3b7fe0' : '#e04b4b');
          ctx.beginPath(); ctx.arc(ex, ey, 11, 0, Math.PI * 2); ctx.stroke();
        }
        ctx.restore(); ctx.globalAlpha = 1;
      },
    },
    // 🧲 기본조합 (극성장+frost) — 역극전환
    reversePolarity: {
      name: '역극전환', baseCost: 150, color: '#5a6fd0', isCombo: true,
      desc: lv => `2s마다 양극 반전 · 역선 위 적 급가속 충돌 · 광역 DMG ${16 + lv * 7} · 반전 시 둔화`,
      init(ab) { ab.cooldown = 90; ab.flash = 0; },
      tick(ab) {
        if (ab.flash > 0) ab.flash--;
        if (--ab.cooldown > 0) return;
        ab.cooldown = Math.max(60, 120 - ab.level * 3);
        ab.flash = 18;
        const dmg = 16 + ab.level * 7;
        for (const e of state.enemies) {
          if (e.hp <= 0 || !e._pol) continue;
          e._pol = -e._pol;
          e.slowFrames = Math.max(e.slowFrames || 0, 70);
          if (e._magHitUntil && e._magHitUntil > state.t) continue;
          e._magHitUntil = state.t + 20;
          damageEnemy(e, dmg);
          const [ex, ey] = enemyXY(e);
          spawnParticles(ex, ey, e._pol > 0 ? '#3b7fe0' : '#e04b4b', 6);
        }
      },
      draw(ab) {
        if (ab.flash <= 0) return;
        const a = ab.flash / 18;
        ctx.save(); ctx.globalCompositeOperation = 'lighter'; ctx.globalAlpha = a * 0.5;
        ctx.strokeStyle = '#8aa0ff'; ctx.lineWidth = 3;
        ctx.beginPath(); ctx.arc(CX, CY, (1 - a) * 220, 0, Math.PI * 2); ctx.stroke();
        ctx.restore(); ctx.globalAlpha = 1;
      },
    },
    // 🧲 4돌파 (역극전환+railgun) — 자기 레일건  ※ id 는 magRail (railgun 은 기존 재료라 충돌)
    magRail: {
      name: '자기 레일건', baseCost: 240, color: '#6d8bf0', isCombo: true, isTriple: true,
      desc: lv => `1.6s마다 양극 정렬 관통 사격 · DMG ${30 + lv * 14} · 쇳가루 40개까지 위력 누적(개당 +3%)`,
      init(ab) { ab.cooldown = 60; ab.shots = []; },
      tick(ab) {
        for (const s of ab.shots) s.life--;
        compactInPlace(ab.shots, s => s.life > 0);
        if (--ab.cooldown > 0) return;
        ab.cooldown = Math.max(50, 96 - ab.level * 3);
        const pool = state.enemies.filter(e => e.hp > 0);
        if (!pool.length) { ab.cooldown = 20; return; }
        const tgt = pool[Math.floor(Math.random() * pool.length)];
        const [tx, ty] = enemyXY(tgt);
        const ang = Math.atan2(ty - CY, tx - CX);
        // 쇳가루 누적 — 상한 40 (후반 웨이브 폭주 차단)
        const filings = Math.min(40, (state._ferroShards || []).length);
        const dmg = (30 + ab.level * 14) * (1 + filings * 0.03);
        const ex2 = CX + Math.cos(ang) * (ARENA_R + 80), ey2 = CY + Math.sin(ang) * (ARENA_R + 80);
        for (const e of state.enemies) {
          if (e.hp <= 0) continue;
          const [px, py] = enemyXY(e);
          const t = ((px - CX) * Math.cos(ang) + (py - CY) * Math.sin(ang));
          if (t < 0) continue;
          const dx = px - (CX + Math.cos(ang) * t), dy = py - (CY + Math.sin(ang) * t);
          if (dx * dx + dy * dy < 20 * 20) damageEnemy(e, dmg);
        }
        ab.shots.push({ x2: ex2, y2: ey2, life: 14 });
      },
      draw(ab) {
        ctx.save(); ctx.globalCompositeOperation = 'lighter'; ctx.lineCap = 'round';
        for (const s of ab.shots) {
          const a = s.life / 14;
          const g = ctx.createLinearGradient(CX, CY, s.x2, s.y2);
          g.addColorStop(0, '#e04b4b'); g.addColorStop(0.5, '#ffffff'); g.addColorStop(1, '#3b7fe0');
          ctx.strokeStyle = g; ctx.globalAlpha = a; ctx.lineWidth = 2 + a * 7;
          ctx.beginPath(); ctx.moveTo(CX, CY); ctx.lineTo(s.x2, s.y2); ctx.stroke();
        }
        ctx.restore(); ctx.globalAlpha = 1;
      },
    },
    // 🧲 8돌파 (레일건+blackhole) — 자기폭풍 (단극 붕괴)
    magnetStorm: {
      name: '자기폭풍', baseCost: 350, color: '#4060e0', isCombo: true, isTriple: true, isEighth: true,
      desc: lv => `[8돌파] 4s마다 단극 붕괴 · 전체 나선 견인 후 전방위 파편 폭발 DMG ${44 + lv * 20}`,
      init(ab) { ab.cooldown = 140; ab.phase = 0; ab.t = 0; },
      tick(ab) {
        if (ab.phase === 1) {
          ab.t++;
          for (const e of state.enemies) {
            if (e.hp <= 0) continue;
            e.radius = Math.max(28, e.radius - 2.4);
            if (e.targetRadius !== undefined) e.targetRadius = e.radius;
            e.angle = (e.angle || 0) + 0.05;
            e._xyT = -1;
            e.slowFrames = Math.max(e.slowFrames || 0, 30);
          }
          if (ab.t >= 45) {
            ab.phase = 2; ab.t = 0;
            const dmg = 44 + ab.level * 20;
            for (const e of state.enemies) { if (e.hp > 0) damageEnemy(e, dmg); }
            for (let i = 0; i < 30; i++) {
              const a = (Math.PI * 2 / 30) * i;
              spawnParticles(CX + Math.cos(a) * 40, CY + Math.sin(a) * 40, i % 2 ? '#3b7fe0' : '#e04b4b', 3);
            }
            if (typeof shake === 'function') shake(16, 22);
          }
          return;
        }
        if (ab.phase === 2) { if (++ab.t > 20) { ab.phase = 0; ab.t = 0; } return; }
        if (--ab.cooldown > 0) return;
        ab.cooldown = Math.max(150, 260 - ab.level * 5);
        ab.phase = 1; ab.t = 0;
      },
      draw(ab) {
        if (ab.phase === 0) return;
        ctx.save(); ctx.globalCompositeOperation = 'lighter';
        if (ab.phase === 1) {
          const p = ab.t / 45;
          for (let i = 0; i < 10; i++) {
            const a0 = (Math.PI * 2 / 10) * i + p * 5;
            ctx.strokeStyle = i % 2 ? '#3b7fe0' : '#e04b4b';
            ctx.globalAlpha = 0.5; ctx.lineWidth = 2;
            ctx.beginPath();
            for (let k = 0; k <= 20; k++) {
              const r = (1 - p) * 210 * (1 - k / 26), a = a0 + k * 0.22;
              const px = CX + Math.cos(a) * r, py = CY + Math.sin(a) * r;
              if (k === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
            }
            ctx.stroke();
          }
        } else {
          const p = ab.t / 20;
          ctx.globalAlpha = (1 - p) * 0.8; ctx.lineWidth = 6 * (1 - p) + 1;
          ctx.strokeStyle = '#ffffff';
          ctx.beginPath(); ctx.arc(CX, CY, p * 260, 0, Math.PI * 2); ctx.stroke();
        }
        ctx.restore(); ctx.globalAlpha = 1;
      },
    },
    // 🧲 페리아 4★ 별해금 — 강자성 파편 (처치 시 쇳가루 잔류 → magRail 누적과 시너지)
    ferroShard: {
      name: '강자성 파편', isGachaUnique: true, isStarUnlock: true, baseCost: 280, color: '#8fa3c8',
      desc: lv => `[4★히든] 적 처치 시 쇳가루 잔류(최대 ${Math.min(40, 12 + lv * 3)}개) · 접촉 DMG ${5 + lv * 3} · 레일건 위력에 누적`,
      init(ab) { state._ferroShards = []; ab.tick0 = 0; },
      tick(ab) {
        const arr = state._ferroShards || (state._ferroShards = []);
        const cap = Math.min(40, 12 + ab.level * 3);
        // 쇳가루 생성 — "죽은 적 감지"가 아니라 "자기 충돌을 맞은 적"에서 떨어져 나온다.
        //   죽은 적은 배열에서 곧바로 제거될 수 있어 다음 tick 에서 관측이 보장되지 않는다.
        //   e._magHitUntil 은 polarField/monopole 이 충돌 순간에 세우므로 같은 프레임에 확실히 잡힌다.
        for (const e of state.enemies) {
          if (e.hp <= 0 || !e._magHitUntil) continue;
          if (e._magHitUntil !== state.t + 20) continue;   // 방금 세워진 것만 (중복 방지)
          if (arr.length >= cap) break;
          const [ex, ey] = enemyXY(e);
          arr.push({ x: ex, y: ey, a: Math.random() * Math.PI * 2, life: 420 });
        }
        const dmg = 5 + ab.level * 3;
        for (const s of arr) {
          s.life--; s.a += 0.04;
          const ang = Math.atan2(CY - s.y, CX - s.x);
          s.x += Math.cos(ang) * 0.25; s.y += Math.sin(ang) * 0.25;
          for (const e of state.enemies) {
            if (e.hp <= 0) continue;
            if (e._magHitUntil && e._magHitUntil > state.t) continue;
            const [ex, ey] = enemyXY(e);
            const dx = ex - s.x, dy = ey - s.y;
            if (dx * dx + dy * dy < 16 * 16) { e._magHitUntil = state.t + 20; damageEnemy(e, dmg); }
          }
        }
        compactInPlace(arr, s => s.life > 0);
      },
      draw(ab) {
        const arr = state._ferroShards || [];
        ctx.save(); ctx.globalCompositeOperation = 'lighter'; ctx.fillStyle = '#b8c0cc';
        for (const s of arr) {
          ctx.globalAlpha = Math.min(1, s.life / 60) * 0.85;
          ctx.save(); ctx.translate(s.x, s.y); ctx.rotate(s.a);
          ctx.fillRect(-3, -1, 6, 2);
          ctx.restore();
        }
        ctx.restore(); ctx.globalAlpha = 1;
      },
    },
    // 🧲 페리아 8★ 별해금 — 단극자 (상시 흡입 + 극성 적 처형)
    monopole: {
      name: '단극자', isGachaUnique: true, isStarUnlock: true, baseCost: 480, color: '#2f57d8',
      desc: lv => `[8★히든] 상시 흡입장 · 극성 적 지속 DMG ${10 + lv * 6} · 극성 적 HP ${8 + lv}% 이하 처형`,
      init(ab) { ab.pulse = 0; },
      tick(ab) {
        ab.pulse += 0.05;
        const dmg = 10 + ab.level * 6, thr = (8 + ab.level) / 100;
        for (const e of state.enemies) {
          if (e.hp <= 0) continue;
          e.radius = Math.max(30, e.radius - 0.5);
          if (e.targetRadius !== undefined) e.targetRadius = e.radius;
          e._xyT = -1;
          if (!e._pol) continue;
          if (e._magHitUntil && e._magHitUntil > state.t) continue;
          e._magHitUntil = state.t + 20;
          if (!e.isBoss && e.maxHp > 0 && e.hp / e.maxHp <= thr) { damageEnemy(e, e.hp + 1); continue; }
          damageEnemy(e, dmg);
        }
      },
      draw(ab) {
        ctx.save(); ctx.globalCompositeOperation = 'lighter';
        for (let i = 0; i < 3; i++) {
          const r = 60 + i * 55 + Math.sin(ab.pulse + i) * 8;
          ctx.globalAlpha = 0.22 - i * 0.05; ctx.lineWidth = 2;
          ctx.strokeStyle = i % 2 ? '#3b7fe0' : '#e04b4b';
          ctx.beginPath(); ctx.arc(CX, CY, r, 0, Math.PI * 2); ctx.stroke();
        }
        ctx.restore(); ctx.globalAlpha = 1;
      },
    },
```

- [ ] **Step 2: 파싱 검증**

브라우저 새로고침. 콘솔 에러 0건.
Expected: 에러 없음. `Unexpected token` 이 나오면 삽입 위치가 `ABILITY_DEFS` 밖이다.

- [ ] **Step 3: id 충돌 재확인**

Run:
```bash
grep -c "^\s*railgun:" index.html
grep -c "^\s*magRail:" index.html
```
Expected: `railgun:` 1 (기존 유지), `magRail:` 1 (신규).

- [ ] **Step 4: 커밋**

```bash
git add index.html
git commit -m "feat: 페리아(SSR) 자력 능력 6종 추가

polarField/reversePolarity/magRail/magnetStorm + 별해금 ferroShard/monopole.
극성 20체 캡으로 충돌 스캔 상한, 개체당 20프레임 쿨로 N²→N, 쇳가루 40 상한.

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 3: 페리아 레지스트리 배선 (SSR 전체 계통)

**Files:** `index.html` 다수 지점

**Interfaces:**
- Consumes: Task 2의 능력 id 6종
- Produces: 캐릭터 id `feria`, 유물 id `ferroCore`, 칭호 id `feriaMaster`, 업적 id `char8_feria`

- [ ] **Step 1: `CHARACTERS`에 항목 추가**

`kaira:` 항목(22247)이 끝나는 `    },` 뒤, `blanche:` 앞에 삽입:

```js
    feria: {
      name: '🧲 페리아', color: '#3b7fe0',
      desc: '[SSR] 극성장으로 시작. 데미지 +53% / 보스 +50% / 레벨업 -21% / 슬롯 +1 / 둔화 +20%. 극성장 + 서리 = 역극전환. ★4 강자성 파편 · ★8 단극자.',
      startAbilities: ['polarField'],
      passive: { dmgMul: 1.53, bossDmgMul: 1.50, slotMod: 1, levelUpMul: 0.79, slowMul: 1.20 },
      unlockBy: 'gacha:feria',
      isGacha: true, rarity: 'SSR',
      story: [
        { star: 0, title: '입지 않는 갑옷', text: `페리아는 갑옷을 몸에 걸치지 않는다. 강철 조각들은 언제나 그녀 주위를 맴돌 뿐이다.

"무겁잖아. …그리고, 붙여두면 쓸 수가 없어."

손끝을 까딱이자 파편들이 일제히 방향을 틀었다. 보이지 않는 선을 따라, 하나도 어긋나지 않고.` },
        { star: 4, title: '두 개의 극', text: `"당기는 것만 할 줄 아는 줄 알았는데."

포위망 한가운데서 페리아가 손바닥을 뒤집었다. 끌려오던 것들이 순식간에 튕겨 나갔다.

"밀어내는 것도 힘이야. 사람들은 자꾸 그걸 잊더라."` },
        { star: 8, title: '하나로 수렴', text: `그녀가 두 손을 모으자, 흩어져 있던 극이 한 점으로 합쳐졌다.

"…쌍극이 아니라 단극. 원래는 존재할 수 없는 거야."

전장의 모든 쇳조각이 비명을 지르며 그 한 점으로 빨려 들어갔다. 그리고, 터졌다.` },
      ],
    },
```

- [ ] **Step 2: `COMBO_RECIPES` 3줄 추가**

kaira 블록(18566–18569) 뒤에 삽입:

```js
    // 🧲 페리아(자력) 조합 체인
    { parts: ['polarField', 'frost'],          combo: 'reversePolarity' },
    { parts: ['reversePolarity', 'railgun'],   combo: 'magRail', tier: 3 },
    { parts: ['magRail', 'blackhole'],         combo: 'magnetStorm', tier: 4 },
```

- [ ] **Step 3: `CHAR_SIG_ABILITIES` 1줄**

`kaira:` 줄(31004) 뒤:

```js
    feria:    ['polarField', 'reversePolarity', 'magRail', 'magnetStorm'],
```

- [ ] **Step 4: `CHAR_STAR_UNLOCKS` 1줄**

`kaira:` 줄(17486) 뒤:

```js
    feria:  { 4: ['ferroShard'],      8: ['monopole'] },
```

- [ ] **Step 5: `GACHA_POOL.SSR` 에 추가**

```js
    SSR: ['aria', 'misaki', 'elementia', 'sumika', 'blanche', 'kaira', 'feria'],
```

- [ ] **Step 6: `ABILITY_ICON_ORDER` 1줄**

kaira 줄(18356) 뒤, 배열 닫는 `  ];` 앞:

```js
    // 🆕 페리아(SSR) 자력 킷 + 별해금 2종
    'polarField', 'reversePolarity', 'magRail', 'magnetStorm', 'ferroShard', 'monopole',
```

- [ ] **Step 7: `RELICS` 에 `ferroCore` 추가**

`kairaFang` 항목이 끝나는 `    },` 뒤, `RELICS` 닫는 `  };`(17756) 앞:

```js
    // 🧲 Feria 전용 — 자력·견인·관통 능력 각성
    ferroCore: {
      name: '자기 코어', icon: '🧲', rarity: 'ancient',
      isAncient: true, characterId: 'feria',
      triggerAbilities: ['polarField', 'reversePolarity', 'magRail', 'magnetStorm'],
      desc: '🧲 Feria 전용 · ★별마다 강해짐.\n[기본] 데미지 +16%·둔화 +10% (Feria 시너지 +36%·+20%)\n[★4 각성 1] 자력 능력 max 도달 시 — 데미지 +50%·저체력 처형\n[★8 각성 2] 자력 능력 2개 이상 max — 연쇄 방전 + 데미지 +20%',
      apply: (st) => { applyAncientRelic(st, 'ferroCore'); },
      unlockBy: 'ancient:ferroCore',
    },
```

- [ ] **Step 8: `ANCIENT_RELIC_IDS` / `ANCIENT_RELIC_BY_CHAR`**

```js
  const ANCIENT_RELIC_IDS = ['ariaHarp', 'misakiHourglass', 'elementiaSeal', 'sumikaBrush', 'blanchePrism', 'kairaFang', 'ferroCore'];
  const ANCIENT_RELIC_BY_CHAR = { aria: 'ariaHarp', misaki: 'misakiHourglass', elementia: 'elementiaSeal', sumika: 'sumikaBrush', blanche: 'blanchePrism', kaira: 'kairaFang', feria: 'ferroCore' };
```

- [ ] **Step 9: `applyAncientRelic` 분기**

`kairaFang` 분기 뒤, 함수 닫는 `  }` 앞:

```js
    } else if (rid === 'ferroCore') {
      const baseDmg = synergy ? (1.36 + stars * 0.08) : (1.16 + stars * 0.05);
      st.metaMods.dmgMul = (st.metaMods.dmgMul || 1) * baseDmg;
      st.metaMods.slowMul = (st.metaMods.slowMul || 1) * (synergy ? 1.20 : 1.10);
    }
```

- [ ] **Step 10: `activateAncientAwaken` 분기**

`kairaFang` 분기 뒤, 공통 tail(`state.comboFlash = 60;`) 앞:

```js
    } else if (relic.id === 'ferroCore') {
      if (level === 1) {
        state.metaMods.dmgMul *= 1.50;
        state.relicEffects.executeBelow = Math.max(state.relicEffects.executeBelow || 0, 0.10);
        toast(`🧲✨ 자기 코어 · 자극 각성!`);
      } else if (level === 2) {
        state.relicEffects.chainLightning = true;
        state.metaMods.dmgMul *= 1.20;
        toast(`🧲🌟 자기 코어 · 단극 각성!`);
      }
    }
```

- [ ] **Step 11: `TITLES` / `TITLE_ICON_KEY` / `PLATE_TITLES`**

`TITLES` — `kairaMaster` 줄 뒤:
```js
    feriaMaster:     { name: '자력의 지배자',   icon: '🧲', achId: 'char8_feria',     style: 'rainbow' },
```

`TITLE_ICON_KEY` — `kairaMaster:'dragon',` 뒤에 같은 줄로 추가 (값은 기존 29개 엠블럼 키 중 하나여야 한다):
```js
 feriaMaster:'vortex',
```

`PLATE_TITLES` — `'kairaMaster',` 뒤:
```js
'feriaMaster',
```

- [ ] **Step 12: `ACHIEVEMENTS` / `ACH_CAT_MAP`**

`char8_kaira` 항목 뒤:
```js
    { id: 'char8_feria',    name: '🧲 자력의 지배자',  desc: '🧲 페리아 8★ 달성',   reward: 1500,
      check: () => ((META.charStars || {}).feria || 0) >= 8 },
```

`ACH_CAT_MAP.chars` 배열 끝에 `, 'char8_feria'` 추가.

- [ ] **Step 13: `EVO_CHAR_LINES` / `CHAR_AMBUSH_LINES` / `CHAR_AMBUSH` / `_charRelicEv`**

`EVO_CHAR_LINES` — `kaira:` 줄 뒤:
```js
    feria:     '전부 끌어당겨. …도망칠 방향이 없게.',
```

`CHAR_AMBUSH_LINES` — `kaira:` 줄 뒤:
```js
    feria:    '쇳조각 좀 뿌려놨어. 밟으면 아플 거야.',
```

`CHAR_AMBUSH` — `kaira:` 항목 뒤 (SSR이므로 유물 이벤트 포함, 2줄):
```js
    feria:    [ { make: () => _charEv('🧲 페리아의 자장',      '"당겨서 뭉칠까, 밀어서 흩을까?"',                       'dmg',  22, 'polarField') },
                { avail: () => _ancientAvail('feria'), make: () => _charRelicEv('feria') } ],
```

`_charRelicEv` 의 `lore` 맵 — `kaira:` 줄 뒤:
```js
      feria:     { title: '🌌 자기 코어',       text: '"이 코어… 네 극에 맞춰 돌기 시작했어. 가져."' },
```

- [ ] **Step 14: `TD_UNLIMITED_RANGE_IDS` / `abilityPermaCostMul` / `MENU_HERO_IDS`**

`TD_UNLIMITED_RANGE_IDS` — kaira 줄 뒤 (전 맵 능력만):
```js
    'magRail', 'magnetStorm', 'monopole',                                  // 페리아 (관통/전체 붕괴/흡입장)
```

`abilityPermaCostMul` 의 `ssrAbilities` Set — kaira 줄 뒤:
```js
        'polarField', 'reversePolarity', 'magRail', 'magnetStorm', 'ferroShard', 'monopole',                // 🆕 feria
```

`MENU_HERO_IDS` — 배열에 `'feria'` 추가 (SSR이므로 앞쪽):
```js
  const MENU_HERO_IDS = ['aria','misaki','elementia','sumika','blanche','kaira','feria','solar','marine','gravitas','luna','sakura','cardista','levina','amy','chloe','lara','galatea'];
```

- [ ] **Step 15: 배선 검증**

Run:
```bash
grep -c "feria" index.html
grep -c "ferroCore" index.html
```
Expected: `feria` **20건 이상**, `ferroCore` **7건 이상**(RELICS·IDS·BY_CHAR·apply·awaken·unlockBy·lore).

브라우저 새로고침 → 콘솔 에러 0건.

- [ ] **Step 16: 커밋**

```bash
git add index.html
git commit -m "feat: 페리아(SSR) 전 계통 배선

CHARACTERS/COMBO/SIG/STAR_UNLOCKS/GACHA_POOL/아이콘순서/RELICS(ferroCore)/
고대유물 매핑+각성분기/칭호/업적/진화·기습 대사/사거리/영구강화비용/메뉴히어로.

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 4: 트리나 능력 4종 (`ABILITY_DEFS`)

**Files:** `index.html` — `ABILITY_DEFS` 닫는 `  };` 앞 (Task 2가 삽입한 페리아 블록 뒤)

**Interfaces:**
- Consumes: Task 1의 `_phantomDmg` / `_phantomScale`
- Produces: `phantomStage` `chromaticSplit` `encore` `standingOvation`

**환영 규칙 (전 능력 공통):** 환영 피해는 반드시 다음 형태로 감싼다.

```js
_phantomDmg = true; _phantomScale = <비율>;
try { /* damageEnemy 호출 */ } finally { _phantomDmg = false; _phantomScale = 1; }
```

`finally` 없이 쓰면 예외 발생 시 게이트가 켜진 채로 남아 **모든 능력의 즉사가 죽는다.**

- [ ] **Step 1: 4종 삽입**

```js
    // 🎭 트리나(SR) — 환영 타워 킷 (CMY 삼중인쇄 어긋남)
    //   ⚠️ 환영 피해 총 기여는 +90% 하드캡. 환영은 즉사·각인·별보너스·영구강화를 굴리지 않는다.
    //   상시 전체 키트 재현은 CX/CY 가 213곳 하드코딩이라 불가 — T4 에서만 처리한다.
    phantomStage: {
      name: '환영 무대', baseCost: 65, color: '#f0ece4', isGachaUnique: true,
      desc: lv => `환영 1기 · 0.4s 뒤 내 공격 재생(피해 40%) · 환영은 즉사·각인 미발동 · DMG ${30 + lv * 14}`,
      init(ab) { ab.cooldown = 0; ab.ph = []; ab.q = []; },
      tick(ab) {
        const n = 1 + permaCount('phantomStage');
        if (ab.ph.length !== n) {
          ab.ph = [];
          for (let i = 0; i < n; i++) ab.ph.push({ a: (Math.PI * 2 / n) * i, c: ['#00c8d7', '#e0489f', '#e8d24a'][i % 3] });
        }
        const R = ARENA_R * 0.55;
        for (const p of ab.ph) { p.x = CX + Math.cos(p.a) * R; p.y = CY + Math.sin(p.a) * R; }
        // 예약된 환영 타격 처리 (0.4s = 24프레임 지연)
        for (const j of ab.q) j.d--;
        for (const j of ab.q) {
          if (j.d > 0) continue;
          j.done = true;
          _phantomDmg = true; _phantomScale = 0.40;
          try { for (const e of state.enemies) { if (e.hp > 0 && !e._trinaHit) damageEnemy(e, j.dmg); } }
          finally { _phantomDmg = false; _phantomScale = 1; }
        }
        compactInPlace(ab.q, j => !j.done);
        if (--ab.cooldown > 0) return;
        ab.cooldown = Math.max(34, 70 - ab.level * 2);
        const dmg = 30 + ab.level * 14;
        const pool = state.enemies.filter(e => e.hp > 0);
        if (!pool.length) { ab.cooldown = 20; return; }
        // 실체 타격 — 게이트 없이 정상 판정
        const tgt = pool[Math.floor(Math.random() * pool.length)];
        damageEnemy(tgt, dmg);
        ab.q.push({ d: 24, dmg, done: false });
      },
      draw(ab) {
        ctx.save();
        for (const p of ab.ph) {
          ctx.globalAlpha = 0.4; ctx.strokeStyle = p.c; ctx.lineWidth = 2;
          ctx.beginPath(); ctx.arc(p.x, p.y, 13, 0, Math.PI * 2); ctx.stroke();
          ctx.globalAlpha = 0.18; ctx.fillStyle = p.c;
          ctx.beginPath(); ctx.arc(p.x, p.y, 11, 0, Math.PI * 2); ctx.fill();
        }
        ctx.restore(); ctx.globalAlpha = 1;
      },
    },
    // 🎭 기본조합 (환영무대+clone) — 색수차 분열
    chromaticSplit: {
      name: '색수차 분열', baseCost: 150, color: '#e0489f', isCombo: true,
      desc: lv => `환영 3기 120° · 피해 40/28/18%(합산 상한 +90%) · 환영은 판정 미발동 · DMG ${38 + lv * 16}`,
      init(ab) { ab.cooldown = 0; ab.ph = []; },
      tick(ab) {
        const SC = [0.40, 0.28, 0.18];
        const CL = ['#00c8d7', '#e0489f', '#e8d24a'];
        if (ab.ph.length !== 3) { ab.ph = []; for (let i = 0; i < 3; i++) ab.ph.push({ a: (Math.PI * 2 / 3) * i, c: CL[i], s: SC[i] }); }
        const R = ARENA_R * 0.6;
        for (const p of ab.ph) { p.a += 0.004; p.x = CX + Math.cos(p.a) * R; p.y = CY + Math.sin(p.a) * R; }
        if (--ab.cooldown > 0) return;
        ab.cooldown = Math.max(40, 84 - ab.level * 3);
        const pool = state.enemies.filter(e => e.hp > 0);
        if (!pool.length) { ab.cooldown = 20; return; }
        const dmg = 38 + ab.level * 16;
        damageEnemy(pool[Math.floor(Math.random() * pool.length)], dmg);
        // 환영 3기 — 합산 0.86 로 +90% 캡 아래
        let acc = 0;
        for (const p of ab.ph) {
          const s = Math.min(p.s, Math.max(0, 0.90 - acc));
          if (s <= 0) break;
          acc += s;
          const t = pool[Math.floor(Math.random() * pool.length)];
          _phantomDmg = true; _phantomScale = s;
          try { damageEnemy(t, dmg); } finally { _phantomDmg = false; _phantomScale = 1; }
        }
      },
      draw(ab) {
        ctx.save();
        for (const p of ab.ph) {
          ctx.globalAlpha = 0.45; ctx.strokeStyle = p.c; ctx.lineWidth = 2;
          ctx.beginPath(); ctx.arc(p.x, p.y, 14, 0, Math.PI * 2); ctx.stroke();
          ctx.globalAlpha = 0.12; ctx.fillStyle = p.c;
          ctx.beginPath(); ctx.arc(p.x, p.y, 12, 0, Math.PI * 2); ctx.fill();
        }
        ctx.restore(); ctx.globalAlpha = 1;
      },
    },
    // 🎭 4돌파 (색수차+orbital) — 앙코르
    encore: {
      name: '앙코르', baseCost: 240, color: '#c86ab0', isCombo: true, isTriple: true,
      desc: lv => `환영 3기가 적 밀집 방향으로 재배치 · 퇴장 시 마지막 공격 1회 추가 · 합산 상한 +90% · 판정 미발동 · DMG ${46 + lv * 18}`,
      init(ab) { ab.cooldown = 0; ab.ph = []; ab.last = 0; },
      tick(ab) {
        const SC = [0.40, 0.28, 0.18], CL = ['#00c8d7', '#e0489f', '#e8d24a'];
        if (ab.ph.length !== 3) { ab.ph = []; for (let i = 0; i < 3; i++) ab.ph.push({ a: (Math.PI * 2 / 3) * i, c: CL[i], s: SC[i] }); }
        // 적 밀집 각도로 재배치
        let sx = 0, sy = 0, cnt = 0;
        for (const e of state.enemies) { if (e.hp <= 0) continue; const [ex, ey] = enemyXY(e); sx += ex - CX; sy += ey - CY; cnt++; }
        const base = cnt ? Math.atan2(sy, sx) : 0;
        const R = ARENA_R * 0.6;
        for (let i = 0; i < 3; i++) {
          const p = ab.ph[i], want = base + (i - 1) * 0.8;
          p.a += Math.atan2(Math.sin(want - p.a), Math.cos(want - p.a)) * 0.05;
          p.x = CX + Math.cos(p.a) * R; p.y = CY + Math.sin(p.a) * R;
        }
        if (--ab.cooldown > 0) return;
        ab.cooldown = Math.max(46, 92 - ab.level * 3);
        const pool = state.enemies.filter(e => e.hp > 0);
        if (!pool.length) { ab.cooldown = 20; return; }
        const dmg = 46 + ab.level * 18;
        damageEnemy(pool[Math.floor(Math.random() * pool.length)], dmg);
        // 환영 + 앙코르 1회 — 전부 합쳐 +90% 캡 안에서 배분
        let acc = 0;
        const order = [ab.ph[0].s, ab.ph[1].s, ab.ph[2].s, 0.18];
        for (const raw of order) {
          const s = Math.min(raw, Math.max(0, 0.90 - acc));
          if (s <= 0) break;
          acc += s;
          const t = pool[Math.floor(Math.random() * pool.length)];
          _phantomDmg = true; _phantomScale = s;
          try { damageEnemy(t, dmg); } finally { _phantomDmg = false; _phantomScale = 1; }
        }
        ab.last = 14;
      },
      draw(ab) {
        if (ab.last > 0) ab.last--;
        ctx.save();
        for (const p of ab.ph) {
          const boost = ab.last > 0 ? 0.3 : 0;
          ctx.globalAlpha = 0.45 + boost; ctx.strokeStyle = p.c; ctx.lineWidth = 2;
          ctx.beginPath(); ctx.arc(p.x, p.y, 15, 0, Math.PI * 2); ctx.stroke();
          ctx.globalAlpha = 0.12; ctx.fillStyle = p.c;
          ctx.beginPath(); ctx.arc(p.x, p.y, 13, 0, Math.PI * 2); ctx.fill();
        }
        ctx.restore(); ctx.globalAlpha = 1;
      },
    },
    // 🎭 8돌파 (앙코르+turret) — 기립박수 (전체 키트 재생, CX/CY 임시 치환)
    standingOvation: {
      name: '기립박수', baseCost: 350, color: '#f0ece4', isCombo: true, isTriple: true, isEighth: true,
      desc: lv => `[8돌파] 5s간 환영 3기가 내 능력 전체를 재생(각 25%) · 환영은 판정 미발동 · DMG ${60 + lv * 22}`,
      init(ab) { ab.cooldown = 200; ab.on = 0; ab.step = 0; ab.ph = []; },
      tick(ab) {
        const CL = ['#00c8d7', '#e0489f', '#e8d24a'];
        if (ab.ph.length !== 3) { ab.ph = []; for (let i = 0; i < 3; i++) ab.ph.push({ a: (Math.PI * 2 / 3) * i, c: CL[i] }); }
        const R = ARENA_R * (ab.on > 0 ? 0.42 : 0.6);
        for (const p of ab.ph) { p.a += 0.01; p.x = CX + Math.cos(p.a) * R; p.y = CY + Math.sin(p.a) * R; }
        if (ab.on > 0) {
          ab.on--;
          // 6프레임마다 한 기씩 — 프레임 부하 분산
          if (++ab.step % 6 === 0) {
            const p = ab.ph[(ab.step / 6) % 3];
            const _ox = CX, _oy = CY;
            _phantomDmg = true; _phantomScale = 0.25;
            try {
              CX = p.x; CY = p.y;
              for (const t of state.tower.abilities) {
                const def = ABILITY_DEFS[t.id];
                if (!def || def.isPassive || t.id === 'standingOvation') continue;
                try { if (def.tick) def.tick(t); } catch (err) {}
              }
            } finally {
              CX = _ox; CY = _oy;
              _phantomDmg = false; _phantomScale = 1;
            }
          }
          return;
        }
        if (--ab.cooldown > 0) return;
        ab.cooldown = Math.max(300, 480 - ab.level * 8);
        ab.on = 300; ab.step = 0;
        const dmg = 60 + ab.level * 22;
        for (const e of state.enemies) { if (e.hp > 0) damageEnemy(e, dmg); }
        if (typeof shake === 'function') shake(14, 20);
      },
      draw(ab) {
        ctx.save();
        const act = ab.on > 0;
        for (const p of ab.ph) {
          ctx.globalAlpha = act ? 0.7 : 0.4; ctx.strokeStyle = p.c; ctx.lineWidth = act ? 3 : 2;
          ctx.beginPath(); ctx.arc(p.x, p.y, act ? 18 : 15, 0, Math.PI * 2); ctx.stroke();
          ctx.globalAlpha = act ? 0.2 : 0.1; ctx.fillStyle = p.c;
          ctx.beginPath(); ctx.arc(p.x, p.y, act ? 16 : 13, 0, Math.PI * 2); ctx.fill();
        }
        ctx.restore(); ctx.globalAlpha = 1;
      },
    },
```

- [ ] **Step 2: `CX`/`CY` 재대입 가능 여부 확인**

`standingOvation` 은 `CX`/`CY` 에 대입한다. 선언이 `let` 이어야 한다.

Run:
```bash
grep -n "let CX = W/2, CY = H/2;" index.html
```
Expected: **1건**([index.html:6236](../../../index.html)). `const` 라면 이 능력은 동작하지 않으므로 즉시 중단하고 보고한다.

- [ ] **Step 3: 게이트 누수 검증**

Run:
```bash
grep -c "finally { _phantomDmg = false" index.html
grep -c "_phantomDmg = true" index.html
```
Expected: **두 수가 같아야 한다.** 다르면 `finally` 없는 지점이 있다는 뜻이고, 예외 발생 시 게이트가 켜진 채 남아 게임 전체의 즉사가 죽는다.

- [ ] **Step 4: 파싱 검증**

브라우저 새로고침 → 콘솔 에러 0건.

- [ ] **Step 5: 커밋**

```bash
git add index.html
git commit -m "feat: 트리나(SR) 환영 타워 능력 4종 추가

phantomStage/chromaticSplit/encore/standingOvation.
환영 피해 40/28/18% + 합산 90% 하드캡, 전 지점 try/finally 게이트.
T4 만 CX/CY 임시치환으로 전체 키트 재생(6프레임 분산).

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 5: 트리나 레지스트리 배선 (SR)

SR이므로 **별해금·유물·플레이트 칭호는 없다.**

- [ ] **Step 1: `CHARACTERS`**

```js
    trina: {
      name: '🎭 트리나', color: '#e0489f',
      desc: '[SR] 환영 무대로 시작. 데미지 +26% / 보스 +10% / 레벨업 -8% / 슬롯 +1. 환영 + 분신 = 색수차 분열. 환영은 피해만 주고 판정은 굴리지 않는다.',
      startAbilities: ['phantomStage'],
      passive: { dmgMul: 1.26, bossDmgMul: 1.10, slotMod: 1, levelUpMul: 0.92, slowMul: 1 },
      unlockBy: 'gacha:trina',
      isGacha: true, rarity: 'SR',
      story: [
        { star: 0, title: '대기실', text: `무대에 서는 건 언제나 다른 사람이었다. 트리나는 커튼 뒤에서 모든 대사를 외웠다.

"괜찮아. 나는 언제든 설 수 있게 준비만 해두면 되니까."

거울 속 그녀의 윤곽이, 아주 살짝 어긋나 보였다.` },
        { star: 4, title: '세 번 인쇄된 사람', text: `"너… 방금 세 명이었어?"

트리나는 어깨를 으쓱했다. 그녀의 그림자는 분명 세 방향으로 갈라져 있었다.

"대역이 하나뿐이면 곤란하잖아. 나는 늘 여분을 준비해둬."` },
        { star: 8, title: '전원 등장', text: `막이 오르고, 무대 위에는 그녀 하나뿐이었다. 그런데 박수는 사방에서 터져 나왔다.

"주연이 못 되면 어때. …전부 내가 하면 되잖아."

세 개의 윤곽이 동시에 인사했다. 어느 쪽이 진짜인지, 아무도 알 수 없었다.` },
      ],
    },
```

- [ ] **Step 2: `COMBO_RECIPES` 3줄**

```js
    // 🎭 트리나(환영) 조합 체인
    { parts: ['phantomStage', 'clone'],        combo: 'chromaticSplit' },
    { parts: ['chromaticSplit', 'orbital'],    combo: 'encore', tier: 3 },
    { parts: ['encore', 'turret'],             combo: 'standingOvation', tier: 4 },
```

- [ ] **Step 3: 나머지 SR 레지스트리**

`CHAR_SIG_ABILITIES`:
```js
    trina:    ['phantomStage', 'chromaticSplit', 'encore', 'standingOvation'],
```

`GACHA_POOL.SR` 과 `_GACHA_SR_ALL` **둘 다** 에 `'trina'` 추가 (두 배열은 별개다 — 하나만 넣으면 배너 풀에서 누락된다).

`ABILITY_ICON_ORDER`:
```js
    // 🆕 트리나(SR) 환영 킷
    'phantomStage', 'chromaticSplit', 'encore', 'standingOvation',
```

`TITLES`:
```js
    trinaMaster:     { name: '대역 배우',         icon: '🎭', achId: 'char8_trina',   style: 'normal', color: '#e0489f' },
```

`TITLE_ICON_KEY` 에 `trinaMaster:'masks',` 추가. **`PLATE_TITLES` 에는 넣지 않는다**(신규 SR 선례).

`ACHIEVEMENTS`:
```js
    { id: 'char8_trina',    name: '🎭 대역 배우',      desc: '🎭 트리나 8★ 달성',   reward: 300,
      check: () => ((META.charStars || {}).trina || 0) >= 8 },
```
`ACH_CAT_MAP.chars` 에 `'char8_trina'` 추가.

`EVO_CHAR_LINES`:
```js
    trina:     '자, 막을 올릴게 — 오늘은 내가 주연이야.',
```

`CHAR_AMBUSH_LINES`:
```js
    trina:    '대역 셋 데려왔어. 누가 진짜인지 맞춰볼래?',
```

`CHAR_AMBUSH` (SR이므로 유물 이벤트 없이 1줄):
```js
    trina:    [ { make: () => _charEv('🎭 트리나의 무대',      '"환영을 늘릴까, 아니면 한 기를 더 진하게 만들까?"',       'dmg',  20, 'phantomStage') } ],
```

`TD_UNLIMITED_RANGE_IDS`:
```js
    'standingOvation',                                                     // 트리나 (전체 키트 재생)
```

`abilityPermaCostMul` 의 `srAbilities` Set:
```js
        'phantomStage', 'chromaticSplit', 'encore', 'standingOvation',           // 🆕 trina
```

`MENU_HERO_IDS` 배열 끝에 `'trina'` 추가.

- [ ] **Step 4: 배선 검증**

Run:
```bash
grep -c "trina" index.html
grep -n "_GACHA_SR_ALL = " index.html
grep -n "SR:  \['sakura'" index.html
```
Expected: `trina` **16건 이상**. 뒤 두 grep 의 각 배열에 `'trina'` 가 **둘 다** 들어 있어야 한다.

브라우저 새로고침 → 콘솔 에러 0건.

- [ ] **Step 5: 커밋**

```bash
git add index.html
git commit -m "feat: 트리나(SR) 전 계통 배선

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 6: 아이리스 능력 4종 (`ABILITY_DEFS`)

**Interfaces:**
- Produces: `longExposure` `overexposed` `contactSheet` `developingTray`
- Produces: `state._irisGhosts` (흑백 잔상 배열)

**밸런스 규칙:** 개체당 피해는 **노출시간만으로** 산정한다. 잡힌 적 수는 "몇 체를 때리는가"에만 쓰고 개체당 피해에 곱하지 않는다(준-제곱 방지).

- [ ] **Step 1: 4종 삽입**

```js
    // 📷 아이리스(SR) — 사진 킷 (발사 거부 · 노출 충전 · 임계 섬광)
    //   ⚠️ 개체당 피해는 노출시간만으로 산정한다. 적 수를 곱하지 않는다.
    longExposure: {
      name: '장노출', baseCost: 65, color: '#c0392b', isGachaUnique: true,
      desc: lv => `발사 안 하고 노출 충전 · 프레임 내 적 ${Math.max(2, 6 - Math.floor(lv / 3) - permaCount('longExposure'))}체 또는 최대 노출 시 섬광 · 피해는 노출시간으로만 산정 · DMG ${18 + lv * 9}`,
      init(ab) { ab.exp = 0; ab.flash = 0; ab.maxExp = 150; },
      tick(ab) {
        if (ab.flash > 0) ab.flash--;
        ab.exp = Math.min(ab.maxExp, ab.exp + 1);
        // ⭐ 별 퍽 — 임계 인원이 낮아질수록 자주 터진다
        const need = Math.max(2, 6 - Math.floor(ab.level / 3) - permaCount('longExposure'));
        const inFrame = state.enemies.filter(e => e.hp > 0 && (() => { const [x, y] = enemyXY(e); return Math.abs(x - CX) < 150 && Math.abs(y - CY) < 150; })());
        const full = ab.exp >= ab.maxExp;
        if (!full && inFrame.length < need) return;
        if (ab.exp < 30) return;
        // 개체당 피해 = 노출시간만. 적 수는 대상 수에만 영향.
        const dmg = (18 + ab.level * 9) * (ab.exp / ab.maxExp);
        for (const e of inFrame) damageEnemy(e, dmg);
        ab.flash = 12; ab.exp = 0;
      },
      draw(ab) {
        const p = ab.exp / ab.maxExp;
        ctx.save();
        // 조리개 6엽 — 노출이 찰수록 닫힌다
        ctx.globalAlpha = 0.5; ctx.strokeStyle = '#c0392b'; ctx.lineWidth = 2;
        const r = 34 - p * 18;
        for (let i = 0; i < 6; i++) {
          const a0 = (Math.PI * 2 / 6) * i + p * 0.5;
          ctx.beginPath();
          ctx.moveTo(CX + Math.cos(a0) * r, CY + Math.sin(a0) * r);
          ctx.lineTo(CX + Math.cos(a0 + Math.PI * 2 / 6) * r, CY + Math.sin(a0 + Math.PI * 2 / 6) * r);
          ctx.stroke();
        }
        // 뷰파인더 프레임 + 모서리 브래킷
        ctx.globalAlpha = 0.28; ctx.strokeStyle = '#d8d8d8'; ctx.lineWidth = 1.5;
        ctx.strokeRect(CX - 150, CY - 150, 300, 300);
        if (ab.flash > 0) {
          ctx.globalCompositeOperation = 'lighter';
          ctx.globalAlpha = ab.flash / 12 * 0.55; ctx.fillStyle = '#ffffff';
          ctx.fillRect(CX - 150, CY - 150, 300, 300);
        }
        ctx.restore(); ctx.globalAlpha = 1;
      },
    },
    // 📷 기본조합 (장노출+mine) — 과노출
    overexposed: {
      name: '과노출', baseCost: 150, color: '#a03028', isCombo: true,
      desc: lv => `장노출 섬광에 잡힌 적이 흑백 잔상으로 잔류 · 잔상 접촉 지속 DMG ${9 + lv * 5} · 잔상 4s`,
      init(ab) { ab.cooldown = 0; state._irisGhosts = []; },
      tick(ab) {
        const arr = state._irisGhosts || (state._irisGhosts = []);
        const dmg = 9 + ab.level * 5;
        for (const g of arr) {
          g.life--;
          for (const e of state.enemies) {
            if (e.hp <= 0) continue;
            const [ex, ey] = enemyXY(e);
            const dx = ex - g.x, dy = ey - g.y;
            if (dx * dx + dy * dy < 24 * 24) damageEnemy(e, dmg / 10);
          }
        }
        compactInPlace(arr, g => g.life > 0);
        if (--ab.cooldown > 0) return;
        ab.cooldown = Math.max(60, 120 - ab.level * 3);
        // 프레임 안의 적 위치를 필름에 태운다
        let n = 0;
        for (const e of state.enemies) {
          if (e.hp <= 0 || n >= 6) continue;
          const [ex, ey] = enemyXY(e);
          if (Math.abs(ex - CX) > 150 || Math.abs(ey - CY) > 150) continue;
          arr.push({ x: ex, y: ey, life: 240 }); n++;
        }
      },
      draw(ab) {
        const arr = state._irisGhosts || [];
        ctx.save();
        for (const g of arr) {
          const a = Math.min(1, g.life / 60) * 0.4;
          ctx.globalAlpha = a; ctx.strokeStyle = '#d8d8d8'; ctx.lineWidth = 1.5;
          ctx.beginPath(); ctx.arc(g.x, g.y, 13, 0, Math.PI * 2); ctx.stroke();
          ctx.globalAlpha = a * 0.4; ctx.fillStyle = '#8a8a8a';
          ctx.beginPath(); ctx.arc(g.x, g.y, 11, 0, Math.PI * 2); ctx.fill();
        }
        ctx.restore(); ctx.globalAlpha = 1;
      },
    },
    // 📷 4돌파 (과노출+turret) — 컨택트시트
    contactSheet: {
      name: '컨택트시트', baseCost: 240, color: '#8a2a24', isCombo: true, isTriple: true,
      desc: lv => `필드에 프레임 격자 ${4 + Math.floor(lv / 4)}칸 · 각 칸이 자기 임계(2체) 도달 시 독립 발화 · 칸당 DMG ${24 + lv * 11}`,
      init(ab) { ab.cells = []; },
      tick(ab) {
        const n = 4 + Math.floor(ab.level / 4);
        if (ab.cells.length !== n) {
          ab.cells = [];
          for (let i = 0; i < n; i++) {
            const a = (Math.PI * 2 / n) * i;
            ab.cells.push({ x: CX + Math.cos(a) * ARENA_R * 0.55, y: CY + Math.sin(a) * ARENA_R * 0.55, cd: 0, fl: 0 });
          }
        }
        const dmg = 24 + ab.level * 11;
        for (const c of ab.cells) {
          if (c.fl > 0) c.fl--;
          if (c.cd > 0) { c.cd--; continue; }
          const hit = state.enemies.filter(e => e.hp > 0 && (() => { const [x, y] = enemyXY(e); return Math.abs(x - c.x) < 52 && Math.abs(y - c.y) < 52; })());
          if (hit.length < 2) continue;
          for (const e of hit) damageEnemy(e, dmg);
          c.cd = Math.max(40, 90 - ab.level * 2); c.fl = 10;
        }
      },
      draw(ab) {
        ctx.save();
        for (const c of ab.cells) {
          ctx.globalAlpha = c.fl > 0 ? 0.6 : 0.2;
          ctx.strokeStyle = c.fl > 0 ? '#ffffff' : '#c0392b'; ctx.lineWidth = 1.5;
          ctx.strokeRect(c.x - 52, c.y - 52, 104, 104);
          for (const [ox, oy] of [[-52, -52], [52, -52], [-52, 52], [52, 52]]) {
            ctx.beginPath(); ctx.moveTo(c.x + ox, c.y + oy);
            ctx.lineTo(c.x + ox * 0.7, c.y + oy); ctx.stroke();
          }
        }
        ctx.restore(); ctx.globalAlpha = 1;
      },
    },
    // 📷 8돌파 (컨택트시트+timeStop) — 현상액
    developingTray: {
      name: '현상액', baseCost: 350, color: '#c0392b', isCombo: true, isTriple: true, isEighth: true,
      desc: lv => `[8돌파] 5s마다 화면 정지 후 모든 잔상 일괄 인화 · 전체 DMG ${50 + lv * 22} + 잔상 1개당 추가 ${6 + lv * 2}`,
      init(ab) { ab.cooldown = 180; ab.fx = 0; },
      tick(ab) {
        if (ab.fx > 0) ab.fx--;
        if (--ab.cooldown > 0) return;
        ab.cooldown = Math.max(220, 340 - ab.level * 6);
        ab.fx = 30;
        const ghosts = Math.min(20, (state._irisGhosts || []).length);
        const dmg = (50 + ab.level * 22) + ghosts * (6 + ab.level * 2);
        for (const e of state.enemies) {
          if (e.hp <= 0) continue;
          damageEnemy(e, dmg);
          e.slowFrames = Math.max(e.slowFrames || 0, 60);
        }
        if (state._irisGhosts) state._irisGhosts.length = 0;
        if (typeof shake === 'function') shake(14, 20);
      },
      draw(ab) {
        if (ab.fx <= 0) return;
        const p = 1 - ab.fx / 30;
        ctx.save();
        ctx.globalAlpha = (1 - p) * 0.35; ctx.fillStyle = '#1a1a1a';
        ctx.fillRect(0, 0, ctx.canvas.width, ctx.canvas.height);
        ctx.globalCompositeOperation = 'lighter';
        ctx.globalAlpha = (1 - p) * 0.7; ctx.strokeStyle = '#c0392b'; ctx.lineWidth = 3;
        ctx.beginPath(); ctx.arc(CX, CY, p * 300, 0, Math.PI * 2); ctx.stroke();
        ctx.restore(); ctx.globalAlpha = 1;
      },
    },
```

- [ ] **Step 2: 파싱 검증**

브라우저 새로고침 → 콘솔 에러 0건.

- [ ] **Step 3: 커밋**

```bash
git add index.html
git commit -m "feat: 아이리스(SR) 사진 능력 4종 추가

longExposure/overexposed/contactSheet/developingTray.
개체당 피해는 노출시간만으로 산정(적 수 곱 금지).

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 7: 아이리스 레지스트리 배선 (SR)

- [ ] **Step 1: `CHARACTERS`**

```js
    iris: {
      name: '📷 아이리스', color: '#c0392b',
      desc: '[SR] 장노출로 시작. 데미지 +32% / 보스 +22% / 레벨업 -7% / 슬롯 +1. 쏘지 않고 모았다가 한 번에 터뜨린다. 노출 + 지뢰 = 과노출.',
      startAbilities: ['longExposure'],
      passive: { dmgMul: 1.32, bossDmgMul: 1.22, slotMod: 1, levelUpMul: 0.93, slowMul: 1 },
      unlockBy: 'gacha:iris',
      isGacha: true, rarity: 'SR',
      story: [
        { star: 0, title: '기다리는 일', text: `셔터를 누르는 건 한순간이지만, 그 한순간을 기다리는 데는 몇 시간이 걸린다.

"급하게 찍으면 다 흔들려."

아이리스는 조리개를 조금 더 조였다. 어둠이 짙어질수록, 필름은 더 많은 것을 삼켰다.` },
        { star: 4, title: '태워진 상', text: `"…방금 지나간 게, 아직 저기 남아 있어."

빛이 지나간 자리에 형체가 눌어붙어 있었다. 필름에 타버린 잔상이, 실제로 걸어 다니는 것을 붙잡았다.

"움직인 건 네 잘못이야. 나는 그냥 오래 열어뒀을 뿐이고."` },
        { star: 8, title: '현상', text: `그녀가 트레이에 인화지를 담그자, 전장이 통째로 색을 잃었다.

"자, 이제 볼까. …오늘 뭐가 찍혔는지."

정지한 세계 속에서, 그동안 쌓인 모든 잔상이 한꺼번에 떠올랐다.` },
      ],
    },
```

- [ ] **Step 2: `COMBO_RECIPES` 3줄**

```js
    // 📷 아이리스(사진) 조합 체인
    { parts: ['longExposure', 'mine'],         combo: 'overexposed' },
    { parts: ['overexposed', 'turret'],        combo: 'contactSheet', tier: 3 },
    { parts: ['contactSheet', 'timeStop'],     combo: 'developingTray', tier: 4 },
```

> ⚠️ `turret` 이 트리나의 `standingOvation` 재료로도 쓰인다. 한 재료가 여러 레시피에 등장하는 것은 기존에도 있는 패턴이므로 문제없다(`frost` 는 3개 레시피에 등장). 다만 두 조합을 동시에 만족하는 상황에서 어느 쪽이 먼저 형성되는지는 `COMBO_RECIPES` 배열 순서를 따르므로, **트리나 체인을 아이리스 체인보다 앞에 둔다**(Task 5가 먼저 삽입되므로 자동 충족).

- [ ] **Step 3: 나머지 SR 레지스트리**

`CHAR_SIG_ABILITIES`:
```js
    iris:     ['longExposure', 'overexposed', 'contactSheet', 'developingTray'],
```

`GACHA_POOL.SR` 과 `_GACHA_SR_ALL` **둘 다** 에 `'iris'` 추가.

`ABILITY_ICON_ORDER`:
```js
    // 🆕 아이리스(SR) 사진 킷
    'longExposure', 'overexposed', 'contactSheet', 'developingTray',
```

`TITLES`:
```js
    irisMaster:      { name: '암실의 사진사',     icon: '📷', achId: 'char8_iris',    style: 'normal', color: '#c0392b' },
```

`TITLE_ICON_KEY` 에 `irisMaster:'bullseye',` 추가. **`PLATE_TITLES` 제외.**

`ACHIEVEMENTS`:
```js
    { id: 'char8_iris',     name: '📷 암실의 사진사',  desc: '📷 아이리스 8★ 달성', reward: 300,
      check: () => ((META.charStars || {}).iris || 0) >= 8 },
```
`ACH_CAT_MAP.chars` 에 `'char8_iris'` 추가.

`EVO_CHAR_LINES`:
```js
    iris:      '움직이지 마. …지금이 제일 좋은 순간이야.',
```

`CHAR_AMBUSH_LINES`:
```js
    iris:     '한 컷만 찍을게. …오래 걸릴 수도 있어.',
```

`CHAR_AMBUSH`:
```js
    iris:     [ { make: () => _charEv('📷 아이리스의 암실',    '"노출을 더 길게 갈까, 프레임을 더 넓게 열까?"',           'dmg',  20, 'longExposure') } ],
```

`TD_UNLIMITED_RANGE_IDS`:
```js
    'developingTray',                                                      // 아이리스 (전체 인화)
```

`abilityPermaCostMul` 의 `srAbilities` Set:
```js
        'longExposure', 'overexposed', 'contactSheet', 'developingTray',         // 🆕 iris
```

`MENU_HERO_IDS` 배열 끝에 `'iris'` 추가.

- [ ] **Step 4: 검증 + 커밋**

Run:
```bash
grep -c "iris" index.html
```
Expected: **16건 이상**. (주의: `iris` 는 짧은 단어라 오탐이 섞일 수 있다. `grep -n "iris:" index.html` 로 레지스트리 항목만 세면 더 정확하다.)

브라우저 새로고침 → 콘솔 에러 0건.

```bash
git add index.html
git commit -m "feat: 아이리스(SR) 전 계통 배선

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 8: 진화 트리 · 계보 · 배너 · 버전

마지막 태스크. 여기까지 끝나면 3인이 게임에서 실제로 뽑히고 진화 트리에 등장한다.

- [ ] **Step 1: `R_TOWERS[].sr` 4곳 추가 (기존 항목 수정 금지, 배열에 추가만)**

```js
    justice:    { title: '심판의 정의',   ability: 'frost',       sr: ['luna', 'gravitas', 'iris'] },
    empress:    { title: '풍요의 여황제', ability: 'clone',       sr: ['cardista', 'marine', 'lara', 'trina'] },
    world:      { title: '완성의 세계',   ability: 'orbital',     sr: ['luna', 'gravitas', 'trina'] },
    hierophant: { title: '신성의 교황',   ability: 'beam',        sr: ['luna', 'sakura', 'amy', 'iris'] },
```

- [ ] **Step 2: `SR_TO_SSR` 2쌍 추가**

```js
  const SR_TO_SSR = { marine:'elementia', levina:'elementia', luna:'misaki', gravitas:'misaki', sakura:'sumika', cardista:'sumika', solar:'aria', amy:'blanche', galatea:'blanche', chloe:'kaira', lara:'kaira', trina:'feria', iris:'feria' };
```

- [ ] **Step 3: `LINEAGE_RESONANCE` 4종**

키 규칙은 `<R타워의 ability>_<ssrId>` 이고, `sr` 값은 해당 R타워의 `sr` 배열에 있으면서 `SR_TO_SSR` 로 그 SSR에 도달하는 SR이어야 한다. 아래 4개는 Step 1·2와 정합한다.

kaira 블록 뒤, 객체 닫는 `  };` 앞:

```js
    // ── 🧲 페리아 (자력·쌍극) ── 브릿지: trina·iris
    clone_feria:          { sr:'trina',    ssr:'feria',     axis:'echo',  name:'복제 자장',
                            lines:['트리나: 분신 세워둘게 — 자리는 내가 잡아.', '페리아: 좋아. …전부 같은 극으로 묶는다.'] },
    orbital_feria:        { sr:'trina',    ssr:'feria',     axis:'echo',  name:'궤도 정렬',
                            lines:['트리나: 궤도는 맞춰뒀어. 신호만 줘.', '페리아: 궤도가 있으면 — 끌어당기기 쉬워지지.'] },
    frost_feria:          { sr:'iris',     ssr:'feria',     axis:'ice',   name:'정지 노출',
                            lines:['아이리스: 움직이지 말라니까. 셔터 열어둘게.', '페리아: 멈춘 건 …자석에서 못 벗어나.'] },
    beam_feria:           { sr:'iris',     ssr:'feria',     axis:'pierce',name:'관통 인화',
                            lines:['아이리스: 한 줄로 세워줘. 그럼 한 컷에 담겨.', '페리아: 정렬 완료. …꿰뚫는다.'] },
```

- [ ] **Step 4: 4번째 가챠 배너**

`GACHA_BANNERS` 의 `prismBeast` 항목 뒤, 배열 닫는 `  ];` 앞:

```js
    {
      id: 'ferroPole',
      name: '🧲 페리아 픽업',
      desc: '두 개의 극 — 단독 픽업',
      bannerImg: './icons/gacha-ferroPole.jpg',
      pool: {
        SSR: ['feria'],                               // 단독 픽업
        SR:  _GACHA_SR_ALL,
        R:   [],
      },
      rates: { SR: 0.05, SSR: 0.01 },
      featured: 'feria',
      ancientRelic: 'ferroCore',
      ancientRelicPool: ['ferroCore'],
      ancientRelicRate: 0.005,
    },
```

> 배너 이미지 `icons/gacha-ferroPole.jpg` 는 아직 없다. `<img onerror>` 폴백이 있으므로 로드 실패해도 게임은 정상 동작한다. 이미지가 준비되면 그때 넣는다.

- [ ] **Step 5: `sw.js` — 배너 프리캐시 목록**

```js
const DEFERRED_ASSETS = [
  './icons/gacha-elemSumi.png',
  './icons/gacha-ariaMisa.png',
  './icons/gacha-prismBeast.jpg',
  './icons/gacha-ferroPole.jpg',
];
```

`cache.add` 는 개별 `.catch(() => {})` 로 감싸져 있으므로 파일이 없어도 설치가 실패하지 않는다.

- [ ] **Step 6: 버전 bump**

`index.html`: `const APP_VERSION = 673;`
`sw.js`: `const CACHE = 'dot-defense-v673';`

- [ ] **Step 7: 전체 검증**

브라우저 새로고침 → 콘솔 에러 0건.

메뉴에서 `123123123` 입력해 치트를 켜고 `unlock all` 실행.
Expected: 캐릭터 수 **17 → 20**.

배너를 좌우로 넘겨 4번째 배너 이름이 **"🧲 페리아 픽업"** 으로 표시되는지 확인.

Run:
```bash
grep -c "'feria'" index.html
grep -c "'trina'" index.html
grep -c "'iris'" index.html
```
Expected: 셋 다 **8건 이상**.

- [ ] **Step 8: 커밋**

```bash
git add index.html sw.js
git commit -m "feat: 신규 3인 진화트리·계보·배너 편입 + v673

R_TOWERS.sr 4곳 추가(기존 항목 수정 0), SR_TO_SSR 2쌍, 계보공명 4종,
4번째 단독픽업 배너 ferroPole, sw 프리캐시.

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## 실기기 확인 항목 (개발 환경에서 검증 불가)

프리뷰 환경은 `rAF` 가 정지해 있어 캔버스가 그려지지 않는다. 아래는 반드시 실기기에서 본다.

1. **트리나 환영이 즉사·각인을 굴리지 않는지.** 유물 `executeBelow` 를 보유한 상태로 트리나 런을 돌려 즉사 빈도가 비정상적으로 튀지 않는지 확인. 이게 새면 밸런스 설계 전체가 무의미해진다.
2. **`standingOvation` 의 CX/CY 치환 구간**에서 좌표를 `init` 에 캐시하는 능력(예: `magnetStorm` 의 `ab.bx/by` 류)이 어긋나 보이지 않는지.
3. **페리아 충돌 쿨**이 밀집 웨이브에서 프레임을 지켜내는지 (모바일).
4. **아이리스 흑백**이 스미카(먹빛)와 화면에서 구분되는지.
5. 신규 3인의 치비가 인게임 타워 중앙에 정상 표시되는지 (v672 크로마키 제거 후 첫 신규 캐릭터).
