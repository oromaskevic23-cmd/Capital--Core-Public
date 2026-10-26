#!/usr/bin/env python3
"""Build two portable, static, multilingual sites without dependencies or deployment."""
from pathlib import Path
from html import escape as esc
import hashlib, json, shutil
from urllib.parse import urlsplit
from xml.etree import ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/'source/content.json').read_text())
LANGS=DATA['languages']
T=DATA['translations']
FOUNDER=DATA['founder_origin']
COMPANY=DATA['ecosystem_origin']
GITHUB=DATA['github']
PHOTO='/assets/alexander-romaskevich-portrait.jpeg'
PERSON_ID=FOUNDER+'/#person'
ORG_ID=COMPANY+'/#organization'
EVIDENCE=GITHUB+'/IMPERIAL-Core-Public/blob/'+DATA['baseline_commit']+'/docs/EVIDENCE.md'
LOCALES={'en':'en_US','uk':'uk_UA','ru':'ru_RU','de':'de_DE','fr':'fr_FR','es':'es_ES','pt':'pt_BR','ja':'ja_JP','zh':'zh_CN','ar':'ar_AR'}

def path(lang):return '/' if lang=='en' else '/'+lang+'/'
def a(url,label,cls='',extra=''):
    return f'<a href="{esc(url,quote=True)}"'+(f' class="{cls}"' if cls else '')+f' {extra}>{esc(label)}</a>'
def graph(kind,lang,url,title,description):
    person={'@type':'Person','@id':PERSON_ID,'name':'Alexander Romaskevich','alternateName':['Александр Николаевич Ромаскевич','Александр Ромаскевич','Олександр Ромаскевич','RomaskevicH'],'url':FOUNDER+'/','image':FOUNDER+PHOTO,'jobTitle':T[lang]['role']+' · IMPERIAL Core','description':T[lang]['bio'],'sameAs':[GITHUB],'affiliation':{'@id':ORG_ID},'knowsAbout':T[lang]['fields']}
    org={'@type':'Organization','@id':ORG_ID,'name':'IMPERIAL Core','url':COMPANY+'/','description':T[lang]['architectureBody'],'founder':{'@id':PERSON_ID},'sameAs':[GITHUB+'/IMPERIAL-Core-Public']}
    base=FOUNDER if kind=='founder' else COMPANY
    page={'@type':'ProfilePage' if kind=='founder' else 'WebPage','@id':url+'#page','url':url,'name':title,'description':description,'inLanguage':lang,'mainEntity':{'@id':PERSON_ID if kind=='founder' else ORG_ID},'isPartOf':{'@id':base+'/#website'}}
    website={'@type':'WebSite','@id':base+'/#website','url':base+'/','name':'Alexander Romaskevich' if kind=='founder' else 'IMPERIAL Core','inLanguage':LANGS,'publisher':{'@id':ORG_ID}}
    return {'@context':'https://schema.org','@graph':[page,person,org,website]}

def projects(lang):
    t=T[lang]
    return ''.join(f'''<article class="project"><div class="project-top"><span class="number">{i:02}</span><span class="source-label">{esc(t['source'])}</span></div><h3>{esc(p['name'])}</h3><p>{esc(p['descriptions'][lang])}</p>{a(p['url'],'GitHub ↗','text-link')}</article>''' for i,p in enumerate(DATA['projects'],1))

def language_menu(lang):
    links=''.join(a(path(l),T[l]['label'],'language-option',f'lang="{l}" hreflang="{l}"'+(' aria-current="page"' if l==lang else '')) for l in LANGS)
    return f'<details class="language-menu"><summary aria-label="{esc(T[lang]["choose"])}"><span aria-hidden="true">◎</span> {esc(T[lang]["label"])} <span class="chevron" aria-hidden="true">⌄</span></summary><nav class="language-panel" aria-label="{esc(T[lang]["lang"])}">{links}</nav></details>'

def header(kind,lang):
    t=T[lang]
    brand='Alexander Romaskevich' if kind=='founder' else 'IMPERIAL Core'
    sub='RomaskevicH' if kind=='founder' else 'Build Software. Verify Everything.'
    logo='AR' if kind=='founder' else 'I'
    return f'''<a class="skip" href="#main">{esc(t['skip'])}</a><header class="header"><a class="brand" href="{path(lang)}"><span class="monogram" aria-hidden="true">{logo}</span><span><strong>{brand}</strong><small>{sub}</small></span></a><nav class="main-nav" aria-label="{esc(t['projects'])}">{a('#about',t['about'] if kind=='founder' else 'IMPERIAL Core')}{a('#projects',t['projects'])}{a('#evidence',t['evidence'])}{a('#contact',t['contact'])}</nav>{language_menu(lang)}</header>'''

