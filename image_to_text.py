import codecs
import mlx.core as mx
from mlx_vlm.prompt_utils import apply_chat_template
from mlx_vlm.utils import generate, get_model_path, load, load_config, load_image_processor

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
    model_path = get_model_path(model_path)
    model, processor = load(model_path, lazy=False, trust_remote_code=True)
    processor.eos_token_id = 1
    config = load_config(model_path, trust_remote_code=True)

    output_list = []
    for prompt_item in prompt_list:
        # チャットテンプレートを適用
        prompt_item = codecs.decode(prompt_item, "unicode_escape")
        formatted_prompt = apply_chat_template(
            processor, config, prompt_item, num_images=len(image_paths)
        )
        # 出力を生成
        output = generate(model, processor, formatted_prompt, image=image_paths, max_tokens = 500, verbose=False)
        output_list.append(output)
    
    return output_list

if __name__ == "__main__":
    # モデル名、画像パス、プロンプトを設定
    #model_path = "mlx-community/Qwen2-VL-7B-Instruct-4bit"
    model_path = "mlx-community/deepseek-vl2-tiny-4bit"
    image_paths = ["./student_answers/158R228020-MINUTE-2411251550_page1.jpg"]
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

    # 関数を呼び出して結果を取得
    output = process_images_with_prompt(model_path, image_paths, [prompt])

    # 出力を表示
    print("出力結果:")
    print(output[0])
