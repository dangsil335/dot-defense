# 별돌파 12종 (SR 6명) 구현 계획 — 고유장비 단계 0-a

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 별돌파가 없는 SR 6명(에이미·클로에·라라·갈라테아·트리나·아이리스)에게 4★/8★ 능력 12종을 신규 추가해, 20명 전원이 동일한 "메인(t1 시그니처) + 서브(별돌파 4★)" 구조를 갖게 한다.

**Architecture:** 기존 `ABILITY_DEFS`에 능력 12종을 추가하고 5개 레지스트리에 배선한다. 로직은 `init/tick/draw` 클로저로 코드에 유지(기존 패턴). 신규 인프라 없음.

**Tech Stack:** 바닐라 JS IIFE, Canvas 2D, 단일 파일 `index.html`. **빌드 없음. 테스트 프레임워크 없음.**

**상위 스펙:** `docs/superpowers/specs/2026-07-21-unique-gear-design.md` §4
**선례:** v674 카르디스타·레비나 4종 추가 (커밋 `c75d86b` 능력 + `d5810f5` 배선)

---

## Global Constraints

- **플래그는 정확히 `isGachaUnique: true, isStarUnlock: true` 둘만.** `isCombo`/`isTriple`/`isEighth`는 인런 조합체인 시스템이라 **절대 금지**(붙이면 조합 카드에 뜨고 비용 계산이 틀어짐).
- **`baseCost`: 4★ = 280, 8★ = 480.** 예외 없음.
- **`desc` 접두사: 4★ = `[4★히든-SR]`, 8★ = `[8★히든-SR]`.**
- **`CHAR_SIG_ABILITIES`에 절대 넣지 않는다.** 그건 t1~t4 조합체인 전용이고, 별돌파 id는 사쿠라·루나도 거기 없다.
- **`abilityPermaCostMul` 배선 불필요** — `isStarUnlock`이면 함수 첫 줄에서 3.0을 반환한다.
- **트리나 2종은 환영 게이트 필수** — 아래 별도 항목 참조.
- **버전 규율:** 최종 Task에서 `index.html`의 `APP_VERSION`과 `sw.js`의 `CACHE='dot-defense-vNNN'`을 **둘 다** 올린다. 현재 v674 → 완료 시 **v675**.
- **편집 규율:** `index.html`은 2MB다. Edit 도구로 유니크한 `old_string`을 써라. `replace_all` 금지. 파일 통째 재작성 금지.
- **검증(테스트 프레임워크 없음):** ① 인라인 `<script>` 추출 후 `node --check` ② 브라우저 콘솔 에러 0 ③ grep 배선 확인.

### ⚠️ 트리나 전용 제약 (환영 게이트)

트리나 능력은 **환영이 때리는 피해**다. 모듈 스코프 플래그 `_phantomDmg`/`_phantomScale`(`damageEnemy` 옆에 선언)이 켜져 있으면 `damageEnemy`가 피해를 배율하고 **즉사·계보각인·별보너스·영구강화 4가지 판정을 건너뛴다**.

**모든 환영 피해는 반드시 이 형태로 감싼다:**
```js
_phantomDmg = true; _phantomScale = <비율>;
try { /* damageEnemy 호출 */ } finally { _phantomDmg = false; _phantomScale = 1; }
```
`finally`가 없으면 예외 발생 시 플래그가 켜진 채 남아 **게임 전체의 즉사·각인이 죽는다.** 조용히 망가지는 종류다.

또한 신규 트리나 능력 2종을 **`TRINA_PHANTOM_IDS`(~L6757)에 추가**해야 한다. 이 Set은 `standingOvation`이 다른 능력을 재생할 때 제외할 목록이고, 빠뜨리면 재생된 능력의 `finally`가 공유 플래그를 먼저 꺼서 이후 재생분이 판정 미적용 없이 발동한다.

---

## 신규 능력 12종 개요

| 캐릭터 | 4★ | 8★ |
|---|---|---|
| 에이미 (드론) | `droneSwarm` 드론 군집 | `skyDominion` 제공권 |
| 클로에 (산성) | `acidRain` 산성비 | `omniSolvent` 만상 용해 |
| 라라 (인형) | `stringWeb` 실 그물 | `grandGuignol` 그랑 기뇰 |
| 갈라테아 (석화) | `stoneGarden` 석상 정원 | `gorgonRealm` 고르곤의 영역 |
| 트리나 (환영) | `understudyCall` 대역 소집 | `finalBow` 마지막 인사 |
| 아이리스 (사진) | `flashbulb` 플래시 | `darkroomVault` 암실 금고 |

**12개 id 전부 파일 내 충돌 없음(확인 완료).**

---

## File Structure

| 파일 | 변경 |
|---|---|
| `index.html` | 수정 (전 Task) — `ABILITY_DEFS` 삽입 + 레지스트리 5곳 |
| `sw.js` | 수정 (Task 7) — CACHE 버전만 |
| `icons/abilities/*.png` | **미제작 — 없어도 색상박스+첫글자 폴백으로 동작. 이번 범위 밖.** |

**삽입 위치:** `ABILITY_DEFS`의 닫는 `  };`(현재 ~L18492) **바로 앞**. Task 1~6이 순차로 그 앞에 쌓는다. 각 Task는 편집 전에 닫는 위치를 직접 재확인할 것(앞 Task 때문에 줄이 밀린다).

**공용 헬퍼(전부 이미 존재):** `damageEnemy(e,dmg)`, `enemyXY(e)→[x,y]`, `spawnParticles(x,y,color,n)`, `compactInPlace(arr,keepPred)`, `_alivePredLife`, `_predNotDone`, `getGlowSprite(color)`, `permaCount(id)`, `W`, `H`, `CX`, `CY`, `ARENA_R`(=290, [index.html:6258](../../../index.html)), `state.enemies`, `state.t`, `state.bullets`, `ctx`, `e.slowFrames`, `e.size`, `e.isBoss`, `e.maxHp`, `e.timeStopped`, `shake(a,b)`.

**탄 객체 형태(`state.bullets.push` 시 필수 필드):**
```js
{ x, y, vx, vy, dmg, life, color, target, leader: null, offsetAngle: 0, sourceId: state.currentAbilityId || null }
```

---

## Task 1: 에이미 별돌파 2종

**Files:** Modify `index.html` — `ABILITY_DEFS` 닫는 `  };` 앞

**Interfaces:**
- Produces: 능력 id `droneSwarm`(4★), `skyDominion`(8★)

- [ ] **Step 1: 두 능력 삽입**

`ABILITY_DEFS`의 닫는 `  };`를 찾아 그 **바로 앞**에 삽입:

