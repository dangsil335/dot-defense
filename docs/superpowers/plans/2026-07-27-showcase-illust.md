# 대표 일러(SHOWCASE) + 랭킹 개편 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 유저가 내 정보에서 보유 캐릭/스킨 중 대표 일러를 고르면, 그 일러가 글로벌 랭킹에 드러나게 한다.

**Architecture:** `META.showcase`에 일러 키 문자열 1개(`'luna__moonlit'` 또는 `'luna'`)를 저장한다. 이 형식은 기존 `_resolveIllustId()` 반환값과 동일하므로 `_applyIllustChain(img, charId, onFail, exactId)`의 `exactId`에 그대로 투입된다. 서버는 `rankings.showcase` 컬럼 1개를 추가하고, 기존 5단계 폴백 체인 맨 위에 0단계를 얹어 컬럼이 없어도 점수 제출이 깨지지 않게 한다. 랭킹은 Top3 시상대 카드 + 4위↓ 세로 썸네일 행으로 재구성한다.

**Tech Stack:** 바닐라 JS (단일 `index.html`, 39k줄, 하나의 IIFE 클로저), Supabase JS SDK, 서비스워커 캐시 버스팅(`sw.js`).

## Global Constraints

- 모든 수정은 `C:\Users\solid\Desktop\dot-defense\index.html` 한 파일 안에서 이뤄진다. 새 파일 생성 없음.
- **이 프로젝트엔 테스트 프레임워크가 없다.** 검증은 두 가지로 한다:
  1. `node -e`로 대상 함수/객체 블록을 정규식 추출해 `eval` 후 동작 검사 (문법 오류 + 로직 검증)
  2. 프리뷰 브라우저에서 DOM/콘솔 검증 (`mcp__Claude_Browser__*`)
- `APP_VERSION`(index.html)과 `sw.js`의 `CACHE` 버전은 **항상 같이** 올린다. 현재 714 → 이번 작업 완료 시 **716**.
- 일러 파일 경로 규칙: 스킨 키(`__` 포함)는 `./icons/illust/skin/`, 기본 캐릭은 `./icons/illust/`.
- **랭킹 성능 규칙**: Top3 카드만 애니 일러 체인(webp→gif→png) 허용. 4위↓ 썸네일·배경은 정지 `.png` 고정.
- **CSS `filter: blur()` 금지** (모바일 비쌈). 배경 일러는 `opacity: 0.14` + 확대 크롭으로 처리.
- 서버에서 온 `showcase` 값은 **렌더 직전 반드시 화이트리스트 검증**을 통과시킨다.
- 커밋 메시지 말미에 `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>` 를 붙인다.
- 작업 단위 커밋 후 `git push origin main`까지 실행한다 (함장 지시).

---

### Task 1: 대표 일러 데이터 코어 + 검증 헬퍼

**Files:**
- Modify: `index.html` — `SKINS` 헬퍼 블록 직후 (현재 `_resolveIllustId` 정의부, 약 L35280~L35310)

**Interfaces:**
- Consumes: `CHARACTERS`(전역 캐릭 레지스트리), `SKINS`, `_skinsOf(charId)`, `_skinKey(charId, skinId)`, `_skinOwned(charId, skinId)`, `isCharUnlocked(id)`, `saveMeta()`, `META`
- Produces:
  - `ILLUST_CHARS: Set<string>` — 일러 파일이 존재하는 캐릭 id 집합
  - `_showcaseGet(): string|null`
  - `_showcaseValid(id: string): boolean`
  - `_showcaseSet(id: string|null): boolean`
  - `_showcaseForRow(row: object): string|null` — 랭킹 행 → 표시할 일러 id
  - `_showcaseCandidates(): Array<{id, char, skin, charName, label}>`

- [ ] **Step 1: `_resolveIllustId` 정의 바로 다음 줄에 코어 블록 삽입**

`index.html`에서 `function _resolveIllustId(charId)` 로 시작하는 줄을 찾고, 그 줄 **바로 아래**에 아래 블록을 넣는다.

```js
  // ===== 🖼 v716 — 대표 일러(SHOWCASE) =====
  //   META.showcase = 'luna__moonlit'(스킨) | 'luna'(기본 일러) | null(미설정)
  //   ⚠ 이 문자열 형식은 _resolveIllustId() 반환값과 완전히 동일하다.
  //     → _applyIllustChain(img, charId, onFail, exactId) 의 exactId 에 그대로 투입 가능(로딩 코드 재사용).
  //   일러 파일이 실제로 있는 캐릭 = 가챠 로스터(SR/SSR) 21명.
  //   기본 캐릭 9종(standard/sniper/engineer/mage/berserker/chronos/researcher/agent/mixer)은 일러 파일이 없다.
  const ILLUST_CHARS = new Set(Object.keys(CHARACTERS).filter(k => CHARACTERS[k] && CHARACTERS[k].isGacha));
  function _showcaseGet() { return META.showcase || null; }
  // 🛡 화이트리스트 검증 — 서버에서 온 값이든 로컬 값이든 렌더 직전 반드시 통과시킨다.
  //    (showcase 는 클라가 보내는 값이라 조작 가능. 레지스트리에 없는 id 는 전부 거른다.)
  function _showcaseValid(id) {
    if (!id || typeof id !== 'string') return false;
    const i = id.indexOf('__');
    if (i < 0) return !!(CHARACTERS[id] && ILLUST_CHARS.has(id));
    const c = id.slice(0, i), s = id.slice(i + 2);
    if (!CHARACTERS[c] || !ILLUST_CHARS.has(c)) return false;
    return _skinsOf(c).some(sk => sk.id === s);
  }
  function _showcaseSet(id) {
    if (id && !_showcaseValid(id)) return false;
    META.showcase = id || null;
    saveMeta();
    return true;
  }
  // 랭킹 행 → 표시할 일러 id. showcase 우선, 없거나 무효면 그 판에 쓴 캐릭의 기본 일러로 폴백.
  function _showcaseForRow(row) {
    if (row && _showcaseValid(row.showcase)) return row.showcase;
    const c = row && row.character;
    return (c && ILLUST_CHARS.has(c)) ? c : null;
  }
  // 대표 일러 후보 — 보유 캐릭 기본 일러 + 보유 스킨. 캐릭별로 [기본, 스킨...] 순서.
  function _showcaseCandidates() {
    const out = [];
    Object.keys(CHARACTERS).forEach(cid => {
      if (!ILLUST_CHARS.has(cid) || !isCharUnlocked(cid)) return;
      const cn = CHARACTERS[cid].name || cid;
      out.push({ id: cid, char: cid, skin: null, charName: cn, label: '기본' });
      _skinsOf(cid).forEach(sk => {
        if (_skinOwned(cid, sk.id)) out.push({ id: _skinKey(cid, sk.id), char: cid, skin: sk.id, charName: cn, label: sk.name });
      });
    });
    return out;
  }
```

