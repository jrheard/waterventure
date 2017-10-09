from collections import namedtuple

from madison_wcb import wcb


### Watercolor helper functions

def draw_box(color_index, x, y, width, height):
    wcb.get_color(color_index)
    wcb.move_to(x, y)
    wcb.brush_down()

    wcb.point_in_direction(0)
    wcb.move_forward(width)
    wcb.turn_right(90)
    wcb.move_forward(height)
    wcb.turn_right(90)
    wcb.move_forward(width)
    wcb.turn_right(90)
    wcb.move_forward(height)
    wcb.brush_up()

### Game code

Room = namedtuple("Room", ["id", "x", "y", "width", "height", "color_index", "description_fn"])

def describe_kitchen():
    description = "A kitchen. It's very tidy."

    if state['jar_opened']:
        if state['frank_fed']:
            description += "\nThere's a huge jar of cat treats on the counter."
        else:
            description += "\nThere's a huge jar of cat treats on the counter. It's open. Frank is frantic with excitement."
    else:
        description += "\nThere's a huge jar of cat treats on the counter. It's tightly closed so that Frank can't get into it."

    return description

world = {
    'rooms': [
        # TODO deal with coordinates, sizes
        Room(0, -100, 0, 100, 100, 0, lambda: "A living room. There is a comfy couch here, but you don't want to sit in it right now."),
        Room(1, -100, 0, 100, 100, 0, lambda: "A dining room. Not much going on in here."),
        Room(2, -100, 0, 100, 100, 0, lambda: "A bathroom. It's not very interesting."),
        Room(3, -100, 0, 100, 100, 0, describe_kitchen),
        Room(4, -100, 0, 100, 100, 0, lambda: "A garage. It's empty - you're all alone for the weekend."),
    ],
    # A map of {room_id -> {direction_string: room_id}},
    # indicating which rooms are connected to which.
    'connections': {
        0: {'west': 2, 'south': 1}, # TODO hallway
        1: {'north': 0, 'west': 3},
        2: {'east': 0, 'south': 3},
        3: {'north': 2, 'east': 1, 'west': 4},
    }
}

state = {
    'current_room': world['rooms'][0],
    'drawn_rooms': set(),
    'jar_opened': False,
    'frank_fed': False,
}

def travel_in_direction(direction):
    # TODO error handling
    next_room_id = world['connections'][state['current_room'].id][direction]
    state['current_room'] = world['rooms'][next_room_id]

def process_command(command):
    words = command.split(" ")

    # TODO help command

#[when you feed frank]Frank gobbles down the treat.
#He's suddenly filled with energy. He bolts out of the room and runs a lap around the house.
#You hear a loud crash off in the distance.
#Frank returns and sits by your feet. He purrs happily.
#[if you try to feed him again]Frank's full and doesn't want any more treats.

    if words[0] == "go":
        travel_in_direction(words[1])
    else:
        print("I don't know how to do that. Try something like 'go east'.")

def render_room(room):
    if room.id not in state['drawn_rooms']:
        state['drawn_rooms'].add(room.id)
        draw_box(room.color_index, room.x, room.y, room.width, room.height)

    wcb.move_to(room.x + room.width / 2, room.y - room.height / 2)

    print(room.description_fn() + "\n")
    if room.id in world['connections']:
        exits = world['connections'][room.id]
        print("There are exits in these directions: {0}".format(', '.join(exits.keys())))


def play():
    wcb.initialize()

    print("""You're sitting on the couch in your living room, absentmindedly petting your cat Frank,
when a local news report on the TV catches your attention:

"...that's right, Bob, this year's winter is going to be just truly, unbelievably dark.
It's barely October, and Portland residents are already preparing for the worst;
marshmallows and blankets are flying off store shelves, and there isn't a single
SAD lamp left for sale in the entire city."

Oh no, it's almost winter! Your mom gave you a SAD lamp last year when you were feeling
super depressed, and it sounds like you're really going to need it this year.
Now where did you put it?

Suddenly nothing in the world is more important to you than finding your special lamp.
You jump off the couch and begin your search. Frank follows you, meowing hungrily.

[This game is a text adventure. Type commands after the >>> and press "enter". Type "help"
to see a list of some example commands.]
""")

    while True:
        render_room(state['current_room'])

        if state['current_room'] == world['rooms'][-1]:
            input("Congratulations, you won the game! Press Enter to quit.")
            break

        process_command(input(">>> "))


if __name__ == '__main__':
    play()
