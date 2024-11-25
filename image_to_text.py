import mlx.core as mx
from mlx_vlm import load, generate
from mlx_vlm.prompt_utils import apply_chat_template
from mlx_vlm.utils import load_config

def process_images_with_prompt(model_path, image_paths, prompt_list):
    """
    モデル名、画像ファイルリスト、プロンプトを受け取り、出力テキストを返す関数。

    Args:
        model_path (str): 使用するモデルのパス。
        image_paths (list of str): 入力画像のファイルパスのリスト。
        prompt_list (str): モデルに与えるプロンプトのリスト。

    Returns:
        str: モデルからの出力テキスト。
    """
    # モデルとプロセッサをロード
    model, processor = load(model_path)
    config = load_config(model_path)

    output_list = []
    for prompt_item in prompt_list:
        # チャットテンプレートを適用
        formatted_prompt = apply_chat_template(
            processor, config, prompt_item, num_images=len(image_paths)
        )
        # 出力を生成
        output = generate(model, processor, image_paths, formatted_prompt, max_tokens = 500, verbose=False)
        output_list.append(output)
    
    return output_list

if __name__ == "__main__":
    # モデル名、画像パス、プロンプトを設定
    model_path = "mlx-community/Qwen2-VL-7B-Instruct-4bit"
#    image_paths = ["./student_answers/158R218016-MINUTE-2411181639_page1.jpg"]
#    image_paths = ["./student_answers/158R218026-MINUTE-2411181639_page1.jpg"]
#    image_paths = ["./student_answers/158R218067-MINUTE-2411181639_page1.jpg"]
    image_paths = ["./student_answers/158R228020-MINUTE-2411181641_page1.jpg"]
    prompt = """
Analyze the image and extract a 10-character alphanumeric ID that starts with '158R'.
The ID will be in the format '158R******' where '*' represents numbers.
Output the result as 'ID: 158R*****'.
If no such ID is found, respond with 'No ID found'.
"""
    prompt = """
Analyze the image and extract the information for grade, class, and number.
Output the result in the format:
Grade: [extracted grade]
Class: [extracted class]
Number: [extracted number]
"""
    prompt = """
"Analyze the image and extract answers labeled as '(1)' to '(5)'.
Each answer is a single uppercase alphabet letter.
Output the results in the following format:
(1) [Answer]
(2) [Answer]
(3) [Answer]
(4) [Answer]
(5) [Answer]
If any answer cannot be identified, replace it with '???'.
"""

    # 関数を呼び出して結果を取得
    output = process_images_with_prompt(model_path, image_paths, [prompt])

    # 出力を表示
    print("出力結果:")
    print(output[0])
