import vtracer
import os
import tempfile
import shutil
import glob
from PIL import Image
import xml.etree.ElementTree as ET
import re

# デフォルトのパラメータ設定
DEFAULT_PARAMS = {
    # カラーモード設定
    'COLORMODE': 'color',  # 'color' または 'binary'

    # 階層モード設定
    'HIERARCHICAL': 'stacked',  # 'stacked' または 'cutout'

    # トレースモード設定
    'MODE': 'spline',  # 'spline', 'polygon', または 'none'

    # フィルタ設定
    'FILTER_SPECKLE': 10,  # ノイズフィルタ (0-128)
    'COLOR_PRECISION': 6,  # 色精度 (1-8)
    'LAYER_DIFFERENCE': 16,  # グラデーションステップ (0-128)

    # カーブフィッティング設定
    'CORNER_THRESHOLD': 60,  # 角度閾値 (0-180)
    'LENGTH_THRESHOLD': 4.0,  # セグメント長 (3.5-10)
    'MAX_ITERATIONS': 10,  # 最大反復回数 (1-20)
    'SPLICE_THRESHOLD': 45,  # スプライス閾値 (0-180)
    'PATH_PRECISION': 9,  # パス精度 (1-10)
}

def calculate_path_area(path_data):
    """
    Estimates the area of a path by calculating its bounding box.
    This is a simplification - for precise area calculation,
    a more complex algorithm would be needed.
    
    Args:
        path_data (str): SVG path data string
        
    Returns:
        float: Estimated area of the path
    """
    # Extract coordinates from the path data
    coords = re.findall(r'[A-Z]\s*(-?\d+\.?\d*)\s+(-?\d+\.?\d*)', path_data)

    if not coords:
        # Try to extract coordinates from more complex path data
        coords = re.findall(r'(-?\d+\.?\d*)\s+(-?\d+\.?\d*)', path_data)

    if not coords:
        return 0

    # Convert to float
    coords = [(float(x), float(y)) for x, y in coords]

    # Find the bounding box
    min_x = min(x for x, _ in coords)
    max_x = max(x for x, _ in coords)
    min_y = min(y for _, y in coords)
    max_y = max(y for _, y in coords)

    # Calculate area
    width = max_x - min_x
    height = max_y - min_y
    return width * height

def optimize_svg(svg_path, min_area_percentage=0.01):
    """
    Optimize SVG by removing tiny paths that are likely noise.
    
    Args:
        svg_path (str): Path to the SVG file
        min_area_percentage (float): Minimum area as percentage of total SVG area
        
    Returns:
        str: Path to the optimized SVG file
    """
    try:
        # Parse the SVG file
        tree = ET.parse(svg_path)
        root = tree.getroot()
        
        # Find all path elements
        paths = root.findall(".//{http://www.w3.org/2000/svg}path")
        
        if not paths:
            print(f"No paths found in {svg_path}")
            return svg_path
            
        # Get SVG dimensions
        width = float(root.get('width', '100'))
        height = float(root.get('height', '100'))
        total_area = width * height
        min_area = total_area * min_area_percentage / 100
        
        # Count paths before optimization
        path_count_before = len(paths)
        
        # Remove tiny paths
        paths_to_remove = []
        for path in paths:
            path_data = path.get('d', '')
            area = calculate_path_area(path_data)
            if area < min_area:
                paths_to_remove.append(path)
        
        for path in paths_to_remove:
            parent = path.getparent()
            if parent is not None:
                parent.remove(path)
        
        # Count paths after optimization
        paths_after = root.findall(".//{http://www.w3.org/2000/svg}path")
        path_count_after = len(paths_after)
        
        print(f"Optimized SVG: removed {path_count_before - path_count_after} of {path_count_before} paths")
        
        # Save the optimized SVG
        optimized_path = svg_path.replace('.svg', '_optimized.svg')
        tree.write(optimized_path)
        
        return optimized_path
        
    except Exception as e:
        print(f"Error optimizing SVG: {str(e)}")
        return svg_path

