from decimal import Decimal
from django.test import TestCase
from spectrum.color import Color


class TestColor(TestCase):
    def test_default_opacity(self):
        color = Color('FFFFFF')
        self.assertEqual(color.opacity, 1)

    def test_invalid_color_type(self):
        tests = [
            None,
            255,
            (255, 255, 0),
            Color('#FFFF00'),
        ]

        for value in tests:
            with self.subTest(value):
                with self.assertRaises(TypeError):
                    Color(value)

    def test_invalid_color_value(self):
        tests = [
            '',
            '#',
            '#1',
            '#12',
            '#1234',
            '#12345',
            '#1234567',
            '1',
            '12',
            '1234',
            '12345',
            '1234567',
            '####',
            '##FFF',
            'XXX',
            'ABCDEH',
            '#GGG',
            '#A0A0G0',
        ]

        for value in tests:
            with self.subTest(value):
                with self.assertRaises(ValueError):
                    Color(value)

    def test_invalid_opacity_type(self):
        tests = [
            None,
            [1, 5],
            (0, 1, 2),
            {1},
            {1: 0.25},
        ]

        for value in tests:
            with self.subTest(value):
                with self.assertRaises(TypeError):
                    Color('FFFFFF', value)

    def test_invalid_opacity_value(self):
        tests = [
            -0.1,
            1.1,
            2,
            '2',
            Decimal('Infinity'),
        ]

        for value in tests:
            with self.subTest(value):
                with self.assertRaises(ValueError):
                    Color('FFFFFF', value)

    def test_hex(self):
        tests = {
            '000': '#000000',
            'a55': '#AA5555',
            '#bAc': '#BBAACC',
            '#123': '#112233',
            'b00b00': '#B00B00',
            '806099': '#806099',
            '#de1e7e': '#DE1E7E',
            '#Facade': '#FACADE',
        }

        for value, output in tests.items():
            with self.subTest(value):
                self.assertEqual(Color(value).hex, output)

    def test_opacity(self):
        tests = {
            0: Decimal('0'),
            1: Decimal('1'),
            0.501: Decimal('0.5'),
            0.254: Decimal('0.25'),
            0.255: Decimal('0.26'),
            0.124: Decimal('0.12'),
            0.125: Decimal('0.12'),
            '0': Decimal('0'),
            '0.123': Decimal('0.12'),
            '_0.3__': Decimal('0.3'),      # acceptable by decimal.Decimal
            Decimal('0.543'): Decimal('0.54'),
        }

        for value, output in tests.items():
            with self.subTest(value):
                self.assertEqual(Color('c0ffee', value).opacity, output)

    def test_str(self):
        color = Color('#60A')
        self.assertEqual(str(color), '#6600AA')

        color = Color('#ABC', 1)
        self.assertEqual(str(color), '#AABBCC')

        color = Color('#60A', 0.8)
        self.assertEqual(str(color), 'rgba(102,0,170,0.8)')

        color = Color('#BADA00', 1)
        self.assertEqual(str(color), '#BADA00')

    def test_comparison(self):
        self.assertNotEqual(Color('#FFFF00'), 'FFFF00')

        self.assertEqual(Color('#60A'), '#6600AA')
        self.assertEqual(Color('#c0FFeE'), '#C0FFEE')
        self.assertEqual(Color('#c0FFeE'), '#c0ffee')
        self.assertEqual(Color('#60A'), Color('#6600AA'))
        self.assertEqual(Color('#c0FFeE'), Color('#C0FFEE'))
        self.assertEqual(Color('#c0FFeE'), Color('#c0ffee'))
        self.assertNotEqual(Color('#AABBCC', 0.99), '#AABBCC')

    def test_rgb(self):
        tests = {
            '#C0C0C0': 'rgb(192,192,192)',
            '#A52A2A': 'rgb(165,42,42)',
            '#ff7f50': 'rgb(255,127,80)',
            '#006400': 'rgb(0,100,0)',
        }

        for value, output in tests.items():
            with self.subTest(value):
                self.assertEqual(Color(value).rgb, output)

    def test_rgba(self):
        tests = {
            ('#C0C0C0',): 'rgba(192,192,192,1)',
            ('#A52A2A', 0.5): 'rgba(165,42,42,0.5)',
            ('#ff7f50', 0): 'rgba(255,127,80,0)',
            ('#006400', 0.134): 'rgba(0,100,0,0.13)',
            ('#c0FFee', 0.135): 'rgba(192,255,238,0.14)',
        }

        for value, output in tests.items():
            with self.subTest(value):
                self.assertEqual(Color(*value).rgba, output)