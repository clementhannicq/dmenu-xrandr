from unittest import TestCase
from unittest.mock import patch

from dmenuxrandr.prompt import prompt, InvalidValue


class TestPrompt(TestCase):
    def test_prompt_returns_sole_entry_if_unless_stupid(self):
        entry = 'oneEntry'
        output = prompt([entry], unless_stupid=True, allow_unknown_values=False)
        self.assertEqual(entry, output, 'Should return the only possible output')

    @patch('dmenuxrandr.prompt.dmenu.show', return_value='userValue')
    def test_prompt_still_prompts_the_user_if_unknown_values(self, dmenu_show):
        prompt(['meh'], unless_stupid=True, allow_unknown_values=True)
        self.assertTrue(dmenu_show.called, 'dmenu.show should have been called')

    @patch('dmenuxrandr.prompt.dmenu.show', return_value='2')
    def test_prompt_returns_the_selected_value(self, dmenu_show):
        output = prompt(['1', '2', '3'])
        self.assertEqual('2', output)

    @patch('dmenuxrandr.prompt.dmenu.show', return_value='not in the list')
    def test_prompt_thows_on_unknown_values(self, dmenu_show):
        self.assertRaises(InvalidValue, lambda: prompt(['1', '2', '3'], allow_unknown_values=False))

    @patch('dmenuxrandr.prompt.dmenu.show', return_value='not in the list')
    def test_prompt_returns_unknown_values(self, dmenu_show):
        output = prompt(['1', '2', '3'], allow_unknown_values=True)
        self.assertEqual('not in the list', output)