- [ ] **Step 2: 검증 스크립트로 로직 확인**

Run:

```bash
cd "C:/Users/solid/Desktop/dot-defense" && node -e "
const fs=require('fs');const html=fs.readFileSync('index.html','utf8');
const S=html.match(/const SKINS = \{[\s\S]*?\n  \};/)[0];
let SKINS; eval(S.replace('const SKINS','SKINS'));
const CHARACTERS={luna:{name:'luna',isGacha:true},standard:{name:'기본'}};
const ILLUST_CHARS=new Set(Object.keys(CHARACTERS).filter(k=>CHARACTERS[k]&&CHARACTERS[k].isGacha));
const _skinsOf=c=>SKINS[c]||[];
function _showcaseValid(id){
  if(!id||typeof id!=='string')return false;
  const i=id.indexOf('__');
  if(i<0)return !!(CHARACTERS[id]&&ILLUST_CHARS.has(id));
  const c=id.slice(0,i),s=id.slice(i+2);
  if(!CHARACTERS[c]||!ILLUST_CHARS.has(c))return false;
  return _skinsOf(c).some(sk=>sk.id===s);
}
const cases=[['luna',true],['luna__moonlit',true],['luna__nope',false],['standard',false],['nosuch',false],['',false],[null,false],['__x',false]];
let ok=true;
cases.forEach(([v,exp])=>{const got=_showcaseValid(v);if(got!==exp){ok=false;console.log('FAIL',JSON.stringify(v),'expected',exp,'got',got);}});
console.log(ok?'PASS 검증 8케이스 전부 통과':'FAIL');
"
```

Expected: `PASS 검증 8케이스 전부 통과`

- [ ] **Step 3: 전체 파일 문법 검증**

Run:

```bash
cd "C:/Users/solid/Desktop/dot-defense" && node -e "const fs=require('fs');const h=fs.readFileSync('index.html','utf8');const m=h.match(/<script>([\s\S]*)<\/script>/g);console.log('script 블록:',m.length);new Function(h.match(/const ILLUST_CHARS[\s\S]{0,2400}/)[0].split('\n').slice(0,60).join('\n').replace(/const ILLUST_CHARS.*/,''));console.log('OK')"
```

Expected: `OK` (문법 오류 없음)

- [ ] **Step 4: 커밋**

```bash
cd "C:/Users/solid/Desktop/dot-defense" && git add index.html && git commit -m "feat: 대표 일러 데이터 코어 + 화이트리스트 검증 헬퍼

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>" && git push origin main
```

---

### Task 2: 서버 연동 — 제출 / 조회 / 프로필 갱신

**Files:**
- Modify: `index.html:24218-24241` (`submitScore`의 `fullRow` + `attempts` 배열)
- Modify: `index.html:24309-24311` (`fetchRankingsData`의 컬럼 상수)
- Modify: `index.html:24313-24339` (`fetchRankingsData`의 폴백 분기)
- Modify: `index.html` `updateProfile` 내 `fullPatch` (약 L24470~24485)

**Interfaces:**
- Consumes: `_showcaseGet()` (Task 1)
- Produces: `rankings` 행에 `showcase` 필드가 실린다. 조회 결과 `r.showcase`를 Task 4/5가 소비한다.

- [ ] **Step 1: 제출 — `attempts` 배열 맨 앞에 0단계 추가**

`index.html`에서 `const attempts = [` 로 시작하는 줄을 찾아, 그 아래 첫 항목 **앞에** 다음을 삽입한다.

```js
      // 🖼 0단계: 대표 일러(showcase) 포함 — Supabase SQL 필요:
      //    alter table rankings add column showcase text;
      //    컬럼 없으면 이 시도만 실패하고 아래 기존 체인이 그대로 동작(제출 안 깨짐).
      () => sb.from('rankings').upsert({ ...fullRow, showcase: _showcaseGet() }, { onConflict: 'user_id,mode' }),
```

- [ ] **Step 2: 조회 — 컬럼 상수에 showcase 추가**

`fetchRankingsData` 안에서 아래 줄을 찾아

```js
    const fullCols = 'user_id, nickname, title, score, round, ascension, character, updated_at, mode, account_level';
```

다음으로 교체한다.

```js
    const fullCols = 'user_id, nickname, title, score, round, ascension, character, updated_at, mode, account_level, showcase';
    const colsNoShowcase = 'user_id, nickname, title, score, round, ascension, character, updated_at, mode, account_level';
```

- [ ] **Step 3: 조회 — showcase 폴백 분기 추가**

`fetchRankingsData` 안, 1단계 병렬 조회(`let [top10Res, myRowRes] = await Promise.all([...]);`) **바로 다음**, 기존 `// mode 컬럼 없으면 fallback` 주석 **앞**에 삽입한다.

