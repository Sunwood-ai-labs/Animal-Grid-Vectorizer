import os
from utils.image_captioner import ImageCaptioner

# テスト用のAPIキー（実際のテストでは有効なAPIキーが必要です）
API_KEY = "YOUR_API_KEY_HERE"  # 実際のテストでは有効なAPIキーに置き換えてください

# テスト用ディレクトリの作成
test_output_dir = os.path.join('static', 'test_captioning')
os.makedirs(test_output_dir, exist_ok=True)

# テスト画像のパス
test_img_dir = os.path.join('static', 'test_output', 'refined_animals')
if os.path.exists(test_img_dir):
    print(f'テストディレクトリが見つかりました: {test_img_dir}')
    
    # ディレクトリ内の画像を取得
    image_files = [f for f in os.listdir(test_img_dir) 
                  if f.endswith(('.png', '.jpg', '.jpeg'))]
    
    if image_files:
        test_img = os.path.join(test_img_dir, image_files[0])
        print(f'テスト画像が見つかりました: {test_img}')
        
        # ImageCaptionerのインスタンスを作成
        captioner = ImageCaptioner(api_key=API_KEY)
        
        # APIキーが設定されているか確認
        if captioner.is_configured() and API_KEY != "YOUR_API_KEY_HERE":
            # キャプション生成をテスト
            caption = captioner.generate_caption(test_img)
            print(f'生成されたキャプション: {caption}')
            
            # ファイル名生成をテスト
            new_filename, caption = captioner.generate_filename(test_img, "animal")
            print(f'生成されたファイル名: {new_filename}')
            print(f'キャプション: {caption}')
            
            print('キャプション生成テスト完了')
        else:
            print('APIキーが設定されていないか、デフォルトのままです。実際のテストには有効なAPIキーが必要です。')
            print('モジュールのロードテストのみ完了しました。')
    else:
        print('テスト画像が見つかりませんでした')
else:
    print(f'テストディレクトリが見つかりませんでした: {test_img_dir}')
    
    # サンプル画像ディレクトリを確認
    sample_dir = 'static'
    if os.path.exists(sample_dir):
        print(f'サンプルディレクトリが見つかりました: {sample_dir}')
        
        # サンプル画像を探す
        for root, dirs, files in os.walk(sample_dir):
            image_files = [f for f in files if f.endswith(('.png', '.jpg', '.jpeg'))]
            if image_files:
                test_img = os.path.join(root, image_files[0])
                print(f'サンプル画像が見つかりました: {test_img}')
                
                # ImageCaptionerのインスタンスを作成
                captioner = ImageCaptioner(api_key=API_KEY)
                
                # APIキーが設定されているか確認
                if captioner.is_configured() and API_KEY != "YOUR_API_KEY_HERE":
                    # キャプション生成をテスト
                    caption = captioner.generate_caption(test_img)
                    print(f'生成されたキャプション: {caption}')
                    
                    print('キャプション生成テスト完了')
                else:
                    print('APIキーが設定されていないか、デフォルトのままです。実際のテストには有効なAPIキーが必要です。')
                    print('モジュールのロードテストのみ完了しました。')
                break
        else:
            print('サンプル画像が見つかりませんでした')
