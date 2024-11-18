
import mylib
import sys
import csv
import os
from mlx_lm import load, generate

def generate_with_prompt(model, prompt):
    """
    プロンプトを受け取り、モデルからの出力を返す関数。

    Args:
        model (str): 使用するモデル。
        prompt (str): モデルに与えるプロンプト。

    Returns:
        str: モデルからの出力。
    """
    model, tokenizer = load(model)

    messages = [{"role": "user", "content": prompt}]
    prompt = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    response = generate(model, tokenizer, prompt=prompt, verbose=False)
    return response

def compare_lists(list1, list2):
    """
    2つのリストを比較して、指定の条件に基づいて出力する関数。
    
    - 1つ目のリストの項目が '*' の場合は 2つ目のリストの項目を出力。
    - '*' でない場合、2つのリストの値を比較し、同じなら 1、異なれば 0 を出力。

    Parameters:
        list1 (list): 比較元のリスト。
        list2 (list): 比較対象のリスト。

    Returns:
        list: 比較結果のリスト。
    """
    if len(list1) != len(list2):
        message = mylib.log_error(f"リストの長さが一致していません。: {list1},\n {list2}")
        return message

    result = []
    for item1, item2 in zip(list1, list2):
        if item1 == "*":
            result.append(item2)
        else:
            result.append(1 if item1 == item2 else 0)
    return result

if __name__ == "__main__":
    # モデル名、プロンプトを設定
    model_path = "mlx-community/Mistral-7B-Instruct-v0.3-4bit"
    prompt = """
Read the following and output the student ID followed by answers (1) to (20) separated by commas in this order.
(e.g., 158R228020, A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T)
=====
"""
    txt_path = "./student_answers/158R228020-MINUTE-2411181641_page1.txt"
    answer_file = "./correct_answer/answer.txt"

    content = mylib.read_text_file(txt_path)
    prompt = prompt + content
    student_answer = generate_with_prompt(model_path, prompt)
    #print(student_answers)
    student_answer_list = [item.strip() for item in student_answer.split(",")]
    student_answer_list.insert(0, os.path.basename(txt_path)[:10])
    print(student_answer_list)

    correct_answer = mylib.read_text_file(answer_file)
    correct_answer_list = [item.strip() for item in correct_answer.split(",")]
    grade_list = compare_lists(correct_answer_list, student_answer_list)
    print(grade_list)

    # テキストファイルに出力
    base, ext = os.path.splitext(txt_path)
    txt_path = base + "-grade.txt"
    mylib.write_to_csv(txt_path, [student_answer_list, grade_list], None)