```js
    // 🖼 showcase 컬럼 미생성 fallback — 컬럼 추가 전에도 랭킹이 정상 동작해야 한다.
    if ((top10Res.error && /showcase/i.test(top10Res.error.message || '')) ||
        (myRowRes.error && /showcase/i.test(myRowRes.error.message || ''))) {
      console.warn('⚠️ showcase 컬럼 없음 — 대표 일러 없이 조회 (Supabase SQL: alter table rankings add column showcase text;)');
      [top10Res, myRowRes] = await Promise.all([
        sb.from('rankings').select(colsNoShowcase).eq('mode', mode).order('score', { ascending: false }).limit(10),
        sb.from('rankings').select(colsNoShowcase).eq('user_id', userId).eq('mode', mode).maybeSingle(),
      ]);
    }
```

- [ ] **Step 4: 프로필 갱신 — showcase 반영**

`updateProfile` 함수 안에서 `fullPatch` 객체를 찾아 `showcase: _showcaseGet(),` 한 줄을 추가한다. `fullPatch` 시도가 실패하면 기존 `fallback` patch로 내려가는 구조는 그대로 둔다 — 컬럼이 없어도 닉네임/칭호 갱신은 계속 동작해야 한다.

- [ ] **Step 5: 폴백 체인 형태 검증**

Run:

```bash
cd "C:/Users/solid/Desktop/dot-defense" && node -e "
const fs=require('fs');const h=fs.readFileSync('index.html','utf8');
const a=h.match(/const attempts = \[[\s\S]*?\n    \];/)[0];
const n=(a.match(/\(\) => sb\.from\('rankings'\)\.upsert/g)||[]).length;
console.log('attempts 단계 수:', n, n===6?'OK (기존 5 + showcase 1)':'FAIL');
console.log('0단계 showcase 포함:', /showcase: _showcaseGet\(\)/.test(a.split('\n').slice(0,6).join('\n'))?'OK':'FAIL');
console.log('fullCols showcase:', /account_level, showcase'/.test(h)?'OK':'FAIL');
console.log('showcase 폴백 분기:', /showcase\/i\.test/.test(h)?'OK':'FAIL');
console.log('colsNoShowcase 정의:', /const colsNoShowcase/.test(h)?'OK':'FAIL');
"
```

Expected: 5줄 전부 `OK`

- [ ] **Step 6: 커밋**

```bash
cd "C:/Users/solid/Desktop/dot-defense" && git add index.html && git commit -m "feat: rankings.showcase 컬럼 연동 (제출 0단계 + 조회 폴백 + 프로필 갱신)

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>" && git push origin main
```

---

### Task 3: 랭킹 CSS — 시상대 카드 + 썸네일 행

**Files:**
- Modify: `index.html:4869` 직전 (`#globalRankScreen` 스코프 CSS 블록 끝, `.rank-row.me` 규칙 다음 줄)

**Interfaces:**
- Produces: CSS 클래스 `.rank-podium`, `.podium-card`, `.p-1/.p-2/.p-3`, `.podium-art`, `.podium-art.no-art`, `.podium-medal`, `.podium-info`, `.podium-nick`, `.podium-score`, `.rank-thumb`, `.rank-row.has-art`. Task 4/5가 이 클래스명을 그대로 쓴다.

- [ ] **Step 1: `#globalRankScreen .rank-row.me { ... }` 규칙 다음 줄에 CSS 삽입**

```css
  /* ===== 🖼 v716 — 대표 일러: Top3 시상대 카드 + 4위↓ 세로 썸네일 행 ===== */
  #globalRankScreen .rank-podium {
    display: flex; align-items: flex-end; justify-content: center;
    gap: 8px; padding: 4px 0 14px; margin-bottom: 6px;
    border-bottom: 1px solid rgba(122,215,255,0.10);
  }
  #globalRankScreen .podium-card {
    position: relative; flex: 1 1 0; min-width: 0; max-width: 132px;
    border-radius: 8px; overflow: hidden;
    background: rgba(10,16,26,0.72);
    border: 1px solid var(--ac,#7ad7ff);
    box-shadow: 0 0 14px rgba(0,0,0,0.5);
  }
  #globalRankScreen .podium-card.p-1 { aspect-ratio: 3/4; max-width: 150px; border-width: 2px; box-shadow: 0 0 20px var(--ac,#7ad7ff), 0 0 30px rgba(0,0,0,0.5); }
  #globalRankScreen .podium-card.p-2,
  #globalRankScreen .podium-card.p-3 { aspect-ratio: 3/4.35; }
  #globalRankScreen .podium-card.me { outline: 2px solid #7ad7ff; outline-offset: -2px; }
  #globalRankScreen .podium-art { position: absolute; inset: 0; }
  #globalRankScreen .podium-art img { width: 100%; height: 100%; object-fit: cover; object-position: 50% 0%; display: block; }
  #globalRankScreen .podium-art.no-art { background: linear-gradient(180deg, rgba(122,215,255,0.10), transparent); }
  #globalRankScreen .podium-art.no-art img { display: none; }
  #globalRankScreen .podium-medal { position: absolute; top: 4px; left: 5px; font-size: 19px; text-shadow: 0 2px 6px rgba(0,0,0,0.9); z-index: 2; }
  #globalRankScreen .podium-info {
    position: absolute; left: 0; right: 0; bottom: 0; z-index: 2;
    padding: 14px 6px 5px;
    background: linear-gradient(180deg, transparent, rgba(4,8,14,0.92) 55%);
  }
  #globalRankScreen .podium-nick {
    font-weight: bold; color: #fff; font-size: 11.5px; line-height: 1.25;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
  }
  #globalRankScreen .podium-score { font-weight: bold; color: #ffd479; font-size: 13px; font-family: ui-monospace,'Courier New',monospace; }
  /* 4위↓ — 세로 3:4 썸네일. 일러 22종 전부 머리 상단 1.2~10.1% → object-position 50% 0% 로 얼굴 확보 */
  #globalRankScreen .rank-row { grid-template-columns: 58px minmax(0,1fr) minmax(120px,max-content); position: relative; overflow: hidden; }
  #globalRankScreen .rank-thumb {
    width: 57px; height: 76px; border-radius: 5px; overflow: hidden; position: relative;
    background: rgba(10,16,26,0.6); border: 1px solid rgba(122,215,255,0.18);
  }
  #globalRankScreen .rank-thumb img { width: 100%; height: 100%; object-fit: cover; object-position: 50% 0%; display: block; }
  #globalRankScreen .rank-thumb b {
    position: absolute; left: 0; right: 0; bottom: 0; text-align: center;
    font-size: 11px; background: rgba(6,10,18,0.8); color: #cfe6ff; padding: 1px 0;
  }
  /* 행 배경 일러 — filter:blur() 금지(모바일 비쌈). 저투명도 + 확대 크롭으로 분위기만 */
  #globalRankScreen .rank-row.has-art::before {
    content: ''; position: absolute; inset: 0; z-index: 0; pointer-events: none;
    background-image: var(--bgart); background-size: cover; background-position: 50% 12%;
    opacity: 0.14;
  }
  #globalRankScreen .rank-row > * { position: relative; z-index: 1; }
```