```js
    // 🛰 에이미 4★/8★ 별해금 — 드론 군집 / 제공권
    droneSwarm: {
      name: '드론 군집', isGachaUnique: true, isStarUnlock: true, baseCost: 280, color: '#FFB703',
      desc: lv => `[4★히든-SR] ${3 + Math.floor(lv / 2)}기 자율 드론 상시 순찰 · 자동 요격 DMG ${12 + lv * 6}`,
      init(ab) { ab.drones = []; },
      tick(ab) {
        const n = 3 + Math.floor(ab.level / 2) + permaCount('droneSwarm');
        if (ab.drones.length !== n) {
          ab.drones = [];
          for (let i = 0; i < n; i++) ab.drones.push({ a: (Math.PI * 2 / n) * i, r: 84 + (i % 3) * 16, cd: i * 6 });
        }
        const dmg = 12 + ab.level * 6;
        for (const d of ab.drones) {
          d.a += 0.022;
          d.x = CX + Math.cos(d.a) * d.r; d.y = CY + Math.sin(d.a) * d.r;
          if (--d.cd > 0) continue;
          let best = null, bd = 1e9;
          for (const e of state.enemies) {
            if (e.hp <= 0) continue;
            const [ex, ey] = enemyXY(e);
            const q = (ex - d.x) * (ex - d.x) + (ey - d.y) * (ey - d.y);
            if (q < bd) { bd = q; best = e; }
          }
          if (!best) { d.cd = 18; continue; }
          const [tx, ty] = enemyXY(best);
          const ang = Math.atan2(ty - d.y, tx - d.x);
          state.bullets.push({ x: d.x, y: d.y, vx: Math.cos(ang) * 8, vy: Math.sin(ang) * 8, dmg, life: 55, color: '#FFB703', target: best, leader: null, offsetAngle: 0, sourceId: state.currentAbilityId || null });
          d.cd = Math.max(18, 40 - ab.level);
        }
      },
      draw(ab) {
        ctx.save(); ctx.globalCompositeOperation = 'lighter';
        ctx.globalAlpha = 0.12; ctx.strokeStyle = '#FFB703'; ctx.lineWidth = 1;
        for (const r of [84, 100, 116]) { ctx.beginPath(); ctx.arc(CX, CY, r, 0, Math.PI * 2); ctx.stroke(); }
        for (const d of ab.drones) {
          ctx.save(); ctx.translate(d.x, d.y); ctx.rotate(d.a + Math.PI / 2);
          ctx.globalAlpha = 0.9; ctx.fillStyle = '#ffd24a';
          ctx.beginPath(); ctx.moveTo(0, -5); ctx.lineTo(4, 4); ctx.lineTo(-4, 4); ctx.closePath(); ctx.fill();
          ctx.globalAlpha = 0.5; ctx.fillStyle = '#fff2c0';
          ctx.beginPath(); ctx.arc(0, 0, 1.8, 0, Math.PI * 2); ctx.fill();
          ctx.restore();
        }
        ctx.restore(); ctx.globalAlpha = 1;
      },
    },
    skyDominion: {
      name: '제공권', isGachaUnique: true, isStarUnlock: true, baseCost: 480, color: '#ffcf40',
      desc: lv => `[8★히든-SR] 3s마다 전 맵 ${6 + lv}지점 정밀폭격 · 광역 DMG ${35 + lv * 18}`,
      init(ab) { ab.cooldown = 100; ab.marks = []; },
      tick(ab) {
        const dmg = 35 + ab.level * 18, exR = 62 + ab.level * 4;
        for (const m of ab.marks) {
          m.t++;
          if (m.t < 22) continue;
          m.done = true;
          for (const e of state.enemies) {
            if (e.hp <= 0) continue;
            const [ex, ey] = enemyXY(e);
            if ((ex - m.x) * (ex - m.x) + (ey - m.y) * (ey - m.y) < exR * exR) { damageEnemy(e, dmg); spawnParticles(ex, ey, '#ffcf40', 4); }
          }
        }
        compactInPlace(ab.marks, _predNotDone);
        if (--ab.cooldown > 0) return;
        ab.cooldown = Math.max(150, 240 - ab.level * 6);
        const pool = state.enemies.filter(e => e.hp > 0);
        const n = 6 + ab.level;
        for (let i = 0; i < n; i++) {
          let mx, my;
          if (pool.length) { const t = pool[Math.floor(Math.random() * pool.length)]; const [tx, ty] = enemyXY(t); mx = tx + (Math.random() - 0.5) * 60; my = ty + (Math.random() - 0.5) * 60; }
          else { mx = CX + (Math.random() - 0.5) * 300; my = CY + (Math.random() - 0.5) * 300; }
          ab.marks.push({ x: mx, y: my, t: -i * 3, done: false });
        }
      },
      draw(ab) {
        ctx.save(); ctx.globalCompositeOperation = 'lighter';
        for (const m of ab.marks) {
          if (m.t < 0) continue;
          const p = m.t / 22;
          ctx.globalAlpha = 0.25 + p * 0.5; ctx.strokeStyle = '#ffcf40'; ctx.lineWidth = 1.6;
          ctx.beginPath(); ctx.arc(m.x, m.y, 30 * (1 - p) + 8, 0, Math.PI * 2); ctx.stroke();
          ctx.beginPath(); ctx.moveTo(m.x - 10, m.y); ctx.lineTo(m.x + 10, m.y);
          ctx.moveTo(m.x, m.y - 10); ctx.lineTo(m.x, m.y + 10); ctx.stroke();
          if (p > 0.92) { ctx.globalAlpha = 0.7; ctx.fillStyle = '#fff0b0'; ctx.beginPath(); ctx.arc(m.x, m.y, 22, 0, Math.PI * 2); ctx.fill(); }
        }
        ctx.restore(); ctx.globalAlpha = 1;
      },
    },
```

- [ ] **Step 2: 문법 검증**

Run (git-bash):
```bash
cd /c/Users/solid/Desktop/dot-defense
SC="$(pwd)/.superpowers/sdd/_chk.js"
node -e "const fs=require('fs');const h=fs.readFileSync('index.html','utf8');const m=h.match(/<script>([\s\S]*)<\/script>/);fs.writeFileSync(process.argv[1],m[1]);" "$SC" && node --check "$SC" && echo "SYNTAX OK" && rm -f "$SC"
```
Expected: `SYNTAX OK`

- [ ] **Step 3: 브라우저 검증**

`mcp__Claude_Browser__preview_start` `{name: "dot-defense"}` → `mcp__Claude_Browser__tabs_context`로 tabId → `mcp__Claude_Browser__read_console_messages` `{onlyErrors: true}`
Expected: 에러 0건

- [ ] **Step 4: 플래그 확인**

Run:
```bash
grep -n "droneSwarm:\|skyDominion:" index.html
grep -c "isCombo" index.html
```
Expected: 두 id가 각 1회 정의. 두 능력 헤더에 `isCombo`/`isTriple`/`isEighth`가 **없어야** 한다(육안 확인).

