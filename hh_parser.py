import timeit

start = timeit.default_timer()

def get_names(hand_array):
    player_names = []
    for indx, line in enumerate(hand_array):
        if "Seat" in line[:5] and "chips" in line:
            name_start = hand_array[indx].find(":") + 2
            name_end = hand_array[indx].find("(") - 1
            player_name = hand_array[indx][name_start : name_end]
            player_names.append(player_name)

    return player_names 

def get_btn_seat(hand_array):
    btn_seat_indx = hand_array[1].find("#") + 1
    btn_seat = int(hand_array[1][btn_seat_indx])    
    
    return btn_seat

def create_ordered_positions(btn_seat):
    # position_names = ["BTN", "CO", "HJ", "UTG", "BB", "SB"]
    position_names = ["BB", "SB", "BTN", "CO", "HJ", "UTG"]
    positions_order = [btn_seat-1, btn_seat-2, btn_seat-3, btn_seat-4, btn_seat-5, btn_seat-6]
    ordered_positions = [position_names[i] for i in positions_order]

    return ordered_positions

def create_names_pos_dict(player_names, ordered_pos):
    names_pos_dict = dict(zip(player_names, ordered_pos))

    return names_pos_dict

def replace_names_with_positions(hand_array, player_names, names_pos_dict):
    hand_array_out = []
    for line in hand_array:
        if any(player_name in line for player_name in player_names):
            player_name_in_line = [s for s in player_names if s in line]
            new_line = line.replace(player_name_in_line[0], names_pos_dict[player_name_in_line[0]])

            hand_array_out.append(new_line)
        else:
            hand_array_out.append(line)

    return hand_array_out

def write_output(array_out, file_name):
    with open(file_name, "w") as f:
        for line in array_out:
            f.write(f"{line}\n")


input_name = "hh_ps_multi"


lines_array = []
with open(f"{input_name}.txt", "r") as file:
    line = file.read().splitlines()
    lines_array += line

print(any("" == line for line in lines_array))

list_hands = []
hand_array = []
for indx, line in enumerate(lines_array):

    if line != "":
        hand_array.append(line)
    
    if "PokerStars Hand #" in line and lines_array[indx - 1] == "" and lines_array[indx - 2] == "":
        list_hands.append(hand_array)

    elif "PokerStars Hand #" in line and lines_array[0] == line:
        print(line)


print(len(list_hands))

list_of_hands = []
hand_array = []
for indx, line in enumerate(lines_array):
    hand_array.append(line)
   
    # print(line == "" and "PokerStars Hand #" in lines_array[indx+1])
    # print(line == lines_array[-1])

    if line == "" and "PokerStars Hand #" in lines_array[indx+1]:
        list_of_hands.append(hand_array)
        hand_array = []


if not any("" == line for line in lines_array):
    list_of_hands.append(hand_array)

print(list_of_hands)
print(len(list_of_hands))


output_array = []
for indx, hand in enumerate(list_of_hands):
    player_names = get_names(hand)
    btn_seat = get_btn_seat(hand)

    ordered_positions = create_ordered_positions(btn_seat)
    names_pos_dict = create_names_pos_dict(player_names, ordered_positions)

    lines_array_new = replace_names_with_positions(hand, player_names, names_pos_dict)

    output_array.extend(lines_array_new)

write_output(output_array, f"{input_name}_out.txt")

end = timeit.default_timer()
print(end-start)