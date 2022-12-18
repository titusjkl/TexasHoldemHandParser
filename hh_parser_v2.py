import glob
from tqdm import tqdm
from itertools import groupby


def load_hh_txt(input_name, encode):
    all_hands_array = []

    with open(f"{input_name}", "r", encoding=encode) as file: # "ISO-8859-1" , "latin-1"
        line = file.read().splitlines()
        all_hands_array += line
    
    return all_hands_array

def hands_to_hand(all_hands_array):
    list_hands = [list(hand) for k, hand in groupby(all_hands_array, key=bool) if k]
    
    return list_hands

def max_filter(list_hands):
    list_hands_2 = list_hands[:]

    for hand in list_hands:
        if "6-max" not in hand[1]:
            list_hands_2.remove(hand)
    removed_hands = len(list_hands) - len(list_hands_2)

    return list_hands_2, removed_hands

def get_btn_seat(hand_array, seats_names_dict):
    try:
        btn_seat_indx = hand_array[1].find("#") + 1
    except:
        print("Get BTN Seat Error")
        print(hand_array[0])
        print(hand_array[1])
        print(hand_array)
        exit(1)

    try:
        btn_seat_no = int(hand_array[1][btn_seat_indx])
    except:
        print("Get BTN Seat Error")
        print(hand_array[0])
        print(hand_array[1])
        print(hand_array)
        exit(1)

    try:
        btn_seat = list(seats_names_dict.keys()).index(btn_seat_no)
    except:
        print("Get BTN Seat Error")
        print(hand_array[0])
        print(hand_array[1])
        print(hand_array)
        exit(1)

    return btn_seat

def get_seats_names(hand_array):
    names_array = []
    seats_array = []

    for indx, line in enumerate(hand_array):
        if "Seat" in line[:5] and "chips" in line:
            name_start = hand_array[indx].find(":") + 2
            name_end = hand_array[indx].find("(") - 1
            player_name = hand_array[indx][name_start : name_end]

            seat_idx = 5 # hand_array[indx].find("Seat ") + 1
            seat_no = int(hand_array[indx][seat_idx])

            names_array.append(player_name)
            seats_array.append(seat_no)

    return seats_array, names_array

def create_seats_names_dict(seats_array, names_array):
    seats_names_dict = dict(zip(seats_array, names_array))

    return seats_names_dict

def order_pos(btn_seat, seats_names_dict):
    no_seats = len(seats_names_dict)

    if no_seats == 3:
        pos_names = ["Button", "BigBlind", "SmallBlind"]
        pos_order = [btn_seat, btn_seat-1, btn_seat-2]
    elif no_seats == 4:
        pos_names = ["Button", "CutOff", "BigBlind", "SmallBlind"]
        pos_order = [btn_seat, btn_seat-1, btn_seat-2, btn_seat-3]
    elif no_seats == 5:
        pos_names = ["Button", "CutOff", "Hijack", "BigBlind", "SmallBlind"]
        pos_order = [btn_seat, btn_seat-1, btn_seat-2, btn_seat-3, btn_seat-4]
    else:
        pos_names = ["Button", "CutOff", "Hijack", "Lojack", "BigBlind", "SmallBlind"]
        pos_order = [btn_seat, btn_seat-1, btn_seat-2, btn_seat-3, btn_seat-4, btn_seat-5]

    pos_ordered = [pos_names[i] for i in pos_order]
    
    return pos_ordered

def create_names_pos_dict(names_array, pos_ordered):
    names_pos_dict = dict(zip(names_array, pos_ordered))

    return names_pos_dict

def replace_names_positions(hand_array, names_array, names_pos_dict):
    hand_array_out = []
    for line in hand_array:
        if any(player_name in line for player_name in names_array):
            player_name_in_line = [s for s in names_array if s in line]
            new_line = line.replace(player_name_in_line[0], names_pos_dict[player_name_in_line[0]])

            hand_array_out.append(new_line)
        else:
            hand_array_out.append(line)

    hand_array_out.append("\n\n")
    return hand_array_out

def write_output(array_out, file_name, encode):
    with open(f"{file_name}", "w", encoding=encode) as f:
        for line in array_out:
            f.write(f"{line}\n")


path_hh_files = r"D:\Dokumente\Poker\HHSmithy\hh_positions\*txt"
# path_hh_files = r"D:\Dokumente\Poker\HHSmithy\temp\*txt"
encoder = "utf-8"
removed_hands_sum = 0
for hh_txt_file in tqdm(glob.iglob(path_hh_files), total=len(glob.glob(path_hh_files))):
    lines_array = load_hh_txt(hh_txt_file, encode=encoder)
    list_hands = hands_to_hand(lines_array)

    list_hands, removed_hands = max_filter(list_hands)
    removed_hands_sum += removed_hands

    lines_array_out = []
    for hand in list_hands:       
        seats, names = get_seats_names(hand)

        s_n_dict = create_seats_names_dict(seats, names)
        btn_no = get_btn_seat(hand, s_n_dict)

        ordered_pos = order_pos(btn_no, s_n_dict)
        names_pos_dict = create_names_pos_dict(names, ordered_pos)

        hand_out = replace_names_positions(hand, names, names_pos_dict)
        lines_array_out.extend(hand_out)

    write_output(lines_array_out, hh_txt_file, encode=encoder)
print(f"{removed_hands_sum} Non 6-max Hands Filtered")