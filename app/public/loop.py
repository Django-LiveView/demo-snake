from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from time import sleep
from django.template.loader import render_to_string
import threading
from random import randint


# Create matrix 20 x 20 with random numbers between 0 and 4
canvas = []

def create_canvas():
    for i in range(20):
        canvas.append([])
        for j in range(20):
            canvas[i].append(randint(0, 4))
    return canvas


def refresh_resources():
    create_canvas()
    my_channel_layer = get_channel_layer()

    if my_channel_layer:
        html = render_to_string(
            "components/canvas.html", {"canvas": canvas}
        )
        # Render
        data = {"action": "Update canvas", "selector": "#canvas", "html": html}
        async_to_sync(my_channel_layer.group_send)(
            "broadcast", {"type": "send_data_to_frontend", "data": data}
        )

def loop():
    while True:
        sleep(2)
        refresh_resources()

def start():
    threading.Thread(target=loop).start()