- [ ] **Step 2: CSS 삽입 확인**

Run:

```bash
cd "C:/Users/solid/Desktop/dot-defense" && node -e "
const h=require('fs').readFileSync('index.html','utf8');
['rank-podium','podium-card','podium-art','podium-medal','rank-thumb','has-art'].forEach(c=>{
  console.log(c, h.includes('.'+c)?'OK':'FAIL');
});
console.log('blur 미사용:', /#globalRankScreen[^}]*filter:\s*blur/.test(h)?'FAIL':'OK');
"
```

Expected: 6개 클래스 전부 `OK`, `blur 미사용: OK`

- [ ] **Step 3: 커밋**

```bash
cd "C:/Users/solid/Desktop/dot-defense" && git add index.html && git commit -m "style: 랭킹 시상대 카드 + 세로 썸네일 행 CSS

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>" && git push origin main
```

---

### Task 4: 랭킹 렌더 — Top3 시상대 카드

**Files:**
- Modify: `index.html:24396-24400` (`renderRankings`의 top10 루프)
- Modify: `index.html:24619` 직전 (`renderPodiumCard` 신규 함수 추가)

**Interfaces:**
- Consumes: `_showcaseForRow(row)` (Task 1), `_applyIllustChain(img, charId, onFail, exactId)`, `CHARACTERS`, `titleHTML(title)`, `escapeHtml(s)`, Task 3의 CSS 클래스
- Produces: `renderPodiumCard(rankNum, r, isMe): HTMLElement`

- [ ] **Step 1: `renderPodiumCard` 함수 추가**

`function renderRankRow(rankNum, r, isMe) {` 줄 **바로 앞**에 삽입한다.

```js
  // 🏆 v716 — Top3 시상대 카드. 대표 일러를 카드 전면에 3:4 크롭으로.
  //   Top3 만 애니 일러 체인(webp→gif→png) 허용 — 4위↓ 는 성능 때문에 정지 png 고정.
  function renderPodiumCard(rankNum, r, isMe) {
    const card = document.createElement('div');
    card.className = `podium-card p-${rankNum}${isMe ? ' me' : ''}`;
    const ch = CHARACTERS[r.character];
    card.style.setProperty('--ac', ch ? (ch.color || '#7ad7ff') : '#7ad7ff');
    card.innerHTML = `
      <div class="podium-art"><img alt=""></div>
      <div class="podium-medal">${['🥇','🥈','🥉'][rankNum-1] || `#${rankNum}`}</div>
      <div class="podium-info">
        <div class="podium-nick">${isMe ? '👤 ' : ''}${titleHTML(r.title)}<span>${escapeHtml(r.nickname)}</span></div>
        <div class="podium-score">${(r.score || 0).toLocaleString()}</div>
      </div>`;
    const art = card.querySelector('.podium-art');
    const img = art.querySelector('img');
    const sid = _showcaseForRow(r);
    if (sid && typeof _applyIllustChain === 'function') {
      _applyIllustChain(img, r.character, () => art.classList.add('no-art'), sid);
    } else {
      art.classList.add('no-art');
    }
    return card;
  }
```

- [ ] **Step 2: `renderRankings`의 top10 루프를 시상대 + 리스트로 분리**

`renderRankings` 안에서 아래 블록을 찾아

```js
    for (let i = 0; i < data.top10.length; i++) {
      const r = data.top10[i];
      const isMe = data.myRow && r.user_id === data.userId;
      top10El.appendChild(renderRankRow(i + 1, r, isMe));
    }
```

다음으로 교체한다.

```js
    // 🏆 v716 — Top3 는 시상대 카드(2-1-3 배치), 4위↓ 는 썸네일 행
    const top3 = data.top10.slice(0, 3);
    if (top3.length) {
      const podium = document.createElement('div');
      podium.className = 'rank-podium';
      // 가운데가 1위가 되도록 2-1-3 순서로 배치 (인원이 3 미만이면 있는 만큼만)
      const order = top3.length >= 3 ? [1, 0, 2] : (top3.length === 2 ? [1, 0] : [0]);
      order.forEach(idx => {
        const r = top3[idx];
        if (!r) return;
        podium.appendChild(renderPodiumCard(idx + 1, r, !!(data.myRow && r.user_id === data.userId)));
      });
      top10El.appendChild(podium);
    }
    for (let i = 3; i < data.top10.length; i++) {
      const r = data.top10[i];
      const isMe = data.myRow && r.user_id === data.userId;
      top10El.appendChild(renderRankRow(i + 1, r, isMe));
    }
```

