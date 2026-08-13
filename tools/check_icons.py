# -*- coding: utf-8 -*-
"""
메뉴 아이콘 10장을 통과 기준으로 검사하고, 눈으로 볼 대조표를 만든다.

1차 발주가 실패한 지점이 "40px 로 줄이면 뭔지 모르겠다" 였으므로,
대조표 아래쪽에 **독의 실제 조건(어두운 반투명 띠 위 40px)** 을 같이 깐다.
거기서 안 읽히면 크게 봐서 예뻐도 못 쓴다.

  python tools/check_icons.py
"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding='utf-8')
ROOT  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MENU  = os.path.join(ROOT, 'icons', 'ui', 'menu')
NAMES = ['shop', 'codex', 'perma', 'achieve', 'chars',
         'records', 'core', 'rank', 'scout', 'start']

# §2 팔레트 — 열 장이 이 안에 있어야 한 세트로 보인다
PALETTE = [('sky', '#4EA8E8'), ('sky-L', '#9FD9F8'), ('gold', '#F2B33C'),
           ('gold-L', '#FFDE93'), ('mint', '#43C7A4'), ('mint-L', '#96E8D0'),
           ('purple', '#9A7DF0'), ('purple-L', '#C9B8FB'), ('white', '#FFFFFF')]
PAL = np.array([[int(h[i:i+2], 16) for i in (1, 3, 5)] for _, h in PALETTE], float)

def main():
    imgs, bad = [], 0
    print('%-9s %-11s %-7s %-6s %s' % ('파일', '크기', '가장자리', '채움', '팔레트 벗어남'))
    print('-' * 58)
    for n in NAMES:
        p = os.path.join(MENU, n + '.webp')
        if not os.path.exists(p):
            print('%-9s ⚠ 없음' % n); bad += 1; continue
        im = Image.open(p).convert('RGBA')
        a = np.array(im)
        edge = max(a[0, :, 3].max(), a[-1, :, 3].max(), a[:, 0, 3].max(), a[:, -1, 3].max())
        opaque = a[..., 3] > 200
        fill = opaque.mean() * 100
        rgb = a[..., :3][opaque].astype(float)
        off = 0.0
        if len(rgb):
            step = max(1, len(rgb) // 4000)
            s = rgb[::step]
            dist = np.sqrt(((s[:, None, :] - PAL[None, :, :]) ** 2).sum(-1)).min(1)
            off = (dist > 78).mean() * 100        # 어느 팔레트 색과도 먼 픽셀 비율
        sz = '%dx%d' % im.size
        f1 = '' if im.size == (256, 256) else ' ⚠'
        f2 = '' if edge == 0 else ' ⚠'
        f3 = ' ⚠' if off > 45 else ''
        if f1 or f2 or f3: bad += 1
        print('%-9s %-9s%s %5d%s %5.1f%% %8.1f%%%s' % (n, sz, f1, edge, f2, fill, off, f3))
        imgs.append((n, im))

    # 대조표 — 위: 크게 / 아래: 독 실제 조건 40px
    BG, C, P = (232, 238, 246, 255), 150, 14
    sh = Image.new('RGBA', (C * 5, C * 2 + 80), BG)
    d = ImageDraw.Draw(sh)
    for i, (n, im) in enumerate(imgs):
        x, y = (i % 5) * C + P, (i // 5) * C + P
        sh.alpha_composite(im.resize((C - P * 2, C - P * 2), Image.LANCZOS), (x, y))
        d.text((x + 2, y + C - P * 2 + 3), n, fill=(60, 80, 110, 255))
    sy = C * 2 + 12
    d.rounded_rectangle([16, sy, C * 5 - 16, sy + 56], radius=15, fill=(26, 40, 60, 255))
    for i, (n, im) in enumerate(imgs):
        sh.alpha_composite(im.resize((40, 40), Image.LANCZOS), (36 + i * 68, sy + 8))
    out = os.path.join(ROOT, 'icons', 'ui', 'menu_preview.png')
    sh.convert('RGB').save(out)

    print('\n대조표: icons/ui/menu_preview.png')
    print('   아래 어두운 띠가 독의 실제 조건(40px)이다. 거기서 안 읽히면 못 쓴다.')
    print('결과: %s' % ('전부 통과' if bad == 0 else '%d장 확인 필요' % bad))
    return 0

sys.exit(main())
