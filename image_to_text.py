import codecs
import mlx.core as mx
from mlx_vlm.prompt_utils import apply_chat_template
from mlx_vlm.utils import generate, get_model_path, load, load_config, load_image_processor


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

if __name__ == "__main__":
    # モデル名、画像パス、プロンプトを設定
    #model_path = "mlx-community/Qwen2-VL-7B-Instruct-4bit"
    model_path = "mlx-community/deepseek-vl2-tiny-4bit"
    image_paths = ["./student_answers/158R228020-MINUTE-2411251550_page1.jpg"]
    prompt = """
The main part of the document is a grid with questions numbered 1 to 50.
For each question, there is a single-digit hand-written answer.
Output accurately the anwers to the questions directly in plain text within this response without any reference to a file.
Write each answer on a separate line into the following simple text format:
(Question number) Answer's digit
Ensure that the question number is enclosed in parentheses.
Example output (for illustration only):
## Final Result
(1) 0
(2) 0
(3) 0
"""

    # 関数を呼び出して結果を取得
    output = process_images_with_prompt(model_path, image_paths, [prompt])

    # 出力を表示
    print("出力結果:")
    print(output[0])
