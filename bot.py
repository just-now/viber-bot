from flask import Flask, request, Response
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages.text_message import TextMessage
from viberbot.api.messages.rich_media_message import RichMediaMessage
from viberbot.api.viber_requests import ViberConversationStartedRequest
from viberbot.api.viber_requests import ViberFailedRequest
from viberbot.api.viber_requests import ViberMessageRequest
from viberbot.api.viber_requests import ViberSubscribedRequest
from viberbot.api.viber_requests import ViberUnsubscribedRequest
import ssl
import json

import time
import logging
import sched
import threading

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='/tmp/vbot.log',
                    filemode='w')
logger = logging.getLogger('ZeleniyOstrivBot')



app = Flask(__name__)
viber = Api(BotConfiguration(
    name='ZeleniyOstrivBot',
    avatar='https://uk.wikipedia.org/wiki/GNU#/media/File:Gnu_logo.jpg',
    auth_token='48a4cbb063e7d1de-579b151d93e568f1-1e549e8f54025f04'
))

class BotRequest(object):

    def usage():
        pass

    def registered():
        return false;

    def register():
        pass

    def process_request():
        if not registered():
            usage()
            return


    def __init__(self, viber_request):
        self._viber_request = viber_request
        self._commands = [
            { 'cmd': '/reg',  'has_reg': False, 'help' : "FIO,dom,kv" },
            { 'cmd': '/info', 'has_reg': True , 'help' : '' }
        ]


KBB="""{
"Type":"keyboard",
"DefaultHeight":true,
"Buttons":[
     {
      "ActionType":"reply",
      "ActionBody":"Регистрация",
      "Text":"Регистрация",
      "TextSize":"regular"
     },
     {
      "ActionType":"reply",
      "ActionBody":"Информация",
      "Text":"Информация",
      "TextSize":"regular"
     },
     {
      "ActionType":"reply",
      "ActionBody":"Информировать жильцов на этаже#",
      "Text":"Информировать жильцов на этаже#",
      "TextSize":"regular"
     },
     {
      "ActionType":"reply",
      "ActionBody":"Информировать жильцов дома#",
      "Text":"Информировать жильцов на дома#",
      "TextSize":"regular"
     },
     {
      "ActionType":"reply",
      "ActionBody":"Форум",
      "Text":"Форум",
      "TextSize":"regular"
     },
     {
      "ActionType":"reply",
      "ActionBody":"#1",
      "Text":"#1",
      "TextSize":"regular"
     },
     {
      "ActionType":"reply",
      "ActionBody":"#2",
      "Text":"#2",
      "TextSize":"regular"
     },
     {
      "ActionType":"reply",
      "ActionBody":"#3",
      "Text":"#3",
      "TextSize":"regular"
     },
     {
      "ActionType":"reply",
      "ActionBody":"#4",
      "Text":"#4",
      "TextSize":"regular"
     }
   ]
}
"""

@app.route('/', methods=['POST'])
def incoming():
    logger.debug("received request. post data: {0}".format(request.get_data()))
    # every viber message is signed, you can verify the signature using this method
    if not viber.verify_signature(request.get_data(), request.headers.get('X-Viber-Content-Signature')):
        return Response(status=403)

    # this library supplies a simple way to receive a request object
    viber_request = viber.parse_request(request.get_data())

    if isinstance(viber_request, ViberMessageRequest):
        message = viber_request.message
        message2 = TextMessage(text="@@@", keyboard=json.loads(KBB))


        # lets echo back
        logger.debug("### {0}".format(viber_request.sender.id))
        viber.send_messages(viber_request.sender.id, [
            message,
            message2
        ])
    elif isinstance(viber_request, ViberConversationStartedRequest):
        viber.send_messages(viber_request.user.id, [
            TextMessage(text="welcome here.")
        ])
    elif isinstance(viber_request, ViberFailedRequest):
        logger.warn("client failed receiving message. failure: {0}".format(viber_request))

    return Response(status=200)


def set_webhook(viber):
    logger.warn("set_web_hook")
    viber.set_webhook('https://test.just-now.online:8443')

if __name__ == "__main__":
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain('/etc/letsencrypt/live/test.just-now.online/fullchain.pem',
                            '/etc/letsencrypt/live/test.just-now.online/privkey.pem')

    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(5, 1, set_webhook, (viber,))
    t = threading.Thread(target=scheduler.run)
    t.start()

    app.run(host='0.0.0.0', port=8443, debug=True, ssl_context=context)
