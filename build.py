#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
canpass-training-site ビルダー。
研修/運用ガイドの pptx→PDF→JPG を assets/ に書き出し、
自己完結HTMLスライド（矢印キー操作・外部依存なし・noindex・PWゲート）を生成する。

前提: 各pptxを soffice でPDF化済み（intermediate/qa/*.pdf）、PyMuPDF(fitz) 利用可。
再生成: python3 build.py
"""
import os, glob, fitz

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC_PDF = os.path.expanduser("~/work/cancer/intermediate/qa")
PASSWORD = "CanPass"  # ※クライアント側の軽いゲート（限定URL+noindexと併用）。真のアクセス制御ではない。

DECKS = [
    {"key": "worker", "title": "CanPass はたらき方研修（ワーカー向け）",
     "pdf": "20260612_canpass-worker-training_v1.pdf", "note": "従事者教育用・敲き"},
    {"key": "admin", "title": "CanPass 運用ガイド（PM/運用向け）",
     "pdf": "20260612_canpass-admin-ops-guide_v2.pdf", "note": "L2・経営幹部/PM限定・敲き"},
]


def render(deck):
    out = os.path.join(ROOT, "assets", deck["key"])
    for f in glob.glob(os.path.join(out, "*.jpg")):
        os.remove(f)
    d = fitz.open(os.path.join(SRC_PDF, deck["pdf"]))
    n = d.page_count
    for i in range(n):
        d[i].get_pixmap(matrix=fitz.Matrix(1.6, 1.6)).save(os.path.join(out, f"{i+1:02d}.jpg"))
    d.close()
    return n


HEAD = """<!doctype html><html lang="ja"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow"><title>{title}</title>
<style>
:root{{--bg:#0f1c2e;--ink:#16263f;--muted:#6b7c92;--line:#d6e0ec;--accent:#2455a4}}
*{{box-sizing:border-box}}html,body{{margin:0;height:100%}}
body{{background:var(--bg);font-family:'Hiragino Kaku Gothic ProN',sans-serif;color:#fff;overflow:hidden}}
#gate{{position:fixed;inset:0;background:#0f1c2e;display:flex;align-items:center;justify-content:center;z-index:10}}
#gate .box{{background:#fff;color:var(--ink);padding:28px 26px;border-radius:14px;max-width:340px;width:88%;text-align:center;box-shadow:0 10px 40px rgba(0,0,0,.4)}}
#gate h1{{font-size:18px;margin:0 0 4px}}#gate p{{font-size:12px;color:var(--muted);margin:0 0 16px}}
#gate input{{width:100%;padding:11px 12px;border:1px solid var(--line);border-radius:8px;font-size:15px;margin-bottom:10px}}
#gate button{{width:100%;padding:11px;border:0;border-radius:8px;background:var(--accent);color:#fff;font-size:15px;cursor:pointer}}
#gate .err{{color:#b23b3b;font-size:12px;height:14px;margin-top:6px}}
#app{{display:none;height:100%;flex-direction:column}}
#stage{{flex:1;display:flex;align-items:center;justify-content:center;min-height:0;padding:14px}}
#stage img{{max-width:100%;max-height:100%;border-radius:6px;box-shadow:0 6px 30px rgba(0,0,0,.5)}}
#bar{{display:flex;align-items:center;justify-content:center;gap:18px;padding:8px 14px;background:#0b1626;font-size:13px;color:#9fb1c8}}
#bar button{{background:#1c3257;color:#fff;border:0;border-radius:6px;padding:7px 14px;font-size:14px;cursor:pointer}}
#bar a{{color:#9fb1c8;text-decoration:none;font-size:12px}}
#count{{min-width:64px;text-align:center}}
</style></head><body>
<div id="gate"><form class="box" onsubmit="return unlock(event)">
<h1>CanPass 資料</h1><p>{note}<br>閲覧パスワードを入力してください</p>
<input id="pw" type="password" autocomplete="off" placeholder="パスワード" autofocus>
<button type="submit">開く</button><div class="err" id="err"></div></form></div>
<div id="app">
<div id="stage"><img id="slide" alt="slide"></div>
<div id="bar">
<a href="./index.html">← 一覧</a>
<button onclick="go(-1)">‹ 前</button><span id="count"></span><button onclick="go(1)">次 ›</button>
<span style="color:#5d7characters">{title}</span>
</div></div>
<script>
var N={n},i=0,dir="assets/{key}/";
function pad(x){{return (x<10?'0':'')+x}}
function show(){{document.getElementById('slide').src=dir+pad(i+1)+'.jpg';document.getElementById('count').textContent=(i+1)+' / '+N}}
function go(d){{i=Math.max(0,Math.min(N-1,i+d));show()}}
function open_(){{document.getElementById('gate').style.display='none';document.getElementById('app').style.display='flex';show()}}
function unlock(e){{e.preventDefault();if(document.getElementById('pw').value==='{password}'){{sessionStorage.setItem('cp_ok','1');open_()}}else{{document.getElementById('err').textContent='パスワードが違います'}}return false}}
if(sessionStorage.getItem('cp_ok')==='1'){{open_()}}
document.addEventListener('keydown',function(e){{if(document.getElementById('app').style.display==='none')return;if(e.key==='ArrowRight'||e.key===' ')go(1);if(e.key==='ArrowLeft')go(-1)}});
document.getElementById('stage').addEventListener('click',function(){{go(1)}});
</script></body></html>"""


def write_deck(deck, n):
    html = HEAD.format(title=deck["title"], note=deck["note"], n=n, key=deck["key"], password=PASSWORD)
    # 軽微なtypo保険
    html = html.replace("#5d7characters", "#5d7088")
    with open(os.path.join(ROOT, deck["key"] + ".html"), "w", encoding="utf-8") as f:
        f.write(html)


INDEX = """<!doctype html><html lang="ja"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow"><title>CanPass 研修・運用資料</title>
<style>
:root{{--bg:#0f1c2e;--ink:#16263f;--muted:#6b7c92;--line:#d6e0ec;--accent:#2455a4;--amber:#c95001}}
*{{box-sizing:border-box}}body{{margin:0;min-height:100vh;background:var(--bg);font-family:'Hiragino Kaku Gothic ProN',sans-serif;color:#fff;display:flex;align-items:center;justify-content:center;padding:24px}}
#gate{{position:fixed;inset:0;background:#0f1c2e;display:flex;align-items:center;justify-content:center;z-index:10}}
.box{{background:#fff;color:var(--ink);padding:28px 26px;border-radius:14px;max-width:340px;width:88%;text-align:center;box-shadow:0 10px 40px rgba(0,0,0,.4)}}
.box h1{{font-size:18px;margin:0 0 4px}}.box p{{font-size:12px;color:var(--muted);margin:0 0 16px}}
.box input{{width:100%;padding:11px 12px;border:1px solid var(--line);border-radius:8px;font-size:15px;margin-bottom:10px}}
.box button{{width:100%;padding:11px;border:0;border-radius:8px;background:var(--accent);color:#fff;font-size:15px;cursor:pointer}}
.err{{color:#b23b3b;font-size:12px;height:14px;margin-top:6px}}
#app{{display:none;max-width:680px;width:100%}}
.kicker{{color:#9fb1c8;font-size:12px;letter-spacing:.12em}}
h2{{font-size:26px;margin:6px 0 2px}}.sub{{color:#9fb1c8;font-size:13px;margin-bottom:22px}}
.card{{display:block;background:#16365c;border:1px solid #25446c;border-radius:12px;padding:18px 20px;margin-bottom:14px;text-decoration:none;color:#fff}}
.card:hover{{background:#1c3f6e}}
.card .t{{font-size:17px;font-weight:700}}.card .d{{font-size:12px;color:#9fb1c8;margin-top:4px}}
.tag{{display:inline-block;font-size:11px;padding:2px 8px;border-radius:10px;background:#0b1626;color:#9fb1c8;margin-left:8px}}
.foot{{color:#6b7c92;font-size:11px;margin-top:18px;line-height:1.7}}
</style></head><body>
<div id="gate"><form class="box" onsubmit="return unlock(event)">
<h1>CanPass 研修・運用資料</h1><p>関係者限定（L2・敲き）<br>閲覧パスワードを入力してください</p>
<input id="pw" type="password" autocomplete="off" placeholder="パスワード" autofocus>
<button type="submit">開く</button><div class="err" id="err"></div></form></div>
<div id="app">
<div class="kicker">CANPASS ｜ 関係者限定</div>
<h2>研修・運用資料</h2>
<div class="sub">2026-06 ｜ いずれも最終版ではなく敲き。配布前に久保監修＋代表承認。</div>
<a class="card" href="./worker.html"><div class="t">① CanPass はたらき方研修<span class="tag">ワーカー向け</span></div><div class="d">人×AI／1日の流れ／Claude／アナログ撮影検品／スマホ参画／守ること（全31枚）</div></a>
<a class="card" href="./admin.html"><div class="t">② CanPass 運用ガイド<span class="tag">PM/運用向け・L2</span></div><div class="d">運用モデル／記録／体調連動アサイン／成果物単位／スマホ3レイヤー／Human Gate／レベル制（全33枚）</div></a>
<div class="foot">取り扱い注意：本資料はL2機密・関係者限定。限定URL運用（推測されにくいだけでアクセス制御ではない）＋noindex。医療系の生データ・実名・録画は本サイトに含めない。社外提示前に要精査（PM→代表）。</div>
</div>
<script>
function unlock(e){{e.preventDefault();if(document.getElementById('pw').value==='{password}'){{sessionStorage.setItem('cp_ok','1');document.getElementById('gate').style.display='none';document.getElementById('app').style.display='block'}}else{{document.getElementById('err').textContent='パスワードが違います'}}return false}}
if(sessionStorage.getItem('cp_ok')==='1'){{document.getElementById('gate').style.display='none';document.getElementById('app').style.display='block'}}
</script></body></html>"""


def main():
    counts = {}
    for deck in DECKS:
        n = render(deck)
        write_deck(deck, n)
        counts[deck["key"]] = n
        print(f"{deck['key']}: {n} slides")
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
        f.write(INDEX.format(password=PASSWORD))
    print("index.html written")


if __name__ == "__main__":
    main()