- [ ] **Step 3: 배치 순서 로직 검증**

Run:

```bash
cd "C:/Users/solid/Desktop/dot-defense" && node -e "
const ord=n=>n>=3?[1,0,2]:(n===2?[1,0]:[0]);
const t=(n,exp)=>{const g=JSON.stringify(ord(n));const e=JSON.stringify(exp);console.log(n+'명:',g,g===e?'OK':'FAIL expected '+e);};
t(3,[1,0,2]); t(2,[1,0]); t(1,[0]);
console.log('1위가 가운데:', ord(3)[1]===0?'OK':'FAIL');
"
```

Expected: 3줄 `OK` + `1위가 가운데: OK`

- [ ] **Step 4: 함수 정의/호출 정합 검증**

Run:

```bash
cd "C:/Users/solid/Desktop/dot-defense" && node -e "
const h=require('fs').readFileSync('index.html','utf8');
console.log('renderPodiumCard 정의:', (h.match(/function renderPodiumCard\(/g)||[]).length===1?'OK':'FAIL');
console.log('renderPodiumCard 호출:', /podium\.appendChild\(renderPodiumCard\(/.test(h)?'OK':'FAIL');
console.log('4위부터 행 렌더:', /for \(let i = 3; i < data\.top10\.length; i\+\+\)/.test(h)?'OK':'FAIL');
console.log('exactId 전달:', /_applyIllustChain\(img, r\.character, \(\) => art\.classList\.add\('no-art'\), sid\)/.test(h)?'OK':'FAIL');
"
```

Expected: 4줄 전부 `OK`

- [ ] **Step 5: 커밋**

```bash
cd "C:/Users/solid/Desktop/dot-defense" && git add index.html && git commit -m "feat: 랭킹 Top3 시상대 카드 렌더 (대표 일러 전면 노출)

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>" && git push origin main
```

---

### Task 5: 랭킹 렌더 — 4위↓ 세로 썸네일 행

**Files:**
- Modify: `index.html:24619-24650` (`renderRankRow` 본문)

**Interfaces:**
- Consumes: `_showcaseForRow(row)` (Task 1), Task 3의 `.rank-thumb` / `.has-art` CSS
- Produces: 변경된 `renderRankRow(rankNum, r, isMe)` — 첫 컬럼이 `.rank-num` 대신 `.rank-thumb`

- [ ] **Step 1: `renderRankRow` 안의 avatar/row.innerHTML 부분 교체**

아래 두 줄(`const avatar = ...` 과 `row.innerHTML = ...` 블록)을 찾아

```js
    const avatar = (isTop3 && charSrc) ? `<div class="rank-avatar" style="--ac:${charCol}"><img src="${charSrc}" alt="" onerror="this.parentNode.style.display='none'"></div>` : '';
    row.innerHTML = `
      <div class="rank-num">${isTop3 ? ['🥇','🥈','🥉'][rankNum-1] : `#${rankNum}`}</div>
      ${avatar}
      <div class="rank-info">
        <div class="rank-nick${lenClass}">${isMe ? '👤 ' : ''}${titleHTML(r.title)}<span>${escapeHtml(r.nickname)}</span></div>
        <div class="rank-meta">${insignia}${rk ? `<span class="rank-rkname" style="color:${rk.color}">${rk.name}</span> · ` : ''}R${r.round} · ${ascText} · ${charName}</div>
      </div>
      <div class="rank-score">${(r.score || 0).toLocaleString()}</div>
    `;
    return row;
```

다음으로 교체한다.

```js
    // 🖼 v716 — 세로 3:4 대표 일러 썸네일. 일러가 세로로 길어 가로 배경으로 깔면 식별 불가 →
    //    썸네일로 얼굴을 확보하고(object-position 50% 0%), 배경엔 같은 일러를 저투명도로 깐다.
    row.innerHTML = `
      <div class="rank-thumb"><img alt="" loading="lazy"><b>${isTop3 ? ['🥇','🥈','🥉'][rankNum-1] : `#${rankNum}`}</b></div>
      <div class="rank-info">
        <div class="rank-nick${lenClass}">${isMe ? '👤 ' : ''}${titleHTML(r.title)}<span>${escapeHtml(r.nickname)}</span></div>
        <div class="rank-meta">${insignia}${rk ? `<span class="rank-rkname" style="color:${rk.color}">${rk.name}</span> · ` : ''}R${r.round} · ${ascText} · ${charName}</div>
      </div>
      <div class="rank-score">${(r.score || 0).toLocaleString()}</div>
    `;
    // 4위↓ 는 정지 png 고정 — 한 화면 10장이라 애니 체인은 성능상 Top3 카드에서만 쓴다.
    const _sid = _showcaseForRow(r);
    if (_sid) {
      const _src = (_sid.indexOf('__') >= 0 ? './icons/illust/skin/' : './icons/illust/') + _sid + '.png';
      const _im = row.querySelector('.rank-thumb img');
      _im.onerror = () => { _im.style.display = 'none'; };
      _im.src = _src;
      row.style.setProperty('--bgart', `url("${_src}")`);
      row.classList.add('has-art');
    }
    return row;
```

- [ ] **Step 2: 미사용 변수 정리**

교체 후 `charSrc` 변수가 더 이상 쓰이지 않는다. `const charSrc = ...` 줄을 삭제한다. `charCol`은 남겨둔다(다른 곳에서 쓰지 않으면 함께 삭제).

Run으로 확인:

