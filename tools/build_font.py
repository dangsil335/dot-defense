# -*- coding: utf-8 -*-
"""
fonts/ 에 넣은 원본 폰트를 woff2 로 변환·서브셋한다.

  python tools/build_font.py

⚠ 한글은 전부 남긴다. 실제 쓰는 글자만 남기면 300KB 도 안 되지만,
  글로벌 랭킹에 **다른 사람 닉네임**이 뜬다. 임의의 한글이라 서브셋하면 깨진다.
  대신 안 쓰는 스크립트(일본어·한자·키릴)와 OpenType 기능을 덜어낸다.
"""
import os, sys, glob
sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FDIR = os.path.join(ROOT, 'fonts')

from fontTools.ttLib import TTFont
from fontTools import subset

# 남길 유니코드 — 현대 한글 전부 + 라틴 + 기호
KEEP = []
KEEP += [(0x0020, 0x007E)]          # 기본 라틴
KEEP += [(0x00A0, 0x00FF)]          # 라틴 보충
KEEP += [(0x2010, 0x203A)]          # 문장부호
KEEP += [(0x20A0, 0x20BF)]          # 통화기호(₩)
KEEP += [(0x2190, 0x21FF)]          # 화살표
KEEP += [(0x2200, 0x22FF)]          # 수학기호(×÷)
KEEP += [(0x2460, 0x24FF)]          # 원문자
KEEP += [(0x25A0, 0x25FF)]          # 도형
KEEP += [(0x2600, 0x27BF)]          # 기타 기호
KEEP += [(0x3000, 0x303F)]          # CJK 문장부호
KEEP += [(0x3130, 0x318F)]          # 한글 호환 자모
KEEP += [(0xAC00, 0xD7A3)]          # 현대 한글 음절 11172자 — 전부 남긴다
KEEP += [(0xFF00, 0xFFEF)]          # 전각

def build(src):
    base = os.path.splitext(os.path.basename(src))[0]
    out  = os.path.join(FDIR, base + '.woff2')
    f = TTFont(src, fontNumber=0)
    have = set(f.getBestCmap().keys())
    want = set()
    for a, b in KEEP:
        want |= set(range(a, b + 1))
    uni = sorted(have & want)

    opt = subset.Options()
    opt.layout_features = ['kern', 'liga', 'calt', 'ccmp']
    opt.name_IDs = ['*']
    opt.name_legacy = True
    opt.notdef_outline = True
    opt.recalc_bounds = True
    opt.drop_tables += ['DSIG']
    opt.desubroutinize = False

    s = subset.Subsetter(options=opt)
    s.populate(unicodes=uni)
    s.subset(f)
    f.flavor = 'woff2'
    f.save(out)
    f.close()

    src_kb, out_kb = os.path.getsize(src) / 1024, os.path.getsize(out) / 1024
    g = TTFont(out, lazy=True); cm = g.getBestCmap()
    hangul = sum(1 for c in cm if 0xAC00 <= c <= 0xD7A3); g.close()
    print('  %-22s → %-24s %6.0fKB → %6.0fKB  (%.0f%% 절감)  한글 %d자'
          % (os.path.basename(src), os.path.basename(out), src_kb, out_kb,
             (1 - out_kb / src_kb) * 100, hangul))
    return out

srcs = [p for p in glob.glob(os.path.join(FDIR, '*'))
        if os.path.splitext(p)[1].lower() in ('.ttf', '.otf')]
if not srcs:
    print('fonts/ 에 .ttf/.otf 가 없다.'); sys.exit(1)
print('폰트 변환')
for p in srcs:
    build(p)
print('\n다음: index.html 의 @font-face 와 sw.js 프리캐시에 연결한다.')