- [ ] **Step 5: 커밋**

```bash
git add index.html
git commit -m "feat: 에이미 별돌파 2종 (droneSwarm 4★ / skyDominion 8★)

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 2: 클로에 별돌파 2종

**Files:** Modify `index.html` — `ABILITY_DEFS` 닫는 `  };` 앞 (Task 1 블록 뒤)

**Interfaces:**
- Produces: `acidRain`(4★), `omniSolvent`(8★)

- [ ] **Step 1: 두 능력 삽입**

```js
    // ⚗ 클로에 4★/8★ 별해금 — 산성비 / 만상 용해
    acidRain: {
      name: '산성비', isGachaUnique: true, isStarUnlock: true, baseCost: 280, color: '#a0e050',
      desc: lv => `[4★히든-SR] 4s마다 산성비 ${8 + lv}방울 낙하 · 착탄 산성 장판 · 초당 DMG ${(4 + lv * 2) * 5}`,
      init(ab) { ab.cooldown = 90; ab.drops = []; ab.pools = []; },
      tick(ab) {
        const tick5 = 4 + ab.level * 2;
        for (const p of ab.pools) {
          p.life--;
          if (state.t % 12 !== 0) continue;
          for (const e of state.enemies) {
            if (e.hp <= 0) continue;
            const [ex, ey] = enemyXY(e);
            if ((ex - p.x) * (ex - p.x) + (ey - p.y) * (ey - p.y) < p.r * p.r) {
              damageEnemy(e, tick5);
              e.slowFrames = Math.max(e.slowFrames || 0, 24);
            }
          }
        }
        compactInPlace(ab.pools, _alivePredLife);
        for (const d of ab.drops) {
          d.t++;
          if (d.t < 20) continue;
          d.done = true;
          ab.pools.push({ x: d.x, y: d.y, r: 46 + ab.level * 3, life: 200 });
          spawnParticles(d.x, d.y, '#a0e050', 5);
        }
        compactInPlace(ab.drops, _predNotDone);
        if (--ab.cooldown > 0) return;
        ab.cooldown = Math.max(160, 250 - ab.level * 5);
        const pool = state.enemies.filter(e => e.hp > 0);
        const n = 8 + ab.level;
        for (let i = 0; i < n; i++) {
          let dx, dy;
          if (pool.length) { const t = pool[Math.floor(Math.random() * pool.length)]; const [tx, ty] = enemyXY(t); dx = tx + (Math.random() - 0.5) * 90; dy = ty + (Math.random() - 0.5) * 90; }
          else { dx = CX + (Math.random() - 0.5) * 320; dy = CY + (Math.random() - 0.5) * 320; }
          ab.drops.push({ x: dx, y: dy, t: -i * 2, done: false });
        }
      },
      draw(ab) {
        ctx.save();
        for (const p of ab.pools) {
          const a = Math.min(1, p.life / 40) * 0.30;
          const g = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, p.r);
          g.addColorStop(0, `rgba(160,224,80,${a})`); g.addColorStop(1, 'rgba(160,224,80,0)');
          ctx.fillStyle = g; ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2); ctx.fill();
          ctx.globalAlpha = a * 1.4; ctx.strokeStyle = '#b8f060'; ctx.lineWidth = 1.2;
          ctx.beginPath(); ctx.arc(p.x, p.y, p.r * 0.92, 0, Math.PI * 2); ctx.stroke();
        }
        ctx.globalCompositeOperation = 'lighter';
        for (const d of ab.drops) {
          if (d.t < 0) continue;
          const p = d.t / 20, my = d.y - (1 - p) * 190;
          ctx.globalAlpha = 0.8; ctx.strokeStyle = '#c0ff60'; ctx.lineWidth = 2.4; ctx.lineCap = 'round';
          ctx.beginPath(); ctx.moveTo(d.x, my - 14); ctx.lineTo(d.x, my); ctx.stroke();
          ctx.globalAlpha = 0.25 + p * 0.3; ctx.strokeStyle = '#a0e050'; ctx.lineWidth = 1.3;
          ctx.beginPath(); ctx.arc(d.x, d.y, 8 + p * 10, 0, Math.PI * 2); ctx.stroke();
        }
        ctx.restore(); ctx.globalAlpha = 1;
      },
    },
    omniSolvent: {
      name: '만상 용해', isGachaUnique: true, isStarUnlock: true, baseCost: 480, color: '#c0ff40',
      desc: lv => `[8★히든-SR] 상시 부식장 둔화 · 1.5s마다 전체 ${(2 + lv * 0.4).toFixed(1)}% maxHP 용해`,
      init(ab) { ab.dotT = 0; ab.pulse = 0; },
      tick(ab) {
        ab.pulse += 0.04;
        for (const e of state.enemies) {
          if (e.hp <= 0) continue;
          e.slowFrames = Math.max(e.slowFrames || 0, 10);
        }
        if (++ab.dotT < 90) return;
        ab.dotT = 0;
        const pct = 0.02 + ab.level * 0.004;
        const bossPct = pct * 0.4;
        for (const e of state.enemies) {
          if (e.hp <= 0 || e.maxHp <= 0) continue;
          const p = e.isBoss ? bossPct : pct;
          damageEnemy(e, Math.max(1, Math.ceil(e.maxHp * p)));
        }
      },
      draw(ab) {
        ctx.save();
        const amb = 0.05 + 0.02 * Math.sin(ab.pulse);
        const R = Math.min(W, H) * 0.5;
        const g = ctx.createRadialGradient(CX, CY, 0, CX, CY, R);
        g.addColorStop(0, `rgba(192,255,64,${amb})`); g.addColorStop(0.65, `rgba(160,224,80,${amb * 0.5})`); g.addColorStop(1, 'rgba(160,224,80,0)');
        ctx.fillStyle = g; ctx.beginPath(); ctx.arc(CX, CY, R, 0, Math.PI * 2); ctx.fill();
        ctx.globalCompositeOperation = 'lighter';
        for (let i = 0; i < 3; i++) {
          const r = 70 + i * 60 + Math.sin(ab.pulse + i) * 10;
          ctx.globalAlpha = 0.14 - i * 0.035; ctx.strokeStyle = '#c0ff40'; ctx.lineWidth = 2;
          ctx.beginPath(); ctx.arc(CX, CY, r, 0, Math.PI * 2); ctx.stroke();
        }
        ctx.restore(); ctx.globalAlpha = 1;
      },
    },
```

> 참고: `desc`의 `2 + lv * 0.4`(%)와 `tick`의 `pct = 0.02 + ab.level * 0.004`는 같은 값이다(표시는 %, 계산은 비율).

- [ ] **Step 2: 문법 검증** — Task 1 Step 2와 동일한 명령. Expected: `SYNTAX OK`

- [ ] **Step 3: 브라우저 검증** — 콘솔 에러 0건

- [ ] **Step 4: 커밋**

```bash
git add index.html
git commit -m "feat: 클로에 별돌파 2종 (acidRain 4★ / omniSolvent 8★)

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 3: 라라 별돌파 2종

