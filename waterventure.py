from collections import namedtuple

from madison_wcb import wcb


Room = namedtuple("Room", ["x", "y", "width", "height", "color_index", "exits", "description"])

end_room = Room(100, 100, 100, 100, 2, {}, "There is a wizard here. He knights you.")
start_room = Room(-200, -200, 100, 100, 0, {'east': end_room}, "It is dark, you might be eaten by a grue.")

state = {
    'current_room': start_room,
    'drawn_rooms': set(),
}

def travel_in_direction(direction):
    # TODO error handling
    state['current_room'] = state['current_room'].exits[direction]

def process_command(command):
    words = command.split(" ")

    # TODO help command

    if words[0] == "go":
        travel_in_direction(words[1])
    else:
        print("I don't know how to do that. Try something like 'go east'.")

def render_room(room):
    if room not in state['drawn_rooms']:
        state['drawn_rooms'].add(room)



    print(room.description)
    if room.exits:
        print("There are exits in these directions: {0}".format(', '.join(room.exits.keys())))


def play():
    wcb.initialize()

    while True:
        render_room(state['current_room'])

        if state['current_room'] == end_room:
            input("Congratulations, you won the game! Press Enter to quit.")
            break

        process_command(input(">>> "))


if __name__ == '__main__':
    play()
