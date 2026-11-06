"""Regression checks for source links, glyph integrity, and repeatable rebuilding."""
import json
from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as ET

from build_derivations import link_excerpt
from source_equations import strip_generated_links

ROOT = Path(__file__).resolve().parents[2]


class EquationLinksTest(unittest.TestCase):
    def test_nested_generated_links_do_not_damage_original_links(self):
        original = '<a class="existing-proof" href="proof.html"><title>Original</title><text>A</text></a>'
        glyphs = '<text><tspan class="pdf-char" data-g="1">=</tspan></text>'
        wrapped = ('<a class="section-proof-link" data-derivation-link="true"><title>Generated</title>'
                   '<a class="equation-source-text"><title>Equation</title>'+glyphs+'</a></a></a>')
        self.assertEqual(strip_generated_links(original+wrapped),original+glyphs)

    def test_every_excerpt_is_valid_and_rebuilds_without_changing_glyphs(self):
        html = (ROOT/'Physics_Review_and_Summary_Tutorial.html').read_text()
        data = json.loads(re.search(r'<script id="regenerated-data" type="application/json">(.*?)</script>',html,re.S)[1])
        count = 0
        for chapter,pieces in data.items():
            for svg in pieces:
                with self.subTest(chapter=chapter,piece=count):
                    once, overlays1 = link_excerpt(svg,int(chapter))
                    twice, overlays2 = link_excerpt(once,int(chapter))
                    ET.fromstring(once)
                    self.assertEqual(once,twice)
                    self.assertEqual(overlays1,overlays2)
                    self.assertEqual(strip_generated_links(svg),strip_generated_links(once))
                    count += 1
        self.assertEqual(count,65)


if __name__ == '__main__':
    unittest.main()
