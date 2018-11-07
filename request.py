from transitions.extensions import GraphMachine as Machine
#model.get_graph().draw('my_state_diagram.png', prog='dot')

#from transitions import Machine
from transitions import State
from keyboard import Keyboard
from rutils import RequestPayloadUT


import re
import unittest
import datetime


CMD_REG_TEL          = "Register"
CMD_ADD_HOME_FLAT_NR = "AddHomeFlat"
CMD_ADD_CAR_NR       = "AddCar"
CMD_ADD_NAME         = "AddName"

TXT_IDENTIFY__NEW_USER="""
Кажется, Вы новый пользователь...
"""
TXT_REG_TEL_NR="""
Введите ваш номер телефона:
"""
TXT_GOT_TEL_NR="""
Для подтверждения актуальности Ваших данных, необходимо с регистрируемого
телефона отправить на номер {} СМС с проверочным кодом {}.
"""
TXT_ADD_HOME_FL_NR="""
Введите ваш номер дома и квартиры в формате '4-Д,197':
"""
TXT_GOT_HOME_FL_NR="""
Спасибо. Номер дома и квартиры {} введены.
"""
TXT_ADD_CAR_NR="""
Введите номер вашей машины в формате 'ХХ1111ХХ':
"""
TXT_GOT_CAR_NR="""
Спасибо. Номер машины {} введен.
"""
TXT_ADD_NAME="""
Введите ваше имя:
"""
TXT_GOT_NAME="""
Спасибо. {}, Ваше имя добавлено.
"""
ERR_TEL_NR="""
Убедитесь в правильности ввода телефона.
"""
ERR_GENERAL="""
Неведомая ошибка.
"""
KBD_ALL_KEYS=Keyboard([Keyboard.cmd_button(CMD_REG_TEL),
                       Keyboard.cmd_button(CMD_ADD_NAME),
                       Keyboard.cmd_button(CMD_ADD_CAR_NR),
                       Keyboard.cmd_button(CMD_ADD_HOME_FLAT_NR)])

