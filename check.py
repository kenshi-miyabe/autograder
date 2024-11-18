
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

def text_to_list(text, correct_len):
    student_answer_list = [item.strip() for item in text.split(",")]
    while len(student_answer_list) < correct_len:
        student_answer_list.append("")
    return student_answer_list[:correct_len]

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
prompt0 = """
Read the following input and extract the answers to questions (1) through (15).
Output the answers separated by commas.
For example: A, B, C, D, E, F, G, H, I, J, K, L, M, N, O.
"""
    answer_file = "./correct_answer/answer.txt"
    txt_path = "./student_answers/158R228020-MINUTE-2411181641_page1.txt"

    content = mylib.read_text_file(txt_path)
    prompt = prompt0 + content
    student_answer = check.generate_with_prompt(model_path, prompt)
    student_answer_list = check.text_to_list(student_answer, problem_length)
    student_answer_list.insert(0, os.path.basename(txt_path)[:10])
    student_answer_list.insert(0, os.path.basename(txt_path))

    correct_answer = mylib.read_text_file(answer_file)
    correct_answer_list = check.text_to_list(correct_answer, problem_length+2)
        
    grade_list = check.compare_lists(correct_answer_list, student_answer_list)
    print(grade_list)

    # テキストファイルに出力
    base, ext = os.path.splitext(txt_path)
    txt_path = base + "-grade.txt"
    mylib.write_to_csv(txt_path, [student_answer_list, grade_list], None)
