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
#    image_paths = ["./student_answers/158R218016-MINUTE-2411181639_page1.jpg"]
#    image_paths = ["./student_answers/158R218026-MINUTE-2411181639_page1.jpg"]
#    image_paths = ["./student_answers/158R218067-MINUTE-2411181639_page1.jpg"]
    image_paths = ["./student_answers/158R228020-MINUTE-2411181641_page1.jpg"]
#    prompt = "学生番号の欄に書かれている英数字10桁(158Rで始まる)を答えて．"
#    prompt = "What is the student's ID?"
#    prompt = "氏名の欄に書かれている文字を答えて．"
#    prompt = "年・組・番号の欄に書かれている文字を答えて．"
#    prompt = "What are his/her grade, class, and number?"
#    prompt = "The student's grade is 3 or 4, the student's class is 16. Then, what is the student's number?"
#    prompt = "問題(1)から(5)に何と解答していますか．それぞれ大文字のアルファベットで答えて．"
#    prompt = "The answers to problems (1) through (5) are written in uppercase letters of the alphabet. State what each of them is."
#    prompt = "問題(6)から(10)の解答が小文字のアルファベットで書かれています．何と解答しているか，それぞれ答えて．"
#    prompt = "The answers to problems (6) through (10) are written in lowercase letters of the alphabet. Provide each answer only, separated by commas."
#    prompt = "The answers to problems (6) through (10) are written in lowercase letters of the alphabet. State what each of them is."
#    prompt = "問題(11)から(15)の解答が1桁の数字で書かれています．何と解答しているか，それぞれ答えて．"
#    prompt = "The answers to problems (11) through (15) are written as single-digit numbers. State what each of them is."
#    prompt = "問題(16)から(20)の解答が分数で書かれています．何と解答しているか，それぞれ答えて．"
#    prompt = "The answers for Question (16)-(20) are written in rationals. What are they?"
    prompt = "The answers for Question (16)-(20) are written as fractions. Provide each of them in the format ?/?"

    # 関数を呼び出して結果を取得
    output = process_images_with_prompt(model_path, image_paths, [prompt])

    # 出力を表示
    print("出力結果:")
    print(output[0])