# ---
class Request(object):

    # --- validity checks ---
    def is_tel_nr_valid(self):
        print("is_telephone_nr_valid()")
        self._user_telephone = self._payload.text()
        return not re.match(r'[+]380\d{2}\d{7}', self._user_telephone) is None

    def is_user_name_valid(self):
        print("is_user_name_valid()")
        self._user_name = self._payload.text()
        return not re.match(r'\w+', self._user_name) is None

    def is_home_flat_valid(self):
        print("is_home_flat_valid()")
        return True

    def is_car_valid(self):
        print("is_car_valid()")
        return True

    def is_cmd(self, stype):
        print("is_cmd({})".format(stype))
        cmd = self._payload.text()
        return cmd == "{{" + stype + "}}"

    def is_reg_tel_cmd(self):
        return self.is_cmd(CMD_REG_TEL)

    def is_add_home_flat_cmd(self):
        return self.is_cmd(CMD_ADD_HOME_FLAT_NR)

    def is_add_name_cmd(self):
        return self.is_cmd(CMD_ADD_NAME)

    def is_add_car_cmd(self):
        return self.is_cmd(CMD_ADD_CAR_NR)

    def is_unknown_cmd(self):
        return not (self.is_reg_tel_cmd()       or \
                    self.is_add_home_flat_cmd() or \
                    self.is_add_car_cmd()       or \
                    self.is_add_name_cmd())

    def db_failed(self):
        return False

    # --- on enter ---
    def on_enter_IDENTIFY(self):
        print("on_enter state={}".format(self.state))
        # put sql queries into data base
        # check user is present inside data base tables
        # set _user_identified and _user_confirmed to an appropriate state according to db
        self._user_identified = False
        self._user_confirmed  = False
        self._need_input      = False
        self._need_output     = True
        self._message_out     = TXT_IDENTIFY__NEW_USER
        self._kb_out          = KBD_ALL_KEYS
    # ---
    def generateConfirmationCode(self):
        stime = str(datetime.datetime.timestamp(datetime.datetime.now()))
        return str(stime).replace('.','')[-5:]

    def on_enter_REG_TEL_NR(self):
        print("on_enter state={}".format(self.state))
        self._need_input  = True
        self._message_out = TXT_REG_TEL_NR
        self._kb_out = Keyboard([])

    def on_enter_GOT_TEL_NR(self):
        print("on_enter state={}".format(self.state))
        self._confirmation_code = self.generateConfirmationCode()
        self._need_input        = False
        self._need_output       = False
        self._message_out       = TXT_GOT_TEL_NR
        self._kb_out            = KBD_ALL_KEYS
    # ---
    def on_enter_ADD_HOME_FL_NR(self):
        print("on_enter state={}".format(self.state))
        self._need_input  = True
        self._message_out = TXT_ADD_HOME_FL_NR
        self._kb_out = Keyboard([])

    def on_enter_GOT_HOME_FL_NR(self):
        self._need_input  = False
        self._need_output = False
        self._message_out = TXT_GOT_HOME_FL_NR
        self._kb_out      = KBD_ALL_KEYS
        pass
    # ---
    def on_enter_ADD_CAR_NR(self):
        print("on_enter state={}".format(self.state))
        self._need_input  = True
        self._message_out = TXT_ADD_CAR_NR
        self._kb_out = Keyboard([])

    def on_enter_GOT_CAR_NR(self):
        self._need_input  = False
        self._need_output = False
        self._message_out = TXT_GOT_CAR_NR
        self._kb_out      = KBD_ALL_KEYS
        pass
    # ---
    def on_enter_ADD_NAME(self):
        print("on_enter state={}".format(self.state))
        self._need_input  = True
        self._message_out = TXT_ADD_NAME
        self._kb_out = Keyboard([])

    def on_enter_GOT_NAME(self):
        self._need_input  = False
        self._need_output = False
        self._message_out = TXT_GOT_NAME
        self._kb_out      = KBD_ALL_KEYS
        pass
    # ---
    def on_enter_UPDATE_DB(self):
        print("on_enter state={}".format(self.state))
        self._need_output = False
        self._need_input  = False

    def on_enter_ERROR(self):
        print("on_enter state={}".format(self.state))
        self._message_out = ERR_GENERAL
        self._kb_out      = KBD_ALL_KEYS
        self._need_output = False
        self._need_input  = False

    def on_enter_DELETE(self):
        print("on_enter state={}".format(self.state))
        self._need_input = True

    def _init_sm(self):
        states = ['NEW', 'IDENTIFY',

                  'REG_TEL_NR',     'GOT_TEL_NR',
                  'ADD_HOME_FL_NR', 'GOT_HOME_FL_NR',
                  'ADD_CAR_NR',     'GOT_CAR_NR',
                  'ADD_NAME',       'GOT_NAME',

                  'UPDATE_DB',
                  'DELETE',
                  'ERROR']
        #self._machine = Machine(model=self, states=states, initial='NEW')
        self._machine = Machine(model=self, states=states, initial='NEW', show_conditions=True)
        self._machine.add_transition('advance', 'NEW',                'IDENTIFY')
        # --- IDENTIFY to ALL
        self._machine.add_transition('advance', 'IDENTIFY',           'REG_TEL_NR',
                                     unless='db_failed',
                                     conditions='is_reg_tel_cmd')
        self._machine.add_transition('advance', 'IDENTIFY',           'ADD_HOME_FL_NR',
                                     unless='db_failed',
                                     conditions='is_add_home_flat_cmd')
        self._machine.add_transition('advance', 'IDENTIFY',           'ADD_CAR_NR',
                                     unless='db_failed',
                                     conditions='is_add_car_cmd')
        self._machine.add_transition('advance', 'IDENTIFY',           'ADD_NAME',
                                     unless='db_failed',
                                     conditions='is_add_name_cmd')
        self._machine.add_transition('advance', 'IDENTIFY',           'ERROR',
                                     conditions='db_failed')
        self._machine.add_transition('advance', 'IDENTIFY',           'ERROR',
                                     conditions='is_unknown_cmd')
        # --- TEL_NRs
        self._machine.add_transition('advance', 'REG_TEL_NR',         'GOT_TEL_NR',
                                     conditions='is_tel_nr_valid')
        self._machine.add_transition('advance', 'REG_TEL_NR',         'ERROR')
        self._machine.add_transition('advance', 'GOT_TEL_NR',         'UPDATE_DB')
        # --- HOME_FL_NRs
        self._machine.add_transition('advance', 'ADD_HOME_FL_NR',     'GOT_HOME_FL_NR',
                                     conditions='is_home_flat_valid')
        self._machine.add_transition('advance', 'ADD_HOME_FL_NR',     'ERROR')
        self._machine.add_transition('advance', 'GOT_HOME_FL_NR',     'UPDATE_DB')
        # --- CAR_NRs
        self._machine.add_transition('advance', 'ADD_CAR_NR',         'GOT_CAR_NR',
                                     conditions='is_car_valid')
        self._machine.add_transition('advance', 'ADD_CAR_NR',         'ERROR')
        self._machine.add_transition('advance', 'GOT_CAR_NR',         'UPDATE_DB')
        # --- NAME_NRs
        self._machine.add_transition('advance', 'ADD_NAME',           'GOT_NAME',
                                     conditions='is_user_name_valid')
        self._machine.add_transition('advance', 'ADD_NAME',           'ERROR')
        self._machine.add_transition('advance', 'GOT_NAME',           'UPDATE_DB')
        #---
        self._machine.add_transition('advance', 'UPDATE_DB',          'ERROR',
                                     conditions='db_failed')
        self._machine.add_transition('advance', 'UPDATE_DB',          'DELETE')
        self._machine.add_transition('advance', 'ERROR',              'DELETE')

    # ---- Public ----

    def get_kbd(self):
        return self._kb_out

    def get_message_out(self):
        return self._message_out

    def get_user_id(self):
        self._payload.user_id()

    def need_input(self):
        return self._need_input

    def need_output(self):
        return self.need_input() or self._need_output

    def finished(self):
        return self.state == "DELETE"

    def update_payload(self, payload):
        self._payload = payload

    def __init__(self, payload):
        self._payload = payload
        self._message_out = None
        self._kb_out = None

        self._user_identified = None
        self._user_confirmed = None
        self._user_blocked = None
        self._need_input = False
        self._need_output = False

        self._user_telephone=''
        self._user_name=''
        self._confirmation_code=''
        self._user_home_flat=''

        self._init_sm()


