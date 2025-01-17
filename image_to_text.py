import os
import mylib

import codecs
import mlx.core as mx
from mlx_vlm.prompt_utils import apply_chat_template
from mlx_vlm.utils import generate, get_model_path, load, load_config, load_image_processor

import ollama

# 画像ファイルをテキストに変換する関数
def process_images_with_prompt(model_path, image_paths, prompt, max_tokens=5000, temp=0):
    """
    モデル名、画像ファイルリスト、プロンプトを受け取り、出力テキストを返す関数。

    Args:
        model_path (str): 使用するモデルのパス。
        image_paths (list of str): 入力画像のファイルパスのリスト。
        prompt (str): モデルに与えるプロンプト。

    Returns:
        str: モデルからの出力テキスト。
    """
    # モデルとプロセッサをロード
    model_path = get_model_path(model_path)
#    model, processor = load(model_path, lazy=False, trust_remote_code=True)
#    processor.eos_token_id = 1
    model, processor = load(model_path, lazy=False)
    config = load_config(model_path)

    # チャットテンプレートを適用
    prompt = codecs.decode(prompt, "unicode_escape")
    formatted_prompt = apply_chat_template(
        processor, config, prompt, num_images=len(image_paths)
    )
    # 出力を生成
    output = generate(model=model, processor=processor, prompt=formatted_prompt, image=image_paths, max_tokens=max_tokens, temp=temp, verbose=False)
    
    return output

def process_images_with_prompt_ollama(model_path, image_paths, prompt, max_tokens, temp):
    """
    モデル名、画像ファイルリスト、プロンプトを受け取り、出力テキストを返す関数。

    Args:
        model_path (str): 使用するモデルのパス。
        image_paths (list of str): 入力画像のファイルパスのリスト。
        prompt (str): モデルに与えるプロンプト。

    Returns:
        str: モデルからの出力テキスト。
    """
    response = ollama.chat(model=model_path, options={"temperature":temp, "num_predict":max_tokens}, messages=[
        {
            'role': 'user',
            'content': prompt,
            'images': image_paths
        },
    ])
    
    return response['message']['content']

def process_images_to_txt(model_info, prompt, image_path):
    model_path = model_info['model_path']
    model_name = model_info['model_name']
    model_type = model_info['type']
    max_tokens = model_info['max_tokens']
    temp = model_info['temp']
    if model_type == "mlx":
        print(f"{model_name}で{image_path}を処理中")
        output = process_images_with_prompt(model_path, [image_path], prompt, max_tokens, temp)
    elif model_type == "ollama":
        print(f"{model_name}で{image_path}を処理中")
        output = process_images_with_prompt_ollama(model_path, [image_path], prompt, max_tokens, temp)
    else :
        print("Error: unknown model type.")
        return

    # テキストファイルに出力
    base, ext = os.path.splitext(image_path)
    txt_path = base + "-" + model_name + ".txt"
    mylib.write_text_file(txt_path, output)


def process_list(arg_list, prompt, image_path):
    for model_info in arg_list:
        process_images_to_txt(model_info, prompt, image_path)

if __name__ == "__main__":
    # モデル名、画像パス、プロンプトを設定
    model_info = {'model_path': "mlx-community/pixtral-12b-4bit",
                'model_name': "Pixtral-0",
                'type': "mlx",
                'max_tokens': 5000,
                'temp': 0.4
                }
    image_paths = ["./student_answers/158R228044-MINUTE-2501161538_page1.jpg"]
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
    # 関数を呼び出して結果を取得
    output = process_images_with_prompt(model_info['model_path'], image_paths, prompt)

    # 出力を表示
    print("出力結果:")
    print(output)
