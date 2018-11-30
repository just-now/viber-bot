from keyboard import Keyboard
from rutils import RequestPayloadUT

import re
import sys
import unittest
import datetime
import asyncio


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

class Utils(object):
    pass

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

    def generateConfirmationCode(self):
        stime = str(datetime.datetime.timestamp(datetime.datetime.now()))
        return str(stime).replace('.','')[-5:]

    # ---- Private ----

    def _update_payload(self, payload):
        self._payload = payload

    async def co_get_message(self):
        self._future = self._loop.create_future()
        self._loop.stop()
        await self._future
        return self._future.result()

    async def co_run_task(self):
        print("co_run_task()")
        try:
            # indentifying user
            self._user_identified = False
            self._user_confirmed  = False

            self._need_output     = True
            self._message_out     = TXT_IDENTIFY__NEW_USER
            self._kb_out          = KBD_ALL_KEYS
            incoming_payload = await self.co_get_message()
            self._update_payload(incoming_payload)

            # parse commands
            if self.is_reg_tel_cmd():
                self._need_input  = True
                self._message_out = TXT_REG_TEL_NR
                self._kb_out = Keyboard([])
                incoming_payload = await self.co_get_message()
                self._update_payload(incoming_payload)
                # inside the message we got tel nr from user
                if self.is_tel_nr_valid():
                    #update db
                    print("valid tel nr")
                    print("update db")
                    pass
                else:
                    #send user error message
                    print("invalid tel nr")
                    pass

            elif self.is_add_home_flat_cmd():
                pass
            elif self.is_add_car_cmd():
                pass
            elif self.is_add_name_cmd():
                pass
            else:
                print("Unknown command!")
        except Exception as e:
            print("Something wrong happened! {}".format(e))
            sys.exit(1)
        finally:
            self._loop.stop()
            print("Coroutine finished")
            self._finished = True

    # ---- Public ----

    def get_kbd(self):
        return self._kb_out

    def get_message_out(self):
        return self._message_out

    def get_user_id(self):
        self._payload.user_id()

    def finished(self):
        return self._finished

    def __init__(self, loop):
        self._payload = None
        self._message_out = None
        self._kb_out = None

        self._user_identified = None
        self._user_confirmed = None
        self._user_blocked = None
        self._need_output = False
        self._finished = False

        self._user_telephone=''
        self._user_name=''
        self._confirmation_code=''
        self._user_home_flat=''

        self._loop = loop
        self._task = loop.create_task(self.co_run_task())
        self._loop.run_forever()

    def advance(self, payload):
        self._future.set_result(payload)
        self._loop.run_forever()
        return self._need_output

if __name__ == '__main__':
    unittest.main()
