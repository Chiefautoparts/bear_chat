from channels import route

def message_handler(message):
	print(message['text'])

channel_routing = [
    route("websocekt.receive", message_handler)
]