
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
import image_to_text_ollama
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
# モデル名、プロンプトを設定
#"""
arg_list = [
    {'model_path': "mlx-community/QVQ-72B-Preview-4bit", 'model_name': "QVQ", 'type': "mlx", 'max_tokens': 15000, 'temp': 0}, #0.99
    {'model_path': "mlx-community/Qwen2-VL-72B-Instruct-4bit", 'model_name': "Qwen-72B-0", 'type': "mlx", 'max_tokens': 10000, 'temp': 0.4}, #0.95
    {'model_path': "mlx-community/Qwen2-VL-72B-Instruct-4bit", 'model_name': "Qwen-72B-1", 'type': "mlx", 'max_tokens': 10000, 'temp': 0.4}, #0.99
    {'model_path': "mlx-community/Qwen2-VL-72B-Instruct-4bit", 'model_name': "Qwen-72B-2", 'type': "mlx", 'max_tokens': 10000, 'temp': 0.4}, #0.99
    {'model_path': "mlx-community/pixtral-12b-8bit", 'model_name': "Pixtral-0", 'type': "mlx", 'max_tokens': 5000, 'temp': 0.4}, #0.96
    {'model_path': "mlx-community/pixtral-12b-8bit", 'model_name': "Pixtral-1", 'type': "mlx", 'max_tokens': 5000, 'temp': 0.4}, #0.93
    {'model_path': "mlx-community/pixtral-12b-8bit", 'model_name': "Pixtral-2", 'type': "mlx", 'max_tokens': 5000, 'temp': 0.4}, #0.93
#    {'model_path': "mlx-community/Qwen2-VL-7B-Instruct-8bit", 'model_name': "Qwen-7B", 'type': "mlx", 'max_tokens': 5000}, #0.80
#    {'model_path': "llama3.2-vision:90b", 'model_name': "llama-90B", 'type': "ollama", 'max_tokens': 5000}, #0.70
#    {'model_path': "llama3.2-vision", 'model_name': "llama-11B", 'type': "ollama", 'max_tokens': 5000}, #0.81
#    {'model_path': "mlx-community/Llama-3.2-11B-Vision-Instruct-8bit", 'model_name': "llama-11B-mlx", 'type': "mlx", 'max_tokens': 5000}, #0.76
#    {'model_path': "llava:34b", 'model_name': "llava", 'type': "ollama", 'max_tokens': 5000}, #0.058
#    {'model_path': "minicpm-v", 'model_name': "minicpm", 'type': "ollama", 'max_tokens': 5000} #0.45
]
#"""
"""
arg_list = [
    {'model_path': "mlx-community/pixtral-12b-4bit", 'model_name': "Pixtral-0", 'type': "mlx", 'max_tokens': 5000, 'temp': 0.4}, #0.94
    {'model_path': "mlx-community/pixtral-12b-4bit", 'model_name': "Pixtral-1", 'type': "mlx", 'max_tokens': 5000, 'temp': 0.4}, #0.94
    {'model_path': "mlx-community/pixtral-12b-4bit", 'model_name': "Pixtral-2", 'type': "mlx", 'max_tokens': 5000, 'temp': 0.4}, #0.94
#    {'model_path': "mlx-community/Qwen2-VL-7B-Instruct-8bit", 'model_name': "Qwen-0", 'type': "mlx", 'max_tokens': 5000, 'temp': 0.4}, #0.76
#    {'model_path': "llama3.2-vision", 'model_name': "llama-0", 'type': "ollama", 'max_tokens': 5000, 'temp': 0}, #0.80
#    {'model_path': "llava:13b", 'model_name': "llava", 'type': "ollama", 'max_tokens': 5000}, #0.12
#    {'model_path': "minicpm-v", 'model_name': "minicpm", 'type': "ollama", 'max_tokens': 5000}
]
#"""

prompt = """
Please extract all 50 answers from the main section as they are.

The background is white, and the text is handwritten in black ink.
The main section of the document consists of a grid with 50 questions, numbered from (1) to (50).
Each question has a single-digit handwritten answer or a cross mark `X'.
Your task is to output all 50 answers accurately in plain text directly within this response, without referencing or creating any files.

First, output the points to be noted.
Then, output the string `**Final Answer**' followed by the answers to the questions.
Format each answer on a separate line in the following style without using TeX formatting:
=====
(Question number) Answer's digit
=====
Make sure the question number is enclosed in parentheses.
If the answer is a cross mark or blank, replace `Answer's digit' with `X'.

Example final output:
=====
**Final Answer**
(1) 0
(2) 1
(3) 2
(4) X
=====

Ensure the final output is in plain text format, without TeX formatting or file references.
"""

prompt0 = """
Please extract all 50 answers from the main section as they are.

The background is white, and the text is handwritten in black ink.
The main section of the document consists of a grid with 50 questions, numbered from (1) to (50).
Each question has a single-digit handwritten answer or a cross mark "X".

Example final output:
=====
(1) ? (2) ? (3) ? (4) ? (5) ?
(6) ? (7) ? (8) ? (9) ? (10) ?
...
=====
Make sure each question number is enclosed in parentheses, and each answer is a digit or "X".
Do not use "O".
"""

"""
for file_name in sorted(os.listdir(dir_students)):

    if file_name.endswith("_page1.jpg"):
        image_path = os.path.join(dir_students, file_name)
        print(f"{image_path}を処理中")

        for model_info in arg_list:
            model_path = model_info['model_path']
            model_name = model_info['model_name']
            model_type = model_info['type']
            max_tokens = model_info['max_tokens']
            temp = model_info['temp']
            if model_type == "mlx":
                print(f"{model_path}で{image_path}を処理中")
                output = image_to_text.process_images_with_prompt(model_path, [image_path], prompt, max_tokens, temp)
            elif model_type == "ollama":
                print(f"{model_path}で{image_path}を処理中")
                output = image_to_text_ollama.process_images_with_prompt(model_path, [image_path], prompt, max_tokens, temp)
            else :
                print("Error: unknown model type.")
                break

            # テキストファイルに出力
            base, ext = os.path.splitext(image_path)
            txt_path = base + "-" + model_name + ".txt"
            mylib.write_text_file(txt_path, output)
#"""

#テキストファイルを集計し，多数決をとって，もう一度テキストファイルとして出力する
#"""
problem_length = 50
columns = ["学生番号"] + [f"Q{i:02}" for i in range(1, problem_length+1)]
df_list = []
for model_info in arg_list:
    model_name = model_info['model_name']
    df_list.append(txt_to_df.construct_df(dir_students, "_page1-" + model_name + ".txt", columns, problem_length))
df_consensus = txt_to_df.consensus_df(df_list, threshold=4/7)
print(df_consensus.head())
#for df in df_list:
#    print(txt_to_df.calculate_match_rate(df_consensus, df))
#"""


