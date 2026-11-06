"""Asset coverage, accessible captions, proof links, and scientific geometry."""
import ast
from html.parser import HTMLParser
import json
import math
from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
NS = {'s': 'http://www.w3.org/2000/svg'}


class Page(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.elements = []
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))


def drawing(slug, key='concept'):
    return ET.parse(ROOT / f'derivations/assets/diagrams/{slug}-{key}.svg').getroot()


def points(path):
    return [tuple(map(float, p.split(','))) for p in re.findall(r'[-\d.]+,[-\d.]+', path.get('d'))]


def vector(line):
    return tuple(float(line.get(b))-float(line.get(a)) for a, b in [('x1', 'x2'), ('y1', 'y2')])


class DiagramTests(unittest.TestCase):
    def test_every_page_has_accessible_local_images_and_exact_proof_targets(self):
        topics = json.loads((ROOT / 'content/derivations.json').read_text())
        files = set()
        for topic in topics:
            page = Page((ROOT / topic['file']).read_text())
            ids = {a['id'] for _, a in page.elements if 'id' in a}
            self.assertEqual(sum(d['step'] == 0 for d in topic['diagrams']), 1, topic['slug'])
            for d in topic['diagrams']:
                path = ROOT / d['file']
                files.add(path)
                image = next(a for tag, a in page.elements if tag == 'img' and a['src'] == 'assets/diagrams/'+path.name)
                self.assertGreater(len(image['alt']), 60)
                svg = ET.parse(path).getroot()
                self.assertEqual(svg.get('viewBox'), '0 0 520 380')
                self.assertTrue(svg.find('s:title', NS).text)
                self.assertEqual(svg.find('s:desc', NS).text, image['alt'])
                self.assertFalse(any('href' in k for el in svg.iter() for k in el.attrib))
                proof = '#proof-'+(f"step-{d['step']}" if d['step'] else 'main')
                self.assertIn(proof[1:], ids)
                self.assertTrue(any(tag == 'a' and a.get('href') == proof and 'data-proof-link' in a for tag, a in page.elements))
        self.assertEqual(files, set((ROOT / 'derivations/assets/diagrams').glob('*.svg')))

    def test_centripetal_and_magnetic_forces_are_perpendicular_to_velocity(self):
        for slug, v_id, a_id in [('centripetal-acceleration', 'velocity', 'acceleration'),
                                  ('magnetic-orbit', 'magnetic-velocity', 'magnetic-force')]:
            svg = drawing(slug)
            velocity = vector(svg.find(f'.//*[@id="{v_id}"]'))
            acceleration = vector(svg.find(f'.//*[@id="{a_id}"]'))
            self.assertAlmostEqual(sum(a*b for a, b in zip(velocity, acceleration)), 0)
            self.assertLess(acceleration[0], 0)  # Inward at the rightmost point.

    def test_thin_lens_rays_obey_lens_equation_and_magnification(self):
        svg = drawing('thin-lens')
        parallel = points(svg.find('.//*[@id="lens-ray-parallel"]'))
        central = points(svg.find('.//*[@id="lens-ray-central"]'))
        self.assertEqual(parallel[0], central[0])
        self.assertEqual(parallel[-1], central[-1])
        (xo, yo), (xl, axis), (xi, yi) = central
        _, ray_height = parallel[1]
        focus = xl+(axis-ray_height)*(xi-xl)/(yi-ray_height)
        f, do, di = focus-xl, xl-xo, xi-xl
        self.assertAlmostEqual(1/f, 1/do+1/di)
        self.assertAlmostEqual((yi-axis)/(yo-axis), -di/do)

    def test_carnot_states_follow_two_isotherms_and_two_adiabats(self):
        svg = drawing('carnot', 'pv-cycle')
        states = ast.literal_eval(svg.find('.//*[@id="cycle-states"]').text)
        (v1, p1), (v2, p2), (v3, p3), (v4, p4) = states
        self.assertAlmostEqual(p1*v1, p2*v2)
        self.assertAlmostEqual(p3*v3, p4*v4)
        self.assertAlmostEqual(p2*v2**(5/3), p3*v3**(5/3))
        self.assertAlmostEqual(p4*v4**(5/3), p1*v1**(5/3))
        self.assertGreater(p1*v1, p3*v3)
        self.assertGreater(v2, v1)
        self.assertGreater(v3, v2)

    def test_terminal_force_balance_and_equal_speed_velocity_triangle(self):
        svg = drawing('terminal-speed')
        arrows = [e for e in svg.findall('.//s:line', NS) if e.get('marker-end') and e.get('x1') == '390.000']
        self.assertEqual(len(arrows), 2)
        self.assertEqual(vector(arrows[0])[1], -vector(arrows[1])[1])
        svg = drawing('centripetal-acceleration', 'velocity-change')
        arrows = [e for e in svg.findall('.//s:line', NS) if e.get('x1') == '110.000']
        lengths = [math.hypot(*vector(e)) for e in arrows]
        self.assertAlmostEqual(lengths[0], lengths[1], places=3)


if __name__ == '__main__':
    unittest.main()