def footer(kind,lang):
    t=T[lang];other=(COMPANY if kind=='founder' else FOUNDER)+path(lang)
    return f'''<footer class="footer wrap"><div class="footer-brand"><span class="monogram" aria-hidden="true">{'AR' if kind=='founder' else 'I'}</span><div><strong>{'Alexander Romaskevich' if kind=='founder' else 'IMPERIAL Core'}</strong><p>{esc(t['footer'])}</p></div></div><div class="footer-links">{a(other,t['ecosystem'] if kind=='founder' else t['profile'])}{a(GITHUB,'GitHub ↗')}{a('#top',t['back']+' ↑')}</div><details class="disclosure"><summary>{esc(t['notes'])}</summary><p>{esc(t['disclosure'])}</p></details><p class="copyright">RomaskevicH · IMPERIAL Core · 2026</p></footer>'''

def profile_hero(lang):
    t=T[lang]
    return f'''<section class="profile-hero wrap" id="top"><div class="hero-copy"><p class="eyebrow"><span class="tiny-star" aria-hidden="true">✧</span> RomaskevicH · IMPERIAL Core</p><h1><span>Alexander</span><span>Romaskevich<span class="gold-dot">.</span></span></h1><p class="role">{esc(t['role'])}</p><p class="hero-statement">{esc(t['headline'])}<br><em>{esc(t['accent'])}</em></p><p class="intro">{esc(t['intro'])}</p><div class="actions">{a('#projects',t['projects']+' ↗','button primary')}{a(COMPANY+path(lang),t['ecosystem']+' →','button secondary')}</div><p class="signature">RomaskevicH</p></div><figure class="portrait hero-portrait"><div class="portrait-frame"><img src="{PHOTO}" width="1122" height="1402" alt="{esc(t['photo'])}" fetchpriority="high" decoding="async"></div><figcaption><span>{esc(t['name'])}</span><span>IMPERIAL Core</span></figcaption><span class="corner top-left" aria-hidden="true"></span><span class="corner bottom-right" aria-hidden="true"></span></figure></section>'''

def company_hero(lang):
    t=T[lang]
    pillars=''.join(f'<a class="pillar" href="{esc(p["url"],quote=True)}"><span class="pillar-index" aria-hidden="true">0{i} /</span><strong>{esc(p["name"])}</strong><p>{esc(p["descriptions"][lang])}</p><span class="pillar-arrow" aria-hidden="true">↗</span></a>' for i,p in enumerate([DATA['projects'][1],DATA['projects'][2],DATA['projects'][5]],1))
    return f'''<section class="company-hero" id="top"><div class="wrap company-hero-inner"><div class="hero-copy"><p class="eyebrow"><span class="system-dot" aria-hidden="true"></span> IMPERIAL Core · RomaskevicH</p><h1>{esc(t['companyHeadline'])}<br><em>{esc(t['companyAccent'])}</em></h1><p class="intro">{esc(t['companyIntro'])}</p><div class="actions">{a('#projects',t['projects']+' ↗','button primary')}{a(FOUNDER+path(lang),t['profile']+' →','button secondary')}</div></div><div class="company-pillars">{pillars}</div></div><div class="principles wrap"><span>Federated Multi-Orchestrator Architecture</span><span>Identity ≠ Authority</span><span>Evidence First</span></div></section>'''