def convert_image_to_svg(input_path, output_path, params=None):
    """
    画像をSVGに変換する関数

    Args:
        input_path (str): 入力画像のパス
        output_path (str): 出力SVGのパス
        params (dict, optional): 変換パラメータ

    Returns:
        str: 生成されたSVGファイルのパス、エラー時はNone
    """
    # パラメータの設定
    if params is None:
        params = DEFAULT_PARAMS.copy()
    else:
        # デフォルトパラメータをベースに、指定されたパラメータで上書き
        actual_params = DEFAULT_PARAMS.copy()
        actual_params.update(params)
        params = actual_params

    # 一時ファイルを格納するディレクトリ
    temp_dir = tempfile.mkdtemp()
    temp_input = os.path.join(temp_dir, "temp_input.jpg")

    try:
        # 画像が存在するか確認
        if not os.path.exists(input_path):
            print(f"エラー: 入力ファイル '{input_path}' が見つかりません。")
            return None

        # 画像をコピーして処理
        print(f"入力画像を処理: {input_path}")
        img = Image.open(input_path)

        # 画像を一時ファイルとして保存（絶対パスで）
        img.save(temp_input, "JPEG")
        print(f"一時ファイルを作成: {temp_input}")

        # 絶対パスに変換
        abs_output_path = os.path.abspath(output_path)

        print(f"変換を開始... 入力: {temp_input}, 出力: {abs_output_path}")

        # VTracerを使用して画像をSVGに変換
        vtracer.convert_image_to_svg_py(
            temp_input,
            abs_output_path,
            colormode=params['COLORMODE'],
            hierarchical=params['HIERARCHICAL'],
            mode=params['MODE'],
            filter_speckle=params['FILTER_SPECKLE'],
            color_precision=params['COLOR_PRECISION'],
            layer_difference=params['LAYER_DIFFERENCE'],
            corner_threshold=params['CORNER_THRESHOLD'],
            length_threshold=params['LENGTH_THRESHOLD'],
            max_iterations=params['MAX_ITERATIONS'],
            splice_threshold=params['SPLICE_THRESHOLD'],
            path_precision=params['PATH_PRECISION']
        )

        print(f"変換完了: '{input_path}' → '{abs_output_path}'")
        
        # SVGの最適化（オプション）
        # optimized_path = optimize_svg(abs_output_path)
        # return optimized_path
        
        return abs_output_path

    except Exception as e:
        print(f"変換中にエラーが発生しました: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

    finally:
        # 一時ディレクトリとファイルを削除
        try:
            shutil.rmtree(temp_dir)
            print(f"一時ファイルをクリーンアップしました")
        except:
            pass

def batch_convert_folder(input_folder, output_folder, params=None):
    """
    指定フォルダ内のすべての画像をSVGに変換する

    Args:
        input_folder (str): 入力画像のフォルダ
        output_folder (str): 出力SVGのフォルダ
        params (dict, optional): 変換パラメータ

    Returns:
        list: 生成されたSVGファイルのパスリスト
    """
    # 出力フォルダが存在しない場合は作成
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"出力フォルダを作成しました: {output_folder}")

    # 画像ファイルの拡張子
    image_extensions = ('*.jpg', '*.jpeg', '*.png', '*.bmp', '*.tiff')

    # 変換結果のリスト
    converted_files = []

    # フォルダ内の全画像ファイルをリストアップ
    image_files = []
    for ext in image_extensions:
        image_files.extend(glob.glob(os.path.join(input_folder, ext)))
        image_files.extend(glob.glob(os.path.join(input_folder, ext.upper())))

    total_files = len(image_files)
    print(f"変換する画像ファイル数: {total_files}")

    # 各画像を変換
    for i, img_path in enumerate(image_files, 1):
        # 出力ファイル名を生成
        file_name = os.path.splitext(os.path.basename(img_path))[0]
        output_path = os.path.join(output_folder, f"{file_name}.svg")

        print(f"処理中 {i}/{total_files}: {img_path}")

        # 変換実行
        result = convert_image_to_svg(img_path, output_path, params)
        if result:
            converted_files.append(result)

    print(f"バッチ処理完了。成功: {len(converted_files)}/{total_files}")
    return converted_files

def update_params(base_params, new_params):
    """
    パラメータを更新する関数

    Args:
        base_params (dict): ベースとなるパラメータ辞書
        new_params (dict): 更新するパラメータの辞書
        
    Returns:
        dict: 更新されたパラメータ辞書
    """
    updated_params = base_params.copy()
    for key, value in new_params.items():
        if key in updated_params:
            updated_params[key] = value
            print(f"パラメータ更新: {key} = {value}")
        else:
            print(f"警告: 未知のパラメータ '{key}' は無視されました。")
    return updated_params

def print_params(params):
    """
    パラメータ設定を表示する関数
    
    Args:
        params (dict): 表示するパラメータ辞書
    """
    print("現在のパラメータ設定:")
    for key, value in params.items():
        print(f"  {key}: {value}")

def process_images_to_svg(image_paths, output_folder, params=None):
    """
    複数の画像をSVGに変換する
    
    Args:
        image_paths (list): 入力画像のパスのリスト
        output_folder (str): 出力SVGのフォルダ
        params (dict, optional): 変換パラメータ
        
    Returns:
        list: 生成されたSVGファイルのパスリスト
    """
    # 出力フォルダが存在しない場合は作成
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"出力フォルダを作成しました: {output_folder}")
        
    converted_files = []
    total_files = len(image_paths)
    
    for i, img_path in enumerate(image_paths, 1):
        # 出力ファイル名を生成
        file_name = os.path.splitext(os.path.basename(img_path))[0]
        output_path = os.path.join(output_folder, f"{file_name}.svg")

        print(f"処理中 {i}/{total_files}: {img_path}")

        # 変換実行
        result = convert_image_to_svg(img_path, output_path, params)
        if result:
            converted_files.append(result)
            
    print(f"処理完了。成功: {len(converted_files)}/{total_files}")
    return converted_files