**Files:** Modify `index.html` — `ABILITY_DEFS` 닫는 `  };` 앞

**Interfaces:**
- Produces: `stringWeb`(4★), `grandGuignol`(8★)

- [ ] **Step 1: 두 능력 삽입**

```js
    // 🎭 라라 4★/8★ 별해금 — 실 그물 / 그랑 기뇰
    stringWeb: {
      name: '실 그물', isGachaUnique: true, isStarUnlock: true, baseCost: 280, color: '#d070c0',
      desc: lv => `[4★히든-SR] 실 그물 ${4 + Math.floor(lv / 2)}가닥 · 닿은 적 슬로우 + 지속 DMG ${10 + lv * 5}`,
      init(ab) { ab.nodes = []; ab.rot = 0; },
      tick(ab) {
        const n = 4 + Math.floor(ab.level / 2);
        if (ab.nodes.length !== n) {
          ab.nodes = [];
          for (let i = 0; i < n; i++) ab.nodes.push({ a: (Math.PI * 2 / n) * i, r: 130 + (i % 2) * 44 });
        }
        ab.rot += 0.006;
        for (const nd of ab.nodes) { nd.x = CX + Math.cos(nd.a + ab.rot) * nd.r; nd.y = CY + Math.sin(nd.a + ab.rot) * nd.r; }
        if (state.t % 10 !== 0) return;
        const dmg = 10 + ab.level * 5;
        for (const e of state.enemies) {
          if (e.hp <= 0) continue;
          const [ex, ey] = enemyXY(e);
          for (let i = 0; i < ab.nodes.length; i++) {
            const a = ab.nodes[i], b = ab.nodes[(i + 1) % ab.nodes.length];
            const vx = b.x - a.x, vy = b.y - a.y;
            const L2 = vx * vx + vy * vy || 1;
            let t = ((ex - a.x) * vx + (ey - a.y) * vy) / L2;
            t = t < 0 ? 0 : (t > 1 ? 1 : t);
            const px = a.x + vx * t, py = a.y + vy * t;
            if ((ex - px) * (ex - px) + (ey - py) * (ey - py) < 14 * 14) {
              damageEnemy(e, dmg);
              e.slowFrames = Math.max(e.slowFrames || 0, 40);
              spawnParticles(ex, ey, '#e070d0', 2);
              break;
            }
          }
        }
      },
      draw(ab) {
        if (ab.nodes.length < 2) return;
        ctx.save(); ctx.globalCompositeOperation = 'lighter';
        ctx.globalAlpha = 0.42; ctx.strokeStyle = '#e070d0'; ctx.lineWidth = 1.6;
        ctx.beginPath();
        for (let i = 0; i < ab.nodes.length; i++) {
          const a = ab.nodes[i], b = ab.nodes[(i + 1) % ab.nodes.length];
          ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y);
        }
        ctx.stroke();
        ctx.globalAlpha = 0.16; ctx.lineWidth = 1;
        ctx.beginPath();
        for (const nd of ab.nodes) { ctx.moveTo(CX, CY); ctx.lineTo(nd.x, nd.y); }
        ctx.stroke();
        ctx.globalAlpha = 0.8; ctx.fillStyle = '#f0a0e0';
        for (const nd of ab.nodes) { ctx.beginPath(); ctx.arc(nd.x, nd.y, 3, 0, Math.PI * 2); ctx.fill(); }
        ctx.restore(); ctx.globalAlpha = 1;
      },
    },
    grandGuignol: {
      name: '그랑 기뇰', isGachaUnique: true, isStarUnlock: true, baseCost: 480, color: '#e64fd0',
      desc: lv => `[8★히든-SR] 거대 인형 자율 추격 · 근접 DMG ${40 + lv * 20} + 3s마다 실폭발`,
      init(ab) { ab.x = CX; ab.y = CY - 70; ab.cd = 0; ab.burst = 0; ab.ang = 0; },
      tick(ab) {
        let best = null, bd = 1e9;
        for (const e of state.enemies) {
          if (e.hp <= 0) continue;
          const [ex, ey] = enemyXY(e);
          const q = (ex - ab.x) * (ex - ab.x) + (ey - ab.y) * (ey - ab.y);
          if (q < bd) { bd = q; best = e; }
        }
        if (best) {
          const [tx, ty] = enemyXY(best);
          const d = Math.hypot(tx - ab.x, ty - ab.y) || 1;
          ab.x += (tx - ab.x) / d * 2.2; ab.y += (ty - ab.y) / d * 2.2;
          ab.ang = Math.atan2(ty - ab.y, tx - ab.x);
        }
        if (ab.burst > 0) ab.burst--;
        const dmg = 40 + ab.level * 20;
        if (--ab.cd <= 0) {
          ab.cd = 30;
          for (const e of state.enemies) {
            if (e.hp <= 0) continue;
            const [ex, ey] = enemyXY(e);
            if ((ex - ab.x) * (ex - ab.x) + (ey - ab.y) * (ey - ab.y) < 46 * 46) { damageEnemy(e, dmg); spawnParticles(ex, ey, '#e64fd0', 4); }
          }
        }
        if (state.t % 180 !== 0) return;
        ab.burst = 24;
        const bd2 = Math.floor(dmg * 0.8);
        for (const e of state.enemies) {
          if (e.hp <= 0) continue;
          const [ex, ey] = enemyXY(e);
          if ((ex - ab.x) * (ex - ab.x) + (ey - ab.y) * (ey - ab.y) < 150 * 150) { damageEnemy(e, bd2); e.slowFrames = Math.max(e.slowFrames || 0, 50); }
        }
      },
      draw(ab) {
        ctx.save();
        if (ab.burst > 0) {
          const p = 1 - ab.burst / 24;
          ctx.globalCompositeOperation = 'lighter'; ctx.globalAlpha = (1 - p) * 0.6;
          ctx.strokeStyle = '#e64fd0'; ctx.lineWidth = 3;
          ctx.beginPath(); ctx.arc(ab.x, ab.y, p * 150, 0, Math.PI * 2); ctx.stroke();
          ctx.lineWidth = 1.2; ctx.globalAlpha = (1 - p) * 0.4;
          ctx.beginPath();
          for (let i = 0; i < 10; i++) { const a = (Math.PI * 2 / 10) * i; ctx.moveTo(ab.x, ab.y); ctx.lineTo(ab.x + Math.cos(a) * p * 150, ab.y + Math.sin(a) * p * 150); }
          ctx.stroke();
        }
        ctx.globalCompositeOperation = 'source-over';
        ctx.globalAlpha = 0.30; ctx.strokeStyle = '#f0a0e0'; ctx.lineWidth = 1;
        ctx.beginPath(); ctx.moveTo(CX, CY); ctx.lineTo(ab.x, ab.y); ctx.stroke();
        ctx.save(); ctx.translate(ab.x, ab.y); ctx.rotate(ab.ang + Math.PI / 2);
        ctx.globalAlpha = 0.95; ctx.fillStyle = '#3a2038'; ctx.strokeStyle = '#e64fd0'; ctx.lineWidth = 2;
        ctx.beginPath(); ctx.moveTo(0, -22); ctx.lineTo(15, 10); ctx.lineTo(0, 20); ctx.lineTo(-15, 10); ctx.closePath();
        ctx.fill(); ctx.stroke();
        ctx.fillStyle = '#ffd0f0';
        ctx.beginPath(); ctx.arc(-5, -8, 2.4, 0, Math.PI * 2); ctx.fill();
        ctx.beginPath(); ctx.arc(5, -8, 2.4, 0, Math.PI * 2); ctx.fill();
        ctx.restore();
        ctx.restore(); ctx.globalAlpha = 1;
      },
    },
```

