import os
from utils.background_remover import remove_background_simple, remove_background_advanced

# テスト用ディレクトリの作成
test_output_dir = os.path.join('static', 'test_bg_removal')
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
        
        # シンプルな背景除去をテスト
        simple_output = os.path.join(test_output_dir, 'bg_removed_simple.png')
        simple_result = remove_background_simple(test_img, simple_output)
        print(f'シンプル背景除去結果: {simple_result}')
        
        # 高度な背景除去をテスト
        advanced_output = os.path.join(test_output_dir, 'bg_removed_advanced.png')
        advanced_result = remove_background_advanced(test_img, advanced_output)
        print(f'高度な背景除去結果: {advanced_result}')
        
        print('背景除去テスト完了')
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
                
                # シンプルな背景除去をテスト
                simple_output = os.path.join(test_output_dir, 'bg_removed_simple.png')
                simple_result = remove_background_simple(test_img, simple_output)
                print(f'シンプル背景除去結果: {simple_result}')
                
                print('背景除去テスト完了')
                break
        else:
            print('サンプル画像が見つかりませんでした')
