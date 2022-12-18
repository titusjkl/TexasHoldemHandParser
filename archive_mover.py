import shutil
import os

source_dir = r"C:\HM3Archive"
destination_dir = r"D:\Dokumente\Poker\Handhistory\HM3_Archive Imported"

file_names = os.listdir(source_dir)

for file_name in file_names:
    shutil.move(os.path.join(source_dir, file_name), destination_dir)