def body(kind,lang):
    t=T[lang]
    hero=profile_hero(lang) if kind=='founder' else company_hero(lang)
    fields=''.join(f'<li>{esc(x)}</li>' for x in t['fields'])
    if kind=='founder':
        about=f'''<section class="section wrap about-grid" id="about"><div><p class="eyebrow">01 / {esc(t['about'])}</p><h2>{esc(t['aboutTitle'])}</h2><p class="identity-line">Alexander Romaskevich<br>Александр Николаевич Ромаскевич<br>Олександр Ромаскевич</p></div><div class="prose"><p class="lead">{esc(t['bio'])}</p><p>{esc(t['bio2'])}</p><p class="field-label">{esc(t['fieldLabel'])}</p><ul class="fields">{fields}</ul></div></section>'''
    else:
        about=f'''<section class="section wrap about-grid" id="about"><div><p class="eyebrow">01 / IMPERIAL Core</p><h2>{esc(t['architecture'])}</h2></div><div class="prose"><p class="lead">{esc(t['architectureBody'])}</p><p>{esc(t['governanceBody'])}</p><ul class="fields">{fields}</ul></div></section>'''
    catalog=f'''<section class="section wrap" id="projects"><div class="section-heading"><div><p class="eyebrow">02 / {esc(t['projects'])}</p><h2>{esc(t['catalog'])}</h2></div><p>{esc(t['catalogIntro'])}</p></div><div class="project-grid">{projects(lang)}</div></section>'''
    evidence=f'''<section class="section wrap" id="evidence"><div class="evidence-panel"><div class="evidence-symbol" aria-hidden="true">↗</div><div><p class="eyebrow">03 / {esc(t['evidence'])}</p><h2>{esc(t['evidenceTitle'])}</h2><p>{esc(t['evidenceBody'])}</p>{a(EVIDENCE,t['evidenceLink']+' ↗','button primary')}</div></div></section>'''
    if kind=='founder':
        further=f'''<section class="section wrap governance-grid"><div><p class="eyebrow">IMPERIAL Core</p><h2>{esc(t['governance'])}</h2><p>{esc(t['governanceBody'])}</p>{a(COMPANY+path(lang),t['ecosystem']+' →','text-link')}</div><div class="architecture-card"><p class="eyebrow">ARCHITECTURE</p><h3>{esc(t['architecture'])}</h3><p>{esc(t['architectureBody'])}</p><div class="architecture-names"><span>HANTER</span><span>LEGION / Nano Core Agents</span><span>ORION</span><span>VELION MAX</span></div></div></section>'''
    else:
        further=f'''<section class="section wrap company-founder"><figure class="portrait compact"><div class="portrait-frame"><img src="{PHOTO}" alt="{esc(t['photo'])}" width="1122" height="1402" loading="lazy" decoding="async"></div><figcaption>Alexander Romaskevich — RomaskevicH</figcaption></figure><div><p class="eyebrow">RomaskevicH · IMPERIAL Core</p><h2>{esc(t['founderTitle'])}</h2><p class="founder-name">{esc(t['name'])}</p><p class="role">{esc(t['role'])}</p><p>{esc(t['bio'])}</p><p class="identity-line">Alexander Romaskevich · Александр Николаевич Ромаскевич · Олександр Ромаскевич</p>{a(FOUNDER+path(lang),t['profile']+' ↗','button primary')}</div></section>'''
    crypto=f'''<section class="section wrap crypto-section"><div><p class="eyebrow">CRYPTO IMPERIAL Ecosystem</p><h2>{esc(t['cryptoTitle'])}</h2></div><div><p>{esc(t['crypto'])}</p>{a(GITHUB+'/CRYPTO-IMPERIAL-Ecosystem-Public',t['read']+' ↗','text-link')}</div></section>'''
    contact=f'''<section class="section wrap contact-section" id="contact"><p class="eyebrow">04 / {esc(t['contact'])}</p><h2>{esc(t['contactTitle'])}</h2><p>{esc(t['contactBody'])}</p><div class="actions">{a(GITHUB,'GitHub · RomaskevicH ↗','button primary')}{a(GITHUB+'/IMPERIAL-Core-Public/issues',t['issues']+' ↗','button secondary')}</div></section>'''
    return hero+about+catalog+evidence+further+crypto+contact

