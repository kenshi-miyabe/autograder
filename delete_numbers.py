
import os

dir_students = "./student_answers"
delete_length = 9
start_str = "理工"

def rename_files_in_directory(directory, delete_length, start_str):
    # ディレクトリ内の全ファイルを取得
    for filename in os.listdir(directory):
        # "理工"で始まり、長さが9文字以上の場合
        if filename.startswith(start_str) and len(filename) > delete_length:
            new_filename = filename[delete_length:]  # 最初の9文字を削除
            old_path = os.path.join(directory, filename)
            new_path = os.path.join(directory, new_filename)
            
            # ファイル名を変更
            os.rename(old_path, new_path)
            print(f"Renamed: {filename} -> {new_filename}")

rename_files_in_directory(dir_students, delete_length, start_str)
