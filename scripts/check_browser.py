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
            for width in (390, 768, 1280):
                command('Emulation.setDeviceMetricsOverride', {'width': width, 'height': 900, 'deviceScaleFactor': 1, 'mobile': False})
                for route in ('/', '/publications/', '/research/', '/repositories/', '/teaching/', '/cv/'):
                    command('Page.navigate', {'url': origin + route})
                    for _ in range(120):
                        if evaluate("document.readyState === 'complete' && location.pathname === " + json.dumps(route)):
                            break
                        time.sleep(.1)
                    expect(evaluate('document.documentElement.scrollWidth <= innerWidth + 2'), f'horizontal overflow at {width}px on {route}')
                    expect(evaluate("document.querySelectorAll('main').length === 1 && document.querySelectorAll('h1').length === 1"), 'landmarks/headings on ' + route)
                    expect(evaluate("Array.from(document.images).every(img => !img.complete || img.naturalWidth > 0)"), 'broken loaded image on ' + route)
                    if route == '/publications/' and width == 390:
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
                    if route == '/' and width == 390:
                        evaluate("document.querySelector('.skip-link').focus()")
                        command('Input.dispatchKeyEvent', {'type': 'keyDown', 'key': 'Enter', 'code': 'Enter', 'windowsVirtualKeyCode': 13, 'text': '\r', 'unmodifiedText': '\r'})
                        command('Input.dispatchKeyEvent', {'type': 'keyUp', 'key': 'Enter', 'code': 'Enter', 'windowsVirtualKeyCode': 13})
                        expect(evaluate("document.activeElement.id === 'main-content'"), 'skip-link keyboard activation')
                        evaluate("document.querySelector('.navbar-toggler').focus()")
                        command('Input.dispatchKeyEvent', {'type': 'keyDown', 'key': ' ', 'code': 'Space', 'windowsVirtualKeyCode': 32})
                        command('Input.dispatchKeyEvent', {'type': 'keyUp', 'key': ' ', 'code': 'Space', 'windowsVirtualKeyCode': 32})
                        time.sleep(.5)
                        expect(evaluate("document.querySelector('.navbar-toggler').getAttribute('aria-expanded') === 'true'"), 'mobile keyboard navigation menu')
            print(f'PASS: {checks} browser checks at 390, 768 and 1280px, including keyboard controls and publication filtering' if not errors else f'Browser checks: {len(errors)} errors')
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
