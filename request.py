from transitions.extensions import GraphMachine as Machine
#model.get_graph().draw('my_state_diagram.png', prog='dot')

#from transitions import Machine
from transitions import State
from keyboard import Keyboard
from rutils import RequestPayloadUT

import re
import unittest

CMD_REGISTER = "Register"
CMD_ADD_HOME = "AddHome"

NEW_USER_IDENTIFY="""
Кажется, Вы новый пользователь...
"""

NEW_USER_REGISTRATION="""
Для использования бота Вам будет необходимо пройти процедуру
регистрации.  Вам будет предложено ввести Ваше ФИО и номер телефона.

Теперь, введите Ваше ФИО:
"""

NEW_USER_GOT_PERSONAL_NAME="""
Теперь, когда Ваше ФИО введено, введите Ваш номер телефона:
"""

NEW_USER_PROCESS_PN_TNR="""
Ваши данные введены.
Для подтверждения актуальности Ваших данных, необходимо с
регистрируемого телефона отправить на номер +38077-777-5555 СМС с
подтверждающим регистрацию проверочным кодом.

Вот этот код:
{}
"""

# ---
class Request(object):
    def telephone_nr_is_valid(self):
        print("telephone_nr_is_valid()")
        self._user_telephone = self._payload.text()
        return not re.match(r'[+]380\d{2}\d{7}', self._user_telephone) is None

    def personal_name_is_valid(self):
        print("personal_name_is_valid()")
        self._user_name = self._payload.text()
        return not re.match(r'\w+ \w+ \w+', self._user_name) is None

    def home_nr_is_valid(self):
        print("home_nr_is_valid()")
        self._user_name = self._payload.text()
        return not re.match(r'4-[БВГД]', self._user_name) is None

    def home_nr_is_valid(self):
        print("flat_nr_is_valid()")
        self._user_name = self._payload.text()
        return not re.match(r'\d+', self._user_name) is None

    def tries_not_acceptable(self):
        return True

    def db_failed(self):
        return False

    def is_reg_cmd(self):
        print("is_reg_cmd()")
        cmd = self._payload.text()
        return cmd == "{{" + CMD_REGISTER + "}}"

    def is_add_home_cmd(self):
        print("is_reg_cmd()")
        cmd = self._payload.text()
        return cmd == "{{" + CMD_ADD_HOME + "}}"

    def on_enter_IDENTIFY(self):
        print("on_enter state={}".format(self.state))
        # put sql queries into data base
        # check user is present inside data base tables
        # set _user_identified and _user_confirmed to an appropriate state according to db
        self._user_identified = False
        self._user_confirmed  = False
        self._need_input      = True

        if not self._user_identified and not self._user_confirmed:
            self._message_out = NEW_USER_IDENTIFY
            self._kb_out = Keyboard([Keyboard.cmd_button(CMD_REGISTER)])

    def on_enter_REGISTRATION(self):
        print("on_enter state={}".format(self.state))
        if not self._user_identified and not self._user_confirmed:
            self._message_out = NEW_USER_REGISTRATION
            self._kb_out = Keyboard([])

    def on_enter_GOT_PERSONAL_NAME(self):
        print("on_enter state={}".format(self.state))
        if not self._user_identified and not self._user_confirmed:
            self._message_out = NEW_USER_GOT_PERSONAL_NAME
            self._kb_out = Keyboard([])

    def on_enter_PROCESS_PN_TNR(self):
        # put information user inputed into database
        print("on_enter state={}".format(self.state))
        self._need_input = False
        self._message_out = NEW_USER_PROCESS_PN_TNR
        self._kb_out = Keyboard([Keyboard.cmd_button('Check-If-Registered')])

    def on_enter_ADD_HOME_NR(self):
        print("on_enter state={}".format(self.state))
        pass
    def on_enter_ADD_FLAT_NR(self):
        print("on_enter state={}".format(self.state))
        pass
    def on_enter_PROCESS_ADD_HNR_FNR(self):
        print("on_enter state={}".format(self.state))
        pass

    def on_enter_ERROR(self):
        print("on_enter state={}".format(self.state))

    def on_enter_DELETE(self):
        print("on_enter state={}".format(self.state))
        self._need_input = True

    def _init_sm(self):
        states = ['NEW', 'IDENTIFY',

                  'REGISTRATION', 'GOT_PERSONAL_NAME', 'PROCESS_PN_TNR',
                  'ADD_HOME_NR', 'ADD_FLAT_NR', 'PROCESS_ADD_HNR_FNR',
                  #'ADD_CAR_NR', 'PROCESS_ADD_CNR',
                  #'DEL_CAR_NR', 'PROCESS_ADD_CNR',
                  #'DEL_HOUSE_NR', 'DEL_FLAT_NR', 'PROCESS_DEL_HNR_FNR',

                  'DELETE',
                  'ERROR']
        #self._machine = Machine(model=self, states=states, initial='NEW')
        self._machine = Machine(model=self, states=states, initial='NEW', show_conditions=True)
        self._machine.add_transition('advance', 'NEW',                'IDENTIFY')
        # ---
        self._machine.add_transition('advance', 'IDENTIFY',           'REGISTRATION',
                                     unless='db_failed',
                                     conditions='is_reg_cmd')
        self._machine.add_transition('advance', 'IDENTIFY',           'ERROR',
                                     conditions='db_failed')
        self._machine.add_transition('advance', 'IDENTIFY',           'ERROR',
                                     unless='is_reg_cmd')
        self._machine.add_transition('advance', 'REGISTRATION',       'REGISTRATION',
                                     unless=['tries_not_acceptable','personal_name_is_valid'])
        self._machine.add_transition('advance', 'REGISTRATION',       'GOT_PERSONAL_NAME',
                                     conditions='personal_name_is_valid')
        self._machine.add_transition('advance', 'REGISTRATION',       'ERROR',
                                     unless='personal_name_is_valid',
                                     conditions='tries_not_acceptable')
        self._machine.add_transition('advance', 'GOT_PERSONAL_NAME',  'GOT_PERSONAL_NAME',
                                     unless=['tries_not_acceptable','telephone_nr_is_valid'])
        self._machine.add_transition('advance', 'GOT_PERSONAL_NAME',  'PROCESS_PN_TNR',
                                     conditions='telephone_nr_is_valid')
        self._machine.add_transition('advance', 'GOT_PERSONAL_NAME',  'ERROR',
                                     unless='telephone_nr_is_valid',
                                     conditions='tries_not_acceptable')
        self._machine.add_transition('advance', 'PROCESS_PN_TNR',     'DELETE',
                                     unless='db_failed')
        self._machine.add_transition('advance', 'PROCESS_PN_TNR',     'ERROR',
                                     conditions='db_failed')
        # ---
        self._machine.add_transition('advance', 'IDENTIFY',           'ADD_HOME_NR',
                                     unless='db_failed',
                                     conditions='is_add_home_cmd')
        self._machine.add_transition('advance', 'IDENTIFY',           'ERROR',
                                     unless='is_add_home_cmd')
        self._machine.add_transition('advance', 'ADD_HOME_NR',        'ADD_HOME_NR',
                                     unless=['tries_not_acceptable','home_nr_is_valid'])
        self._machine.add_transition('advance', 'ADD_HOME_NR',        'ADD_FLAT_NR',
                                     conditions='home_nr_is_valid')
        self._machine.add_transition('advance', 'ADD_HOME_NR',        'ERROR',
                                     unless='home_nr_is_valid',
                                     conditions='tries_not_acceptable')
        self._machine.add_transition('advance', 'ADD_FLAT_NR',        'ADD_FLAT_NR',
                                     unless=['tries_not_acceptable','flat_nr_is_valid'])
        self._machine.add_transition('advance', 'ADD_FLAT_NR',        'PROCESS_ADD_HNR_FNR',
                                     conditions='flat_nr_is_valid')
        self._machine.add_transition('advance', 'ADD_FLAT_NR',        'ERROR',
                                     unless='flat_nr_is_valid',
                                     conditions='tries_not_acceptable')
        self._machine.add_transition('advance', 'PROCESS_ADD_HNR_FNR','DELETE',
                                     unless='db_failed')
        self._machine.add_transition('advance', 'PROCESS_ADD_HNR_FNR','ERROR',
                                     conditions='db_failed')
        #---
        self._machine.add_transition('advance', 'ERROR',              'DELETE')

    # ---- Public ----

    def get_kbd(self):
        return self._kb_out

    def get_message_out(self):
        return self._message_out

    def need_input(self):
        return self._need_input

    def __init__(self, payload):
        self._payload = RequestPayloadUT(payload)
        self._message_out = None
        self._kb_out = None
        self._user_identified = None
        self._user_confirmed = None
        self._user_blocked = None
        self._need_input = False

        self._user_telephone=""
        self._user_name=""

        self._init_sm()


