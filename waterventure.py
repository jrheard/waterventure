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
            description += "\nThere's a huge jar of cat treats on the counter. It's open."
    else:
        description += "\nThere's a huge jar of cat treats on the counter. It's tightly closed so that Frank can't get into it."

    return description

def describe_hallway():
    description = "A hallway."

    if state['frank_fed']:
        description += "\nA giant picture of your family used to hang on the wall, but it's been knocked down somehow.\nThere's a weird door behind where the picture used to be."
    else:
        description += "\nA giant picture of your family hangs on the wall. It's incredibly big, stretching from the floor to the ceiling."

    return description

def describe_your_room():
    if state['lights_on']:
        description = "Your room. Your bed is unmade."
        if not state['key_taken']:
            description += "\nYour favorite book is on the nightstand. There's a weird key next to it."

    else:
        description = "It's too dark to see anything. You should probably turn on the lights."

    return description

world = {
    'rooms': [
        Room(0, -130, 50, 50, 50, 4, lambda: "A living room. There is a comfy couch here, but you don't want to sit in it right now."),
        Room(1, -130, 0, 50, 50, 1, lambda: "A dining room. Not much going on in here."),
        Room(2, -170, 50, 40, 50, 2, lambda: "A bathroom. It's not very interesting."),
        Room(3, -180, 0, 50, 50, 3, describe_kitchen),
        Room(4, -230, 0, 50, 50, 0, lambda: "A garage. It's empty - you're all alone for the weekend."),
        Room(5, -80, 50, 150, 50, 5, describe_hallway),
        Room(6, -50, 100, 100, 50, 6, describe_your_room),
        Room(7, 70, 50, 100, 100, 7, lambda: "Your parents' room. You're not supposed to be in here."),
        Room(8, -30, 0, 50, 50, 4, lambda: "You walk through the weird door and into a strange closet."),
    ],
    # A map of {room_id -> {direction_string: room_id}},
    # indicating which rooms are connected to which.
    'connections': {
        0: {'west': 2, 'south': 1, 'east': 5},
        1: {'north': 0, 'west': 3},
        2: {'east': 0, 'south': 3},
        3: {'north': 2, 'east': 1, 'west': 4},
        4: {'east': 3},
        5: {'west': 0, 'north': 6, 'east': 7},
        6: {'south': 5},
        7: {'west': 5},
    }
}

state = {
    'current_room': world['rooms'][0],
    'drawn_rooms': set(),
    'jar_opened': False,
    'frank_fed': False,
    'key_taken': False,
    'lights_on': False,
}

def travel_in_direction(direction):
    connections = world['connections'][state['current_room'].id]

    if direction in connections:
        state['current_room'] = world['rooms'][connections[direction]]
        render_room(state['current_room'])
    else:
        print("There isn't an exit in that direction.")


def process_command(command):
    command = command.lower()
    words = command.split(" ")
    in_kitchen = state['current_room'].id == 3
    in_hallway = state['current_room'].id == 5
    in_your_room = state['current_room'].id == 6

    if words[0] == "go":
        travel_in_direction(words[1])

    elif command == "help":
        print("""Here are some example commands to try:
look
go east
pet frank
take key
open jar

There are other commands, too, but you've got to figure them out on your own!""")

    elif command == "look":
        render_room(state['current_room'])

    elif command == "pet frank":
        print("You pet Frank. He purrs contentedly.")

    elif in_kitchen and command in ("open jar", "take lid off jar", "open the jar", "take the lid off the jar"):
        if state['jar_opened']:
            print("The jar's already open.")
        else:
            state['jar_opened'] = True
            print("You take the lid off the jar. Frank is frantic with excitement.")

    elif in_kitchen and command in ("feed frank", "give frank a treat", "give treat to frank", "give a treat to frank", "feed frank a treat"):
        if state['frank_fed']:
            print("Frank's full and doesn't want any more treats.")
        else:
            state['frank_fed'] = True
            print("""Frank gobbles down the treat.
He's suddenly filled with energy. He bolts out of the room and runs a lap around the house.

You hear a loud crash off in the distance.

Frank returns and sits by your feet. He purrs happily.""")

    elif in_your_room and command in ("flip switch", "turn lights on", "turn on lights", "turn light on", "turn on light", "turn on the lights", "turn on lights", "turn on the light"):
        if state['lights_on']:
            print("The lights are already on.")
        else:
            state['lights_on'] = True
            print("You flip the light switch. The lights turn on - you can see well enough to look around now.")

    elif in_your_room and command in ("take key", "take the key", "pick up the key", "get the key", "get key", "pick up key", "take weird key") and not state['key_taken']:
        state['key_taken'] = True
        print("You take the weird key.")

    elif in_hallway and command in ("open door", "open the door") and not state['key_taken']:
        print("It's locked.")

    elif in_hallway and command in ("open door", "open the door", "unlock door", "unlock the door") and state['key_taken']:
        print("You use the weird key to unlock the weird door. The door swings open.\n")

        # Add connection from hallway to end room.
        world['connections'][5]['south'] = 8

        render_room(state['current_room'])

    else:
        print("I don't know how to do that. Try something like 'go east' or 'help'.")

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

    render_room(state['current_room'])

    while True:
        if state['current_room'] == world['rooms'][-1]:
            print("""You've found your SAD lamp! You can't remember why you put it here in the first place, but that doesn't matter now.
Exhausted, you turn the lamp on and flop down next to it.
Frank meows happily and curls up next to you, basking in the lamp's glorious blue glow.
""")
            input("Congratulations, you've beaten the game! Press Enter to quit.")
            break

        print('')
        process_command(input(">>> "))


if __name__ == '__main__':
    play()
