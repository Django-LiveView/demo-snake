from liveview import liveview_handler
from app.public.loop import direction, create_canvas

# Initialize canvas when module loads
create_canvas()


@liveview_handler("key_up")
def key_up(consumer, content):
	"""Handle up arrow key"""
	if direction[0]["player"]["direction"] != "down":
		direction[0]["player"]["direction"] = "up"


@liveview_handler("key_right")
def key_right(consumer, content):
	"""Handle right arrow key"""
	if direction[0]["player"]["direction"] != "left":
		direction[0]["player"]["direction"] = "right"


@liveview_handler("key_down")
def key_down(consumer, content):
	"""Handle down arrow key"""
	if direction[0]["player"]["direction"] != "up":
		direction[0]["player"]["direction"] = "down"


@liveview_handler("key_left")
def key_left(consumer, content):
	"""Handle left arrow key"""
	if direction[0]["player"]["direction"] != "right":
		direction[0]["player"]["direction"] = "left"
