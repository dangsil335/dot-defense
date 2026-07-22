# 능력 수치 데이터화 (고유장비 단계 0-b) 실행 계획

> **For agentic workers:** 이 계획은 `superpowers:subagent-driven-development` 로 태스크 단위 실행한다.

**목표:** 고유 메커니즘 옵션이 건드릴 능력 상수를 `tick`/`init` 본문 리터럴에서 빼내 데이터로 노출한다.

**아키텍처:** 능력 정의에 `stats` 객체를 추가하고, 런타임에는 헬퍼 `_S(ab)` 로 지연 생성한 인스턴스 사본을 읽는다. 고유장비 옵션은 런 시작 시 `state.abilityStatOverrides` 를 채우고, `_S` 가 이를 병합한다.

**대상 범위:** [unique-options-A.md](../../../.superpowers/sdd/unique-options-A.md) · [unique-options-B.md](../../../.superpowers/sdd/unique-options-B.md) 두 문서의 **부록 표에 실린 상수만**. 전면 리팩터가 아니다.

---

## Global Constraints

- **`init` 호출 지점 8곳(21087 / 26322 / 26392 / 30643 / 30658 / 32005 / 32493 / 33620)을 건드리지 않는다.** `stats` 주입을 그 8곳에 심으면 하나만 빠뜨려도 그 경로로 얻은 능력이 크래시한다. 반드시 지연 생성으로 처리한다.
- **동작을 바꾸지 않는다.** 이 작업은 순수 리팩터다. 리터럴을 `stats` 로 옮기되 **값은 그대로**여야 한다. 밸런스 변경은 이 단계의 범위가 아니다.
- **`desc` 를 건드리지 않는다.** 값이 안 바뀌므로 표시도 그대로다.
- 검증: `node --check` + 브라우저 콘솔 에러 0 + grep. 테스트 프레임워크 없음.
- 버전은 **마지막 태스크에서 한 번만** bump (index.html `APP_VERSION` + sw.js `CACHE` 동시).

---

## 인프라 설계

### `_S(ab)` — 지연 생성 헬퍼

`damageEnemy` 근처(공용 헬퍼 구역)에 둔다.

```js
// 능력 인스턴스별 stats. init 경로가 8곳으로 흩어져 있어 지연 생성한다 —
// 어느 경로로 만들어진 ab 든 첫 호출 시점에 만들어지므로 주입 누락이 원천적으로 없다.
function _S(ab) {
  if (!ab._stats) {
    const def  = ABILITY_DEFS[ab.id];
    const base = (def && def.stats) || {};
    const ov   = state.abilityStatOverrides && state.abilityStatOverrides[ab.id];
    ab._stats = ov ? Object.assign({}, base, ov) : Object.assign({}, base);
  }
  return ab._stats;
}
```

- `stats` 가 없는 능력에도 안전하다(빈 객체 반환).
- 레벨 스케일링은 기존대로 `ab.level` 로 계산한다. `stats` 는 **레벨 무관 상수만** 담는다.

### `state.abilityStatOverrides`

런 시작 시 `state.metaMods` 를 만드는 자리(20743 부근, `applyGearEffects` 호출부) 근처에서 `{}` 로 초기화한다. 고유장비 옵션은 나중 단계에서 이 객체를 채운다. **이번 단계에서는 초기화만 하고 아무도 채우지 않는다.**

### 능력 정의 작성 형식

```js
inkSlash: {
  name: '먹빛 도', /* ... */,
  stats: { critChance: 0.25, critMul: 2.2, markCap: 5, markDur: 240 },
  tick(ab) {
    const S = _S(ab);
    const crit = Math.random() < S.critChance;
    /* ... */
  },
}
```

- 이름은 **의미가 드러나게** 짓는다(`c1`/`v2` 금지). 고유 옵션 문서가 이 이름으로 옵션을 서술하게 된다.
- `draw` 안의 순수 연출 상수는 **옮기지 않는다**(옵션 대상이 아니다).

---

## 태스크

각 태스크는 능력 묶음 하나를 처리하고 `node --check` + 콘솔 에러 0 을 확인한 뒤 커밋한다.

### Task 1: 인프라 + 파일럿 4종

