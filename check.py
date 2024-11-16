
import mylib
import sys
import csv

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
        raise ValueError("リストの長さが一致していません。")

    result = []
    for item1, item2 in zip(list1, list2):
        if item1 == "*":
            result.append(item2)
        else:
            result.append(1 if item1 == item2 else 0)
    return result



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