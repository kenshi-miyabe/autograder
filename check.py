
import mylib
import sys
import csv

answer_file = "answer.csv"
student_file = "sample.csv"

df_correct_answer = mylib.load_csv(answer_file)
if df_correct_answer is None:
    mylib.log_error("エラー: 模範解答ファイルからデータを読み込めませんでした．スクリプトを終了します。")
    sys.exit()  # スクリプトを終了

df_your_answer = mylib.load_csv(student_file)
if df_your_answer is None:
    mylib.log_error("エラー: 学生解答ファイルからデータを読み込めませんでした．スクリプトを終了します。")
    sys.exit()  # スクリプトを終了

def compare_lists(list1, list2):
    """
    2つのリストを比較して、指定の条件に基づいて出力する関数。
    
    - 1つ目のリストの項目が '*' の場合は '*' を出力。
    - '*' でない場合、2つのリストの値を比較し、同じなら 1、異なれば 0 を出力。

    Parameters:
        list1 (list): 比較元のリスト。
        list2 (list): 比較対象のリスト。

    Returns:
        list: 比較結果のリスト。
    """
    if len(list1) != len(list2):
        raise ValueError("リストの長さが一致していません。")

    result = []
    for item1, item2 in zip(list1, list2):
        if item1 == "*":
            result.append("*")
        else:
            result.append(1 if item1 == item2 else 0)
    return result

# 比較
result = compare_lists(df_correct_answer.iloc[0], df_your_answer.iloc[0])
print(result)

def append_to_csv(file_name, data_list):
    """
    リストをCSVファイルに追記する関数。
    
    Parameters:
        file_name (str): 書き込むCSVファイルの名前。
        data_list (list): CSVに追記するリスト（1行分のデータ）。
    """
    try:
        with open(file_name, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(data_list)
        print(f"データを{file_name}に追記しました。")
    except Exception as e:
        mylib.error_log(f"エラーが発生しました: {e}")

append_to_csv(student_file, result)

"""
from mlx_lm import load, generate

model, tokenizer = load("mlx-community/Mistral-7B-Instruct-v0.3-4bit")

prompt = "Write a story about Einstein"

messages = [{"role": "user", "content": prompt}]
prompt = tokenizer.apply_chat_template(
    messages, tokenize=False, add_generation_prompt=True
)

response = generate(model, tokenizer, prompt=prompt, verbose=True)
"""