from collections import namedtuple

import madison_wcb


Room = namedtuple("Room", ["x", "y", "width", "height", "exits", "description"])


world = [
    Room(-200, -200, 100, 100, {}, "It is dark, you might be eaten by a grue.")
]

state = {
    'current_room': world[0],
    'drawn_rooms': set(),
}


def play():
    while True:
        # outputs the room description and info about exits
        # draws the room on the bot if it hasn't been drawn yet
        render_room(state['current_room'])

if __name__ == '__main__':
    play()