# ---
class TestRequest(unittest.TestCase):

    def test_success_registration(self):
        message = RequestPayloadUT(["MESSAGE_REQUEST", "{{"+CMD_REG_TEL+"}}", "time_12:00", "user_id"])
        rq = Request(message)
        # first entering into chat
        # ->incoming() with ViberMessageRequest called
        self.assertTrue(rq.state == 'NEW')
        self.assertTrue(rq.need_input() is False)

        rq.advance()
        self.assertTrue(rq.state == 'IDENTIFY')
        self.assertTrue(rq._user_identified is False)
        self.assertTrue(rq._user_confirmed is False)
        self.assertTrue(rq.need_input() is False)
        self.assertTrue(rq.get_message_out() == TXT_IDENTIFY__NEW_USER)
        self.assertTrue(rq.get_kbd().eq(KBD_ALL_KEYS))

        rq.advance()
        self.assertTrue(rq.state == 'REG_TEL_NR')
        self.assertTrue(rq._user_identified is False)
        self.assertTrue(rq._user_confirmed is False)
        self.assertTrue(rq.need_input() is True)
        self.assertTrue(rq.get_message_out() == TXT_REG_TEL_NR)
        self.assertTrue(rq.get_kbd().eq(Keyboard([])))
        message._payload[1] = '+380667176666'

        rq.advance()
        self.assertTrue(rq.state == 'GOT_TEL_NR')
        self.assertTrue(rq._user_identified is False)
        self.assertTrue(rq._user_confirmed is False)
        self.assertTrue(rq.need_input() is False)
        self.assertTrue(re.match(r'\d{5}', rq._confirmation_code))
        self.assertTrue(rq.get_message_out() == TXT_GOT_TEL_NR)
        self.assertTrue(rq.get_kbd().eq(KBD_ALL_KEYS))

        rq.advance()
        self.assertTrue(rq.state == 'UPDATE_DB')
        self.assertTrue(rq._user_identified is False)
        self.assertTrue(rq._user_confirmed is False)
        self.assertTrue(rq.need_input() is False)
        self.assertTrue(rq.get_message_out() == TXT_GOT_TEL_NR)
        self.assertTrue(rq.get_kbd().eq(KBD_ALL_KEYS))

        rq.advance()
        self.assertTrue(rq.state == 'DELETE')
        self.assertTrue(rq.get_message_out() == TXT_GOT_TEL_NR)
        self.assertTrue(rq.need_input() is True)

    def test_success_AddEstateInfo(self):
        message = RequestPayloadUT(["MESSAGE_REQUEST", "{{"+CMD_ADD_HOME_FLAT_NR+"}}", "time_12:00", "user_id"])
        rq = Request(message)
        # first entering into chat
        # ->incoming() with ViberMessageRequest called
        self.assertTrue(rq.state == 'NEW')
        self.assertTrue(rq.need_input() is False)

        rq.advance()
        self.assertTrue(rq.state == 'IDENTIFY')
        self.assertTrue(rq._user_identified is False)
        self.assertTrue(rq._user_confirmed is False)
        self.assertTrue(rq.need_input() is False)
        self.assertTrue(rq.get_message_out() == TXT_IDENTIFY__NEW_USER)
        self.assertTrue(rq.get_kbd().eq(Keyboard([Keyboard.cmd_button(CMD_REG_TEL),
                                                  Keyboard.cmd_button(CMD_ADD_NAME),
                                                  Keyboard.cmd_button(CMD_ADD_CAR_NR),
                                                  Keyboard.cmd_button(CMD_ADD_HOME_FLAT_NR)])))

        rq.advance()
        self.assertTrue(rq.state == 'ADD_HOME_FL_NR')
        self.assertTrue(rq._user_identified is False)
        self.assertTrue(rq._user_confirmed is False)
        self.assertTrue(rq.need_input() is True)
        self.assertTrue(rq.get_message_out() == TXT_ADD_HOME_FL_NR)
        self.assertTrue(rq.get_kbd().eq(Keyboard([])))
        message._payload[1] = '4Д,197'

        rq.advance()
        self.assertTrue(rq.state == 'GOT_HOME_FL_NR')
        self.assertTrue(rq._user_identified is False)
        self.assertTrue(rq._user_confirmed is False)
        self.assertTrue(rq.need_input() is False)
        self.assertTrue(rq.get_message_out() == TXT_GOT_HOME_FL_NR)
        self.assertTrue(rq.get_kbd().eq(KBD_ALL_KEYS))

        rq.advance()
        self.assertTrue(rq.state == 'UPDATE_DB')
        self.assertTrue(rq._user_identified is False)
        self.assertTrue(rq._user_confirmed is False)
        self.assertTrue(rq.need_input() is False)
        self.assertTrue(rq.get_message_out() == TXT_GOT_HOME_FL_NR)
        self.assertTrue(rq.get_kbd().eq(KBD_ALL_KEYS))

        rq.advance()
        self.assertTrue(rq.state == 'DELETE')
        self.assertTrue(rq.get_message_out() == TXT_GOT_HOME_FL_NR)
        self.assertTrue(rq.need_input() is True)

    def test_success_AddCarNr(self):
        message = RequestPayloadUT(["MESSAGE_REQUEST", "{{"+CMD_ADD_CAR_NR+"}}", "time_12:00", "user_id"])
        rq = Request(message)
        # first entering into chat
        # ->incoming() with ViberMessageRequest called
        self.assertTrue(rq.state == 'NEW')
        self.assertTrue(rq.need_input() is False)

        rq.advance()
        self.assertTrue(rq.state == 'IDENTIFY')
        self.assertTrue(rq._user_identified is False)
        self.assertTrue(rq._user_confirmed is False)
        self.assertTrue(rq.need_input() is False)
        self.assertTrue(rq.get_message_out() == TXT_IDENTIFY__NEW_USER)
        self.assertTrue(rq.get_kbd().eq(Keyboard([Keyboard.cmd_button(CMD_REG_TEL),
                                                  Keyboard.cmd_button(CMD_ADD_NAME),
                                                  Keyboard.cmd_button(CMD_ADD_CAR_NR),
                                                  Keyboard.cmd_button(CMD_ADD_HOME_FLAT_NR)])))

        rq.advance()
        self.assertTrue(rq.state == 'ADD_CAR_NR')
        self.assertTrue(rq._user_identified is False)
        self.assertTrue(rq._user_confirmed is False)
        self.assertTrue(rq.need_input() is True)
        self.assertTrue(rq.get_message_out() == TXT_ADD_CAR_NR)
        self.assertTrue(rq.get_kbd().eq(Keyboard([])))
        message._payload[1] = 'вн1984не'

        rq.advance()
        self.assertTrue(rq.state == 'GOT_CAR_NR')
        self.assertTrue(rq._user_identified is False)
        self.assertTrue(rq._user_confirmed is False)
        self.assertTrue(rq.need_input() is False)
        self.assertTrue(rq.get_message_out() == TXT_GOT_CAR_NR)
        self.assertTrue(rq.get_kbd().eq(KBD_ALL_KEYS))

        rq.advance()
        self.assertTrue(rq.state == 'UPDATE_DB')
        self.assertTrue(rq._user_identified is False)
        self.assertTrue(rq._user_confirmed is False)
        self.assertTrue(rq.need_input() is False)
        self.assertTrue(rq.get_message_out() == TXT_GOT_CAR_NR)
        self.assertTrue(rq.get_kbd().eq(KBD_ALL_KEYS))

        rq.advance()
        self.assertTrue(rq.state == 'DELETE')
        self.assertTrue(rq.get_message_out() == TXT_GOT_CAR_NR)
        self.assertTrue(rq.need_input() is True)

    def test_success_AddName(self):
        message = RequestPayloadUT(["MESSAGE_REQUEST", "{{"+CMD_ADD_NAME+"}}", "time_12:00", "user_id"])
        rq = Request(message)
        # first entering into chat
        # ->incoming() with ViberMessageRequest called
        self.assertTrue(rq.state == 'NEW')
        self.assertTrue(rq.need_input() is False)

        rq.advance()
        self.assertTrue(rq.state == 'IDENTIFY')
        self.assertTrue(rq._user_identified is False)
        self.assertTrue(rq._user_confirmed is False)
        self.assertTrue(rq.need_input() is False)
        self.assertTrue(rq.get_message_out() == TXT_IDENTIFY__NEW_USER)
        self.assertTrue(rq.get_kbd().eq(KBD_ALL_KEYS))

        rq.advance()
        self.assertTrue(rq.state == 'ADD_NAME')
        self.assertTrue(rq._user_identified is False)
        self.assertTrue(rq._user_confirmed is False)
        self.assertTrue(rq.need_input() is True)
        self.assertTrue(rq.get_message_out() == TXT_ADD_NAME)
        self.assertTrue(rq.get_kbd().eq(Keyboard([])))
        message._payload[1] = 'Анатолий'

        rq.advance()
        self.assertTrue(rq.state == 'GOT_NAME')
        self.assertTrue(rq._user_identified is False)
        self.assertTrue(rq._user_confirmed is False)
        self.assertTrue(rq.need_input() is False)
        self.assertTrue(rq.get_message_out() == TXT_GOT_NAME)
        self.assertTrue(rq.get_kbd().eq(KBD_ALL_KEYS))

        rq.advance()
        self.assertTrue(rq.state == 'UPDATE_DB')
        self.assertTrue(rq._user_identified is False)
        self.assertTrue(rq._user_confirmed is False)
        self.assertTrue(rq.need_input() is False)
        self.assertTrue(rq.get_message_out() == TXT_GOT_NAME)
        self.assertTrue(rq.get_kbd().eq(KBD_ALL_KEYS))

        rq.advance()
        self.assertTrue(rq.state == 'DELETE')
        self.assertTrue(rq.get_message_out() == TXT_GOT_NAME)
        self.assertTrue(rq.need_input() is True)

if __name__ == '__main__':
    unittest.main()
