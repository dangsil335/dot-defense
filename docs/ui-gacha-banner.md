# 상시 가챠 배너 — 1장

> 픽업 배너는 캐릭터 일러가 들어간다. **상시 배너는 캐릭터를 넣으면 안 된다** —
> 넣는 순간 그 캐릭터 배너처럼 보인다.
> 우리 가챠 이름이 **차원 스카우트**이고 아이콘도 레이더다. 그 세계관을 그대로 키운다.

---

## 0. 규격

```
위치    icons/
파일    gacha-standard.webp
크기    1920 × 1080  (16:9)
포맷    WebP  품질 85 정도
용량    400KB 이하 목표
```

**왜 WebP 인가** — 기존 배너 실측:

| 파일 | 크기 | 용량 |
|---|---|---|
| `gacha-elemSumi.png` | 1672×941 | **2385KB** |
| `gacha-ariaMisa.png` | 1672×941 | **2520KB** |
| `gacha-prismBeast.jpg` | 1672×933 | 333KB |
| `gacha-feriaSomnia.jpg` | 1678×937 | 365KB |

PNG 두 장이 **2.4MB** 씩이다. 사진형 일러에 PNG 는 낭비다.
WebP 로 뽑으면 JPG 수준 용량에 화질은 더 낫다.

⚠ 비율만 16:9 면 픽셀 수는 크게 상관없다. 컨테이너가 `aspect-ratio: 16/9` +
`object-fit: contain` 이라 알아서 맞춘다. 다만 **16:9 를 벗어나면 좌우에 빈 띠**가 생긴다.

---

## 1. ⚠ UI 가 덮는 자리 — 비워둘 것

배너 위에 컨트롤이 얹힌다. 실측값이다.

```
┌──────────────────────────────────────────────┐
│  ◀                                        ▶  │  ← 좌우 화살표
│ 2~11%                              89~98%    │    (세로 42~58% 지점)
│                                              │
│         여기가 핵심 볼거리 자리               │
│              (중앙 20~80%)                    │
│                                              │
│  배너 이름이 위에 겹쳐 표시된다               │
└──────────────────────────────────────────────┘
```

프롬프트에 넣을 문장:

```
Keep the far LEFT and far RIGHT edges (about 12% on each side) simple and low-contrast —
navigation arrows are overlaid there. Put the main subject in the CENTER.
```

---

## 2. 영문 프롬프트

```
Anime game gacha banner art, 1920x1080, 16:9 landscape.
NO characters, no people, no figures — this is a scenery/effect banner only.

Subject: a radiant DIMENSIONAL GATE standing open in deep space.
Through the opening you can see a field of stars and drifting constellations.
In front of the gate, concentric radar sweep rings expand outward across the frame,
like a scan pulse. A few small crystalline shards drift near the gate.

Style: hand-painted Japanese anime background art. Clean flat areas of color with
crisp, clearly shaped light — NOT smooth photographic gradients, NOT a 3D render.
Bold simple shapes, confident linework on key edges.

Color: deep indigo and violet night, with cool cyan and warm gold light coming
from the gate. Bright and luminous, not gloomy — the gate is the light source.

Composition: the gate is centered. Keep the far LEFT and far RIGHT edges
(about 12% on each side) simple and low-contrast — navigation arrows are overlaid there.
Horizon level, straight-on view, nothing tilted.

No text, no letters, no numbers, no logo, no UI, no watermark, no frame.
```

**네거티브**
```
characters, people, person, girl, boy, figure, silhouette of a person, hands, face,
3d render, unreal engine, octane, blender, cgi, ray tracing, ambient occlusion,
photograph, photorealistic, hdr, depth of field, bokeh, lens flare,
text, letters, numbers, kanji, logo, watermark, signature, UI, interface, frame, border,
busy detail on the left, busy detail on the right, clutter at the edges,
dark, gloomy, muddy, desaturated, washed out,
cyberpunk, sci-fi hologram, neon signage, fisheye, wide angle, tilted horizon,
sketch, unfinished, rough
```

⚠ `characters, people` 를 반드시 넣을 것 — 안 넣으면 모델이 알아서 인물을 그려 넣는다.
그러면 픽업 배너와 구분이 안 된다.
⚠ `3d render` 계열도 필수다. 배경 일러 1차가 그걸로 실사가 됐다.

---

## 3. 통과 기준 — 내가 확인한다

1. 1920×1080 (16:9)
2. **사람이 그려져 있지 않은가** — 하나라도 있으면 실패
3. **좌우 12% 가 단순한가** — 화살표가 얹힌다
4. 평균 밝기 90 이상 (어두우면 다른 배너 옆에서 죽는다)
5. 글자·로고 없음
6. 용량 400KB 이하

---

## 4. 넣은 뒤 (내가 하는 일)

파일만 `icons/gacha-standard.webp` 로 넣으면 된다. 배너 추가는 코드 한 덩어리다.

```javascript
{
  id: 'standard',
  name: '🌌 상시 차원 스카우트',
  desc: '모든 차원에 닿는다 — 픽업 없음',
  bannerImg: './icons/gacha-standard.webp',
  pool: { SSR: [...전체 SSR...], SR: _GACHA_SR_ALL, R: [] },
  rates: { SR: 0.05, SSR: 0.01 },
  featured: null,
}
```

### 아직 정할 것

- **SSR 풀** — 전체 SSR 을 넣을지, 픽업 배너에 없는 캐릭까지 넣을지
- **확률** — 픽업과 같게(1%) 할지, 상시라 조금 낮게(0.8%) 할지
  · 같게 두면 "픽업은 원하는 캐릭 확률이 높다"는 이점만 남아 깔끔하다
  · 낮추면 상시를 쓸 이유가 약해진다. 같게 두는 쪽을 권한다
- **오늘의 픽업 로테이션** — 상시는 빼야 한다. 픽업이 아니니까
  (`getTodayBannerIdx()` 가 배너 배열 인덱스를 쓰므로 상시를 배열에 넣으면 로테이션에 낀다.
   상시를 배열 맨 뒤에 두고 로테이션은 앞 4개만 돌게 고쳐야 한다)
