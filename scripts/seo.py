"""Author profile and search metadata for the static publication."""
import json
from html import escape as e
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape

def enhance(out, posts, page):
    origin = 'https://fishbox225.com'
    author_url = origin + '/jordan-tupper.html'
    person = {'@type': 'Person', '@id': author_url + '#person', 'name': 'Jordan Tupper', 'url': author_url,
              'description': 'Baton Rouge musician, Night Hog bassist, and creator of The Fish Box, an independent Kingfish fan publication.',
              'sameAs': ['https://jordantupper.com/', 'https://jordantuppermusic.com/', 'https://www.youtube.com/@jordanjtupper', 'https://www.linkedin.com/in/jordantupper225/', 'https://www.facebook.com/jordantuppermusic']}
    publisher = {'@type': 'Organization', '@id': origin + '/#publication', 'name': 'The Fish Box', 'url': origin + '/', 'founder': {'@id': person['@id']}}
    bio = '''<article class="wrap prose"><div class="eyebrow">MEET THE PERSON BEHIND THE FISH BOX</div>
<h1>Jordan Tupper</h1><p class="profile-lead">Baton Rouge musician. Hockey fan. Creator of The Fish Box.</p>
<p>I’m Jordan Tupper, and The Fish Box is where I write about Baton Rouge Kingfish hockey from a fan’s seat. You’ll find game recaps, roster questions, predictions, and the occasional opinion about the food at the River Center.</p>
<p>For the Kingfish home opener, my father in law and I sat in section 110. Better food, solid hockey, and a win made for a pretty good evening. That’s the perspective I bring here: someone who enjoys going to games and wants to keep talking hockey afterward.</p>
<h2>What I write about</h2><p>I follow the Kingfish through the season, from offseason signings to the final horn. Some articles look at player performances and team news. Others are about the experience of being a hockey fan in Baton Rouge. Predictions are opinions, and when something is still uncertain, I’ll say so.</p>
<p>The Fish Box is an independent fan publication. It is not affiliated with the Baton Rouge Kingfish or the FPHL. Team announcements and game reports help inform the coverage, while the commentary reflects my own perspective.</p>
<h2>Outside the rink</h2><p>I’m also a musician based in Baton Rouge, Louisiana. I play bass with Night Hog and am available for freelance gigs across genres on upright and electric bass. My music website has more about that side of my work.</p>
<h2>My websites and projects</h2><div class="profile-links">
<p><a href="https://jordantupper.com/">JordanTupper.com</a><br>My main personal website and a starting point for my work and projects.</p>
<p><a href="https://jordantuppermusic.com/">Jordan Tupper Music</a><br>My music, bass playing, and freelance performance information.</p>
<p><a href="https://www.nighthogbr.com/">Night Hog</a><br>The Baton Rouge band I play bass with. Visit for band information and upcoming shows.</p>
<p><a href="https://tuppertravel.com/">Tupper Travel</a><br>My travel planning website.</p>
<p><a href="https://thinksday.org/">Thinksday</a><br>Weekly reflections by my father, Nat Tupper. I build and maintain the website.</p></div>
<h2>Connect with me</h2><p><a rel="me" href="https://www.youtube.com/@jordanjtupper">Jordan Tupper on YouTube</a> · <a rel="me" href="https://www.linkedin.com/in/jordantupper225/">LinkedIn</a> · <a rel="me" href="https://www.facebook.com/jordantuppermusic">Jordan Tupper Music on Facebook</a></p>
<p>For Fish Box story ideas, corrections, or hockey conversation, email <a href="mailto:Contact@fishbox225.com">Contact@fishbox225.com</a>.</p>
<h2>Articles by Jordan Tupper</h2><div class="author-articles">'''
    for p in posts:
        bio += f'<p><a href="articles/{e(p["slug"])}.html">{e(p["title"])}</a><br><span class="meta">{e(p["date"])}</span><br>{e(p["excerpt"])}</p>'
    bio += '</div></article>'
    (out/'jordan-tupper.html').write_text(page('Jordan Tupper | Baton Rouge Writer & Musician', bio, active='About Jordan', description='Meet Jordan Tupper, creator of The Fish Box, Baton Rouge Kingfish fan writer and Night Hog bassist. Read his articles and explore his music, websites and social profiles.'))
    by_slug = {p['slug']: p for p in posts}
    urls = []
    for path in out.rglob('*.html'):
        rel = path.relative_to(out).as_posix()
        depth = '../' if rel.startswith('articles/') else ''
        doc = path.read_text()
        doc = doc.replace('<nav class="nav" aria-label="Main navigation">', '<nav class="nav" aria-label="Main navigation">')
        doc = doc.replace('</nav>', f'<a href="{depth}jordan-tupper.html"'+(' aria-current="page"' if rel=='jordan-tupper.html' else '')+'>About Jordan</a></nav>')
        doc = doc.replace(' · The Fish Box</p>', f' · <a rel="author" href="{depth}jordan-tupper.html">Jordan Tupper</a></p>')
        doc = doc.replace('The Fish Box · Baton Rouge, Louisiana</span>', f'The Fish Box · Baton Rouge, Louisiana · <a href="{depth}jordan-tupper.html">By Jordan Tupper</a></span>')
        if rel == '404.html':
            doc = doc.replace('</head>', '<meta name="robots" content="noindex"></head>')
            path.write_text(doc)
            continue
        url = origin + ('/' if rel=='index.html' else '/' + rel)
        urls.append(url)
        graph = [person, publisher, {'@type':'WebSite','@id':origin+'/#website','url':origin+'/','name':'The Fish Box','publisher':{'@id':publisher['@id']}}]
        if rel == 'jordan-tupper.html':
            graph.append({'@type':'ProfilePage','@id':url+'#webpage','url':url,'name':'Jordan Tupper','mainEntity':{'@id':person['@id']}})
        elif rel.startswith('articles/'):
            p = by_slug[path.stem]
            graph.append({'@type':'BlogPosting','@id':url+'#article','url':url,'mainEntityOfPage':url,'headline':p['title'],'description':p['excerpt'],'datePublished':p['date'],'author':{'@type':'Person','@id':person['@id'],'name':'Jordan Tupper','url':author_url},'publisher':{'@id':publisher['@id']},'inLanguage':'en-US'})
            graph.append({'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'The Fish Box','item':origin+'/'},{'@type':'ListItem','position':2,'name':'The Blog','item':origin+'/blog.html'},{'@type':'ListItem','position':3,'name':p['title'],'item':url}]})
            doc = doc.replace('property="og:type" content="website"', 'property="og:type" content="article"')
        metadata = f'<link rel="canonical" href="{e(url)}"><meta property="og:url" content="{e(url)}"><meta property="og:site_name" content="The Fish Box"><meta name="twitter:card" content="summary"><meta name="author" content="Jordan Tupper">'
        metadata += '<script type="application/ld+json">'+json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False).replace('<','\\u003c')+'</script>'
        doc = doc.replace('</head>', metadata+'</head>')
        path.write_text(doc)
    (out/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+xml_escape(url)+'</loc></url>' for url in sorted(urls))+'</urlset>')
    (out/'robots.txt').write_text('User-agent: *\nAllow: /\n\nSitemap: '+origin+'/sitemap.xml\n')
