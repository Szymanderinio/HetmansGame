# coding=utf-8
# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import random
import string

colors = {"black": "\033[0;37;40m", "white": "\033[0;37;47m",
          "yellow_txt": "\033[0;33;40m", "white_txt": "\033[1;37;40m", "red_txt_black_bgr": "\033[1;31;40m",
          "red_txt_white_bgr": "\033[1;31;47m", "blue_txt_black_bgr": "\033[1;36;40m",
          "blue_txt_white_bgr": "\033[1;36;47m"}


class Cords:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Pawns:
    def __init__(self, cords):
        self.cords = cords


class Hetman(Pawns):
    body_black = colors["red_txt_black_bgr"] + " H " + colors['black']
    body_white = colors["red_txt_white_bgr"] + " H " + colors['black']


class Pawn(Pawns):
    body_black = colors["blue_txt_black_bgr"] + " P " + colors['black']
    body_white = colors["blue_txt_white_bgr"] + " P " + colors['black']


def get_hetmans_count():
    while True:
        allowed_quantity = [1, 2, 3, 4, 5]
        quantity = int(input("How many Hetmans do you want to place on the board?\n"))
        if quantity in allowed_quantity:
            return quantity


def get_decision():
    while True:
        allowed_quantity = [1, 2, 3, 4]
        quantity = int(input("\nChoose an option:\n{}. Generate new coordinates for a {}\n"
                             .format(colors["yellow_txt"] + "1" + colors["white_txt"],
                                     colors["blue_txt_black_bgr"] + "Pawn" + colors["white_txt"])
                             + "{}. Delete a chosen {}"
                             .format(colors["yellow_txt"] + "2" + colors["white_txt"],
                                     colors["red_txt_black_bgr"] + "Hetman" + colors["white_txt"])
                             + "\n{}. Show actual chessboard".format(colors["yellow_txt"] + "3" + colors["white_txt"], )
                             + "\n{}. Exit a program\n".format(colors["yellow_txt"] + "4" + colors["white_txt"], )))
        if quantity in allowed_quantity:
            return quantity


def delete_chosen_hetman():
    allowed_quantity = list(range(0, len(enemy_hetmans)))
    if not allowed_quantity:
        print("No hetmans to be deleted!")
    else:
        do = True
        while do:
            quantity = int(input("Which {} would you like to delete?\n"
                                 .format((colors["red_txt_black_bgr"] + "Hetman" + colors["white_txt"]))))
            # print(enemy_hetmans[quantity].cords.y + 1, enemy_hetmans[quantity].cords.x + 1)
            if quantity in allowed_quantity:
                for pawns in pawn_cords:
                    if pawns.cords == enemy_hetmans[quantity].cords:
                        pawn_cords.remove(pawns)
                        do = False


def get_hetmans_cords_with_one_pawn(hetmans_quantity_inner):
    temp = [Pawn(generate_cords())]
    for i in range(hetmans_quantity_inner):
        temp_cords_inner = generate_cords()
        while check_if_cords_taken(temp_cords_inner, temp):
            temp_cords_inner = generate_cords()
        temp.append(Hetman(temp_cords_inner))

    return temp


def check_if_cords_taken(coordinates, list_of_pawns):
    taken = False
    for pawn in list_of_pawns:
        if pawn.cords.x == coordinates.x and pawn.cords.y == coordinates.y:
            taken = True
            break
    return taken


def generate_cords():
    return Cords(random.randrange(1, 8), random.randrange(1, 8))


