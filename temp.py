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


path_hh_files = r"D:\Dokumente\Poker\HHSmithy\hh_positions\*txt"
# path_hh_files = r"D:\Dokumente\Poker\HHSmithy\temp\*txt"

encoder = "utf-8"
removed_hands_sum = 0
for hh_txt_file in tqdm(glob.iglob(path_hh_files), total=len(glob.glob(path_hh_files))):
    lines_array = load_hh_txt(hh_txt_file, encode=encoder)
    list_hands = hands_to_hand(lines_array)

    list_hands, removed_hands = max_filter(list_hands)
    removed_hands_sum += removed_hands
print(f"{removed_hands_sum} Non 6-max Hands Filtered")