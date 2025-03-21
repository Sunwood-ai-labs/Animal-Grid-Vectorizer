import cv2
import numpy as np
import os
import xml.etree.ElementTree as ET
import re

def remove_background_simple(image_path, output_path=None, threshold=240):
    """
    シンプルな閾値ベースの背景除去関数
    
    Args:
        image_path (str): 入力画像のパス
        output_path (str, optional): 出力画像のパス。Noneの場合は新しいパスを生成
        threshold (int): 背景と判断する閾値 (0-255)
        
    Returns:
        str: 処理された画像のパス
    """
    # 画像を読み込む
    img = cv2.imread(image_path)
    if img is None:
        print(f"エラー: 画像を読み込めませんでした: {image_path}")
        return None
    
    # グレースケールに変換
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 閾値処理で背景を分離
    _, mask = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY_INV)
    
    # アルファチャンネルを作成
    alpha = np.zeros_like(gray)
    alpha[mask > 0] = 255
    
    # BGRA画像を作成
    bgra = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    bgra[:, :, 3] = alpha
    
    # 出力パスが指定されていない場合は生成
    if output_path is None:
        filename, ext = os.path.splitext(image_path)
        output_path = f"{filename}_nobg.png"
    
    # 画像を保存
    cv2.imwrite(output_path, bgra)
    print(f"背景除去画像を保存しました: {output_path}")
    
    return output_path

def remove_background_advanced(image_path, output_path=None, iterations=5):
    """
    GrabCutアルゴリズムを使用した高度な背景除去関数
    
    Args:
        image_path (str): 入力画像のパス
        output_path (str, optional): 出力画像のパス。Noneの場合は新しいパスを生成
        iterations (int): GrabCutの反復回数
        
    Returns:
        str: 処理された画像のパス
    """
    # 画像を読み込む
    img = cv2.imread(image_path)
    if img is None:
        print(f"エラー: 画像を読み込めませんでした: {image_path}")
        return None
    
    # 画像のサイズを取得
    height, width = img.shape[:2]
    
    # マスクを初期化
    mask = np.zeros(img.shape[:2], np.uint8)
    
    # 背景と前景のモデルを初期化
    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)
    
    # 前景領域を推定するための矩形
    # 画像の中央部分を前景と仮定
    margin = min(width, height) // 8
    rect = (margin, margin, width - 2*margin, height - 2*margin)
    
    # GrabCutアルゴリズムを実行
    cv2.grabCut(img, mask, rect, bgdModel, fgdModel, iterations, cv2.GC_INIT_WITH_RECT)
    
    # マスクを生成 (0と2が背景、1と3が前景)
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
    
    # マスクを適用して背景を透明にする
    img_fg = img * mask2[:, :, np.newaxis]
    
    # アルファチャンネルを作成
    alpha = np.zeros_like(mask2, dtype=np.uint8)
    alpha[mask2 > 0] = 255
    
    # BGRA画像を作成
    bgra = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    bgra[:, :, 3] = alpha
    
    # 出力パスが指定されていない場合は生成
    if output_path is None:
        filename, ext = os.path.splitext(image_path)
        output_path = f"{filename}_nobg_advanced.png"
    
    # 画像を保存
    cv2.imwrite(output_path, bgra)
    print(f"背景除去画像を保存しました: {output_path}")
    
    return output_path

def calculate_path_area(path_data):
    """
    パスの面積を推定する関数（バウンディングボックスを使用）
    """
    # パスデータから座標を抽出
    coords = re.findall(r'[A-Z]\s*(-?\d+\.?\d*)\s+(-?\d+\.?\d*)', path_data)

    if not coords:
        # より複雑なパスデータから座標を抽出
        coords = re.findall(r'(-?\d+\.?\d*)\s+(-?\d+\.?\d*)', path_data)

    if not coords:
        return 0

    # 浮動小数点に変換
    coords = [(float(x), float(y)) for x, y in coords]

    # バウンディングボックスを見つける
    min_x = min(x for x, _ in coords)
    max_x = max(x for x, _ in coords)
    min_y = min(y for _, y in coords)
    max_y = max(y for _, y in coords)

    # 面積を計算
    width = max_x - min_x
    height = max_y - min_y

    return width * height

def get_transform_values(transform_attr):
    """変換属性から平行移動値を抽出する関数"""
    if not transform_attr:
        return 0, 0

    match = re.search(r'translate\((-?\d+\.?\d*),(-?\d+\.?\d*)\)', transform_attr)
    if match:
        return float(match.group(1)), float(match.group(2))
    return 0, 0

