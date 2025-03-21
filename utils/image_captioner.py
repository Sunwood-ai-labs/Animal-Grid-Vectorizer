import os
import base64
from litellm import completion

class ImageCaptioner:
    """
    Geminiを使用して画像のキャプションを生成するクラス
    """
    
    def __init__(self, api_key=None, model="xai/grok-2-vision-1212"):
        """
        初期化関数
        
        Args:
            api_key (str, optional): XAI API Key
            model (str): 使用するモデル名
        """
        self.api_key = api_key
        self.model = model
        
    def set_api_key(self, api_key):
        """APIキーを設定する"""
        self.api_key = api_key
        
    def is_configured(self):
        """APIキーが設定されているかを確認する"""
        return self.api_key is not None and self.api_key.strip() != ""
        
    def generate_caption(self, image_path, prompt=None):
        """
        画像のキャプションを生成する
        
        Args:
            image_path (str): 画像ファイルのパス
            prompt (str, optional): キャプション生成のためのプロンプト
            
        Returns:
            str: 生成されたキャプション
        """
        if not self.is_configured():
            return "APIキーが設定されていません"
            
        if not os.path.exists(image_path):
            return f"画像ファイルが見つかりません: {image_path}"
            
        # デフォルトプロンプト
        if prompt is None:
            prompt = "この画像に写っている動物を簡潔に説明してください。動物の種類と特徴を含めてください。"
            
        try:
            # 環境変数にAPIキーを設定
            os.environ['XAI_API_KEY'] = self.api_key
            
            # 画像をBase64エンコード
            with open(image_path, "rb") as f:
                image_data = f.read()
                base64_image = base64.b64encode(image_data).decode('utf-8')
            
            # LitellmでXAI APIを呼び出す
            response = completion(
                model=self.model,
                messages=[
                    {
                        "role": "user", 
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ]
            )
            
            # レスポンスからテキストを抽出
            if response and hasattr(response, 'choices') and len(response.choices) > 0:
                return response.choices[0].message.content
            else:
                return "キャプションを生成できませんでした"
                
        except Exception as e:
            return f"エラーが発生しました: {str(e)}"
            
    def generate_filename(self, image_path, prefix="animal", prompt=None):
        """
        画像のキャプションを生成してファイル名として使用する
        
        Args:
            image_path (str): 画像ファイルのパス
            prefix (str): ファイル名のプレフィックス
            prompt (str, optional): キャプション生成のためのプロンプト
            
        Returns:
            tuple: (新しいファイル名, 生成されたキャプション)
        """
        # キャプション生成
        caption = self.generate_caption(image_path, prompt)
        
        # キャプションからファイル名を生成
        # 不正な文字を除去し、長さを制限
        invalid_chars = r'<>:"/\|?*'
        filename = caption.lower()
        
        # 不正な文字を除去
        for char in invalid_chars:
            filename = filename.replace(char, '')
            
        # 空白をアンダースコアに置換
        filename = filename.replace(' ', '_')
        
        # 長さを制限
        if len(filename) > 50:
            filename = filename[:50]
            
        # 拡張子を取得
        _, ext = os.path.splitext(image_path)
        
        # 最終的なファイル名を生成
        final_filename = f"{prefix}_{filename}{ext}"
        
        return final_filename, caption
        
    def batch_generate_filenames(self, image_dir, output_dir=None, prefix="animal", prompt=None):
        """
        ディレクトリ内の全画像のキャプションを生成してファイル名を変更する
        
        Args:
            image_dir (str): 画像ファイルのディレクトリ
            output_dir (str, optional): 出力ディレクトリ
            prefix (str): ファイル名のプレフィックス
            prompt (str, optional): キャプション生成のためのプロンプト
            
        Returns:
            dict: {元のファイルパス: (新しいファイルパス, キャプション)}
        """
        if not self.is_configured():
            print("APIキーが設定されていません")
            return {}
            
        # 出力ディレクトリが指定されていない場合は入力ディレクトリを使用
        if output_dir is None:
            output_dir = image_dir
            
        # 出力ディレクトリが存在しない場合は作成
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        results = {}
        
        # ディレクトリ内の画像を処理
        for filename in os.listdir(image_dir):
            if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                continue
                
            input_path = os.path.join(image_dir, filename)
            
            # キャプションとファイル名を生成
            new_filename, caption = self.generate_filename(input_path, prefix, prompt)
            output_path = os.path.join(output_dir, new_filename)
            
            # ファイルをコピーまたは移動
            if output_dir != image_dir:
                # 別ディレクトリの場合はコピー
                with open(input_path, 'rb') as src_file:
                    with open(output_path, 'wb') as dst_file:
                        dst_file.write(src_file.read())
            else:
                # 同じディレクトリの場合は名前変更
                os.rename(input_path, output_path)
                
            results[input_path] = (output_path, caption)
            print(f"処理完了: {filename} → {new_filename}")
            print(f"キャプション: {caption}")
            
        return results
