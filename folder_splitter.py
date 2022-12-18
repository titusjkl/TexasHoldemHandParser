import os
import shutil
from tqdm import tqdm

def move_files(abs_dirname, n):
    """Move files into subdirectories."""

    files = [os.path.join(abs_dirname, f) for f in os.listdir(abs_dirname)]

    i = 0
    curr_subdir = None
    files.sort()

    for f in tqdm(files, total=len(files)):
        # create new subdir if necessary
        if i % n == 0:
            subdir_name = os.path.join(abs_dirname, '{0:03d}'.format(i // n + 1))
            os.mkdir(subdir_name)
            curr_subdir = subdir_name

        # move file to current dir
        f_base = os.path.basename(f)
        shutil.move(f, os.path.join(subdir_name, f_base))
        i += 1


path = r"D:\Dokumente\Poker\HHSmithy\hh_positions"
n = 500

move_files(path, n)