# ---
class TestRequest(unittest.TestCase):
    def test_success_registration(self):
        message = ["MESSAGE_REQUEST", "{{Register}}", "time_12:00", "user_id"]
        rq = Request(message)
        # first entering into chat
        # ->incoming() with ViberMessageRequest called
        self.assertTrue(rq.state == 'NEW')
        self.assertTrue(rq.need_input() is False)

        rq.advance()
        self.assertTrue(rq.state == 'IDENTIFY')
        self.assertTrue(rq._user_identified is False)
        self.assertTrue(rq._user_confirmed is False)
        self.assertTrue(rq.need_input() is True)
        self.assertTrue(rq.get_message_out() == NEW_USER_IDENTIFY)
        self.assertTrue(rq.get_kbd().eq(Keyboard([Keyboard.cmd_button('Register')])))

        rq.advance()
        self.assertTrue(rq.state == 'REGISTRATION')
        self.assertTrue(rq._user_identified is False)
        self.assertTrue(rq._user_confirmed is False)
        self.assertTrue(rq.need_input() is True)
        self.assertTrue(rq.get_message_out() == NEW_USER_REGISTRATION)
        self.assertTrue(rq.get_kbd().eq(Keyboard([])))
        message[1] = 'Vsiliy Yetovich Terkin'

        rq.advance()
        self.assertTrue(rq.state == 'GOT_PERSONAL_NAME')
        self.assertTrue(rq.get_message_out() == NEW_USER_GOT_PERSONAL_NAME)
        self.assertTrue(rq.get_kbd().eq(Keyboard([])))
        self.assertTrue(rq.need_input() is True)
        message[1] = '+380667176666'

        rq.advance()
        self.assertTrue(rq.state == 'PROCESS_PN_TNR')
        self.assertTrue(rq.get_kbd().eq(Keyboard([Keyboard.cmd_button('Check-If-Registered')])))
        self.assertTrue(rq.get_message_out() == NEW_USER_PROCESS_PN_TNR)
        self.assertTrue(rq.need_input() is False)

        rq.advance()
        self.assertTrue(rq.state == 'DELETE')
        self.assertTrue(rq.need_input() is True)


if __name__ == '__main__':
    unittest.main()