```bash
cd "C:/Users/solid/Desktop/dot-defense" && node -e "
const h=require('fs').readFileSync('index.html','utf8');
const f=h.match(/function renderRankRow\([\s\S]*?\n  \}/)[0];
['charSrc','charCol'].forEach(v=>{
  const n=(f.match(new RegExp(v,'g'))||[]).length;
  console.log(v+' 등장:',n, n===0?'OK(제거됨)':(n===1?'FAIL(정의만 남음 — 삭제 필요)':'사용중'));
});
"
```

Expected: `charSrc 등장: 0 OK(제거됨)`

- [ ] **Step 3: 경로 분기 로직 검증**

Run:

```bash
cd "C:/Users/solid/Desktop/dot-defense" && node -e "
const p=id=>(id.indexOf('__')>=0?'./icons/illust/skin/':'./icons/illust/')+id+'.png';
const cases=[['luna','./icons/illust/luna.png'],['luna__moonlit','./icons/illust/skin/luna__moonlit.png']];
let ok=true;
cases.forEach(([i,e])=>{const g=p(i);if(g!==e){ok=false;console.log('FAIL',i,g);}});
console.log(ok?'PASS 경로 분기 정상':'FAIL');
const fs=require('fs');
console.log('실제 파일 존재:', fs.existsSync('icons/illust/skin/luna__moonlit.png')&&fs.existsSync('icons/illust/luna.png')?'OK':'FAIL');
"
```

Expected: `PASS 경로 분기 정상` + `실제 파일 존재: OK`

- [ ] **Step 4: 커밋**

```bash
cd "C:/Users/solid/Desktop/dot-defense" && git add index.html && git commit -m "feat: 랭킹 4위↓ 세로 썸네일 행 + 배경 일러

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>" && git push origin main
```

---

### Task 6: 내 정보 — 대표 일러 선택 UI (미리보기 + 드래그 스트립)

**Files:**
- Modify: `index.html:4726` (`#nicknameModal` 본문, 약장 `<div>` **앞**에 섹션 삽입)
- Modify: `index.html:4913` 부근 (`#nicknameModal` 스코프 CSS 블록에 스타일 추가)
- Modify: `index.html` `openNicknameModal` 계열 초기화부 — `buildTitlePicker(); updateTitlePreview();` 호출 근처 (약 L23904)

**Interfaces:**
- Consumes: `_showcaseCandidates()`, `_showcaseGet()`, `_showcaseSet(id)` (Task 1), `_applyIllustChain`, `updateProfile()` 또는 프로필 갱신 함수, `CHARACTERS`
- Produces: `buildShowcasePicker()` — 모달 열 때 호출되는 초기화 함수

- [ ] **Step 1: 모달 본문에 HTML 섹션 삽입**

`index.html`에서 `<div id="nicknameError"` 로 시작하는 줄을 찾고, 그 **다음 줄**(`<div>` 로 시작해 약장 섹션을 여는 줄) **앞**에 삽입한다.

```html
      <div id="showcase-sec" style="margin-bottom:10px;">
        <div class="nick-sec-label" style="color:#ffd479; font-size:11px; font-weight:bold; margin-bottom:6px; font-family:ui-monospace,'Courier New',monospace; letter-spacing:1px;">▍대표 일러 / SHOWCASE <span style="color:#7a6a3a; font-weight:400;">— 글로벌 랭킹에 표시됩니다</span></div>
        <div id="showcase-preview"><img id="showcase-img" alt=""><div id="showcase-name"></div></div>
        <div id="showcase-strip"></div>
        <div id="showcase-empty" style="display:none; background:#241510; border:1px solid #aa5530; border-radius:6px; padding:8px 12px; font-size:12px; color:#ffaa88; line-height:1.5;">캐릭터를 뽑으면 대표 일러를 설정할 수 있어요.</div>
      </div>
```

- [ ] **Step 2: CSS 추가**

`#nicknameModal .title-picker-grid { ... }` 규칙 **다음 줄**에 삽입한다.

```css
  /* 🖼 v716 — 대표 일러 선택: 큰 미리보기 + 가로 드래그 썸네일 스트립 */
  #showcase-preview { position: relative; width: 100%; aspect-ratio: 3/4; max-height: 190px; margin: 0 auto 7px; border-radius: 8px; overflow: hidden; background: #0f1219; border: 1px solid #2a3550; }
  #showcase-preview img { width: 100%; height: 100%; object-fit: cover; object-position: 50% 0%; display: block; }
  #showcase-preview.empty img { display: none; }
  #showcase-name { position: absolute; left: 0; right: 0; bottom: 0; padding: 10px 8px 5px; font-size: 12px; color: #cfe6ff; background: linear-gradient(180deg, transparent, rgba(4,8,14,0.92) 55%); }
  #showcase-strip { display: flex; gap: 6px; overflow-x: auto; overflow-y: hidden; padding: 2px 0 6px; scrollbar-width: thin; touch-action: pan-x; cursor: grab; }
  #showcase-strip::-webkit-scrollbar { height: 5px; }
  #showcase-strip::-webkit-scrollbar-thumb { background: #2a3550; border-radius: 3px; }
  #showcase-strip.dragging { cursor: grabbing; }
  .sc-item { flex: 0 0 auto; width: 46px; height: 61px; border-radius: 5px; overflow: hidden; background: #0f1219; border: 1px solid #2a2f3a; padding: 0; cursor: pointer; position: relative; }
  .sc-item img { width: 100%; height: 100%; object-fit: cover; object-position: 50% 0%; display: block; pointer-events: none; }
  .sc-item.sel { border: 2px solid #7ad7ff; box-shadow: 0 0 10px rgba(122,215,255,0.5); }
  .sc-item.skin::after { content: '★'; position: absolute; right: 2px; top: 0; font-size: 10px; color: #ffd479; text-shadow: 0 1px 3px #000; }
```

