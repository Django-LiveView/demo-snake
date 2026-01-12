from liveview import liveview_handler
from app.public.loop import add_player, remove_player, set_direction


@liveview_handler("init")
def init(consumer, content):
	"""Called when a client initializes"""
	room_id = getattr(consumer, 'room_id', None) or content.get("room")
	if room_id:
		add_player(room_id)


@liveview_handler("key_up")
def key_up(consumer, content):
    """Handle up arrow key"""
    room_id = getattr(consumer, 'room_id', None) or content.get("room")
    if room_id:
        set_direction(room_id, "up")


@liveview_handler("key_right")
def key_right(consumer, content):
    """Handle right arrow key"""
    room_id = getattr(consumer, 'room_id', None) or content.get("room")
    if room_id:
        set_direction(room_id, "right")


@liveview_handler("key_down")
def key_down(consumer, content):
    """Handle down arrow key"""
    room_id = getattr(consumer, 'room_id', None) or content.get("room")
    if room_id:
        set_direction(room_id, "down")


@liveview_handler("key_left")
def key_left(consumer, content):
    """Handle left arrow key"""
    room_id = getattr(consumer, 'room_id', None) or content.get("room")
    if room_id:
        set_direction(room_id, "left")


@liveview_handler("connect")
def on_connect(consumer, content):
    """Called when a client connects"""
    room_id = getattr(consumer, 'room_id', None) or content.get("room")
    if room_id:
        add_player(room_id)


@liveview_handler("disconnect")
def on_disconnect(consumer, content):
    """Called when a client disconnects"""
    room_id = getattr(consumer, 'room_id', None) or content.get("room")
    if room_id:
        remove_player(room_id)
