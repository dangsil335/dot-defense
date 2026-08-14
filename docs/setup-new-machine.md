# 새 컴퓨터에서 이어서 작업하기

## 1. 클론

```bash
git clone https://github.com/dangsil335/dot-defense.git
cd dot-defense
```

⚠ **받는 데 시간이 걸린다.** 추적 파일 958개 / **859MB** 다.

| 폴더 | 용량 | 내용 |
|---|---|---|
| `icons/` | 769MB | 그중 `icons/illust/_orig/` 만 **458MB** (원본 고해상도 보관본, 161장) |
| `3D/` | 82MB | |
| 나머지 | 8MB | `index.html` `sw.js` `docs/` `tools/` `fonts/` |

**빨리 시작하고 싶으면** — 히스토리를 빼고 최신본만 받는다:

```bash
git clone --depth 1 https://github.com/dangsil335/dot-defense.git
```

되돌리려면 나중에 `git fetch --unshallow`.

> `_orig/` 458MB 는 게임 실행에 안 쓰인다. 고해상도 원본 보관용이라
> 작업만 하려면 없어도 된다. 정리하려면 별도 저장소나 클라우드로 옮기는 걸 권한다.

---

## 2. 도구 설치

**Python** (내가 에셋 검사·폰트 변환에 쓴다)

```bash
pip install pillow numpy fonttools brotli
```

| 패키지 | 쓰는 곳 |
|---|---|
| `pillow` `numpy` | 아이콘·배경 검사 (`tools/check_icons.py`, `tools/trim_plate.py`) |
| `fonttools` `brotli` | 폰트 서브셋·woff2 변환 (`tools/build_font.py`) |

**Node** — `index.html` 안의 JS 문법 검사(`node --check`)에 쓴다. 없으면 검사만 건너뛴다.

---

## 3. 실행

개발 서버 설정(`.claude/launch.json`)이 깃에 들어 있다. 그대로 뜬다.

```bash
python -m http.server 8777
```

브라우저에서 `http://localhost:8777`.

⚠ `file://` 로 직접 열면 안 된다 — service worker 와 fetch 가 막힌다.

---

## 4. ⚠ 깃에 없는 것

| 항목 | 어디 있나 | 필요한가 |
|---|---|---|
| **내(Claude) 기억 파일** | `~/.claude/projects/C--Users-solid/memory/` | 이어서 일하려면 **복사 권장** |
| `_wip/` `_trash_*/` `_backup_*/` | 로컬에만 | 시안·폐기본. 없어도 무방 |
| `.superpowers/` | 로컬에만 | 없어도 무방 |
| **게임 세이브** | 브라우저 localStorage | 계정 로그인으로 서버에서 복구 |

### 기억 파일을 옮기면 좋은 이유

작업하며 쌓인 교훈이 들어 있다. 없으면 같은 실수를 반복한다.

```
feedback_kill_animation_before_measuring.md   측정 전 애니메이션 끄기
feedback_confirm_failing_layer.md             증상 반복되면 층부터 다시 가르기
feedback_measure_lists_before_asserting.md    목록은 짐작 말고 실측
project_dot_defense_*.md                      설계 결정들
MEMORY.md                                     위 파일들의 색인
```

새 컴퓨터의 같은 경로(`~/.claude/projects/<프로젝트폴더명>/memory/`)에 넣으면 된다.
폴더명은 작업 경로에 따라 달라진다 — 새 컴퓨터에서 한 번 대화를 시작하면 자동으로 생긴다.

### 게임 세이브

`localStorage` 라 컴퓨터를 옮기면 안 따라온다.
게임 안에서 **계정 만들기 / 로그인**을 해두면 서버에서 불러온다.
안 해뒀으면 새 컴퓨터에선 새 계정으로 시작된다.

---

## 5. 옮기기 전 체크

```bash
git status          # 비어 있어야 한다
git log --oneline -1
```

미커밋 파일이 있으면 그건 새 컴퓨터로 안 따라간다.
특히 **GPT 가 방금 떨어뜨린 에셋**이 커밋 안 돼 있기 쉽다.

---

## 6. 현재 상태 (2026-08-13)

- 버전 **v855**, 배포 `dangsil335.github.io/dot-defense`
- 로비 UI 개편이 거의 끝났다 — 발바닥 독 + 원형 CTA(우주선·레이더) + 라이트 팔레트
- 화면 UI 는 공용 크롬(13화면) + 리스트 카드(4화면) + 난이도·진화·가챠 완료
- 로비 배경 10장, 화면 배경 4장 들어감

### 남은 일

- 대표 캐릭터 설정 UI 가 아직 세로 기준 — 가로에서 확인 필요
- 로비 배경 밝기 편차 (`alba__sleepyguard` 58 ~ `alba__lifeguard` 176) → 스크림 조정 여지
- 로비 배경 나머지 (스킨 56종 중 10장 완료)
- `L2` 가로 유도 (manifest `orientation: landscape` + 회전 안내)

### 개발용 콘솔 명령

```javascript
__allSkins(true)     // 스킨 전체 해금 (배경 테스트용). false 로 원복
__lobbyBgStatus()    // 로비 배경 파일이 있는 스킨 목록
```
