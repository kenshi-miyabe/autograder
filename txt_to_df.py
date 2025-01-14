
import os
import re
import pandas as pd
import mylib

def construct_df(dir_name, end_str, columns, problem_length):
    df = pd.DataFrame(columns=columns)
    for file_name in sorted(os.listdir(dir_name)):
        if file_name.endswith(end_str):
            txt_path = os.path.join(dir_name, file_name)
            print(f"{txt_path}を処理中")
            content = mylib.read_text_file(txt_path)
            # 数字、()、_, ? 以外を削除
            cleaned_text = re.sub(r"[^\d\(\)_\?\n]", "", content)
            answer_list = ["_"] * problem_length  # 初期値を "_" に設定
            
            for i in range(1, problem_length + 1):
                # 正規表現を修正し、解答が _ または ? の場合にも対応
                match = re.search(rf"\({i}\)\s*([\d\_?])?", cleaned_text)
                if match and match.group(1):  # 解答が存在する場合のみ値を設定
                    answer_list[i - 1] = match.group(1)
            
            # ファイル名から最初の10文字を抽出して挿入
            answer_list.insert(0, os.path.basename(txt_path)[:10])
            # データフレームに行を追加
            df.loc[len(df)] = answer_list
    return df

if __name__ == "__main__":
    problem_length = 50
    columns = ["学生番号"] + [f"Q{i}" for i in range(1, problem_length+1)]
    df = construct_df('./student_answers', "_page1-Qwen2.txt", columns, problem_length)
    print(df.head())