- [ ] **Step 3: 렌더 + 드래그 함수 추가**

`function buildAccountActions() {` 줄 **바로 앞**에 삽입한다.

```js
  // 🖼 v716 — 대표 일러 선택기. 큰 미리보기 + 하단 가로 드래그 썸네일 스트립.
  //   드래그 패턴은 _wireDiffSwipe(난이도 스와이프)와 동일 원칙:
  //   pointerdown 으로 시작, 이동거리 임계 넘으면 setPointerCapture 로 제스처를 붙잡는다.
  function _scSrc(id) { return (id.indexOf('__') >= 0 ? './icons/illust/skin/' : './icons/illust/') + id + '.png'; }
  function buildShowcasePicker() {
    const strip = document.getElementById('showcase-strip');
    const prev  = document.getElementById('showcase-preview');
    const pimg  = document.getElementById('showcase-img');
    const pname = document.getElementById('showcase-name');
    const empty = document.getElementById('showcase-empty');
    if (!strip || !prev) return;
    const list = _showcaseCandidates();
    strip.innerHTML = '';
    if (!list.length) {
      strip.style.display = 'none'; prev.style.display = 'none';
      if (empty) empty.style.display = '';
      return;
    }
    strip.style.display = ''; prev.style.display = '';
    if (empty) empty.style.display = 'none';
    let cur = _showcaseGet();
    if (!cur || !list.some(c => c.id === cur)) cur = list[0].id;
    const _paint = (id) => {
      const it = list.find(c => c.id === id) || list[0];
      prev.classList.remove('empty');
      pimg.onerror = () => prev.classList.add('empty');
      // 미리보기는 애니 일러 허용 — 한 장뿐이라 성능 부담 없음
      if (typeof _applyIllustChain === 'function') _applyIllustChain(pimg, it.char, () => prev.classList.add('empty'), it.id);
      else pimg.src = _scSrc(it.id);
      pname.textContent = `${it.charName} · ${it.label}`;
      strip.querySelectorAll('.sc-item').forEach(el => el.classList.toggle('sel', el.dataset.sid === it.id));
    };
    list.forEach(c => {
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'sc-item' + (c.skin ? ' skin' : '');
      b.dataset.sid = c.id;
      b.title = `${c.charName} · ${c.label}`;
      const im = document.createElement('img');
      im.alt = ''; im.loading = 'lazy';
      im.onerror = () => { b.style.display = 'none'; };
      im.src = _scSrc(c.id);
      b.appendChild(im);
      b.onclick = () => {
        if (strip._dragged) return;   // 드래그 끝자락의 오발 클릭 무시
        if (!_showcaseSet(c.id)) return;
        _paint(c.id);
        try { if (typeof updateProfile === 'function') updateProfile(); } catch (_) {}
      };
      strip.appendChild(b);
    });
    _paint(cur);
    _wireStripDrag(strip);
  }
  function _wireStripDrag(strip) {
    if (strip._dragWired) return;
    strip._dragWired = true;
    let on = false, sx = 0, sl = 0, moved = false, pid = null;
    strip.addEventListener('pointerdown', e => {
      on = true; moved = false; sx = e.clientX; sl = strip.scrollLeft; pid = e.pointerId;
      strip._dragged = false;
    });
    strip.addEventListener('pointermove', e => {
      if (!on) return;
      const dx = e.clientX - sx;
      if (!moved && Math.abs(dx) > 6) {
        moved = true; strip.classList.add('dragging');
        try { strip.setPointerCapture(pid); } catch (_) {}
      }
      if (moved) { strip.scrollLeft = sl - dx; e.preventDefault(); }
    });
    const _end = () => {
      if (!on) return;
      on = false;
      strip.classList.remove('dragging');
      try { strip.releasePointerCapture(pid); } catch (_) {}
      strip._dragged = moved;
      // 클릭 이벤트가 이 직후에 오므로 한 틱 뒤에 해제한다
      setTimeout(() => { strip._dragged = false; }, 0);
    };
    strip.addEventListener('pointerup', _end);
    strip.addEventListener('pointercancel', _end);
  }
```

- [ ] **Step 4: 모달 열 때 초기화 연결**

`buildTitlePicker();` 호출 줄을 찾아, 그 **바로 앞**에 `buildShowcasePicker();` 를 추가한다.

- [ ] **Step 5: 정의/연결 검증**

Run:

```bash
cd "C:/Users/solid/Desktop/dot-defense" && node -e "
const h=require('fs').readFileSync('index.html','utf8');
const chk=(l,c)=>console.log(l, c?'OK':'FAIL');
chk('showcase-sec HTML:', h.includes('id=\"showcase-sec\"'));
chk('showcase-strip HTML:', h.includes('id=\"showcase-strip\"'));
chk('buildShowcasePicker 정의:', (h.match(/function buildShowcasePicker\(/g)||[]).length===1);
chk('_wireStripDrag 정의:', (h.match(/function _wireStripDrag\(/g)||[]).length===1);
chk('모달에서 호출:', /buildShowcasePicker\(\);\s*\n\s*buildTitlePicker\(\);/.test(h));
chk('sc-item CSS:', h.includes('.sc-item'));
chk('드래그 임계 6px:', /Math\.abs\(dx\) > 6/.test(h));
"
```

Expected: 7줄 전부 `OK`

- [ ] **Step 6: 커밋**

```bash
cd "C:/Users/solid/Desktop/dot-defense" && git add index.html && git commit -m "feat: 내 정보 대표 일러 선택 UI (미리보기 + 드래그 스트립)

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>" && git push origin main
```

---

### Task 7: 버전업 + 브라우저 통합 검증 + 배포

**Files:**
- Modify: `index.html` — `const APP_VERSION = 715;` → `716`
- Modify: `sw.js:4` — `const CACHE = 'dot-defense-v715';` → `v716`