- [ ] **Step 2: 문법 검증** — `SYNTAX OK`
- [ ] **Step 3: 브라우저 검증** — 콘솔 에러 0건
- [ ] **Step 4: 커밋**

```bash
git add index.html
git commit -m "feat: 라라 별돌파 2종 (stringWeb 4★ / grandGuignol 8★)

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 4: 갈라테아 별돌파 2종

**Files:** Modify `index.html` — `ABILITY_DEFS` 닫는 `  };` 앞

**Interfaces:**
- Produces: `stoneGarden`(4★), `gorgonRealm`(8★)
- 사용: `e.timeStopped = state.t + dur` (완전 정지). **보스는 정지 대신 강한 `slowFrames`** — 기존 갈라테아 킷 관례.

- [ ] **Step 1: 두 능력 삽입**

```js
    // 🗿 갈라테아 4★/8★ 별해금 — 석상 정원 / 고르곤의 영역
    stoneGarden: {
      name: '석상 정원', isGachaUnique: true, isStarUnlock: true, baseCost: 280, color: '#c8b890',
      desc: lv => `[4★히든-SR] 석상 ${3 + Math.floor(lv / 3)}기 배치 · 주변 적 석화 + 파쇄 DMG ${16 + lv * 8}`,
      init(ab) { ab.statues = []; ab.cd = 0; },
      tick(ab) {
        const n = 3 + Math.floor(ab.level / 3);
        if (ab.statues.length !== n) {
          ab.statues = [];
          for (let i = 0; i < n; i++) {
            const a = (Math.PI * 2 / n) * i;
            ab.statues.push({ x: CX + Math.cos(a) * 120, y: CY + Math.sin(a) * 120, fx: 0 });
          }
        }
        for (const s of ab.statues) if (s.fx > 0) s.fx--;
        if (--ab.cd > 0) return;
        ab.cd = Math.max(70, 130 - ab.level * 3);
        const dmg = 16 + ab.level * 8, R = 74 + ab.level * 3;
        for (const s of ab.statues) {
          let hit = false;
          for (const e of state.enemies) {
            if (e.hp <= 0) continue;
            const [ex, ey] = enemyXY(e);
            if ((ex - s.x) * (ex - s.x) + (ey - s.y) * (ey - s.y) > R * R) continue;
            hit = true;
            damageEnemy(e, dmg);
            if (e.isBoss) e.slowFrames = Math.max(e.slowFrames || 0, 70);
            else e.timeStopped = state.t + 48;
            spawnParticles(ex, ey, '#d8c8a0', 3);
          }
          if (hit) s.fx = 18;
        }
      },
      draw(ab) {
        ctx.save();
        for (const s of ab.statues) {
          const R = 74 + ab.level * 3;
          if (s.fx > 0) {
            const p = s.fx / 18;
            ctx.globalCompositeOperation = 'lighter'; ctx.globalAlpha = p * 0.35;
            ctx.strokeStyle = '#e8dcc0'; ctx.lineWidth = 2;
            ctx.beginPath(); ctx.arc(s.x, s.y, R * (1 - p) + 10, 0, Math.PI * 2); ctx.stroke();
            ctx.globalCompositeOperation = 'source-over';
          }
          ctx.globalAlpha = 0.12; ctx.strokeStyle = '#c8b890'; ctx.lineWidth = 1;
          ctx.beginPath(); ctx.arc(s.x, s.y, R, 0, Math.PI * 2); ctx.stroke();
          ctx.globalAlpha = 0.9; ctx.fillStyle = '#b8a880'; ctx.strokeStyle = '#e0d4b0'; ctx.lineWidth = 1.4;
          ctx.beginPath(); ctx.moveTo(s.x, s.y - 15); ctx.lineTo(s.x + 8, s.y - 2); ctx.lineTo(s.x + 6, s.y + 13);
          ctx.lineTo(s.x - 6, s.y + 13); ctx.lineTo(s.x - 8, s.y - 2); ctx.closePath();
          ctx.fill(); ctx.stroke();
        }
        ctx.restore(); ctx.globalAlpha = 1;
      },
    },
    gorgonRealm: {
      name: '고르곤의 영역', isGachaUnique: true, isStarUnlock: true, baseCost: 480, color: '#c8b060',
      desc: lv => `[8★히든-SR] 상시 석화 영역 · 3s마다 전체 석화 + 붕괴 DMG ${30 + lv * 15}`,
      init(ab) { ab.cd = 120; ab.wave = 0; ab.pulse = 0; },
      tick(ab) {
        ab.pulse += 0.03;
        if (ab.wave > 0) ab.wave--;
        for (const e of state.enemies) {
          if (e.hp <= 0) continue;
          e.slowFrames = Math.max(e.slowFrames || 0, 14);
        }
        if (--ab.cd > 0) return;
        ab.cd = Math.max(150, 220 - ab.level * 5);
        ab.wave = 30;
        const dmg = 30 + ab.level * 15;
        for (const e of state.enemies) {
          if (e.hp <= 0) continue;
          damageEnemy(e, dmg);
          if (e.isBoss) e.slowFrames = Math.max(e.slowFrames || 0, 90);
          else e.timeStopped = state.t + 60;
          const [ex, ey] = enemyXY(e);
          spawnParticles(ex, ey, '#c8b060', 3);
        }
        if (typeof shake === 'function') shake(12, 18);
      },
      draw(ab) {
        ctx.save();
        const amb = 0.045 + 0.02 * Math.sin(ab.pulse);
        const R = Math.min(W, H) * 0.52;
        const g = ctx.createRadialGradient(CX, CY, 0, CX, CY, R);
        g.addColorStop(0, `rgba(200,176,96,${amb})`); g.addColorStop(0.7, `rgba(160,140,90,${amb * 0.5})`); g.addColorStop(1, 'rgba(160,140,90,0)');
        ctx.fillStyle = g; ctx.beginPath(); ctx.arc(CX, CY, R, 0, Math.PI * 2); ctx.fill();
        if (ab.wave > 0) {
          const p = 1 - ab.wave / 30;
          ctx.globalCompositeOperation = 'lighter'; ctx.globalAlpha = (1 - p) * 0.55;
          ctx.strokeStyle = '#e8d8a0'; ctx.lineWidth = 4 * (1 - p) + 1;
          ctx.beginPath(); ctx.arc(CX, CY, p * R, 0, Math.PI * 2); ctx.stroke();
        }
        ctx.restore(); ctx.globalAlpha = 1;
      },
    },
