# -*- coding: utf-8 -*-
"""
판 이미지의 남는 투명 여백을 잘라낸다.

버튼은 판을 `background-size: 100% 100%` 로 늘려 쓴다.
그래서 **파일의 캔버스 비율 = 버튼 비율** 이어야 안 찌그러진다.
그림이 캔버스 안에서 작게 그려져 오면(가로 63% 등) 버튼 폭을 못 채우므로
여백을 잘라 캔버스를 그림에 맞춘다.

  python tools/trim_plate.py            # 검사만
  python tools/trim_plate.py --apply    # 실제로 자른다

여백은 접지 그림자 몫으로 3% 만 남긴다. 이미 잘려 있으면 아무것도 안 한다.
"""
import os, sys
import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDIR = os.path.join(ROOT, 'icons', 'ui', 'plate')
APPLY = '--apply' in sys.argv
MARGIN = 0.03          # 접지 그림자 자리
FILL_OK = 0.90         # 가로 90% 이상이면 손대지 않는다

print('%-8s %-12s %-8s %-13s %s' % ('파일', '캔버스', '가로채움', '내용 비율', '조치'))
print('-' * 62)
for name in ['cta', 'gold', 'normal']:
    p = os.path.join(PDIR, name + '.webp')
    if not os.path.exists(p):
        print('%-8s 없음' % name); continue
    im = Image.open(p).convert('RGBA')
    a = np.array(im); W, H = im.size
    op = a[..., 3] > 140
    if not op.any():
        print('%-8s 불투명 픽셀 없음' % name); continue
    xs = np.where(op.any(axis=0))[0]; ys = np.where(op.any(axis=1))[0]
    x0, x1, y0, y1 = xs[0], xs[-1], ys[0], ys[-1]
    bw, bh = x1 - x0 + 1, y1 - y0 + 1
    fill = bw / W

    if fill >= FILL_OK:
        print('%-8s %-12s %7.1f%% %12.2f:1  그대로 (이미 꽉 참)'
              % (name, '%dx%d' % (W, H), fill * 100, bw / bh))
        continue

    mx, my = int(bw * MARGIN), int(bh * MARGIN)
    nx0, ny0 = max(0, x0 - mx), max(0, y0 - my)
    nx1, ny1 = min(W, x1 + 1 + mx), min(H, y1 + 1 + my)
    out = im.crop((nx0, ny0, nx1, ny1))
    ow, oh = out.size
    act = '자름 → %dx%d (%.2f:1)' % (ow, oh, ow / oh)
    if APPLY:
        out.save(p, 'WEBP', lossless=True, quality=100)
        act += '  저장됨'
    else:
        act += '  (--apply 필요)'
    print('%-8s %-12s %7.1f%% %12.2f:1  %s'
          % (name, '%dx%d' % (W, H), fill * 100, bw / bh, act))

if not APPLY:
    print('\n실제로 자르려면:  python tools/trim_plate.py --apply')
else:
    print('\n⚠ 잘린 파일의 비율에 맞춰 index.html 의 버튼 aspect-ratio 를 확인할 것.')
