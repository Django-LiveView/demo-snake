from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from time import sleep
from django.template.loader import render_to_string
import threading
from random import randint


# Create matrix 20 x 20 with random numbers between 0 and 4
FPS = 1000 / 40
width = 20
height = 20
canvas = []
target = {"x": randint(0, width - 1), "y": randint(0, height - 1)}
direction = [
    {
        "player": {
            "direction": "left",
            "body": [],
        }
    }
]

def random_x():
    global width
    return randint(0, width - 1)

def random_y():
    global height
    return randint(0, height - 1)

def search_random_free_space():
    global canvas
    global width
    global height
    x = random_x()
    y = random_y()
    if canvas[x][y] == "floor":
        return {"x": x, "y": y}
    search_random_free_space()


def create_canvas():
    global canvas
    global width
    global height
    canvas = []
    for i in range(width):
        canvas.append([])
        for j in range(height):
            canvas[i].append("floor")
    return canvas


def update():
    global canvas
    global width
    global height
    # Move player
    if direction[0]["player"]["direction"] == "left":
        direction[0]["player"]["body"].insert(
            0,
            {
                "x": direction[0]["player"]["body"][0]["x"],
                "y": direction[0]["player"]["body"][0]["y"] - 1
                if direction[0]["player"]["body"][0]["y"] - 1 >= 0
                else height - 1,
            },
        )
        direction[0]["player"]["body"].pop()
    elif direction[0]["player"]["direction"] == "right":
        direction[0]["player"]["body"].insert(
            0,
            {
                "x": direction[0]["player"]["body"][0]["x"],
                "y": direction[0]["player"]["body"][0]["y"] + 1
                if direction[0]["player"]["body"][0]["y"] + 1 <= height - 1
                else 0,
            },
        )
        direction[0]["player"]["body"].pop()
    elif direction[0]["player"]["direction"] == "up":
        direction[0]["player"]["body"].insert(
            0,
            {
                "x": direction[0]["player"]["body"][0]["x"] - 1
                if direction[0]["player"]["body"][0]["x"] - 1 >= 0
                else width - 1,
                "y": direction[0]["player"]["body"][0]["y"],
            },
        )
        direction[0]["player"]["body"].pop()
    elif direction[0]["player"]["direction"] == "down":
        direction[0]["player"]["body"].insert(
            0,
            {
                "x": direction[0]["player"]["body"][0]["x"] + 1
                if direction[0]["player"]["body"][0]["x"] + 1 <= width - 1
                else 0,
                "y": direction[0]["player"]["body"][0]["y"],
            },
        )
        direction[0]["player"]["body"].pop()
    # Die. Check if player is in body
    is_dead = False
    for i in range(1, len(direction[0]["player"]["body"])):
        if (
            direction[0]["player"]["body"][0]["x"]
            == direction[0]["player"]["body"][i]["x"]
            and direction[0]["player"]["body"][0]["y"]
            == direction[0]["player"]["body"][i]["y"]
        ):
            is_dead = True
    if is_dead:
        direction[0]["player"]["body"] = [
            search_random_free_space(),
        ]
    # Eat. Check if player is in target
    if (
        direction[0]["player"]["body"][0]["x"] == target["x"]
        and direction[0]["player"]["body"][0]["y"] == target["y"]
    ):
        new_target = search_random_free_space()
        target["x"] = new_target["x"]
        target["y"] = new_target["y"]
        direction[0]["player"]["body"].append(
            new_target,
        )
    # Fill canvas
    canvas = create_canvas()
    # Add player
    for i in range(len(direction[0]["player"]["body"])):
        if i == 0:
            canvas[direction[0]["player"]["body"][i]["x"]][
                direction[0]["player"]["body"][i]["y"]
            ] = "player_head"
        else:
            canvas[direction[0]["player"]["body"][i]["x"]][
                direction[0]["player"]["body"][i]["y"]
            ] = "player"
    # Add target
    canvas[target["x"]][target["y"]] = "target"


def render():
    global canvas
    my_channel_layer = get_channel_layer()
    if my_channel_layer:
        html = render_to_string("components/canvas.html", {"canvas": canvas})
        data = {
            "target": "#canvas",
            "html": html,
        }
        try:
            async_to_sync(my_channel_layer.group_send)(
                "broadcast", {"type": "broadcast_message", "message": data}
            )
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error sending broadcast: {e}")


def loop():
    while True:
        sleep(0.1)
        update()
        render()


def start():
    global direction

    create_canvas()
    direction[0]["player"]["body"] = [
        search_random_free_space(),
    ]

    thread = threading.Thread(target=loop, daemon=True)
    thread.start()
