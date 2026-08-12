# -*- coding: utf-8 -*-
"""
버튼 판 3장을 직접 그린다.

이미지 생성 AI 로 6번 시도했지만 전부 실패했다(납작한 막대 → 알약 → 발가락 젤리 →
검정 판 → 구슬). 범용 이미지 모델은 정확한 치수·베벨·림라이트가 필요한 UI 크롬을
못 만든다. 그래서 SDF(부호거리장) 기반으로 픽셀 음영을 직접 계산한다.

핵심: 볼록함을 "구"로 만들면 구슬이 된다. 가장자리에서만 말리고 가운데는 거의 평평한
   접시형이어야 버튼으로 읽힌다. dome 진폭을 낮게 유지하는 이유다.

python tools/make_plates.py  → icons/ui/plate/*.webp + _preview.png
"""
import os, sys
import numpy as np
from PIL import Image, ImageFilter

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT  = os.path.join(ROOT, 'icons', 'ui', 'plate')
SS   = 3                      # 슈퍼샘플링 배수

def hexf(h):
    h = h.lstrip('#')
    return np.array([int(h[i:i+2], 16) for i in (0, 2, 4)], dtype=np.float64)

def smooth(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0.0, 1.0)
    return t * t * (3 - 2 * t)

def sdf_round_rect(X, Y, cx, cy, hw, hh, r):
    """음수면 도형 안쪽. r 은 모서리 반경."""
    qx = np.abs(X - cx) - (hw - r)
    qy = np.abs(Y - cy) - (hh - r)
    outside = np.hypot(np.maximum(qx, 0), np.maximum(qy, 0))
    inside  = np.minimum(np.maximum(qx, qy), 0)
    return outside + inside - r

def shade(d, X, Y, cx, cy, hw, hh, c_top, c_bot, c_rim, *,
          bevel, dome=0.10, dome_y=0.34, recessed=False):
    """SDF 한 장을 받아 RGB 를 만든다. recessed=True 면 파인 홈(위가 어둡다)."""
    H, W = d.shape
    # 세로 기본 그라디언트
    ty = np.clip((Y - (cy - hh)) / (2 * hh), 0, 1)
    base = c_top[None, None, :] * (1 - ty)[..., None] + c_bot[None, None, :] * ty[..., None]

    # 가장자리 근접도: 테두리에서 1, 안쪽으로 갈수록 0
    edge = 1.0 - smooth(0.0, bevel, -d)

    # 가장자리가 어느 쪽을 향하는지 → 위를 보면 림라이트, 아래를 보면 그림자
    gy, gx = np.gradient(d)
    n = np.hypot(gx, gy) + 1e-6
    ny = gy / n                                   # +아래, -위
    up   = np.clip(-ny, 0, 1) * edge
    down = np.clip( ny, 0, 1) * edge
    if recessed:                                  # 파인 홈은 명암이 뒤집힌다
        up, down = down, up

    col = base.copy()
    col += (up   * 62)[..., None]                                  # 위 테두리 밝게
    col -= (down * 30)[..., None]                                  # 아래 테두리 어둡게
    # 아래 테두리는 색까지 rim 쪽으로 당긴다 (단순히 어둡게 하면 탁해진다)
    w = (down * 0.85)[..., None]
    col = col * (1 - w) + c_rim[None, None, :] * w

    # 완만한 접시형 볼록 — 진폭을 낮게. 크면 구슬이 된다
    r2 = ((X - cx) / (hw * 1.05)) ** 2 + ((Y - (cy - hh) - 2 * hh * dome_y) / (hh * 1.15)) ** 2
    col += (np.exp(-r2 * 1.6) * (255 * dome))[..., None]

    return col