**Files:** `index.html`

- [ ] `_S(ab)` 헬퍼를 `damageEnemy` 근처에 추가
- [ ] `state.abilityStatOverrides = {}` 초기화 추가 (런 시작 지점)
- [ ] 파일럿 4종에 `stats` 적용 — 구조가 가장 단순한 것부터:
  - `inkSlash` — `critChance 0.25` / `critMul 2.2` / `markCap 5` / `markDur 240` (7711, 7713, 7716-7717)
  - `stormBrand` — `chainRadius 150` (7125)
  - `flashbulb` — `slowDur 90` (18980)
  - `petalStorm` — `petalCount 12` / `petalLife 90` / `petalSpeed 4.5` (16210, 16215-16216)
- [ ] 검증: 각 리터럴이 `stats` 에서 오는지 grep 으로 확인, 값이 바뀌지 않았는지 대조
- [ ] 커밋

**검증 포인트:** 파일럿 4종이 정상 동작하면 인프라가 옳다. 이 태스크의 리뷰가 통과해야 나머지를 진행한다.

### Task 2: A조 전반 5명 (마린 · 솔라 · 그래비타스 · 에이미 · 클로에)

[unique-options-A.md](../../../.superpowers/sdd/unique-options-A.md) 부록 표의 해당 행을 그대로 따른다. 능력 10종.

- [ ] `torpedo` `tidalMaelstrom` `sunspot` `solarFlare` `pullField` `gravityCrush` `interceptorDrone` `droneSwarm` `acidFlask` `acidRain`
- [ ] 커밋

### Task 3: A조 후반 5명 (라라 · 갈라테아 · 블랑슈 · 카이라 · 페리아)

- [ ] `marionette` `stringWeb` `petrifyGaze` `stoneGarden` `prismBolt` `refractionField` `huntingClaw` `beastForm` `polarField` `ferroShard`
- [ ] 커밋

### Task 4: B조 전반 5명 (사쿠라 · 루나 · 아리아 · 미사키 · 레비나)

[unique-options-B.md](../../../.superpowers/sdd/unique-options-B.md) 부록 표를 따른다. `petalStorm` 은 Task 1 에서 처리했으므로 제외.

- [ ] `sakuraSlash` `moonShot` `lunarRain` `starSong` `celestialEcho` `timeButterfly` `temporalLoop` `stormBrand`(완료) `thunderfall`
- [ ] 커밋

### Task 5: B조 후반 5명 (카르디스타 · 스미카 · 엘레미아 · 트리나 · 아이리스)

`inkSlash` `flashbulb` 는 Task 1 에서 처리했으므로 제외.

- [ ] `cardThrow` `wildDeal` `inkBlot` `spritling` `elementCycle` `phantomStage` `understudyCall` `longExposure`
- [ ] **주의:** `phantomStage` 는 `_phantomDmg` 게이트를 쓴다. 게이트 구조(`try`/`finally`)를 절대 건드리지 말고 상수만 옮긴다. 작업 후 `grep -c "_phantomDmg = true"` 가 **8** 인지 확인.
- [ ] **주의:** `longExposure` 의 `maxExp = 150` 은 **상한과 피해 계수 분모를 겸한다.** 고유 옵션(과노출)이 둘을 분리해야 하므로, 이번에 `chargeCap` 과 `expDenom` **두 개의 stats 로 나누되 값은 둘 다 150** 으로 둔다(동작 불변).
- [ ] 커밋

### Task 6: 검증 + 버전 bump

- [ ] 두 부록 표의 모든 행이 실제로 `stats` 로 옮겨졌는지 대조 (누락 0 확인)
- [ ] 옮긴 상수의 값이 원래 값과 **전부 일치**하는지 대조 (동작 불변 확인)
- [ ] `APP_VERSION` + `sw.js` `CACHE` 를 **678** 로 bump
- [ ] 커밋

---

## 완료 후

`state.abilityStatOverrides` 가 준비되므로, 고유장비 단계 3(고유 메커니즘 옵션 구현)은 이 객체를 채우는 것만으로 40종 옵션을 전부 구현할 수 있다. 능력마다 특수 분기를 심을 필요가 없어진다.
