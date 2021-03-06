from functools import wraps
from .exceptions import ClientError
from .models import Room

def catch_client_error(func):
	@wraps(func)
	def inner(message, args, **kwargs):
		try:
			return func(message, args, **kwargs)
		except CLientError as e:
			e.send_to(message.reply_channel)
	return inner

	def get_room_or_error(room_id, user):
		if not user.is_authenticated():
			raise ClientError("USER_HAS_TO_LOGIN")
		try:
			room = Room.objects.get(pk=room_id)
		except Room.DoesNotExist:
			raise ClientError("ROOM_INVALID")

		if room.staff_only and not user.is_staff:
			raise ClientError("ROOM_ACCESS_DENIED")
		return room