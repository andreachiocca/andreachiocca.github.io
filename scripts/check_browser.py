"""Browser smoke checks using Chrome and the existing Jupyter websocket dependency."""
import functools
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import threading
import time
import urllib.request


def check_browser(root):
    chrome = next((shutil.which(name) for name in ('google-chrome', 'chromium', 'chromium-browser') if shutil.which(name)), None)
    if chrome is None:
        print('SKIP: browser checks; Chrome/Chromium is unavailable')
        return []
    try:
        import websocket
    except ImportError:
        print('SKIP: browser checks; websocket-client is unavailable')
        return []

    class QuietHandler(SimpleHTTPRequestHandler):
        def log_message(self, *args):
            pass

    server = ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(QuietHandler, directory=str(root)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    errors = []
    checks = 0
    with tempfile.TemporaryDirectory() as profile:
        process = subprocess.Popen([chrome, '--headless', '--no-sandbox', '--disable-dev-shm-usage', '--remote-debugging-port=0', '--user-data-dir=' + profile, 'about:blank'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        ws = None
        try:
            portfile = Path(profile) / 'DevToolsActivePort'
            for _ in range(150):
                if portfile.exists():
                    break
                if process.poll() is not None:
                    raise RuntimeError('Chrome exited before startup')
                time.sleep(.1)
            port = int(portfile.read_text().splitlines()[0])
            with urllib.request.urlopen(f'http://127.0.0.1:{port}/json') as response:
                target = next(item for item in json.load(response) if item['type'] == 'page')
            ws = websocket.create_connection(target['webSocketDebuggerUrl'], timeout=20, suppress_origin=True)
            counter = 0

            def command(method, params=None):
                nonlocal counter
                counter += 1
                message_id = counter
                ws.send(json.dumps({'id': message_id, 'method': method, 'params': params or {}}))
                while True:
                    result = json.loads(ws.recv())
                    if result.get('id') == message_id:
                        if 'error' in result:
                            raise RuntimeError(str(result['error']))
                        return result.get('result', {})

            def evaluate(expression):
                result = command('Runtime.evaluate', {'expression': expression, 'returnByValue': True, 'awaitPromise': True})
                if result.get('exceptionDetails'):
                    raise RuntimeError(str(result['exceptionDetails']))
                return result['result'].get('value')

            def expect(condition, message):
                nonlocal checks
                checks += 1
                if not condition:
                    errors.append('Browser: ' + message)

            command('Page.enable')
            origin = 'http://127.0.0.1:' + str(server.server_port)
            routes = ['/', '/publications/', '/research/', '/repositories/', '/teaching/', '/cv/', '/thesis/', '/laboratory/']
            routes += ['/' + p.relative_to(root).as_posix().removesuffix('index.html') for p in sorted((root / 'it').rglob('*.html'))]
            for path in sorted(root.rglob('*.html')):
                if '/projects/' in '/' + path.relative_to(root).as_posix():
                    route = '/' + path.relative_to(root).as_posix().removesuffix('index.html')
                    if route not in routes:
                        routes.append(route)
            for width in (375, 390, 768, 1280):
                command('Emulation.setDeviceMetricsOverride', {'width': width, 'height': 900, 'deviceScaleFactor': 1, 'mobile': False})
                for route in routes:
                    command('Page.navigate', {'url': origin + route})
                    for _ in range(120):
                        if evaluate("document.readyState === 'complete' && location.pathname === " + json.dumps(route)):
                            break
                        time.sleep(.1)
                    expect(evaluate('document.documentElement.scrollWidth <= innerWidth + 2'), f'horizontal overflow at {width}px on {route}')
                    expect(evaluate("document.querySelectorAll('main').length === 1 && document.querySelectorAll('h1').length === 1"), 'landmarks/headings on ' + route)
                    expect(evaluate("Array.from(document.images).every(img => !img.complete || img.naturalWidth > 0)"), 'broken loaded image on ' + route)
                    is_home = route in ('/', '/it/')
                    expect(evaluate("document.querySelectorAll('#navbar .nav-link[aria-current]').length") == (0 if is_home else 1), 'unique active content category on ' + route)
                    expect(evaluate("document.querySelector('h1').getBoundingClientRect().top >= document.getElementById('navbar').getBoundingClientRect().bottom"), 'header obscures title on ' + route)
                    labels = 'Ricerca|Didattica|CV' if route.startswith('/it/') else 'Research|Teaching|CV'
                    expect(evaluate("[...document.querySelectorAll('#navbarNav > ul > .nav-item > .nav-link')].map(a => a.textContent.trim()).join('|') === " + json.dumps(labels)), 'three primary navigation categories on ' + route)
                    expect(evaluate("document.querySelector('.navbar-brand').getAttribute('href') === " + json.dumps('/it/' if route.startswith('/it/') else '/')), 'homepage remains reachable through identity on ' + route)
                    expect(evaluate("document.querySelectorAll('.nav-section-toggle[aria-controls][aria-expanded=false]').length === 2 && document.querySelectorAll('.nav-submenu[hidden]').length === 2"), 'submenus start collapsed on ' + route)
                    expect(evaluate("document.querySelectorAll('.language-link').length === 2 && document.querySelectorAll('.language-link[aria-current]').length === 1"), 'language selector on ' + route)
                    canonical_route = route[3:] if route.startswith('/it/') else route
                    italian = route.startswith('/it/')
                    if is_home:
                        expect(evaluate("[...document.querySelectorAll('.home-project p')].every(p => {const rgb = getComputedStyle(p).color.match(/\\d+/g)?.map(Number); return rgb && rgb.slice(0, 3).every(value => value >= 200);})"), 'FABER text remains light on the blue background on ' + route)
                        expect(evaluate("[...document.querySelectorAll('.home-art-heading span, .home-art-footer span, .stress-scrub span, .stress-note p')].length >= 5 && [...document.querySelectorAll('.home-art-heading span, .home-art-footer span, .stress-scrub span, .stress-note p')].every(el => {const rgb = getComputedStyle(el).color.match(/\\d+/g)?.map(Number); return rgb && rgb.slice(0, 3).every(value => value >= 170);})"), 'home figure labels remain light on the blue background on ' + route)
                    if width >= 992:
                        expect(evaluate("Math.abs(document.querySelector('#light-toggle').getBoundingClientRect().top + document.querySelector('#light-toggle').getBoundingClientRect().height / 2 - (document.querySelector('#navbar .nav-link').getBoundingClientRect().top + document.querySelector('#navbar .nav-link').getBoundingClientRect().height / 2)) <= 2"), 'theme button aligns with desktop navigation on ' + route)
                        expect(evaluate("[...document.querySelectorAll('#light-toggle i')].every(i => getComputedStyle(i).paddingTop === '0px' && getComputedStyle(i).paddingLeft === '0px')"), 'theme icon has no offset padding on ' + route)
                    if canonical_route in ('/thesis/', '/laboratory/'):
                        expect(evaluate("[...document.querySelectorAll('.feature-card')].every(card => card.getBoundingClientRect().width >= 280 && card.getBoundingClientRect().right <= innerWidth)"), f'narrow or overflowing resource cards at {width}px on {route}')
                        expect(evaluate("[...document.querySelectorAll('.feature-card .inline-links a, .contact-link, .page-paths a, .institution-list a')].every(a => a.getBoundingClientRect().height >= 44)"), 'resource touch targets on ' + route)
                        expect(evaluate("[...document.querySelectorAll('.feature-card')].every(card => card.querySelector('h3')?.textContent.trim() && card.querySelector('p')?.textContent.trim())"), 'empty resource cards on ' + route)
                    if canonical_route == '/thesis/':
                        expect(evaluate("document.querySelectorAll('.thesis-topic').length === 5 && document.querySelectorAll('#ways-of-working + p + .approach-list .approach').length === 3"), 'thesis directions and approaches')
                        expect(evaluate("document.querySelector('#navbar .nav-link[aria-current]').textContent.trim() === " + json.dumps('Didattica' if italian else 'Teaching') + ""), 'Teaching parent of thesis page')
                    if canonical_route == '/cv/':
                        if width < 576:
                            expect(evaluate("getComputedStyle(document.querySelector('#toc-sidebar')).display === 'none'"), 'mobile CV contents must not overlay the introduction')
                        else:
                            expect(evaluate("document.querySelector('#toc-sidebar').getBoundingClientRect().right <= document.querySelector('h1').getBoundingClientRect().left"), 'CV sidebar overlaps main column')
                    if canonical_route == '/research/':
                        expect(evaluate("[...document.querySelectorAll('.research-figure-index span')].length === 2 && [...document.querySelectorAll('.research-figure-index span')].every(el => {const rgb = getComputedStyle(el).color.match(/\\d+/g)?.map(Number); return rgb && rgb.slice(0, 3).every(value => value >= 170);})"), 'Research figure labels remain light on the blue background on ' + route)
                        expect(evaluate("document.querySelectorAll('.research-chapter').length === 4"), 'four Research chapters on ' + route)
                        expect(evaluate("document.querySelectorAll('.research-chapter .research-technical-figure svg').length === 4"), 'four Research SVGs on ' + route)
                        expect(evaluate("[...document.querySelectorAll('.research-chapter, .research-technical-figure')].every(el => {const r=el.getBoundingClientRect(); return r.left >= -2 && r.right <= innerWidth+2;})"), 'Research figures/content overflow on ' + route)
                        expect(evaluate("[...document.querySelectorAll('.research-quick-links a, .research-chapter details summary, .research-chapter .inline-links a')].every(el => el.getBoundingClientRect().height >= 44)"), 'Research touch targets on ' + route)
                        expect(evaluate("[...document.querySelectorAll('.research-featured-project :is(p, h3, span, li, strong, a)')].every(el => {const channels = getComputedStyle(el).color.match(/\\d+/g)?.map(Number); return channels && channels.slice(0, 3).every(value => value >= 150);})"), 'Research featured project text contrast on ' + route)
                        if width == 390:
                            expect(evaluate("getComputedStyle(document.querySelector('.research-chapter details summary')).display === 'list-item'"), 'Research summary retains native list-item semantics')
                            evaluate("document.querySelector('.research-chapter details').open = false")
                            evaluate("document.querySelector('.research-chapter details summary').focus()")
                            expect(evaluate("document.activeElement === document.querySelector('.research-chapter details summary')"), 'Research disclosure summary receives keyboard focus')
                            command('Input.dispatchKeyEvent', {'type':'keyDown','key':'Enter','code':'Enter','windowsVirtualKeyCode':13,'text':'\r','unmodifiedText':'\r'})
                            command('Input.dispatchKeyEvent', {'type':'keyUp','key':'Enter','code':'Enter','windowsVirtualKeyCode':13})
                            time.sleep(.15)
                            expect(evaluate("document.querySelector('.research-chapter details').open"), 'Research disclosure keyboard accessible')
                    if canonical_route in ('/research/', '/cv/'):
                        expect(evaluate("[...document.querySelectorAll('[data-project=faber] .project-roles li')].some(li => li.textContent.includes('WG3,') && li.textContent.includes('Co-Leader'))"), 'FABER WG3 role missing on ' + route)
                        for group in ('WG4.3', 'WG5.3'):
                            expect(evaluate("[...document.querySelectorAll('[data-project=faber] .project-roles li')].some(li => li.textContent.includes(" + json.dumps(group) + ") && li.textContent.includes(" + json.dumps('Partecipante' if italian else 'Participant') + "))"), 'FABER Participant role missing on ' + route)
                        expect(evaluate("!document.querySelector('main').textContent.includes('2025 - 2025')"), 'duplicated project date on ' + route)
                    if canonical_route == '/repositories/':
                        expect(evaluate("document.querySelector('h1').getBoundingClientRect().top >= document.getElementById('navbar').getBoundingClientRect().bottom"), f'catalogue behind navigation at {width}px')
                        expect(evaluate("[...document.querySelectorAll('.research-output')].every(card => {const r = card.getBoundingClientRect(); return r.left >= 0 && r.right <= innerWidth;})"), f'catalogue card overflow at {width}px')
                        expect(evaluate("[...document.querySelectorAll('.output-links a, .catalogue-filters button, .output-details summary')].every(link => link.getBoundingClientRect().height >= 44)"), f'catalogue touch targets at {width}px')
                        if width == 390:
                            total = evaluate("document.querySelectorAll('.research-output').length")
                            expect(evaluate("!document.querySelector('.catalogue-filters').hidden"), 'catalogue filters initialized')
                            evaluate("document.querySelector('[data-filter=software]').click()")
                            expect(evaluate("[...document.querySelectorAll('.research-output')].every(card => card.hidden === (card.dataset.category !== 'software'))"), 'software catalogue filter')
                            evaluate("document.querySelector('[data-filter=data]').click()")
                            expect(evaluate("[...document.querySelectorAll('.research-output')].every(card => card.hidden === (card.dataset.category !== 'data'))"), 'dataset catalogue filter')
                            evaluate("location.hash='multiaxial-fatigue'")
                            time.sleep(.2)
                            expect(evaluate("!document.getElementById('multiaxial-fatigue').hidden"), 'filtered deep-link recovery')
                            evaluate("document.querySelector('[data-filter=other]').focus()")
                            command('Input.dispatchKeyEvent', {'type': 'keyDown', 'key': ' ', 'code': 'Space', 'windowsVirtualKeyCode': 32})
                            command('Input.dispatchKeyEvent', {'type': 'keyUp', 'key': ' ', 'code': 'Space', 'windowsVirtualKeyCode': 32})
                            expect(evaluate("document.querySelector('[data-filter=other]').getAttribute('aria-pressed') === 'true'"), 'keyboard catalogue filter')
                            evaluate("document.querySelector('[data-filter=all]').click()")
                            expect(evaluate("document.querySelectorAll('.research-output:not([hidden])').length") == total, 'catalogue filter reset')
                            expect(evaluate("document.querySelectorAll('.output-atlas-feature').length === 4"), 'four selected output links')
                            expect(evaluate("!document.getElementById('output-search').hidden"), 'catalogue keyword search is visible')
                            evaluate("document.getElementById('output-search').value='ECP'; document.getElementById('output-search').dispatchEvent(new Event('input'))")
                            expect(evaluate("document.querySelectorAll('.research-output:not([hidden])').length > 0 && document.querySelectorAll('.research-output:not([hidden])').length < 14"), 'catalogue keyword search filters records')
                            evaluate("document.querySelector('[data-filter=software]').click()")
                            expect(evaluate("[...document.querySelectorAll('.research-output:not([hidden])')].every(card => card.dataset.category === 'software')"), 'catalogue combined search and category')
                            evaluate("document.getElementById('output-search').value='no-such-research-output-98765'; document.getElementById('output-search').dispatchEvent(new Event('input'))")
                            expect(evaluate("document.querySelectorAll('.research-output:not([hidden])').length === 0 && !document.getElementById('output-empty').hidden && !document.getElementById('output-reset').hidden"), 'catalogue empty-state and clear button')
                            evaluate("document.getElementById('output-reset').click()")
                            expect(evaluate("document.querySelectorAll('.research-output:not([hidden])').length === 14 && document.getElementById('output-search').value === '' && document.getElementById('output-empty').hidden"), 'catalogue clear restores all records')
                            expect(evaluate("[...document.querySelectorAll('.output-atlas-feature a[href^="#"]')].every(a => document.getElementById(a.hash.slice(1)))"), 'featured catalogue links resolve')
                    if canonical_route == '/publications/' and width == 390:
                        expect(evaluate("document.querySelectorAll('[data-publication-filter]').length === 4 && !document.getElementById('publication-type-filters').hidden"), 'category publication filters initialized')
                        expect(evaluate("document.querySelector('[data-publication-filter=all]').getAttribute('aria-pressed') === 'true'"), 'publication All selected by default')
                        evaluate("document.querySelector('[data-publication-filter=article]').click()")
                        expect(evaluate("[...document.querySelectorAll('ol.bibliography > li:not([hidden])')].every(li => li.closest('section').dataset.publicationCategory === 'article') && document.querySelectorAll('ol.bibliography > li:not([hidden])').length > 0"), 'publication article category filtering')
                        evaluate("document.getElementById('bibsearch').value='2026'; document.getElementById('bibsearch').dispatchEvent(new Event('input'))")
                        expect(evaluate("[...document.querySelectorAll('ol.bibliography > li:not([hidden])')].every(li => li.closest('section').dataset.publicationCategory === 'article' && /2026/.test(li.textContent + (li.closest('ol').previousElementSibling?.textContent || '')))"), 'publication combined type and year search')
                        evaluate("document.getElementById('bibsearch').value='no-such-scientific-paper-98765'; document.getElementById('bibsearch').dispatchEvent(new Event('input'))")
                        expect(evaluate("document.querySelectorAll('ol.bibliography > li:not([hidden])').length === 0 && !document.getElementById('bibsearch-empty').hidden && !document.getElementById('bibsearch-clear').hidden"), 'publication empty state and reset available')
                        evaluate("document.getElementById('bibsearch-clear').click()")
                        expect(evaluate("document.querySelector('[data-publication-filter=all]').getAttribute('aria-pressed') === 'true' && document.getElementById('bibsearch').value === '' && document.getElementById('bibsearch-empty').hidden"), 'publication clear resets category/search')
                        total_publications = evaluate("document.querySelectorAll('ol.bibliography > li').length")
                        expect(evaluate("!document.getElementById('bibsearch').hidden"), 'publication filter not initialized')
                        evaluate("document.getElementById('bibsearch').value='2026'; document.getElementById('bibsearch').dispatchEvent(new Event('input'))")
                        expect(evaluate("Array.from(document.querySelectorAll('ol.bibliography > li')).filter(item => !item.hidden).length > 0 && document.querySelectorAll('ol.bibliography > li[hidden]').length > 0"), 'publication year filter')
                        evaluate("document.getElementById('bibsearch').value=''; document.getElementById('bibsearch').dispatchEvent(new Event('input'))")
                        expect(evaluate("Array.from(document.querySelectorAll('ol.bibliography > li')).filter(item => !item.hidden).length") == total_publications, 'publication filter reset')
                        evaluate("document.querySelector('details summary').focus()")
                        command('Input.dispatchKeyEvent', {'type': 'keyDown', 'key': 'Enter', 'code': 'Enter', 'windowsVirtualKeyCode': 13, 'text': '\r', 'unmodifiedText': '\r'})
                        command('Input.dispatchKeyEvent', {'type': 'keyUp', 'key': 'Enter', 'code': 'Enter', 'windowsVirtualKeyCode': 13})
                        expect(evaluate("document.querySelector('details').open"), 'keyboard publication disclosure')
                    if canonical_route == '/':
                        expect(evaluate("document.querySelector('#research-environment')?.compareDocumentPosition(document.querySelector('.home-paths')) & Node.DOCUMENT_POSITION_FOLLOWING"), 'research context precedes homepage pathways')
                        expect(evaluate("document.querySelector('#research-environment')?.textContent.includes('Gruppo di Costruzione di Macchine') && document.querySelector('#research-environment').textContent.includes('DICI')"), 'verified homepage group affiliation')
                        expect(evaluate("document.querySelector('.office-contact')?.tagName === 'ADDRESS' && !document.querySelector('.office-contact').closest('details') && document.querySelector('.office-contact a[href^=mailto]').getBoundingClientRect().height >= 44"), 'office contact must remain visible')
                        expect(evaluate("document.querySelectorAll('.recent-publications ol.bibliography > li').length === 5"), 'five recent publications on homepage')
                        expect(evaluate("[...document.querySelectorAll('.section-icon')].every(i => i.getAttribute('aria-hidden') === 'true' && getComputedStyle(i,'::before').content !== 'none')"), 'decorative icon accessibility and glyphs')
                    if canonical_route == '/' and width == 390:
                        evaluate("document.querySelector('.skip-link').focus()")
                        command('Input.dispatchKeyEvent', {'type': 'keyDown', 'key': 'Enter', 'code': 'Enter', 'windowsVirtualKeyCode': 13, 'text': '\r', 'unmodifiedText': '\r'})
                        command('Input.dispatchKeyEvent', {'type': 'keyUp', 'key': 'Enter', 'code': 'Enter', 'windowsVirtualKeyCode': 13})
                        expect(evaluate("document.activeElement.id === 'main-content'"), 'skip-link keyboard activation')
                        initial_top = evaluate("document.querySelector('h1').getBoundingClientRect().top")
                        evaluate("document.querySelector('.navbar-toggler').focus()")
                        command('Input.dispatchKeyEvent', {'type': 'keyDown', 'key': ' ', 'code': 'Space', 'windowsVirtualKeyCode': 32})
                        command('Input.dispatchKeyEvent', {'type': 'keyUp', 'key': ' ', 'code': 'Space', 'windowsVirtualKeyCode': 32})
                        time.sleep(.5)
                        expect(evaluate("document.querySelector('.navbar-toggler').getAttribute('aria-expanded') === 'true'"), 'mobile keyboard navigation menu')
                        expect(abs(evaluate("document.querySelector('h1').getBoundingClientRect().top") - initial_top) < 1, 'mobile menu shifts page content')
                        expect(evaluate("document.querySelector('main').inert"), 'background remains interactive behind mobile menu')
                        command('Input.dispatchKeyEvent', {'type': 'keyDown', 'key': 'Escape', 'code': 'Escape', 'windowsVirtualKeyCode': 27})
                        command('Input.dispatchKeyEvent', {'type': 'keyUp', 'key': 'Escape', 'code': 'Escape', 'windowsVirtualKeyCode': 27})
                        expect(evaluate("document.querySelector('.navbar-toggler').getAttribute('aria-expanded') === 'false' && !document.querySelector('main').inert && document.activeElement.matches('.navbar-toggler')"), 'Escape closes menu and restores focus')
                    if canonical_route == '/research/' and width >= 992:
                        evaluate("document.getElementById('nav-research-toggle').click(); document.querySelector('#nav-research a[href$=\"#projects\"]').click()")
                        expect(evaluate("location.hash === '#projects' && document.getElementById('nav-research').hidden && document.getElementById('nav-research-toggle').getAttribute('aria-expanded') === 'false'"), 'same-page destination closes desktop submenu')
                    if canonical_route == '/' and evaluate("document.querySelectorAll('.nav-section-toggle').length === 2"):
                        if width < 992:
                            evaluate("document.querySelector('.navbar-toggler').click()")
                        evaluate("document.getElementById('nav-research-toggle').focus()")
                        command('Input.dispatchKeyEvent', {'type': 'keyDown', 'key': 'Enter', 'code': 'Enter', 'windowsVirtualKeyCode': 13, 'text': '\r'})
                        command('Input.dispatchKeyEvent', {'type': 'keyUp', 'key': 'Enter', 'code': 'Enter', 'windowsVirtualKeyCode': 13})
                        expect(evaluate("document.getElementById('nav-research-toggle').getAttribute('aria-expanded') === 'true' && !document.getElementById('nav-research').hidden"), 'keyboard opens research submenu')
                        command('Input.dispatchKeyEvent', {'type': 'keyDown', 'key': 'Tab', 'code': 'Tab', 'windowsVirtualKeyCode': 9})
                        command('Input.dispatchKeyEvent', {'type': 'keyUp', 'key': 'Tab', 'code': 'Tab', 'windowsVirtualKeyCode': 9})
                        expect(evaluate("document.activeElement === document.querySelector('#nav-research a')"), 'Tab reaches first research destination')
                        command('Input.dispatchKeyEvent', {'type': 'keyDown', 'key': 'Escape', 'code': 'Escape', 'windowsVirtualKeyCode': 27})
                        command('Input.dispatchKeyEvent', {'type': 'keyUp', 'key': 'Escape', 'code': 'Escape', 'windowsVirtualKeyCode': 27})
                        expect(evaluate("document.getElementById('nav-research').hidden && document.activeElement.id === 'nav-research-toggle'"), 'Escape closes submenu and restores trigger focus')
                        if width < 992:
                            expect(evaluate("document.querySelector('.navbar-toggler').getAttribute('aria-expanded') === 'true'"), 'submenu Escape preserves mobile menu')
                        evaluate("document.getElementById('nav-teaching-toggle').click()")
                        expect(evaluate("document.querySelectorAll('#nav-teaching a[data-course]').length === 4 && document.querySelector('#nav-teaching a[data-thesis]').getClientRects().length > 0"), 'courses and thesis reachable from teaching submenu')
                        expect(evaluate("document.getElementById('nav-research').hidden"), 'only one submenu opens at a time')
                        expect(evaluate("[...document.querySelectorAll('.nav-submenu:not([hidden])')].every(menu => {const r=menu.getBoundingClientRect(); return r.left >= 0 && r.right <= innerWidth;})"), 'expanded submenu stays within viewport')
                        evaluate("document.getElementById('nav-teaching-toggle').click()")
                        evaluate("document.getElementById('nav-research-toggle').click(); document.getElementById('nav-teaching-toggle').click()")
                        expect(evaluate("document.getElementById('nav-research').hidden && !document.getElementById('nav-teaching').hidden"), 'opening teaching closes the research disclosure')
                        evaluate("document.getElementById('nav-teaching-toggle').click()")
                        if width >= 992:
                            evaluate("document.getElementById('nav-research-toggle').click(); document.body.click()")
                            expect(evaluate("document.getElementById('nav-research').hidden"), 'outside click closes desktop submenu')
                        if width < 992:
                            evaluate("document.querySelector('.navbar-toggler').click()")
            # Additional, page-scoped checks for bilingual Laboratory and equipment photos.
            for width in (320, 375, 390, 768, 1280, 1920):
                command('Emulation.setDeviceMetricsOverride', {'width': width, 'height': 900, 'deviceScaleFactor': 1, 'mobile': False})
                for route in ('/laboratory/', '/it/laboratory/'):
                    command('Page.navigate', {'url': origin + route})
                    for _ in range(120):
                        if evaluate("document.readyState === 'complete' && location.pathname === " + json.dumps(route)):
                            break
                        time.sleep(.1)
                    expect(evaluate("document.querySelectorAll('[data-laboratory-id]').length === 10"), f'Laboratory equipment records at {width}px on {route}')
                    expect(evaluate("document.documentElement.scrollWidth <= innerWidth + 2"), f'Laboratory horizontal overflow at {width}px on {route}')
                    expect(evaluate("[...document.querySelectorAll('.laboratory-editorial img')].every(el=>{const r=el.getBoundingClientRect();return r.left>=-2&&r.right<=innerWidth+2;})"), f'Laboratory photographs fit at {width}px on {route}')
                    expect(evaluate("[...document.querySelectorAll('.laboratory-quick-links a, .laboratory-collaboration .contact-link')].every(el=>el.getBoundingClientRect().height >= 44)"), f'Laboratory accessible targets at {width}px on {route}')
                    expect(evaluate("document.querySelector('#schenck-axial-torsional').textContent.includes('700 bar')"), f'Laboratory pressure correct at {width}px on {route}')
                    expect(evaluate("[...document.querySelectorAll('.laboratory-editorial img')].every(el=>el.alt.length>0&&el.width>0&&el.height>0)"), f'Laboratory images have alt and dimensions at {width}px on {route}')
                    evaluate("document.documentElement.setAttribute('data-theme','dark')")
                    expect(evaluate("getComputedStyle(document.querySelector('.laboratory-hero-figure')).backgroundColor !== 'rgba(0, 0, 0, 0)'"), f'Laboratory dark theme at {width}px on {route}')
                    evaluate("document.documentElement.removeAttribute('data-theme')")
            # Scoped width coverage for the new Research page at phone and large desktop.
            for width in (320, 1920):
                command('Emulation.setDeviceMetricsOverride', {'width': width, 'height': 900, 'deviceScaleFactor': 1, 'mobile': False})
                for route in ('/research/', '/it/research/'):
                    command('Page.navigate', {'url': origin + route})
                    for _ in range(120):
                        if evaluate("document.readyState === 'complete' && location.pathname === " + json.dumps(route)):
                            break
                        time.sleep(.1)
                    expect(evaluate("document.documentElement.scrollWidth <= innerWidth + 2"), f'Research overflow at {width}px on {route}')
                    expect(evaluate("document.querySelectorAll('.research-chapter').length === 4"), f'Research chapter count at {width}px on {route}')
                    expect(evaluate("[...document.querySelectorAll('.research-chapter')].every(el => {const r=el.getBoundingClientRect(); return r.left >= -2 && r.right <= innerWidth+2;})"), f'Research chapter bounds at {width}px on {route}')
                    expect(evaluate("[...document.querySelectorAll('.research-quick-links a, .research-chapter details summary')].every(el=>el.getBoundingClientRect().height >= 44)"), f'Research controls accessible at {width}px on {route}')
                    evaluate("document.documentElement.setAttribute('data-theme','dark')")
                    expect(evaluate("getComputedStyle(document.querySelector('.research-hero-panel')).backgroundImage !== 'none'"), f'Research dark mode rendered at {width}px on {route}')
                    evaluate("document.documentElement.removeAttribute('data-theme')")
                    expect(evaluate("getComputedStyle(document.querySelector('.research-hilbert-trace')).animationName === 'research-hilbert-draw'"), f'Research Hilbert path animation at {width}px on {route}')
                    command('Emulation.setEmulatedMedia', {'features': [{'name': 'prefers-reduced-motion', 'value': 'reduce'}]})
                    expect(evaluate("getComputedStyle(document.querySelector('.research-hilbert-trace')).animationName === 'none'"), f'Research reduced-motion path at {width}px on {route}')
                    command('Emulation.setEmulatedMedia', {'features': []})
            # Scope added viewport coverage to Publications only.
            for width in (320, 1920):
                command('Emulation.setDeviceMetricsOverride', {'width': width, 'height': 900, 'deviceScaleFactor': 1, 'mobile': False})
                for route in ('/publications/', '/it/publications/'):
                    command('Page.navigate', {'url': origin + route})
                    for _ in range(120):
                        if evaluate("document.readyState === 'complete' && location.pathname === " + json.dumps(route)):
                            break
                        time.sleep(.1)
                    expect(evaluate("document.documentElement.scrollWidth <= innerWidth + 2"), f'Publications overflow at {width}px on {route}')
                    expect(evaluate("[...document.querySelectorAll('.publication-type-filters button, .publications-index .links .btn, .publications-index details summary')].every(el=>el.getBoundingClientRect().height >= 44)"), f'Publications controls accessible at {width}px on {route}')
                    expect(evaluate("document.querySelectorAll('ol.bibliography > li').length > 0"), f'Publications bibliography at {width}px on {route}')
                    evaluate("document.documentElement.setAttribute('data-theme','dark')")
                    expect(evaluate("getComputedStyle(document.querySelector('.publications-index-search')).borderTopWidth !== '0px'"), f'Publications dark theme styles at {width}px on {route}')
                    evaluate("document.documentElement.removeAttribute('data-theme')")
            command('Emulation.setDeviceMetricsOverride', {'width': 844, 'height': 390, 'deviceScaleFactor': 1, 'mobile': False})
            command('Page.navigate', {'url': origin + '/thesis/'})
            for _ in range(120):
                if evaluate("document.readyState === 'complete' && location.pathname === '/thesis/'"):
                    break
                time.sleep(.1)
            evaluate("document.querySelector('.navbar-toggler').click()")
            evaluate("document.getElementById('nav-teaching-toggle')?.click()")
            expect(evaluate("document.getElementById('navbarNav').getBoundingClientRect().bottom <= innerHeight + 1"), 'landscape menu extends past viewport')
            expect(evaluate("document.getElementById('navbarNav').scrollHeight > document.getElementById('navbarNav').clientHeight"), 'landscape menu cannot scroll')
            command('Emulation.setScriptExecutionDisabled', {'value': True})
            for width in (375, 1280):
                command('Emulation.setDeviceMetricsOverride', {'width': width, 'height': 900, 'deviceScaleFactor': 1, 'mobile': False})
                command('Page.navigate', {'url': origin + '/it/'})
                for _ in range(120):
                    if evaluate("document.readyState === 'complete' && location.pathname === '/it/'"):
                        break
                    time.sleep(.1)
                expect(evaluate("document.querySelector('#nav-teaching a[data-thesis]').getClientRects().length > 0"), 'thesis reachable without JavaScript')
                expect(evaluate("document.querySelector('h1').getBoundingClientRect().top >= document.querySelector('#navbar').getBoundingClientRect().bottom"), 'no-JavaScript navigation does not obscure content')
            for route in ('/publications/', '/it/publications/'):
                command('Page.navigate', {'url': origin + route})
                for _ in range(120):
                    if evaluate("document.readyState === 'complete' && location.pathname === " + json.dumps(route)):
                        break
                    time.sleep(.1)
                expect(evaluate("document.querySelectorAll('ol.bibliography > li').length > 0 && [...document.querySelectorAll('ol.bibliography > li')].every(el => !el.hidden)"), 'no-JavaScript bibliography visible on ' + route)
                expect(evaluate("document.getElementById('bibsearch').hidden && document.getElementById('publication-type-filters').hidden"), 'no-JavaScript filters hidden on ' + route)
            # The source-of-truth controls the photo count. Photo assignments
            # can change when a machine is corrected or an asset is added.
            laboratory_data = json.loads(Path('_data/laboratory.json').read_text(encoding='utf8'))
            expected_laboratory_images = 1 + sum(bool(item.get(kind)) for item in laboratory_data['equipment'] for kind in ('image', 'secondary_image'))
            for route in ('/laboratory/', '/it/laboratory/'):
                command('Page.navigate', {'url': origin + route})
                for _ in range(120):
                    if evaluate("document.readyState === 'complete' && location.pathname === " + json.dumps(route)):
                        break
                    time.sleep(.1)
                expect(evaluate("document.querySelectorAll('[data-laboratory-id]').length === 10"), 'Laboratory content present with scripts disabled on '+route)
                expect(evaluate(f"document.querySelectorAll('.laboratory-editorial img[alt]').length === {expected_laboratory_images}"), 'Laboratory photographs match canonical data with scripts disabled on '+route)
                expect(evaluate("document.querySelector('.laboratory-hero-copy strong') !== null"), 'Laboratory intro renders Markdown emphasis on '+route)
                expect(evaluate("!document.querySelector('.laboratory-hero-copy').innerText.includes('<p class=')"), 'Laboratory intro does not expose HTML source on '+route)
            print(f'PASS: {checks} browser checks at 375, 390, 768 and 1280px, including thesis and laboratory pages, courses, navigation and catalogue controls' if not errors else f'Browser checks: {len(errors)} errors')
        except Exception as exc:
            errors.append('Browser check could not complete: ' + str(exc))
        finally:
            if ws:
                ws.close()
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
            server.shutdown()
    return errors