```

- [ ] **Step 2: 문법 검증** — `SYNTAX OK`
- [ ] **Step 3: 브라우저 검증** — 콘솔 에러 0건
- [ ] **Step 4: 커밋**

```bash
git add index.html
git commit -m "feat: 갈라테아 별돌파 2종 (stoneGarden 4★ / gorgonRealm 8★)

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 5: 트리나 별돌파 2종 ⚠️ 환영 게이트

**Files:** Modify `index.html` — `ABILITY_DEFS` 닫는 `  };` 앞, **그리고 `TRINA_PHANTOM_IDS`(~L6757)**

**Interfaces:**
- Consumes: 모듈 스코프 `_phantomDmg` / `_phantomScale`
- Produces: `understudyCall`(4★), `finalBow`(8★)

**이 Task는 다른 Task와 다르다.** Global Constraints의 "트리나 전용 제약"을 먼저 읽어라. 모든 `damageEnemy` 호출이 `try`/`finally`로 감싸져야 하고, 두 신규 id를 `TRINA_PHANTOM_IDS`에 넣어야 한다.

- [ ] **Step 1: 두 능력 삽입**

```js
    // 🎭 트리나 4★/8★ 별해금 — 대역 소집 / 마지막 인사
    //    ⚠️ 환영 피해 = _phantomDmg 게이트 필수 (즉사·각인 미발동). finally 누락 시 전역 파손.
    understudyCall: {
      name: '대역 소집', isGachaUnique: true, isStarUnlock: true, baseCost: 280, color: '#e0489f',
      desc: lv => `[4★히든-SR] 환영 ${2 + Math.floor(lv / 3)}기 추가 · 피해 30% · 환영은 판정 미발동 · DMG ${28 + lv * 13}`,
      init(ab) { ab.cooldown = 0; ab.ph = []; },
      tick(ab) {
        const n = 2 + Math.floor(ab.level / 3);
        const CL = ['#00c8d7', '#e0489f', '#e8d24a'];
        if (ab.ph.length !== n) {
          ab.ph = [];
          for (let i = 0; i < n; i++) ab.ph.push({ a: (Math.PI * 2 / n) * i + 0.4, c: CL[i % 3] });
        }
        const R = ARENA_R * 0.5;
        for (const p of ab.ph) { p.a += 0.006; p.x = CX + Math.cos(p.a) * R; p.y = CY + Math.sin(p.a) * R; }
        if (--ab.cooldown > 0) return;
        ab.cooldown = Math.max(50, 96 - ab.level * 3);
        const pool = state.enemies.filter(e => e.hp > 0);
        if (!pool.length) { ab.cooldown = 20; return; }
        const dmg = 28 + ab.level * 13;
        _phantomDmg = true; _phantomScale = 0.30;
        try {
          for (let i = 0; i < ab.ph.length; i++) {
            const t = pool[Math.floor(Math.random() * pool.length)];
            damageEnemy(t, dmg);
          }
        } finally { _phantomDmg = false; _phantomScale = 1; }
      },
      draw(ab) {
        ctx.save();
        for (const p of ab.ph) {
          ctx.globalAlpha = 0.35; ctx.strokeStyle = p.c; ctx.lineWidth = 2;
          ctx.beginPath(); ctx.arc(p.x, p.y, 11, 0, Math.PI * 2); ctx.stroke();
          ctx.globalAlpha = 0.12; ctx.fillStyle = p.c;
          ctx.beginPath(); ctx.arc(p.x, p.y, 9, 0, Math.PI * 2); ctx.fill();
        }
        ctx.restore(); ctx.globalAlpha = 1;
      },
    },
    finalBow: {
      name: '마지막 인사', isGachaUnique: true, isStarUnlock: true, baseCost: 480, color: '#f0ece4',
      desc: lv => `[8★히든-SR] 5s마다 전 환영 일제 퇴장 폭발 · 환영은 판정 미발동 · 광역 DMG ${55 + lv * 25}`,
      init(ab) { ab.cooldown = 170; ab.fx = 0; ab.ph = []; ab.cols = ['#00c8d7', '#e0489f', '#e8d24a']; },
      tick(ab) {
        const CL = ab.cols;
        if (ab.ph.length !== 3) { ab.ph = []; for (let i = 0; i < 3; i++) ab.ph.push({ a: (Math.PI * 2 / 3) * i, c: CL[i] }); }
        const R = ARENA_R * 0.58;
        for (const p of ab.ph) { p.a += 0.009; p.x = CX + Math.cos(p.a) * R; p.y = CY + Math.sin(p.a) * R; }
        if (ab.fx > 0) ab.fx--;
        if (--ab.cooldown > 0) return;
        ab.cooldown = Math.max(240, 340 - ab.level * 6);
        ab.fx = 26;
        const dmg = 55 + ab.level * 25;
        _phantomDmg = true; _phantomScale = 0.30;
        try {
          for (const e of state.enemies) { if (e.hp > 0) damageEnemy(e, dmg); }
        } finally { _phantomDmg = false; _phantomScale = 1; }
        if (typeof shake === 'function') shake(12, 18);
      },
      draw(ab) {
        ctx.save();
        for (const p of ab.ph) {
          ctx.globalAlpha = ab.fx > 0 ? 0.6 : 0.35; ctx.strokeStyle = p.c; ctx.lineWidth = 2;
          ctx.beginPath(); ctx.arc(p.x, p.y, 13, 0, Math.PI * 2); ctx.stroke();
        }
        if (ab.fx > 0) {
          const p = 1 - ab.fx / 26;
          ctx.globalCompositeOperation = 'lighter';
          const cols = ab.cols || ['#00c8d7', '#e0489f', '#e8d24a'];
          for (let i = 0; i < 3; i++) {
            ctx.globalAlpha = (1 - p) * 0.4; ctx.strokeStyle = cols[i]; ctx.lineWidth = 3;
            ctx.beginPath(); ctx.arc(CX, CY, p * 260 + i * 6, 0, Math.PI * 2); ctx.stroke();
          }
        }
        ctx.restore(); ctx.globalAlpha = 1;
      },
    },
```