def page(kind,lang):
    t=T[lang];base=FOUNDER if kind=='founder' else COMPANY;url=base+path(lang)
    title=("Alexander Romaskevich — Founder of IMPERIAL Core" if lang=='en' else f"{t['name']} — {t['profile']} | IMPERIAL Core") if kind=='founder' else 'IMPERIAL Core — '+t['companyHeadline']+' '+t['companyAccent']
    desc=t['intro'] if kind=='founder' else t['companyIntro']
    alternates='\n'.join(f'<link rel="alternate" hreflang="{l}" href="{base+path(l)}">' for l in LANGS)+f'\n<link rel="alternate" hreflang="x-default" href="{base}/">'
    js=json.dumps(graph(kind,lang,url,title,desc),ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
    image=base+PHOTO
    html = f'''<!doctype html>
<html lang="{lang}" dir="{'rtl' if lang=='ar' else 'ltr'}">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)}</title><meta name="description" content="{esc(desc,quote=True)}"><meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="{url}">
{alternates}
<meta property="og:type" content="{'profile' if kind=='founder' else 'website'}"><meta property="og:site_name" content="{'Alexander Romaskevich' if kind=='founder' else 'IMPERIAL Core'}"><meta property="og:title" content="{esc(title,quote=True)}"><meta property="og:description" content="{esc(desc,quote=True)}"><meta property="og:url" content="{url}"><meta property="og:locale" content="{LOCALES[lang]}"><meta property="og:image" content="{image}"><meta property="og:image:alt" content="{esc(t['photo'],quote=True)}"><meta property="og:image:width" content="1122"><meta property="og:image:height" content="1402"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(title,quote=True)}"><meta name="twitter:description" content="{esc(desc,quote=True)}"><meta name="twitter:image" content="{image}"><meta name="author" content="Alexander Romaskevich"><meta name="theme-color" content="{'#071018' if kind=='founder' else '#f4f2eb'}"><link rel="icon" href="/assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/assets/site.css"><script src="/assets/site.js" defer></script><script type="application/ld+json">{js}</script></head>
<body class="{kind}">{header(kind,lang)}<main id="main">{body(kind,lang)}</main>{footer(kind,lang)}</body></html>\n'''
    # Project Pages lives below /repository/. Apply its base path to local
    # navigation and assets while preserving full canonical/entity URLs.
    prefix=urlsplit(base).path.rstrip('/')
    return html.replace('href="/', f'href="{prefix}/').replace('src="/', f'src="{prefix}/')

def sitemap(kind):
    base=FOUNDER if kind=='founder' else COMPANY
    sm='http://www.sitemaps.org/schemas/sitemap/0.9';xh='http://www.w3.org/1999/xhtml';im='http://www.google.com/schemas/sitemap-image/1.1'
    ET.register_namespace('',sm);ET.register_namespace('xhtml',xh);ET.register_namespace('image',im)
    root=ET.Element('{'+sm+'}urlset')
    for l in LANGS:
        u=ET.SubElement(root,'{'+sm+'}url');ET.SubElement(u,'{'+sm+'}loc').text=base+path(l)
        for alt in LANGS+['x-default']:ET.SubElement(u,'{'+xh+'}link',{'rel':'alternate','hreflang':alt,'href':base+path('en' if alt=='x-default' else alt)})
        image=ET.SubElement(u,'{'+im+'}image');ET.SubElement(image,'{'+im+'}loc').text=base+PHOTO
    return ET.tostring(root,encoding='unicode',xml_declaration=True)+'\n'

def main():
    source=ROOT/'assets/alexander-romaskevich-portrait.jpeg'
    assert hashlib.sha256(source.read_bytes()).hexdigest()==DATA['photo_sha256'],'Portrait bytes changed'
    for kind in ['founder','ecosystem']:
        out=ROOT/kind/'dist'
        if out.exists(): shutil.rmtree(out)
        out.mkdir(parents=True)
        shutil.copytree(ROOT/'assets',out/'assets',dirs_exist_ok=True)
        for lang in LANGS:
            dest=out/('' if lang=='en' else lang);dest.mkdir(exist_ok=True)
            (dest/'index.html').write_text(page(kind,lang),encoding='utf-8')
        base=FOUNDER if kind=='founder' else COMPANY
        (out/'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {base}/sitemap.xml\n')
        (out/'sitemap.xml').write_text(sitemap(kind))
        (out/'.nojekyll').touch()
        (out/'404.html').write_text(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>Page not found</title></head><body><main><h1>Page not found</h1><a href="{base}/">Home</a></main></body></html>\n')
        (ROOT/kind/'.gitignore').write_text('.netlify/\n.openai/\n')
        records=[{'path':p.relative_to(out).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size} for p in sorted(out.rglob('*')) if p.is_file()]
        (ROOT/kind/'publication-manifest.json').write_text(json.dumps({'artifact_status':'BUILT','publication_evidence':'../evidence/live-verification.json','hosting':'GitHub Pages','canonical_origin':base,'files':records},indent=2)+'\n')
        print(kind,len(LANGS),'localized pages;',sum(x['bytes'] for x in records),'bytes total')
if __name__=='__main__':main()
