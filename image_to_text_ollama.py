import ollama

def process_images_with_prompt(model_path, image_paths, prompt, max_tokens):
    """
    モデル名、画像ファイルリスト、プロンプトを受け取り、出力テキストを返す関数。

    Args:
        model_path (str): 使用するモデルのパス。
        image_paths (list of str): 入力画像のファイルパスのリスト。
        prompt (str): モデルに与えるプロンプト。

    Returns:
        str: モデルからの出力テキスト。
    """
    response = ollama.chat(model=model_path, options={"temperature":0, "num_predict":max_tokens}, messages=[
        {
            'role': 'user',
            'content': prompt,
            'images': image_paths
        },
    ])
    
    return response['message']['content']


if __name__ == "__main__":
    response = ollama.chat(model='minicpm-v', options={"temperature":0, "num_predict":5000}, messages=[
        {
            'role': 'user',
            'content': 'Describe this image:',
            'images': ['./student_answers/158R228020-MINUTE-2411251550_page1.jpg']
        },
    ])
    print(response['message']['content'])

