
# txtファイルの整理
# target_substrが含まれる場合，その部分を削除
# target_substrが含まれない場合，ファイルを削除

import os

target_substr = "_page1-QVQ"
dir = './student_answers'

for filename in os.listdir(dir):
    filepath = os.path.join(dir, filename)
    if os.path.isfile(filepath):
        if target_substr in filename:
            new_name = filename.replace(target_substr, "")
            new_path = os.path.join(dir, new_name)
            # リネーム
            os.rename(filepath, new_path)
            print(f"Renamed: {filename} -> {new_name}")
        else:
            # ファイル削除
            os.remove(filepath)
            print(f"Removed: {filename}")

