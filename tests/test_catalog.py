import copy
import importlib.util
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('catalog', ROOT / 'scripts' / 'catalog.py')
catalog = importlib.util.module_from_spec(spec)
spec.loader.exec_module(catalog)


class CatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.entries = catalog.load_entries()

    def test_all_categories_have_content_and_sources(self):
        self.assertEqual(set(catalog.CATEGORIES), {e['category'] for e in self.entries})
        self.assertTrue(all(e['sources'] and e['causes'] for e in self.entries))

    def test_duplicate_id_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            catalog.validate([self.entries[0], self.entries[0]])

    def test_missing_evidence_is_rejected(self):
        bad = copy.deepcopy(self.entries[0]); bad['sources'] = []
        with self.assertRaises(ValueError):
            catalog.validate([bad])

    def test_unscoped_tls_bypass_is_rejected(self):
        bad = copy.deepcopy(self.entries[0])
        bad['commands'] = [{'label':'bad', 'language':'bash', 'kind':'fix', 'note':'bad', 'code':'NODE_TLS_REJECT_UNAUTHORIZED=0 node app.js'}]
        with self.assertRaisesRegex(ValueError, 'unsafe'):
            catalog.validate([bad])

    def test_declared_reproductions_have_evidence(self):
        for entry in self.entries:
            if entry['verification'] == 'reproduced':
                self.assertTrue((ROOT / 'notes' / 'reproductions' / f"{entry['id']}.md").is_file())

    def test_every_error_can_be_found_in_timestamped_log(self):
        for entry in self.entries:
            log = f"2026-11-05T10:00:00Z [build] {entry['error']}\nworker failed"
            self.assertGreater(catalog.score(entry, log), 0, entry['id'])

    def test_script_closing_sequence_cannot_escape_json_payload(self):
        entries = copy.deepcopy(self.entries[:1])
        entries[0]['summary'] = '</script><script>alert(1)</script>'
        page = catalog.products(entries)[ROOT / 'docs' / 'index.html']
        payload = re.search(r'<script type="application/json" id="catalog">(.*?)</script>', page, re.S).group(1)
        self.assertNotIn('<', payload)
        self.assertEqual(json.loads(payload)[0]['summary'], entries[0]['summary'])

    def test_generated_markdown_local_links_exist(self):
        products = catalog.products(self.entries)
        for path, text in products.items():
            if path.suffix != '.md':
                continue
            prose = re.sub(r'```.*?```', '', text, flags=re.S)
            for target in re.findall(r'\]\(([^)]+)\)', prose):
                if '://' not in target:
                    destination = (path.parent / target.split('#')[0]).resolve()
                    self.assertTrue(destination in products or destination.exists(), (path, target))

    def test_generated_outputs_match_committed_files(self):
        for path, expected in catalog.products(self.entries).items():
            self.assertTrue(path.exists(), str(path))
            self.assertEqual(path.read_text(encoding='utf-8'), expected, str(path))


if __name__ == '__main__':
    unittest.main()
