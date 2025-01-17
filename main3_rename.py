
# jpg, txtファイルの整理
# "_page"が含まれる場合，ファイルを削除
# "grade.csv"から各学生のファイルを作成

import os
import pandas as pd

output_file = "./correct_answer/grade.csv"  # 保存するファイル名

# "_page"が含まれる場合，ファイルを削除
dir = './student_answers'
target_substr = "_page"

for filename in os.listdir(dir):
    filepath = os.path.join(dir, filename)
    if os.path.isfile(filepath):
        if target_substr in filename:
            # ファイル削除
            os.remove(filepath)
            print(f"Removed: {filename}")

# "grade.csv"から各学生のファイルを作成
df = pd.read_csv(output_file, header=0, dtype=str)
for index, row in df.iterrows():
    feedback_filename = row["フィードバックファイル名"]  # フィードバックファイル名列の値を取得

    # NaNチェック
    if pd.isna(feedback_filename):
        #print(f"行 {index} のフィードバックファイル名が無効です．スキップします．")
        continue

    # 拡張子を .pdf から .txt に変更
    if feedback_filename.endswith(".pdf"):
        feedback_filename = feedback_filename[:-4] + ".txt"
    
    # 書き出す内容を構築
    file_content = ""
    for i in range(1, 51):  # Q01からQ50まで
        column_name = f"Q{i:02}"  # Q01, Q02, ..., Q50
        if column_name in df.columns:  # 列が存在する場合
            file_content += f"({i}) {row[column_name]}\n"

    # ファイルに書き出し
    output_path = os.path.join(dir, feedback_filename)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(file_content)

print(f"すべてのフィードバックが '{dir}' ディレクトリに書き出されました．")
    
