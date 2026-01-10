from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from time import sleep, time
from django.template.loader import render_to_string
import threading
from random import randint, choice


# Game constants
FPS = 1000 / 40
WIDTH = 20
HEIGHT = 20
PLAYER_TIMEOUT = 30  # seconds

# Color palette for players
PLAYER_COLORS = [
    "#FF6B6B",  # Red
    "#4ECDC4",  # Cyan
    "#45B7D1",  # Blue
    "#FFA07A",  # Light Salmon
    "#98D8C8",  # Mint
    "#F7DC6F",  # Yellow
    "#BB8FCE",  # Purple
    "#85C1E2",  # Sky Blue
    "#F8B88B",  # Peach
    "#52B788",  # Green
]

# Global game state (shared by all players)
game_state = {
    "canvas": [],
    "target": {"x": randint(0, WIDTH - 1), "y": randint(0, HEIGHT - 1)},
    "players": {},  # {room_id: {direction, body, color, last_activity}}
}

game_lock = threading.Lock()


def random_x():
    return randint(0, WIDTH - 1)


def random_y():
    return randint(0, HEIGHT - 1)


def search_random_free_space():
    canvas = game_state["canvas"]
    max_attempts = 100
    for _ in range(max_attempts):
        x = random_x()
        y = random_y()
        if canvas[x][y] == "floor":
            return {"x": x, "y": y}
    # If can't find free space, return random position anyway
    return {"x": random_x(), "y": random_y()}


def create_canvas():
    canvas = []
    for i in range(WIDTH):
        canvas.append([])
        for j in range(HEIGHT):
            canvas[i].append("floor")
    return canvas


def get_unused_color():
    """Get a color not currently used by any player"""
    used_colors = {player["color"] for player in game_state["players"].values()}
    available_colors = [c for c in PLAYER_COLORS if c not in used_colors]
    if available_colors:
        return choice(available_colors)
    # If all colors are used, return random one
    return choice(PLAYER_COLORS)


def add_player(room_id):
    """Add a new player to the game"""
    with game_lock:
        if room_id not in game_state["players"]:
            # Ensure canvas exists
            if not game_state.get("canvas"):
                game_state["canvas"] = create_canvas()

            # Find a free space for the new player
            free_pos = search_random_free_space()

            game_state["players"][room_id] = {
                "direction": "left",
                "body": [free_pos],
                "color": get_unused_color(),
                "last_activity": time(),
            }


def remove_player(room_id):
    """Remove a player from the game"""
    with game_lock:
        if room_id in game_state["players"]:
            del game_state["players"][room_id]


def set_direction(room_id, new_direction):
    """Set the direction for a specific player"""
    with game_lock:
        # Add player if not exists
        if room_id not in game_state["players"]:
            # Ensure canvas exists
            if not game_state.get("canvas"):
                game_state["canvas"] = create_canvas()

            # Find a free space for the new player
            free_pos = search_random_free_space()

            game_state["players"][room_id] = {
                "direction": "left",
                "body": [free_pos],
                "color": get_unused_color(),
                "last_activity": time(),
            }

        player = game_state["players"][room_id]
        current_direction = player["direction"]

        # Prevent reverse direction
        opposite = {
            "up": "down",
            "down": "up",
            "left": "right",
            "right": "left",
        }

        if opposite.get(current_direction) != new_direction:
            player["direction"] = new_direction
        player["last_activity"] = time()


def update():
    """Update all players' positions"""
    with game_lock:
        # Clean up inactive players
        current_time = time()
        inactive_players = [
            room_id
            for room_id, player in game_state["players"].items()
            if current_time - player["last_activity"] > PLAYER_TIMEOUT
        ]
        for room_id in inactive_players:
            del game_state["players"][room_id]

        # Update each player
        for room_id, player in game_state["players"].items():
            direction = player["direction"]
            body = player["body"]

            # Calculate new head position
            head = body[0]
            if direction == "left":
                new_head = {
                    "x": head["x"],
                    "y": (head["y"] - 1) % HEIGHT,
                }
            elif direction == "right":
                new_head = {
                    "x": head["x"],
                    "y": (head["y"] + 1) % HEIGHT,
                }
            elif direction == "up":
                new_head = {
                    "x": (head["x"] - 1) % WIDTH,
                    "y": head["y"],
                }
            elif direction == "down":
                new_head = {
                    "x": (head["x"] + 1) % WIDTH,
                    "y": head["y"],
                }

            # Check if eating target
            will_eat = (
                new_head["x"] == game_state["target"]["x"]
                and new_head["y"] == game_state["target"]["y"]
            )

            # Move snake
            body.insert(0, new_head)
            if not will_eat:
                body.pop()
            else:
                # Generate new target in a free space
                game_state["target"] = search_random_free_space()

        # Check collisions (self and with other snakes)
        players_to_reset = []
        for room_id, player in game_state["players"].items():
            new_head = player["body"][0]

            # Check self-collision
            if new_head in player["body"][1:]:
                players_to_reset.append(room_id)
                continue

            # Check collision with other snakes
            for other_room_id, other_player in game_state["players"].items():
                if room_id != other_room_id:
                    # Check if head collides with any segment of other snake
                    if new_head in other_player["body"]:
                        players_to_reset.append(room_id)
                        break

        # Reset collided snakes
        for room_id in players_to_reset:
            game_state["players"][room_id]["body"] = [search_random_free_space()]

        # Create canvas with all players
        canvas = create_canvas()

        # Add all players to canvas with their color
        for room_id, player in game_state["players"].items():
            for i, segment in enumerate(player["body"]):
                if i == 0:
                    canvas[segment["x"]][segment["y"]] = {"type": "player_head", "color": player["color"]}
                else:
                    canvas[segment["x"]][segment["y"]] = {"type": "player", "color": player["color"]}

        # Add target
        target = game_state["target"]
        canvas[target["x"]][target["y"]] = {"type": "target"}

        game_state["canvas"] = canvas


def render():
    """Broadcast canvas to all connected clients"""
    my_channel_layer = get_channel_layer()
    if my_channel_layer:
        html = render_to_string("components/canvas.html", {
            "canvas": game_state["canvas"],
        })
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
    """Main game loop"""
    while True:
        sleep(0.1)
        update()
        render()


def start():
    """Initialize game and start game loop"""
    game_state["canvas"] = create_canvas()

    thread = threading.Thread(target=loop, daemon=True)
    thread.start()
