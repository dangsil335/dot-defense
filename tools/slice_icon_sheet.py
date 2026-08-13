# -*- coding: utf-8 -*-
"""
아이콘 시트(2행 5열)를 잘라 icons/ui/menu/*.webp 10장으로 정규화한다.

낱장으로 열 번 뽑으면 그림체가 갈리므로 한 장에 열 개를 함께 그리게 한다.
그 시트를 여기서 자른다.

  python tools/slice_icon_sheet.py <시트파일> [--dry]

셀 경계는 고정 격자가 아니라 **알파가 비어 있는 세로/가로 띠**로 찾는다.
모델이 격자를 정확히 안 맞춰도 동작한다.
"""
import os, sys
import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT  = os.path.join(ROOT, 'icons', 'ui', 'menu')
N    = 256
NAMES = [['shop', 'codex', 'perma', 'achieve', 'chars'],
         ['records', 'core', 'rank', 'scout', 'start']]

def bands(mask, want):
    """1차원 불리언(내용 있음)에서 덩어리 want 개의 (시작, 끝)을 찾는다."""
    idx = np.where(mask)[0]
    if not len(idx):
        return []
    gaps = np.where(np.diff(idx) > 1)[0]
    segs, s = [], idx[0]
    for gcut in gaps:
        segs.append((s, idx[gcut])); s = idx[gcut + 1]
    segs.append((s, idx[-1]))
    segs = [g for g in segs if g[1] - g[0] > 4]
    if len(segs) > want:                       # 큰 것 want 개만 남긴다
        segs = sorted(sorted(segs, key=lambda g: g[0] - g[1])[:want])
    return segs

def main():
    if len(sys.argv) < 2:
        print('사용: python tools/slice_icon_sheet.py <시트파일> [--dry]'); return 1
    src = sys.argv[1]
    dry = '--dry' in sys.argv
    if not os.path.exists(src):
        print('파일 없음: ' + src); return 1

    im = Image.open(src).convert('RGBA')
    a = np.array(im)[..., 3] > 12
    if not a.any():
        print('⚠ 알파가 전부 비었다. 배경이 불투명한 시트인지 확인할 것'); return 1

    rows = bands(a.any(axis=1), 2)
    print('시트 %dx%d · 가로 띠 %d개' % (im.size[0], im.size[1], len(rows)))
    if len(rows) != 2:
        print('⚠ 2행을 못 찾았다(%d). 행 간 여백이 붙어 있을 수 있다.' % len(rows)); return 1

    ok = 0
    for r, (y0, y1) in enumerate(rows):
        sub = a[y0:y1 + 1]
        cols = bands(sub.any(axis=0), 5)
        print('  %d행: 세로 띠 %d개' % (r + 1, len(cols)))
        if len(cols) != 5:
            print('  ⚠ 5열을 못 찾았다. 아이콘끼리 붙어 있을 수 있다.'); continue
        for c, (x0, x1) in enumerate(cols):
            name = NAMES[r][c]
            w, h = x1 - x0 + 1, y1 - y0 + 1
            side = int(max(w, h) / 0.84)                  # 캔버스의 84% 를 차지하게
            cell = Image.new('RGBA', (side, side), (0, 0, 0, 0))
            cell.paste(im.crop((x0, y0, x1 + 1, y1 + 1)),
                       ((side - w) // 2, (side - h) // 2))
            cell = cell.resize((N, N), Image.LANCZOS)
            arr = np.array(cell)
            edge = max(arr[0, :, 3].max(), arr[-1, :, 3].max(),
                       arr[:, 0, 3].max(), arr[:, -1, 3].max())
            flag = '' if edge == 0 else '  ⚠가장자리알파 %d' % edge
            print('    %-8s 원본 %dx%-4d → %dx%d%s' % (name, w, h, N, N, flag))
            if not dry:
                cell.save(os.path.join(OUT, name + '.webp'), 'WEBP',
                          lossless=True, quality=100)
            ok += 1

    print('\n%d/10 %s' % (ok, '(dry run — 저장 안 함)' if dry else '저장 완료'))
    if ok == 10 and not dry:
        print('확인:  python tools/check_icons.py')
    return 0

sys.exit(main())