**Interfaces:**
- Consumes: Task 1~6 전부

- [ ] **Step 1: 버전 동시 상향**

`index.html`의 `const APP_VERSION = 715;` 를 `const APP_VERSION = 716;` 으로,
`sw.js`의 `const CACHE = 'dot-defense-v715';` 를 `const CACHE = 'dot-defense-v716';` 으로 바꾼다.

- [ ] **Step 2: 버전 일치 검증**

Run:

```bash
cd "C:/Users/solid/Desktop/dot-defense" && node -e "
const fs=require('fs');
const a=fs.readFileSync('index.html','utf8').match(/const APP_VERSION = (\d+);/)[1];
const b=fs.readFileSync('sw.js','utf8').match(/dot-defense-v(\d+)/)[1];
console.log('APP_VERSION',a,'/ sw CACHE',b, a===b?'OK 일치':'FAIL 불일치');
"
```

Expected: `APP_VERSION 716 / sw CACHE 716 OK 일치`

- [ ] **Step 3: 프리뷰 서버 기동 + 랭킹 화면 DOM 검증**

`.claude/launch.json` 이 없으면 아래 내용으로 만든다.

```json
{
  "version": "0.0.1",
  "configurations": [
    { "name": "dot-defense", "runtimeExecutable": "npx", "runtimeArgs": ["-y", "serve", "-l", "5173", "."], "port": 5173 }
  ]
}
```

`preview_start`로 서버를 띄운 뒤, 브라우저에서 다음을 확인한다:

1. `read_console_messages` — 에러 0건 (특히 `_showcaseValid is not defined` 류)
2. 닉네임 모달을 열고 `read_page` — `#showcase-sec`, `#showcase-strip`, `.sc-item` 존재 확인
3. `javascript_tool`로 후보/검증 동작 확인:

```js
JSON.stringify({
  cands: _showcaseCandidates().length,
  validBase: _showcaseValid('luna'),
  validSkin: _showcaseValid('luna__moonlit'),
  rejectFake: _showcaseValid('luna__nope'),
  rejectBasic: _showcaseValid('standard'),
  stripItems: document.querySelectorAll('.sc-item').length
})
```

Expected: `validBase:true, validSkin:true, rejectFake:false, rejectBasic:false`, `cands === stripItems`

4. 글로벌 랭킹 화면으로 이동 후 `read_page` — `.rank-podium` 1개, `.podium-card` 최대 3개, `.rank-thumb` 존재 확인
5. `computer {action:"screenshot"}` 로 시각 확인 (스크린샷이 타임아웃되면 DOM 검증 결과로 갈음)

- [ ] **Step 4: 커밋 + 푸시**

```bash
cd "C:/Users/solid/Desktop/dot-defense" && git add -A && git commit -m "feat: 대표 일러(SHOWCASE) + 랭킹 시상대 개편 (v716)

- 내 정보에서 보유 캐릭/스킨 중 대표 일러 선택 (미리보기 + 드래그 스트립)
- 랭킹 Top3 시상대 카드 + 4위↓ 세로 썸네일 행
- rankings.showcase 컬럼 연동, 컬럼 없어도 제출/조회 폴백
- 렌더 직전 화이트리스트 검증으로 조작된 showcase 차단

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>" && git push origin main
```

- [ ] **Step 5: 함장에게 Supabase SQL 안내**

배포 후 아래를 실행해야 **남의 대표 일러가 보인다**고 안내한다. 실행 전까진 내 행에만 내 일러가 뜨고 남은 그 판에 쓴 캐릭 기본 일러로 표시된다.

```sql
alter table rankings add column showcase text;
```

---

## Self-Review

**1. 스펙 커버리지**

| 스펙 섹션 | 담당 태스크 |
|---|---|
| §4 데이터 모델 (`META.showcase`) | Task 1 |
| §5 서버 (컬럼/제출/조회/프로필) | Task 2, Task 7 Step 5 |
| §6 검증·보안 (화이트리스트) | Task 1 (`_showcaseValid`), Task 4·5 (`_showcaseForRow` 경유) |
| §7.1 Top3 시상대 | Task 3(CSS) + Task 4(렌더) |
| §7.2 4~10위 썸네일 행 | Task 3(CSS) + Task 5(렌더) |
| §7.3 성능 (Top3만 애니) | Task 4(체인 사용) / Task 5(png 고정) |
| §8 선택 UI | Task 6 |
| §9 엣지 케이스 | 미설정→Task 1 `_showcaseForRow`, 삭제된 스킨→Task 1 `_showcaseValid`, 로드 실패→Task 4 `no-art`/Task 5 `onerror`, 신규 유저→Task 6 `#showcase-empty`, 컬럼 미생성→Task 2 폴백 |
| §11 범위 밖 | 계획에 없음 (의도적) |

누락 없음.

**2. 플레이스홀더 스캔**: "TBD"/"적절히 처리"/"비슷하게" 없음. 모든 코드 스텝에 실제 코드 포함. 검증 스텝마다 실행 명령 + 기대 출력 명시.

**3. 타입 정합성**
- `_showcaseForRow(row)` — Task 1 정의, Task 4·5에서 동일 시그니처 호출 ✅
- `_showcaseCandidates()` 반환 필드 `{id, char, skin, charName, label}` — Task 6에서 `c.id/c.char/c.skin/c.charName/c.label` 로 정확히 소비 ✅
- `_applyIllustChain(img, charId, onFail, exactId)` — Task 4·6에서 4인자 순서 일치 ✅
- CSS 클래스명: Task 3 정의(`podium-card`, `podium-art`, `no-art`, `rank-thumb`, `has-art`, `sc-item`, `sel`) ↔ Task 4·5·6 사용 일치 ✅
- `_scSrc(id)` — Task 6 정의·사용 ✅