> 참고: 색 배열은 `init`에서 `ab.cols`에 저장해 `tick`/`draw`가 공유한다(리터럴 중복 방지).

- [ ] **Step 2: `TRINA_PHANTOM_IDS`에 두 id 추가**

`~L6757`의 선언을 찾아 확장:
```js
  const TRINA_PHANTOM_IDS = new Set(['phantomStage', 'chromaticSplit', 'encore', 'standingOvation', 'understudyCall', 'finalBow']);
```

- [ ] **Step 3: 문법 검증** — `SYNTAX OK`

- [ ] **Step 4: 게이트 균형 검증 (이 Task의 핵심)**

Run:
```bash
grep -c "_phantomDmg = true" index.html
grep -c "_phantomDmg = false" index.html
```
Expected: `= true`가 **6**(기존 4 + 신규 2), `= false`가 **7**(선언 1줄 포함).

그리고 **육안으로** 신규 2곳이 각각 `try` 안에 있고 `finally`가 두 플래그를 모두 되돌리는지 확인하라.

- [ ] **Step 5: 브라우저 검증** — 콘솔 에러 0건

- [ ] **Step 6: 커밋**

```bash
git add index.html
git commit -m "feat: 트리나 별돌파 2종 (understudyCall 4★ / finalBow 8★)

환영 피해이므로 _phantomDmg 게이트 + try/finally 적용,
TRINA_PHANTOM_IDS 에 두 id 추가(standingOvation 재생 제외).

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 6: 아이리스 별돌파 2종

**Files:** Modify `index.html` — `ABILITY_DEFS` 닫는 `  };` 앞

**Interfaces:**
- Produces: `flashbulb`(4★), `darkroomVault`(8★)
- 사용: `state._irisGhosts` (과노출이 만드는 흑백 잔상 배열). **없을 수도 있으므로 `|| []` 가드 필수.**

**밸런스 제약:** 아이리스는 **개체당 피해를 적 수로 곱하지 않는다.** 적 수는 "몇 체를 때리나"에만 쓴다.

- [ ] **Step 1: 두 능력 삽입**

```js
    // 📷 아이리스 4★/8★ 별해금 — 플래시 / 암실 금고
    flashbulb: {
      name: '플래시', isGachaUnique: true, isStarUnlock: true, baseCost: 280, color: '#c0392b',
      desc: lv => `[4★히든-SR] 3s마다 강렬한 섬광 · 광역 DMG ${25 + lv * 12} + 1.5s 눈부심 둔화`,
      init(ab) { ab.cd = 90; ab.fx = 0; },
      tick(ab) {
        if (ab.fx > 0) ab.fx--;
        if (--ab.cd > 0) return;
        ab.cd = Math.max(120, 200 - ab.level * 5);
        ab.fx = 14;
        const dmg = 25 + ab.level * 12, R = 190 + ab.level * 6;
        for (const e of state.enemies) {
          if (e.hp <= 0) continue;
          const [ex, ey] = enemyXY(e);
          if ((ex - CX) * (ex - CX) + (ey - CY) * (ey - CY) > R * R) continue;
          damageEnemy(e, dmg);
          e.slowFrames = Math.max(e.slowFrames || 0, 90);
        }
      },
      draw(ab) {
        if (ab.fx <= 0) return;
        const a = ab.fx / 14, R = 190 + ab.level * 6;
        ctx.save(); ctx.globalCompositeOperation = 'lighter';
        const g = ctx.createRadialGradient(CX, CY, 0, CX, CY, R);
        g.addColorStop(0, `rgba(255,255,255,${a * 0.5})`); g.addColorStop(0.6, `rgba(240,220,215,${a * 0.16})`); g.addColorStop(1, 'rgba(192,57,43,0)');
        ctx.fillStyle = g; ctx.beginPath(); ctx.arc(CX, CY, R, 0, Math.PI * 2); ctx.fill();
        ctx.globalAlpha = a * 0.8; ctx.strokeStyle = '#ffffff'; ctx.lineWidth = 2.5;
        ctx.beginPath(); ctx.arc(CX, CY, (1 - a) * R, 0, Math.PI * 2); ctx.stroke();
        ctx.restore(); ctx.globalAlpha = 1;
      },
    },
    darkroomVault: {
      name: '암실 금고', isGachaUnique: true, isStarUnlock: true, baseCost: 480, color: '#8a2a24',
      desc: lv => `[8★히든-SR] 0.5s마다 잔상 저장 · 4s마다 일괄 방출 · 저장량당 DMG ${20 + lv * 10}`,
      init(ab) { ab.cd = 150; ab.storeCd = 0; ab.vault = 0; ab.fx = 0; },
      tick(ab) {
        if (ab.fx > 0) ab.fx--;
        const cap = Math.min(20, 8 + ab.level);
        if (--ab.storeCd <= 0) {
          ab.storeCd = 30;
          const ghosts = (state._irisGhosts || []).length;
          const live = state.enemies.reduce((n, e) => n + (e.hp > 0 ? 1 : 0), 0);
          ab.vault = Math.min(cap, ab.vault + (ghosts > 0 ? 2 : (live > 0 ? 1 : 0)));
        }
        if (--ab.cd > 0) return;
        ab.cd = Math.max(200, 300 - ab.level * 6);
        if (ab.vault <= 0) { ab.cd = 60; return; }
        ab.fx = 22;
        const dmg = (20 + ab.level * 10) * ab.vault;
        for (const e of state.enemies) { if (e.hp > 0) damageEnemy(e, dmg); }
        ab.vault = 0;
        if (typeof shake === 'function') shake(10, 16);
      },
      draw(ab) {
        ctx.save();
        const cap = Math.min(20, 8 + ab.level);
        ctx.globalAlpha = 0.5; ctx.strokeStyle = '#8a2a24'; ctx.lineWidth = 2.4;
        ctx.beginPath(); ctx.arc(CX, CY, 30, -Math.PI / 2, -Math.PI / 2 + Math.PI * 2 * (ab.vault / cap)); ctx.stroke();
        if (ab.fx > 0) {
          const p = 1 - ab.fx / 22;
          ctx.globalCompositeOperation = 'lighter'; ctx.globalAlpha = (1 - p) * 0.45;
          ctx.fillStyle = '#1a1a1a';
          ctx.fillRect(0, 0, ctx.canvas.width, ctx.canvas.height);
          ctx.globalAlpha = (1 - p) * 0.7; ctx.strokeStyle = '#c0392b'; ctx.lineWidth = 3;
          ctx.beginPath(); ctx.arc(CX, CY, p * 300, 0, Math.PI * 2); ctx.stroke();
        }
        ctx.restore(); ctx.globalAlpha = 1;
      },
    },
