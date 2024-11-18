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
    image_paths = ["./student_answers/158R248006-MINUTE-2411130931_page1.jpg"]
#    prompt = "「Student ID」「学生番号」という文字の右に書かれている10文字の英数字のみを答えて．"
    prompt = "「年・組・番号　?年?組?番」と書かれています．?に当てはまる3つの文字のみをコンマで区切って答えて．"

    # 関数を呼び出して結果を取得
    output = process_images_with_prompt(model_path, image_paths, [prompt])

    # 出力を表示
    print("出力結果:")
    print(output[0])
