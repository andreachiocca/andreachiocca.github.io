"""Verify static page pairs and shared scientific identities using the standard library."""
import json,re,sys
from html.parser import HTMLParser
from pathlib import Path

root=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
origin='https://andreachiocca.github.io'
class Document(HTMLParser):
    def __init__(self,path):
        super().__init__();self.lang=None;self.canonical=None;self.alternates={};self.links=[];self.json=[];self.buffer=None;self.text=[]
        self.feed(path.read_text(encoding='utf8'))
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='html':self.lang=a.get('lang')
        if tag=='a':self.links.append(a.get('href',''))
        if tag=='link' and a.get('rel')=='canonical':self.canonical=a.get('href')
        if tag=='link' and a.get('rel')=='alternate':self.alternates[a.get('hreflang')]=a.get('href')
        if tag=='script' and a.get('type')=='application/ld+json':self.buffer=''
    def handle_data(self,data):
        if self.buffer is not None:self.buffer+=data
        else:self.text.append(data)
    def handle_endtag(self,tag):
        if tag=='script' and self.buffer is not None:self.json.append(json.loads(self.buffer));self.buffer=None

config=Path('_config.yml').read_text(encoding='utf8')
enabled=[s.strip().strip('\"\'') for s in re.search(r'^academic_languages: \[(.*?)\]',config,re.M)[1].split(',')]
sources=[]
for folder in ('_pages','_projects'):
    for path in Path(folder).glob('*.md'):
        text=path.read_text(encoding='utf8')
        key=re.search(r'^translation_key: (.+)$',text,re.M)
        if not key or key[1] not in enabled:continue
        route=re.search(r'^permalink: (.+)$',text,re.M)
        sources.append((key[1],route[1] if route else '/projects/'+path.stem+'/'))
assert len(sources)==len(enabled)==len(set(k for k,_ in sources)), 'Missing or duplicate page identifiers'
it=json.loads(Path('_data/i18n/it/ui.json').read_text(encoding='utf8'))
en=json.loads(Path('_data/i18n/en/ui.json').read_text(encoding='utf8'))
assert set(it)==set(en) and all(it.values()), 'Missing interface translations'
required=set()
for directory in ('_pages','_layouts','_includes'):
    for path in Path(directory).rglob('*'):
        if path.suffix not in ('.html','.md','.liquid'):continue
        text=path.read_text(encoding='utf8')
        required.update(re.findall(r"\{%\s*locale\s+([^\s%]+)\s*%\}",text))
        for double,single in re.findall(r'''(?:"([^"]+)"|'([^']+)')\s*\|\s*t(?:\s*[}|])''',text):
            assert (double or single) in it, 'Missing interface key: '+(double or single)
translated=json.loads(Path('_data/i18n/it/texts.json').read_text(encoding='utf8'))
assert required.issubset(translated) and all(translated[k].strip() for k in required), 'Missing descriptive translations'
sitemap=(root/'sitemap.xml').read_text(encoding='utf8')
for key,route in sources:
    documents=[]
    for lang,url in [('en',route),('it','/it'+route)]:
        doc=Document(root/url.lstrip('/')/'index.html');documents.append(doc)
        assert doc.lang==lang,(key,'incorrect HTML language')
        assert doc.canonical==origin+url,(key,'incorrect canonical')
        expected={'en':origin+route,'it':origin+'/it'+route,'x-default':origin+route}
        assert doc.alternates==expected,(key,'incorrect reciprocal language links')
        assert origin+url in sitemap,(key,'absent from sitemap')
        assert all(not link.startswith(('/it/assets/','/it/TeachingMaterial/','/it/https:')) for link in doc.links),'Rewritten asset/external URL'
        for destination in expected.values():assert destination.removeprefix(origin) in doc.links,(key,'invalid language selector')
    # Article identities, title, DOI and authors are identical across both renderings.
    def papers(doc):return [r for r in doc.json if r.get('@type') in ('ScholarlyArticle','Thesis','CreativeWork')]
    assert papers(documents[0])==papers(documents[1]),(key,'scientific bibliography differs across languages')
    if key=='home':
        assert '**' not in ''.join(documents[1].text), 'Localized Markdown was not rendered'
    if key=='repositories':
        def records(doc):return {(r.get('@type'),r.get('name'),r.get('identifier'),r.get('url')) for r in doc.json if r.get('@type') in ('Dataset','SoftwareSourceCode')}
        assert records(documents[0])==records(documents[1]),'Scientific output identities differ'
    if key=='research':
        assert 'Ricerca' in ''.join(documents[1].text) and 'WG5.3' in ''.join(documents[1].text)
assert not (root/'it/blog').exists(),'Retired Notes were republished'
print(f'PASS: {len(sources)} bilingual page pairs, reciprocal SEO, selector destinations, shared scientific identities and translation completeness')
