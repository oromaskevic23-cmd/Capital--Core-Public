#!/usr/bin/env python3
"""Offline release gate: actual HTML, links, entity graph, locales and bytes."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, urljoin, unquote
from xml.etree import ElementTree as ET
import hashlib
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / 'source/content.json').read_text())
BASES = {kind: DATA[kind + '_origin'] for kind in ('founder', 'ecosystem')}
LANGS = ['en', 'uk', 'ru', 'de', 'fr', 'es', 'pt', 'ja', 'zh', 'ar']

class Document(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.tags = []; self.visible = []; self.jsonld = []; self.capture = None
        self.scripts = []; self.h1 = 0; self.ids = []
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        a = dict(attrs); self.tags.append((tag, a))
        if tag == 'h1': self.h1 += 1
        if 'id' in a: self.ids.append(a['id'])
        if tag == 'script':
            self.capture = a.get('type', 'script'); self.scripts.append(a)
        if tag == 'style': self.capture = 'style'
    def handle_endtag(self, tag):
        if tag in ('script', 'style'): self.capture = None
    def handle_data(self, data):
        if self.capture == 'application/ld+json': self.jsonld.append(json.loads(data))
        elif not self.capture: self.visible.append(data)
    def select(self, tag, **attrs):
        return [a for t, a in self.tags if t == tag and all(a.get(k) == v for k,v in attrs.items())]

def url(kind, lang):
    return BASES[kind] + ('/' if lang == 'en' else '/' + lang + '/')

def file_for(u):
    for kind, base in BASES.items():
        if u.startswith(base + '/'):
            relative = unquote(urlsplit(u[len(base) + 1:]).path)
            p = ROOT / kind / 'dist' / relative
            return p / 'index.html' if p.is_dir() else p
    return None

PAGES = {(kind, lang): Document(file_for(url(kind, lang)).read_text())
         for kind in BASES for lang in LANGS}

class ReleaseGate(unittest.TestCase):
    def test_01_metadata_and_semantic_html(self):
        titles = []
        for (kind, lang), d in PAGES.items():
            with self.subTest(kind=kind, lang=lang):
                html = d.select('html')[0]
                self.assertEqual(html['lang'], lang)
                self.assertEqual(html['dir'], 'rtl' if lang == 'ar' else 'ltr')
                self.assertEqual(d.h1, 1)
                self.assertEqual(len(d.ids), len(set(d.ids)))
                self.assertEqual(len(d.select('main')), 1)
                self.assertEqual(d.select('link', rel='canonical')[0]['href'], url(kind, lang))
                self.assertIn('index,follow', d.select('meta', name='robots')[0]['content'])
                self.assertTrue(d.select('meta', name='description')[0]['content'])
                self.assertEqual(d.select('meta', property='og:url')[0]['content'], url(kind, lang))
                self.assertIn('Alexander Romaskevich', ' '.join(d.visible))
                self.assertIn('Александр Николаевич Ромаскевич', ' '.join(d.visible))
                self.assertEqual(len(d.select('title')), 1)
                title = re.search(r'<title>(.*?)</title>', file_for(url(kind,lang)).read_text()).group(1)
                titles.append(title)
        self.assertEqual(len(titles), len(set(titles)))

    def test_02_reciprocal_hreflang(self):
        for (kind,lang), d in PAGES.items():
            expected = {l: url(kind,l) for l in LANGS}
            expected['x-default'] = url(kind,'en')
            actual = {x['hreflang']: x['href'] for x in d.select('link',rel='alternate')}
            self.assertEqual(actual, expected)
            menu = {x['hreflang'] for x in d.select('a') if 'hreflang' in x}
            self.assertEqual(menu, set(LANGS))

    def test_03_entity_graph_and_truth_boundary(self):
        person_id = BASES['founder'] + '/#person'
        org_id = BASES['ecosystem'] + '/#organization'
        for (kind, lang), d in PAGES.items():
            self.assertEqual(len(d.jsonld),1)
            graph=d.jsonld[0]
            self.assertEqual(graph['@context'],'https://schema.org')
            nodes={n['@type']:n for n in graph['@graph']}
            person=nodes['Person']; org=nodes['Organization']
            self.assertEqual(person['@id'],person_id)
            self.assertEqual(person['name'],'Alexander Romaskevich')
            self.assertEqual(person['sameAs'],[DATA['github']])
            self.assertEqual(person['affiliation']['@id'],org_id)
            self.assertEqual(org['founder']['@id'],person_id)
            page=nodes['ProfilePage' if kind=='founder' else 'WebPage']
            self.assertEqual(page['mainEntity']['@id'],person_id if kind=='founder' else org_id)
            self.assertEqual(page['inLanguage'],lang)
            text=' '.join(d.visible)
            self.assertIn(person['description'],text)
            self.assertIn(org['description'],text)
            self.assertTrue(all(field in text for field in person['knowsAbout']))
            for banned in ['taxID','vatID','leiCode','award','aggregateRating','review','birthDate','address']:
                self.assertNotIn(banned,json.dumps(graph))

    def test_04_all_internal_links_assets_and_fragments(self):
        for (kind,lang),d in PAGES.items():
            current=url(kind,lang)
            for tag,a in d.tags:
                for attr in ['href','src']:
                    if attr not in a: continue
                    target=urljoin(current,a[attr]); parsed=urlsplit(target)
                    self.assertEqual(parsed.scheme,'https')
                    p=file_for(target)
                    if p is None: continue
                    self.assertTrue(p.is_file(), target)
                    if parsed.fragment:
                        self.assertIn(parsed.fragment,Document(p.read_text()).ids,target)
        css=(ROOT/'assets/site.css').read_text()
        self.assertNotIn("url('/",css)
        self.assertNotIn('url("/',css)
        for resource in re.findall(r'url\([\'"]?([^\'"\)]+)',css):
            self.assertTrue((ROOT/'assets'/resource).is_file(),resource)

    def test_05_sitemap_matches_every_page(self):
        ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9','x':'http://www.w3.org/1999/xhtml','i':'http://www.google.com/schemas/sitemap-image/1.1'}
        for kind,base in BASES.items():
            root=ET.parse(ROOT/kind/'dist/sitemap.xml').getroot()
            entries=root.findall('s:url',ns)
            self.assertEqual({x.find('s:loc',ns).text for x in entries},{url(kind,l) for l in LANGS})
            self.assertEqual(len(entries),10)
            for entry in entries:
                self.assertEqual(len(entry.findall('x:link',ns)),11)
                image=entry.find('i:image/i:loc',ns).text
                self.assertTrue(file_for(image).is_file())

    def test_06_portrait_manifest_and_publish_allowlist(self):
        allowed={'.html','.css','.js','.svg','.jpeg','.jpg','.xml','.txt'}
        for kind in BASES:
            dist=ROOT/kind/'dist'
            self.assertEqual(hashlib.sha256((dist/'assets/alexander-romaskevich-portrait.jpeg').read_bytes()).hexdigest(), DATA['photo_sha256'])
            manifest=json.loads((ROOT/kind/'publication-manifest.json').read_text())
            files={p.relative_to(dist).as_posix():p for p in dist.rglob('*') if p.is_file()}
            self.assertEqual(set(files),{x['path'] for x in manifest['files']})
            for record in manifest['files']:
                p=files[record['path']]
                self.assertTrue(p.name=='.nojekyll' or p.suffix in allowed)
                self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),record['sha256'])
                self.assertEqual(p.stat().st_size,record['bytes'])

    def test_07_complete_translations_and_no_secret_patterns(self):
        en=set(DATA['translations']['en'])
        for lang in LANGS:
            t=DATA['translations'][lang]
            self.assertEqual(set(t),en)
            self.assertTrue(all(bool(v) for v in t.values()))
            if lang!='en': self.assertNotEqual(t['intro'], DATA['translations']['en']['intro'])
        secrets=re.compile(r'gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,}|AKIA[0-9A-Z]{16}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----')
        for kind in BASES:
            for p in (ROOT/kind/'dist').rglob('*'):
                if p.is_file() and p.suffix not in ['.jpg','.jpeg']:
                    text=p.read_text()
                    self.assertIsNone(secrets.search(text), str(p))
                    self.assertNotIn('chatgpt.site',text)
                    self.assertNotIn('netlify.app',text)
                    self.assertNotIn('$14',text)
                    self.assertNotIn('google-site-verification',text)

    def test_08_no_tracking_or_javascript_only_content(self):
        for d in PAGES.values():
            self.assertEqual(len(d.select('main')),1)
            self.assertEqual(len(d.select('article')),9)
            for project in DATA['projects']:
                self.assertIn(project['name'],' '.join(d.visible))
            self.assertFalse(d.select('iframe'))
            self.assertFalse(d.select('form'))
            scripts=[s for s in d.scripts if s.get('type')!='application/ld+json']
            self.assertEqual(len(scripts),1)
            self.assertTrue(scripts[0]['src'].endswith('/assets/site.js'))
            self.assertTrue(all(i.get('alt') for i in d.select('img')))

    def test_09_full_name_search_identity(self):
        full_name = 'Александр Николаевич Ромаскевич'
        for (kind, lang), document in PAGES.items():
            self.assertIn(full_name, ' '.join(document.visible))
            person = next(n for n in document.jsonld[0]['@graph'] if n['@type'] == 'Person')
            self.assertIn(full_name, person['alternateName'])
            self.assertIn('RomaskevicH', person['alternateName'])
            if kind == 'founder' and lang == 'ru':
                source = file_for(url(kind, lang)).read_text()
                self.assertIn(full_name, re.search(r'<title>(.*?)</title>', source).group(1))
                self.assertIn(full_name, document.select('meta', name='description')[0]['content'])
                self.assertTrue(all(full_name in i['alt'] for i in document.select('img')))

if __name__=='__main__':
    unittest.main(verbosity=2)
