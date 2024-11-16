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
        output = generate(model, processor, image_paths, formatted_prompt, verbose=False)
        output_list.append(output)
    
    return output_list

if __name__ == "__main__":
    # モデル名、画像パス、プロンプトを設定
    model_path = "mlx-community/Qwen2-VL-7B-Instruct-4bit"
    image_paths = ["./student_answers/20241115-a_page1.jpg"]
    prompt = "画像から(1)から(10)の解答を読み取り，1行目に(1)の解答を，改行して2行目に(2)の解答を，以下同様に英文字1文字で出力してください．"

    # 関数を呼び出して結果を取得
    output = process_images_with_prompt(model_path, image_paths, [prompt])

    # 出力を表示
    print("出力結果:")
    print(output)
