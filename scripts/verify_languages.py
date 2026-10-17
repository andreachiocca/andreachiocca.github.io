"""Verify static page pairs and shared scientific identities using the standard library."""
import json,re,sys
from html.parser import HTMLParser
from pathlib import Path

root=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
origin='https://andreachiocca.github.io'
class Document(HTMLParser):
    def __init__(self,path):
        super().__init__();self.lang=None;self.canonical=None;self.alternates={};self.links=[];self.json=[];self.buffer=None;self.text=[];self.metadata={};self.experiences=[];self.work_ids=[]
        self.feed(path.read_text(encoding='utf8'))
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if a.get('data-experience'):self.experiences.append(a['data-experience'])
        if a.get('data-work-id'):self.work_ids.append(a['data-work-id'])
        if tag=='html':self.lang=a.get('lang')
        if tag=='a':self.links.append(a.get('href',''))
        if tag=='meta':self.metadata[a.get('name') or a.get('property')]=a.get('content')
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
# All currently published descriptive records must have reviewed Italian overrides.
def read_json(path):return json.loads(Path(path).read_text(encoding='utf8'))
resume=read_json('assets/json/resume.json')
lab=read_json('_data/laboratory.json')
thesis=read_json('_data/thesis_opportunities.json')
groups={
    'research_areas':read_json('_data/research_areas.json'),
    'projects':resume['projects'],
    'outputs':read_json('_data/research_outputs.json'),
    'resume':[resume['basics']]+resume['work']+resume['education']+resume['awards'],
    'laboratory':lab['capabilities']+lab['measurement_context']+lab['equipment'],
    'thesis':thesis['directions']+thesis['approaches']+thesis['projects']}
for group,records in groups.items():
    ids=[record['id'] for record in records]
    assert len(ids)==len(set(ids)), ('Duplicate scientific record',group)
    translations=read_json('_data/i18n/it/'+group+'.json')
    assert set(ids).issubset(translations), ('Missing reviewed record translation',group,set(ids)-set(translations))
    for record in records:
        override=translations[record['id']]
        immutable={'id','url','doi','github_url','github_full_name','zenodo_record_id','creators','startDate','endDate','date','year','institution','name','programme','working_groups','links','specifications'}
        if group in ('outputs','projects','resume'):immutable.add('title')
        assert not immutable.intersection(override), ('Translation overrides canonical metadata',group,record['id'])
        assert all(value not in ('',None) for value in override.values()), ('Empty descriptive translation',group,record['id'])
sitemap=(root/'sitemap.xml').read_text(encoding='utf8')
for key,route in sources:
    documents=[]
    for lang,url in [('en',route),('it','/it'+route)]:
        doc=Document(root/url.lstrip('/')/'index.html');documents.append(doc)
        assert doc.lang==lang,(key,'incorrect HTML language')
        assert doc.metadata.get('description'), (key,'missing description')
        assert doc.metadata.get('og:locale')==('it_IT' if lang=='it' else 'en_GB'), (key,'incorrect social language')
        if lang=='it':
            metadata=read_json('_data/i18n/it/pages.json')[key]
            assert doc.metadata['description']==metadata['description'], (key,'unlocalized metadata')
            leaked={text.strip() for text in doc.text if text.strip() in it and it[text.strip()]!=text.strip()}
            assert not leaked, (key,'English interface fragments',sorted(leaked))
        assert all(not href.startswith(origin+'/it/assets/') for href in doc.links), 'Localized asset URL'
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
    if key=='repositories':
        assert len(records(documents[0]))==len(groups['outputs']), 'Missing or duplicate rendered resource'
    rendered_text=' '.join(documents[1].text)
    # Established institutional names affect display only; canonical JSON-LD stays shared.
    english_text=' '.join(documents[0].text)
    if key in ('home','laboratory','thesis','cv'):
        assert 'Department of Civil and Industrial Engineering' not in rendered_text, (key,'English department in Italian display')
        assert 'Dipartimento di Ingegneria Civile e Industriale' in rendered_text, (key,'missing Italian department')
        assert 'Department of Civil and Industrial Engineering' in english_text, (key,'English department changed')
    if key in ('home','laboratory','thesis','teaching','cv','course-1','course-2','course-3','course-4'):
        assert 'University of Pisa' not in rendered_text, (key,'English university in Italian display')
        assert 'Università di Pisa' in rendered_text, (key,'missing Italian university')
        assert 'University of Pisa' in english_text, (key,'English university changed')
    expected_groups={'research':['research_areas','projects'],'cv':['resume','projects'],'repositories':['outputs'],'laboratory':['laboratory'],'thesis':['thesis']}.get(key,[])
    for group in expected_groups:
        overrides=read_json('_data/i18n/it/'+group+'.json')
        for record in groups[group]:
            translation=overrides[record['id']]
            for field in ('description','summary'):
                if field in translation:assert translation[field] in rendered_text, (key,'rendered description was not localized',record['id'],field)
    if key=='research':
        assert 'Ricerca' in ''.join(documents[1].text) and 'WG5.3' in ''.join(documents[1].text)
        visits=read_json('_data/research_visits.json')
        contacts={item['name'] for item in thesis['international_contacts']}
        work={item['id']:item for item in resume['work']}
        for visit in visits:
            assert visit['contact'] in contacts, ('Unknown visited institution',visit['id'])
            for activity in visit.get('activities',[]):
                assert activity['work_id'] in work, ('Unknown employment/visit reference',activity)
        for doc in documents:
            assert doc.experiences==['ctu-2026','aarhus-2026','ntnu-2024','fraunhofer'], 'Missing or inconsistent international experiences'
            assert doc.work_ids==['lbf-student-intern','lbf-research-assistant','lbf-doctoral-visit'], 'Fraunhofer experiences were conflated'
            text=' '.join(doc.text)
            for work_id in doc.work_ids:
                record=work[work_id]
                assert record['startDate']+'–'+record['endDate'] in text, ('Rendered experience dates differ from CV',work_id)
assert not (root/'it/blog').exists(),'Retired Notes were republished'
print(f'PASS: {len(sources)} bilingual page pairs, reciprocal SEO, selector destinations, shared scientific identities and translation completeness')
