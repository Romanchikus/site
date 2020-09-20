from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync
from ecomapp.models import Chat, Member
from ecomapp.views import get_last_10_messages
import urllib.request
import os


class ChatConsumer(WebsocketConsumer):
    def fetch_messages(self, data):
        messages = get_last_10_messages(data["chat_id"])
        content = {"command": "messages", "messages": self.messages_to_json(messages)}
        self.send_message(content)

    def new_message(self, data):

        message = data["message"]

        if self.scope["user"].is_superuser:
            chat_id = data["chat_id"]
            chat = Chat.objects.get(id=chat_id)
            member = chat.member
            message = chat.send_message(member, message, admin=True)
        else:
            member_id = self.scope["cookies"]["sessionid"]
            print("-------", member_id)
            try:
                member = Member.objects.get(member=member_id)
                chat = Chat.objects.get(member=member)
            except:
                member = Member(member=member_id)
                member.save()
                chat = Chat(member=member)
                chat.save()
            message = chat.send_message(member, message)
        content = {"command": "new_message", "message": self.message_to_json(message)}

        token = "875809845:AAHxB49VM_TowQhXtaBz80fx07XrIvgcHIc"
        tl_chat_id = 406434091
        forma = urllib.parse.quote(
            "http://{}/chat_view/{}/".format(os.environ["adress"], str(chat.id))
        )
        urllib.request.urlopen(
            "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}".format(
                token, tl_chat_id, forma
            )
        )

        return self.send_chat_message(content)

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        # result.reverse()
        return result

    def message_to_json(self, message):
        return {
            "member": str(message.member),
            "message": str(message.message),
            "pub_date": str(message.pub_date.strftime(" %B %d,%Y, %A %I:%M%p ")),
            "admin": message.admin,
        }

    commands = {"fetch_messages": fetch_messages, "new_message": new_message}

    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data["command"]](self, data)

    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    def chat_message(self, event):
        message = event["message"]
        self.send(text_data=json.dumps(message))