def show_board(pawns_cords):
    squares = [colors['black'] + "   " + colors['black'], colors['white'] + "   " + colors['black']]
    added = False
    for x in range(8):
        c_indx = x % 2
        print("")
        # vertical column (1)(2)(3)....
        print("(" + colors['yellow_txt'] + "{}".format(x + 1), end="" + colors['white_txt'] + ")")
        for y in range(8):
            for z in pawns_cords:
                if x == z.cords.x and y == z.cords.y:
                    if c_indx == 1:
                        print(z.body_white, end="")
                    else:
                        print(z.body_black, end="")
                    added = True
            if added is False:
                print(squares[c_indx], end="")
            added = False
            c_indx = (c_indx + 1) % 2
    print("\n   ", end="")

    # bottom row (A)(B)(C)...
    for i in range(8):
        print("(" + colors['yellow_txt'] + "{}".format(string.ascii_uppercase[i]), end="" + colors['white_txt'] + ")")
    print("")


def which_hetmans_can_beat_pawn(pawns_cords):
    pawn_x = pawns_cords[0].cords.x
    pawn_y = pawns_cords[0].cords.y
    # print("P x:{} y:{}".format(pawn_x+1, string.ascii_uppercase[pawn_y]))
    print(colors['yellow_txt'] +
          "\n{}Red ID{} - can beat a {}Pawn{}\n{}Yellow ID{} - can't beat a {}Pawn{}\n".format
          (colors["red_txt_black_bgr"], colors["white_txt"],colors["blue_txt_black_bgr"],
           colors["white_txt"], colors["yellow_txt"], colors["white_txt"],
           colors["blue_txt_black_bgr"], colors["white_txt"])
          + colors["white_txt"])
    # delete pawn
    if type(pawns_cords[0]) is Pawns:
        pawns_cords.pop(0)
    hetmans_that_can_beat = []
    for pion in pawns_cords:
        # print("type:{}  x:{}  y:{}".format(type(pion), pion.cords.x+1, string.ascii_uppercase[pion.cords.y]))
        if (pion.cords.x == pawn_x or pion.cords.y == pawn_y or can_beat_diagonally(Cords(pawn_x, pawn_y), pion)) \
                and (type(pion) is Hetman):
            print("ID:{} x:{}  y:{}".format(colors["red_txt_black_bgr"]
                                            + str(len(hetmans_that_can_beat))
                                            + colors["white_txt"],
                                            string.ascii_uppercase[pion.cords.y],
                                            pion.cords.x + 1))
            hetmans_that_can_beat.append(pion)
        elif type(pion) is Hetman:
            print("ID:{} x:{}  y:{}".format(colors["yellow_txt"]
                                            + str(len(hetmans_that_can_beat))
                                            + colors["white_txt"],
                                            string.ascii_uppercase[pion.cords.y],
                                            pion.cords.x + 1))
            hetmans_that_can_beat.append(pion)

    return hetmans_that_can_beat


def can_beat_diagonally(pawn_cords_inner, hetman_cords):
    pawn_x = pawn_cords_inner.x
    pawn_y = pawn_cords_inner.y
    hetman_x = hetman_cords.cords.x
    hetman_y = hetman_cords.cords.y

    for x in range(8):
        if (pawn_x - x == hetman_x and pawn_y + x == hetman_y) or \
                (pawn_x + x == hetman_x and pawn_y - x == hetman_y) or \
                (pawn_x + x == hetman_x and pawn_y + x == hetman_y) or \
                (pawn_x - x == hetman_x and pawn_y - x == hetman_y):
            return True
            # print("{} {}".format(string.ascii_uppercase[hetman_y], hetman_x+1))
    return False


if __name__ == '__main__':
    print(colors['yellow_txt'])
    hetmans_quantity = get_hetmans_count()

    pawn_cords = get_hetmans_cords_with_one_pawn(hetmans_quantity)
    print(colors['black'])
    show = True
    while True:
        if show:
            show_board(pawn_cords)
            enemy_hetmans = which_hetmans_can_beat_pawn(pawn_cords)
        show = False
        decision = get_decision()

        if decision == 1:
            temp_cords = generate_cords()
            if not check_if_cords_taken(temp_cords, pawn_cords):
                pawn_cords[0].cords = temp_cords

        if decision == 2:
            delete_chosen_hetman()

        if decision == 3:
            show = True

        if decision == 4:
            break
