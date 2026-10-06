"""Build dependency-free static pages for GitHub Pages."""
import json, html, re, shutil
from urllib.parse import quote
from pathlib import Path
from datetime import datetime
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '_site'
if OUT.exists(): shutil.rmtree(OUT)
OUT.mkdir()
shutil.copytree(ROOT/'assets', OUT/'assets')
site = json.loads((ROOT/'data/site.json').read_text())
schedule = json.loads((ROOT/'data/schedule.json').read_text())
e = html.escape

def inline(text):
    text = e(text)
    return re.sub(r'\[([^\]]+)\]\((https?://[^\s)]+)\)', r'<a href="\2">\1</a>', text)

def markdown(text):
    parts=[]
    for block in re.split(r'\n\s*\n',text.strip()):
        if block.startswith('## '): parts.append('<h2>'+inline(block[3:])+'</h2>')
        else: parts.append('<p>'+inline(block.replace('\n',' '))+'</p>')
    return ''.join(parts)

posts=[]
for p in (ROOT/'posts').glob('*.md'):
    _,meta,body=p.read_text().split('---',2)
    post=json.loads(meta); post['body']=markdown(body); post['slug']=p.stem
    posts.append(post)
posts.sort(key=lambda p:p['date'],reverse=True)

def page(title,content,depth=0,active='Home',description=None):
    base='../'*depth
    nav=''.join(f'<a href="{base}{url}"'+(' aria-current="page"' if label==active else '')+f'>{label}</a>' for label,url in [('Home','index.html'),('Schedule','schedule.html'),('The Blog','blog.html'),('Contact','index.html#contact')])
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)} | The Fish Box</title><meta name="description" content="{e(description or site['tagline'])}"><meta name="theme-color" content="#102c38"><meta property="og:title" content="{e(title)} | The Fish Box"><meta property="og:description" content="{e(description or site['tagline'])}"><meta property="og:type" content="website"><link rel="icon" href="{base}assets/icon.svg" type="image/svg+xml"><link rel="stylesheet" href="{base}assets/style.css"><script src="{base}assets/app.js" defer></script></head><body><a class="skip" href="#main">Skip to content</a><header class="header"><div class="wrap"><a class="brand" href="{base}index.html"><img src="{base}assets/icon.svg" alt=""><div><strong>THE FISH BOX</strong><small>BATON ROUGE HOCKEY / 225</small></div></a><nav class="nav" aria-label="Main navigation">{nav}</nav></div></header><main id="main">{content}</main><footer class="footer"><div class="wrap"><span>© {datetime.now().year} The Fish Box · Baton Rouge, Louisiana</span><span>An independent fan publication. Not affiliated with the Baton Rouge Kingfish.</span></div></footer></body></html>'''

def card(p,base='',featured=False):
    return f'<article class="card {"featured" if featured else ""}"><div class="eyebrow">{e(p["category"])}</div><a class="article-link" href="{base}articles/{p["slug"]}.html"><h3>{e(p["title"])}</h3></a><p>{e(p["excerpt"])}</p><p class="meta">{e(p["date"])} · {e(p["author"])}</p><a href="{base}articles/{p["slug"]}.html">Read the article →</a></article>'

def games():
    rows=[]
    for g in sorted(schedule['games'],key=lambda g:g['date']+g['time']):
        d=datetime.fromisoformat(g['date']); t=datetime.strptime(g['time'],'%H:%M').strftime('%I:%M %p').lstrip('0'); home=g['home']
        rows.append(f'<li class="game" data-game="{"home" if home else "away"}"><div class="date-box"><small>{d.strftime("%b").upper()}</small>{d.day}</div><div><strong>{"vs." if home else "at"} {e(g["opponent"])}</strong><span class="meta">{d.strftime("%a")} · {t} CT · {e(g["venue"])}</span></div><span class="badge {"" if home else "away"}">{"HOME" if home else "AWAY"}</span></li>')
    return '<ul class="game-list">'+''.join(rows)+'</ul>'

latest=card(posts[0],featured=True) if posts else '<p>First article coming soon.</p>'
contact=(f'<a class="button" href="mailto:{e(site["email"])}">{e(site["email"])} →</a>' if site['email'] else '<div><span class="pill" style="border-color:var(--line)">CONTACT OPENING SOON</span><p class="note" style="margin-top:12px">An inbox for tips, questions, and hockey talk is on the way.</p></div>')
home=f'''<section class="hero"><div class="wrap hero-grid"><div><span class="pill">INDEPENDENT KINGFISH COVERAGE</span><h1>HOCKEY.<br>WITH A<br><span>LOCAL BITE.</span></h1><p>{site['tagline']} Kingfish news, game nights, and a little time in the penalty box.</p><a class="button" href="blog.html">Step into The Fish Box →</a></div><div class="hero-art" aria-hidden="true"><div class="rink"><div class="rink-circle"></div><div class="rink-word"><div>THE<br>FISH BOX<small>BATON ROUGE • 225</small></div></div></div></div></div></section><div class="strip"><div class="wrap"><span>FROM THE STANDS. AFTER THE HORN.</span><span>2026 / 2027 SEASON</span></div></div>
<section class="section wrap"><div class="section-head"><h2>Fresh from the box</h2><a href="blog.html">All articles →</a></div><div class="grid">{latest}<aside class="accent" data-next-game><div class="eyebrow">NEXT LISTED GAME</div><h3 data-opponent>vs. Monroe Moccasins</h3><p data-date>Friday, October 16</p><p class="meta" data-venue>Raising Cane’s River Center</p><a class="button" href="schedule.html">See the schedule →</a><p class="meta" style="margin-top:16px">All game times are Central. Schedule subject to change.</p></aside></div></section>
<section class="section social-section"><div class="wrap social-grid"><div><div class="eyebrow">STRAIGHT FROM THE TEAM</div><h2>Keep your<br>line in the water.</h2><p>Official announcements, team news, and game night updates from the Baton Rouge Kingfish.</p><a class="button outline" href="{e(site['facebook'])}" target="_blank" rel="noopener">Follow the official Facebook page ↗</a><p class="note" style="margin-top:18px">The Fish Box is an independent fan site. Team posts belong to the team.</p></div><div class="social-frame"><h3>Official team feed</h3><p class="note">Live updates from the team’s Facebook page. If the feed is unavailable, use the official page link.</p><iframe title="Official Baton Rouge Kingfish Facebook timeline" src="https://www.facebook.com/plugins/page.php?href={quote(site['facebook'], safe='')}&amp;tabs=timeline&amp;width=500&amp;height=500&amp;small_header=true&amp;adapt_container_width=true&amp;hide_cover=false&amp;show_facepile=false" loading="lazy" referrerpolicy="strict-origin-when-cross-origin"></iframe></div></div></section>
<section class="section wrap"><div class="section-head"><h2>Mark the calendar</h2><a href="schedule.html">Schedule →</a></div>{games()}<p class="note" style="margin-top:18px">{e(schedule['coverage'])}</p></section>
<section id="contact" class="section wrap contact"><div><div class="eyebrow">GOT SOMETHING TO SAY?</div><h2>Talk hockey with me.</h2><p>Story ideas, questions, a different take on the game? There’s room for your voice in The Fish Box.</p></div>{contact}</section><script type="application/json" id="games-data">{json.dumps(schedule['games']).replace('<','\\u003c')}</script>'''
(OUT/'index.html').write_text(page('Baton Rouge Kingfish news & fan takes',home))
(OUT/'schedule.html').write_text(page('Schedule',f'<div class="wrap"><div class="page-title"><div class="eyebrow">2026 / 2027 KINGFISH HOCKEY</div><h1>Make it a game night.</h1><p>{e(schedule["coverage"])}</p><a class="button" href="{e(site["schedule"])}" target="_blank" rel="noopener">Full official schedule ↗</a></div><div class="filters" aria-label="Filter games"><button data-filter="all" aria-pressed="true">All games</button><button data-filter="home" aria-pressed="false">Home</button><button data-filter="away" aria-pressed="false">Away</button></div>{games()}<p class="note" style="margin:24px 0 60px">All times Central. Last verified {schedule["updated"]}. <a href="{e(schedule["source"])}">Schedule source</a>. Confirm details with the team before traveling.</p></div>',active='Schedule'))
(OUT/'blog.html').write_text(page('The Blog', '<div class="wrap"><div class="page-title"><div class="eyebrow">ARTICLES / RECAPS / THE OCCASIONAL RANT</div><h1>From the stands.</h1><p>The conversation doesn’t end at the final horn.</p></div><div class="archive">'+''.join(card(p) for p in posts)+'</div></div>',active='The Blog'))
(OUT/'articles').mkdir()
for p in posts:
    (OUT/'articles'/f'{p["slug"]}.html').write_text(page(p['title'],f'<article class="wrap prose"><a href="../blog.html">← All articles</a><div class="eyebrow" style="margin-top:35px">{e(p["category"])}</div><h1>{e(p["title"])}</h1><p class="meta">{e(p["date"])} · {e(p["author"])}</p>{p["body"]}</article>',depth=1,active='The Blog',description=p['excerpt']))
(OUT/'404.html').write_text(page('Page not found','<section class="section wrap"><h1>Off the ice.</h1><p>That page could not be found.</p><a class="button" href="./index.html">Back to The Fish Box</a></section>'))
(OUT/'.nojekyll').touch()
print(f'Built {len(posts)} articles and {len(schedule["games"])} games into {OUT}')
