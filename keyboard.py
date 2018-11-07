from enum import Enum
import unittest

# ---
class Keyboard(object):
    class Layout(Enum):
        L1xN = 1
        L2xN = 2
        L3xN = 3

    @staticmethod
    def _validate1(button):
        return \
            button.get('ActionType') != None      and \
            isinstance(button['ActionType'], str) and \
            button['ActionType'] in ['reply']     and \
            button.get('ActionBody') != None      and \
            isinstance(button['ActionBody'], str) and \
            button.get('Text') != None            and \
            isinstance(button['Text'], str)

    def _validate(self):
        for b in self._buttons:
            if not Keyboard._validate1(b):
                raise ValueError("Error in keyboard format near {}".format(b))

    def __init__(self, buttons, layout=Layout.L1xN):
        self._buttons = buttons
        self._layout  = layout
        self._validate()

    def eq(self, other):
        if len(self._buttons) != len(other._buttons):
            return False
        for i in range(len(self._buttons)):
            if \
            self._buttons[i]['ActionType'] != other._buttons[i]['ActionType'] or \
            self._buttons[i]['ActionBody'] != other._buttons[i]['ActionBody'] or \
            self._buttons[i]['Text']       != other._buttons[i]['Text']:
                return False
        return self._layout == other._layout

    def to_viber_keys(self):
        pass

    def to_ut_str(self):
        return ' '.join(list(map(lambda x: x['Text'], self._buttons)))

    @staticmethod
    def cmd_button(name):
        return {'ActionType':'reply',
                'ActionBody':name,
                'Text':'{{{{{}}}}}'.format(name)}


# ---
class TestKeyboard(unittest.TestCase):
    def test_keyboard(self):
        with self.assertRaises(ValueError):
            kbdx = Keyboard([{'ActionType':'reply',
                              'Text':'{{reg}}'}])

        kbd = Keyboard([{'ActionType':'reply',
                         'ActionBody':'reg',
                         'Text':'{{reg}}'},
                        {'ActionType':'reply',
                         'ActionBody':'info',
                         'Text':'{{info}}'}])
        kbd2 = Keyboard([Keyboard.cmd_button('reg'),
                         Keyboard.cmd_button('info')])
        kbd3 = Keyboard([Keyboard.cmd_button('regx'),
                         Keyboard.cmd_button('info')])

        self.assertTrue(kbd2.eq(kbd))
        self.assertFalse(kbd3.eq(kbd))
        self.assertFalse(kbd3.eq(Keyboard([])))

    def test_keyboard_to_viber(self):
        pass

# ---
if __name__ == '__main__':
    unittest.main()
