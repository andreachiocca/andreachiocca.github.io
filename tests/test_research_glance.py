"""Results at a glance: every card links to a Research data figure that exists, in both languages."""
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).parents[1]


def load(lang):
    return json.loads((ROOT / f'_data/i18n/{lang}/research_glance.json').read_text(encoding='utf8'))


class ResearchGlanceTests(unittest.TestCase):
    def test_cards_point_to_figures_bound_to_research_chapters(self):
        areas = json.loads((ROOT / '_data/research_areas.json').read_text(encoding='utf8'))
        ids = {}
        for area in areas:
            for name in area.get('figures', []):
                text = (ROOT / '_includes' / name).read_text(encoding='utf8')
                fig_id = re.search(r'<figure id="([\w-]+)"', text).group(1)
                fig_no = re.search(r'FIG\. (R\d{2}\.\d)', text).group(1)
                ids[fig_id] = fig_no
        items = load('en')['items']
        self.assertEqual({i['anchor'] for i in items}, set(ids), 'one card per Research data figure')
        for item in items:
            self.assertEqual(item['fig'], ids[item['anchor']], item['anchor'])

    def test_languages_match(self):
        en, it = load('en'), load('it')
        self.assertEqual([(i['fig'], i['anchor']) for i in en['items']], [(i['fig'], i['anchor']) for i in it['items']])
        for lang in (en, it):
            for item in lang['items']:
                self.assertTrue(10 <= len(item['text'].split()) <= 25, item['text'])


if __name__ == '__main__':
    unittest.main()
