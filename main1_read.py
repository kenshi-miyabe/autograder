
# pdfから文字を読み取りtxtファイルに保存
# 複数モデルで結果を比較して差異を抽出する
# その後，手動でdiff_log, txt, pdfを見ながらtxtを修正する

# 学生の解答用紙ファイルのディレクトリ設定
dir_students = './student_answers'
diff_log = "./correct_answer/diff_log.txt"

import os
import pandas as pd
import re
import mylib
import pdf_to_jpg
import image_to_text
import txt_to_df


# pdfファイルをjpgに変換
#"""
for file_name in sorted(os.listdir(dir_students)):
    if file_name.endswith(".pdf"):
        pdf_path = os.path.join(dir_students, file_name)
        print(f"{pdf_path}を処理中")
        pdf_to_jpg.convert_pdf_to_jpg(pdf_path)
#"""

# 画像からテキストを抽出
problem_length = 50
# モデル名、プロンプトを設定
model_path_list = ["mlx-community/Qwen2-VL-72B-Instruct-4bit",
                "mlx-community/pixtral-12b-8bit",
                "mlx-community/Qwen2-VL-7B-Instruct-8bit"]
model_name_list = ["Qwen2-72B",
                "Pixtral",
                "Qwen2-7B"]
#mlx-community/Qwen2-VL-7B-Instruct-4bit
#mlx-community/Qwen2-VL-2B-Instruct-bf16
#mlx-community/pixtral-12b-4bit
#mlx-community/Phi-3.5-vision-instruct-bf16
#mlx-community/Phi-3-vision-128k-instruct-4bit
#mlx-community/Llama-3.2-11B-Vision-Instruct-4bit
#mlx-community/Molmo-7B-D-0924-4bit

prompt_list = []
prompt = """
The answers to questions (1) through (50) must be written as single-digit numbers, exactly as shown in the image.
Each answer must strictly adhere to the following format and be written on a separate line:
(Question number) Answer's digit
Example output (for illustration only):
(1) 0
(2) 0
(3) 0
Ensure that the question number is enclosed in parentheses.
"""
prompt_list.append(prompt)

#"""
for file_name in sorted(os.listdir(dir_students)):
    if file_name.endswith("_page1.jpg"):
        image_path = os.path.join(dir_students, file_name)

        print(f"{image_path}を処理中")
        for model_path, model_name in zip(model_path_list, model_name_list):
            output_list = image_to_text.process_images_with_prompt(model_path, [image_path], prompt_list)

            # テキストファイルに出力
            base, ext = os.path.splitext(image_path)
            txt_path = base + "-" + model_name + ".txt"
            mylib.write_text_file(txt_path, output_list)
#"""

#テキストファイルからデータフレームの作成
columns = ["学生番号"] + [f"Q{i:02}" for i in range(1, problem_length+1)]
df0 = txt_to_df.construct_df(dir_students, "_page1-" + model_name_list[0] + ".txt", columns, problem_length)
df1 = txt_to_df.construct_df(dir_students, "_page1-" + model_name_list[1] + ".txt", columns, problem_length)
df2 = txt_to_df.construct_df(dir_students, "_page1-" + model_name_list[2] + ".txt", columns, problem_length)
df_student = df0
print(df_student.head())

differences = []
for row in range(df0.shape[0]):
    for col in range(df0.shape[1]):
        if df0.iat[row, col] != df1.iat[row, col] and df1.iat[row, col] == df2.iat[row, col]:
            differences.append((row, col))

# 相違のある行と列を抽出
if differences:
    for row, col in differences:
        log = f"Diff at ID '{df0.at[row,"学生番号"]}', column '{col}': df0={df0.iat[row, col]}, df1=df2={df1.iat[row, col]}"
        print(log)
        mylib.log_error(log, file_name=diff_log)
else:
    print("No shared objection.")


