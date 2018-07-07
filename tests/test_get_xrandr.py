from unittest import TestCase
from unittest.mock import patch
import os

from dmenuxrandr.xrandr import get_xrandr


def read_from_file(path):
    with open(os.path.dirname(os.path.realpath(__file__)) + '/xrandr_fixtures/' + path, 'rb') as xrandr_output_file:
        return xrandr_output_file.read()


class TestXrandr(TestCase):
    @patch('dmenuxrandr.xrandr.check_output', return_value=read_from_file('2_screens.txt'))
    def test_xrandr_two_screens_has_primary_screen(self, xrandr_mock):
        outputs = get_xrandr()
        self.assertEqual(4, len(outputs), 'Number of outputs')
        self.assertIn('eDP1', outputs, 'Main screen in ouputs')
        self.assertTrue(outputs['eDP1']['isPrimary'])
        self.assertTrue(outputs['eDP1']['isMapped'])
        self.assertTrue(outputs['eDP1']['isConnected'])
        self.assertIn('1920x1080', outputs['eDP1']['modes'], 'HD resolution is available')

    @patch('dmenuxrandr.xrandr.check_output', return_value=read_from_file('2_screens.txt'))
    def test_xrandr_two_screens_has_two_active_screens(self, xrandr_mock):
        outputs = get_xrandr()
        self.assertEqual(4, len(outputs), 'Number of outputs')
        self.assertIn('eDP1', outputs, 'Main screen in ouputs')
        self.assertIn('DP1', outputs, 'Offscreen in ouputs')
        self.assertTrue(outputs['eDP1']['isPrimary'])
        self.assertTrue(outputs['eDP1']['isMapped'])
        self.assertTrue(outputs['eDP1']['isConnected'])
        self.assertFalse(outputs['DP1']['isPrimary'])
        self.assertTrue(outputs['DP1']['isMapped'])
        self.assertTrue(outputs['DP1']['isConnected'])
        self.assertIn('1920x1080', outputs['eDP1']['modes'], 'HD resolution is available')

    @patch('dmenuxrandr.xrandr.check_output', return_value=read_from_file('connected_unmapped_screen.txt'))
    def test_xrandr_connected_unmapped_screen(self, xrandr_mock):
        outputs = get_xrandr()
        output = 'DP2'
        self.assertIn(output, outputs, 'new screen is in the outputs')
        self.assertTrue(outputs[output]['isConnected'], 'new screen is connected')
        self.assertFalse(outputs[output]['isMapped'], 'new screen is not mapped')

    @patch('dmenuxrandr.xrandr.check_output', return_value=read_from_file('disconnected_mapped_screen.txt'))
    def test_xrandr_disconnected_mapped_screen(self, xrandr_mock):
        outputs = get_xrandr()
        output = 'DP2'
        self.assertIn(output, outputs, 'new screen is in the outputs')
        self.assertFalse(outputs[output]['isConnected'], 'new screen is not connected')
        self.assertTrue(outputs[output]['isMapped'], 'new screen is mapped')