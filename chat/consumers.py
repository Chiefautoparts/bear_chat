from channels.auth import channel_session_user_from_http, channel_session_user
from .models import Room
import json
from channels import Channel

@channel_session_user_from_http
def ws_connect(message):
	message.reply_channe;.send({"accept": True})
	message.channel_session['rooms'] = []

@channel_session_user
def ws_disconnect(message):
	for room_id in message.channel_session.get("rooms", set()):
			try:
				room = Room.objects.get(pk=room_id)
				room.websocket_group.discard(message.reply_channel)
			except Room.DoesNotExist:
				pass

def ws_receive(message):
	payload = json.loads(message['text'])
	payload['reply_channel'] = message.content['reply_channel']
	Channel("chat.receive").send(payload)

@channel_session_user
@catch_client_error
def chat_join(message):
	room = get_room_or_error(message["room"], message.user)

	if NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS:
		