```

- [ ] **Step 2: 문법 검증** — `SYNTAX OK`

- [ ] **Step 3: 밸런스 규칙 확인**

`darkroomVault`의 피해는 `(20 + lv*10) * ab.vault`다. `ab.vault`는 **적 수가 아니라 저장 카운터**이고 `cap`(최대 20)으로 제한된다. `flashbulb`는 개체당 고정 피해다. **적 수가 개체당 피해를 곱하는 곳이 없어야 한다** — 육안 확인.

- [ ] **Step 4: 브라우저 검증** — 콘솔 에러 0건

- [ ] **Step 5: 커밋**

```bash
git add index.html
git commit -m "feat: 아이리스 별돌파 2종 (flashbulb 4★ / darkroomVault 8★)

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 7: 레지스트리 배선 + 버전 bump

**Files:** Modify `index.html` (4곳), `sw.js` (1곳)

**Interfaces:**
- Consumes: Task 1~6의 12개 능력 id

- [ ] **Step 1: `CHAR_STAR_UNLOCKS`에 6줄 추가**

`~L18494`의 객체에서 `levina:` 줄 뒤, 닫는 `};` 앞에 삽입:

```js
    // 🆕 신규 SR 6명도 별돌파 부여 — 20명 전원 메인(t1)+서브(4★) 구조 통일
    amy:      { 4: ['droneSwarm'],      8: ['skyDominion'] },
    chloe:    { 4: ['acidRain'],        8: ['omniSolvent'] },
    lara:     { 4: ['stringWeb'],       8: ['grandGuignol'] },
    galatea:  { 4: ['stoneGarden'],     8: ['gorgonRealm'] },
    trina:    { 4: ['understudyCall'],  8: ['finalBow'] },
    iris:     { 4: ['flashbulb'],       8: ['darkroomVault'] },
```

- [ ] **Step 2: `ABILITY_ICON_ORDER`에 12개 추가**

배열의 닫는 `  ];` 앞에 삽입:

```js
    // 🆕 신규 SR 6명 별해금 (4★/8★)
    'droneSwarm', 'skyDominion',          // 에이미
    'acidRain', 'omniSolvent',            // 클로에
    'stringWeb', 'grandGuignol',          // 라라
    'stoneGarden', 'gorgonRealm',         // 갈라테아
    'understudyCall', 'finalBow',         // 트리나
    'flashbulb', 'darkroomVault',         // 아이리스
```

- [ ] **Step 3: `ABILITY_TAGS`에 12개 추가**

객체의 닫는 `  };` 앞에 삽입. **legal 태그만 사용**(TAG_COLORS에 있는 것):

```js
    // 🆕 신규 SR 6명 별해금
    droneSwarm:     ['자율', '다중공격', '유도'],
    skyDominion:    ['낙하', '광역', '폭발'],
    acidRain:       ['낙하', '영역', '슬로우'],
    omniSolvent:    ['영역', '광역', '슬로우'],
    stringWeb:      ['영역', '슬로우'],
    grandGuignol:   ['자율', '광역', '슬로우'],
    stoneGarden:    ['영역', '정지', '광역'],
    gorgonRealm:    ['광역', '정지', '영역'],
    understudyCall: ['다중공격', '단일'],
    finalBow:       ['광역', '폭발'],
    flashbulb:      ['광역', '슬로우'],
    darkroomVault:  ['광역', '폭발'],
```

- [ ] **Step 4: `TD_UNLIMITED_RANGE_IDS`에 전 맵 능력 추가**

Set의 닫는 `  ]);` 앞에 삽입. **전 맵 효과인 것만**(반경 제한이 있는 `droneSwarm`·`stringWeb`·`stoneGarden`·`flashbulb`·`understudyCall`은 **제외**):

```js
    'skyDominion', 'acidRain',                                             // 에이미·클로에 (전 맵 낙하)
    'omniSolvent', 'gorgonRealm',                                          // 클로에·갈라테아 (전체 상시)
    'grandGuignol', 'finalBow', 'darkroomVault',                           // 라라·트리나·아이리스 (전체)
```

- [ ] **Step 5: 버전 bump**

`index.html`: `const APP_VERSION = 674;` → `675`
`sw.js`: `const CACHE = 'dot-defense-v674';` → `'dot-defense-v675'`

- [ ] **Step 6: 문법 검증** — `SYNTAX OK`

- [ ] **Step 7: 배선 전수 확인**

Run:
```bash
for id in droneSwarm skyDominion acidRain omniSolvent stringWeb grandGuignol stoneGarden gorgonRealm understudyCall finalBow flashbulb darkroomVault; do
  echo "$id: $(grep -c "$id" index.html)"
done
grep -n "APP_VERSION = " index.html
grep -n "^const CACHE" sw.js
```
Expected: 12개 id 각각 **4건 이상**(ABILITY_DEFS 정의 + CHAR_STAR_UNLOCKS + ICON_ORDER + TAGS, 전 맵 능력은 +1). 버전은 양쪽 675.

- [ ] **Step 8: 브라우저 + 인게임 확인**

브라우저 콘솔 에러 0건. 그리고 치트로 별돌파 표시를 확인:
메뉴에서 `123123123` 입력 → 치트 패널 → "🔓 모든 가챠 캐릭터 해금" 클릭 → 캐릭터 화면에서 6명에게 4★/8★ 능력이 표시되는지 확인.
(rAF 정지로 캔버스가 안 그려질 수 있다. 그 경우 grep 검증으로 갈음하고 리포트에 명시하라.)

- [ ] **Step 9: 커밋**

```bash
git add index.html sw.js
git commit -m "feat: 신규 SR 6명 별돌파 배선 + v675

CHAR_STAR_UNLOCKS/아이콘순서/ABILITY_TAGS/전맵사거리 배선.
20명 전원이 메인(t1 시그니처)+서브(별돌파 4★) 구조로 통일 —
고유장비 시스템(단계 0-a)의 선행 조건 충족.

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## 실기기 확인 항목 (개발 환경에서 검증 불가)

프리뷰는 `rAF`가 정지해 캔버스가 그려지지 않는다. 아래는 실기기에서 본다.

1. **12종 능력의 실제 이펙트** — 특히 `grandGuignol`(거대 인형 추격), `gorgonRealm`(전체 석화), `darkroomVault`(금고 게이지).
2. **트리나 2종이 즉사·각인을 굴리지 않는지** — 유물 `executeBelow` 보유 상태로 확인. 이게 새면 밸런스 설계가 무의미해진다.
3. **`stoneGarden`/`gorgonRealm`의 `timeStopped`** — 보스에게 정지가 걸리지 않고 강한 슬로우만 걸리는지.
4. **프레임 부하** — `stringWeb`은 적×선분 이중 루프다. 후반 대규모 웨이브에서 모바일 프레임 확인.
5. **4★/8★ 해금 UI** — 6명이 실제로 별돌파 카드를 받는지.