def calculate_new_dimensions(paths):
    """残りのパスを含むために必要な寸法を計算する関数"""
    if not paths:
        return 0, 0, 0, 0

    min_x, min_y = float('inf'), float('inf')
    max_x, max_y = float('-inf'), float('-inf')

    for path in paths:
        path_data = path.get('d', '')
        transform = path.get('transform', '')
        tx, ty = get_transform_values(transform)

        # 座標を抽出
        coords = re.findall(r'[A-Z]\s*(-?\d+\.?\d*)\s+(-?\d+\.?\d*)', path_data)
        if not coords:
            coords = re.findall(r'(-?\d+\.?\d*)\s+(-?\d+\.?\d*)', path_data)

        if coords:
            # 変換を適用して境界を更新
            for x_str, y_str in coords:
                x, y = float(x_str) + tx, float(y_str) + ty
                min_x = min(min_x, x)
                max_x = max(max_x, x)
                min_y = min(min_y, y)
                max_y = max(max_y, y)

    # パディングを追加
    padding = 10
    min_x = max(0, min_x - padding)
    min_y = max(0, min_y - padding)
    max_x += padding
    max_y += padding

    return min_x, min_y, max_x, max_y

def find_and_remove_largest_rectangle(svg_file, output_file, auto_resize=True):
    """SVGファイルから最大の長方形を見つけて削除する関数"""
    # SVGファイルを解析
    try:
        tree = ET.parse(svg_file)
        root = tree.getroot()
    except Exception as e:
        print(f"SVGファイルの解析エラー: {e}")
        return None

    # すべてのパス要素を見つける
    paths = root.findall('.//{http://www.w3.org/2000/svg}path')
    if not paths:
        paths = root.findall('.//path')  # 名前空間なしで試す

    if not paths:
        print("SVGファイルにパスが見つかりません。")
        return None

    largest_area = 0
    largest_path = None

    # 最大面積のパスを見つける
    for path in paths:
        path_data = path.get('d', '')

        # 閉じたパスかどうかを確認（Zを含む）
        if 'Z' in path_data:
            # 面積を計算
            area = calculate_path_area(path_data)

            # 変換が存在する場合は適用（面積に影響する可能性がある）
            transform = path.get('transform', '')
            tx, ty = get_transform_values(transform)

            # 変換に基づく単純なスケーリング係数（近似値）
            transform_factor = 1 + (abs(tx) + abs(ty)) / 1000
            area *= transform_factor

            if area > largest_area:
                largest_area = area
                largest_path = path

    # 最大の長方形が見つかった場合は削除
    if largest_path is not None:
        parent = None
        for p in root.findall('.//*'):
            for child in p:
                if child == largest_path:
                    parent = p
                    break

        if parent is not None:
            parent.remove(largest_path)
        else:
            # ルートの直接の子
            root.remove(largest_path)

        print(f"面積 {largest_area} の長方形を削除しました")

        # 削除後にパスを再計算
        paths = root.findall('.//{http://www.w3.org/2000/svg}path')
        if not paths:
            paths = root.findall('.//path')
    else:
        print("削除する長方形が見つかりませんでした。")

    # 要求された場合はSVGを自動リサイズ
    if auto_resize and paths:
        min_x, min_y, max_x, max_y = calculate_new_dimensions(paths)
        width = max_x - min_x
        height = max_y - min_y

        # SVG属性を更新
        if width > 0 and height > 0:
            root.set('width', str(int(width)))
            root.set('height', str(int(height)))
            root.set('viewBox', f"{min_x} {min_y} {width} {height}")
            print(f"SVGをリサイズしました: width={width}, height={height}")

    # 適切なXML宣言で出力ファイルに書き込む
    ET.register_namespace('', "http://www.w3.org/2000/svg")
    tree.write(output_file, encoding='utf-8', xml_declaration=True)

    return output_file

def batch_remove_background(input_dir, output_dir=None, method='simple', threshold=240, iterations=5):
    """
    ディレクトリ内の全画像の背景を一括で除去する関数
    
    Args:
        input_dir (str): 入力画像のディレクトリ
        output_dir (str, optional): 出力画像のディレクトリ。Noneの場合は入力ディレクトリ内に新しいディレクトリを作成
        method (str): 背景除去方法 ('simple' または 'advanced')
        threshold (int): シンプルモードでの閾値
        iterations (int): 高度モードでのGrabCutの反復回数
        
    Returns:
        list: 処理された画像のパスのリスト
    """
    # 出力ディレクトリが指定されていない場合は生成
    if output_dir is None:
        output_dir = os.path.join(input_dir, 'nobg')
    
    # 出力ディレクトリが存在しない場合は作成
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"出力ディレクトリを作成しました: {output_dir}")
    
    # 処理された画像のパスのリスト
    processed_paths = []
    
    # ディレクトリ内の画像を処理
    for filename in os.listdir(input_dir):
        if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            continue
        
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}_nobg.png")
        
        # 背景除去を実行
        if method.lower() == 'simple':
            result_path = remove_background_simple(input_path, output_path, threshold)
        else:
            result_path = remove_background_advanced(input_path, output_path, iterations)
        
        if result_path:
            processed_paths.append(result_path)
    
    print(f"合計 {len(processed_paths)} 個の画像の背景を除去しました")
    return processed_paths