def make(name, W, H, c_top, c_bot, c_rim, badge=None, circle=False):
    w, h = W * SS, H * SS
    Y, X = np.mgrid[0:h, 0:w].astype(np.float64)

    pad = min(w, h) * 0.045                       # 접지 그림자 자리
    cx, cy = w / 2, (h - pad * 1.1) / 2 + pad * 0.15

    if circle:
        R = min(w, h) / 2 - pad * 2.0
        d = np.hypot(X - cx, Y - cy) - R
        hw = hh = R
        rad = R
    else:
        hw = w / 2 - pad * 1.6
        hh = h / 2 - pad * 1.9
        rad = hh * 0.86                           # 거의 완전히 둥근 모서리
        d = sdf_round_rect(X, Y, cx, cy, hw, hh, rad)

    bevel = min(hw, hh) * 0.30
    col = shade(d, X, Y, cx, cy, hw, hh, c_top, c_bot, c_rim,
                bevel=bevel, dome=0.11 if circle else 0.085,
                dome_y=0.30 if circle else 0.26)

    # ── 좌측 배지 홈 (cta / gold) ──
    if badge:
        bl, bw, bh, brr = badge                   # 캔버스 대비 비율
        bx0 = (cx - hw) + 2 * hw * bl
        bcw, bch = 2 * hw * bw / 2, 2 * hh * bh / 2
        bcx, bcy = bx0 + bcw, cy
        bd = sdf_round_rect(X, Y, bcx, bcy, bcw, bch, min(bcw, bch) * brr)
        # 홈은 판보다 살짝 밝은 톤 + 명암 반전
        bt = c_top + (255 - c_top) * 0.30
        bb = c_bot + (255 - c_bot) * 0.22
        bcol = shade(bd, X, Y, bcx, bcy, bcw, bch, bt, bb, c_rim,
                     bevel=min(bcw, bch) * 0.34, dome=0.0, recessed=True)
        m = smooth(0.6, -0.6, bd)[..., None]      # 홈 안쪽 마스크
        col = col * (1 - m) + bcol * m

    # ── 미세 그레인: 완벽히 매끈하면 플라스틱으로 보인다 ──
    rng = np.random.default_rng(7)
    col += rng.normal(0, 1.7, col.shape)

    alpha = smooth(0.6, -0.6, d) * 255.0

    rgba = np.dstack([np.clip(col, 0, 255), alpha]).astype(np.uint8)
    im = Image.fromarray(rgba, 'RGBA').resize((W, H), Image.LANCZOS)

    # ── 접지 그림자: 알파를 아래로 밀고 블러 ──
    a = im.getchannel('A')
    sh = Image.new('L', (W, H), 0)
    sh.paste(a, (0, max(1, int(H * 0.035))))
    sh = sh.filter(ImageFilter.GaussianBlur(max(1.5, H * 0.030)))
    shadow = Image.new('RGBA', (W, H), (36, 54, 84, 0))
    shadow.putalpha(sh.point(lambda v: int(v * 0.42)))
    im = Image.alpha_composite(shadow, im)

    p = os.path.join(OUT, name + '.webp')
    im.save(p, 'WEBP', lossless=True, quality=100)

    # 검증
    arr = np.array(im).astype(np.float64)
    op = arr[..., 3] > 200
    lum = (0.2126 * arr[..., 0] + 0.7152 * arr[..., 1] + 0.0722 * arr[..., 2])[op]
    edges = np.concatenate([arr[0, :, 3], arr[-1, :, 3], arr[:, 0, 3], arr[:, -1, 3]])
    print('  %-7s %4dx%-4d 평균밝기 %5.1f  가장자리 최대알파 %3d  %5.1fKB'
          % (name, W, H, lum.mean(), edges.max(), os.path.getsize(p) / 1024))
    return im

print('버튼 판 생성')
ims = [
    make('normal', 320, 320, hexf('ffffff'), hexf('e6edf6'), hexf('c4d0e0'), circle=True),
    make('cta',    480, 240, hexf('9ed6f6'), hexf('4f9bd2'), hexf('3d7fae'),
         badge=(0.045, 0.25, 0.72, 0.30)),
    make('gold',   476, 140, hexf('fbeec9'), hexf('dfbc6e'), hexf('b39a63'),
         badge=(0.040, 0.19, 0.74, 0.32)),
]

# 미리보기 한 장
PW = 1120
prev = Image.new('RGBA', (PW, 430), (235, 240, 248, 255))
prev.alpha_composite(ims[0], (40, 55))
prev.alpha_composite(ims[1], (410, 60))
prev.alpha_composite(ims[2], (410, 330))
prev.convert('RGB').save(os.path.join(ROOT, 'icons', 'ui', 'plate_preview.png'))
print('\n미리보기: icons/ui/plate_preview.png')
