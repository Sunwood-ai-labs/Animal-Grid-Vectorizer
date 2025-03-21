import os
from dotenv import load_dotenv
import gradio as gr
import tempfile
import shutil

# .envファイルを読み込む
load_dotenv()
from PIL import Image
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.grid_splitter import process_grid_image
from utils.svg_vectorizer import process_images_to_svg, DEFAULT_PARAMS
from utils.background_remover import remove_background_simple, remove_background_advanced, find_and_remove_largest_rectangle
from utils.image_captioner import ImageCaptioner

# 絵文字の定義
EMOJI = {
    "grid": "🔲",
    "split": "✂️",
    "vector": "🖋️",
    "settings": "⚙️",
    "upload": "📤",
    "download": "📥",
    "success": "✅",
    "error": "❌",
    "animal": "🐾",
    "art": "🎨",
    "magic": "✨",
    "folder": "📁",
    "image": "🖼️",
    "svg": "📐",
    "processing": "⏳",
    "complete": "🏁",
    "background": "🧹",
    "caption": "💬",
    "ai": "🤖"
}

def create_interface():
    """Gradio インターフェースを作成する関数"""
    
    with gr.Blocks(title=f"{EMOJI['animal']} Animal Grid Vectorizer {EMOJI['vector']}") as app:
        gr.Markdown(f"""
        # {EMOJI['animal']} Animal Grid Vectorizer {EMOJI['vector']}
        
        グリッド状に配置された動物イラストを分割し、SVGベクター形式に変換するツールです。
        
        ## 使い方
        1. {EMOJI['upload']} グリッド画像をアップロードします
        2. {EMOJI['grid']} グリッドの行数と列数を設定します
        3. {EMOJI['background']} 背景除去の設定を調整します（オプション）
        4. {EMOJI['caption']} Geminiによる画像キャプション生成の設定を調整します（オプション）
        5. {EMOJI['settings']} SVG変換の設定を調整します（オプション）
        6. {EMOJI['magic']} 「処理開始」ボタンをクリックします
        7. {EMOJI['download']} 結果をダウンロードします
        """)
        
        with gr.Row():
            with gr.Column():
                # 入力セクション
                with gr.Group():
                    gr.Markdown(f"## {EMOJI['upload']} 入力")
                    input_image = gr.Image(
                        label=f"{EMOJI['image']} グリッド画像をアップロード",
                        type="filepath"
                    )
                
                # グリッド設定
                with gr.Group():
                    gr.Markdown(f"## {EMOJI['grid']} グリッド設定")
                    with gr.Row():
                        rows = gr.Slider(
                            minimum=1, maximum=10, value=3, step=1,
                            label=f"行数"
                        )
                        cols = gr.Slider(
                            minimum=1, maximum=10, value=6, step=1,
                            label=f"列数"
                        )
                
                # 背景除去設定
                with gr.Group():
                    gr.Markdown(f"## {EMOJI['background']} 背景除去設定")
                    remove_bg = gr.Checkbox(
                        label=f"背景を除去する",
                        value=False
                    )
                    bg_method = gr.Radio(
                        choices=["simple", "advanced"],
                        value="simple",
                        label="背景除去方法",
                        info="simple: シンプルな閾値ベースの背景除去（高速）、advanced: 高度なGrabCutアルゴリズムを使用した背景除去（高品質）"
                    )
                    remove_rectangle = gr.Checkbox(
                        label=f"SVGから最大の長方形を削除する",
                        value=False,
                        info="SVGファイルから最大の長方形（通常は背景）を削除し、自動的にリサイズします"
                    )
                
                # Geminiキャプション設定
                with gr.Group():
                    gr.Markdown(f"## {EMOJI['caption']} キャプション生成設定")
                    use_gemini = gr.Checkbox(
                        label=f"{EMOJI['ai']} Geminiを使って画像キャプションを生成",
                        value=False
                    )
                    # .envから値を取得
                    default_api_key = os.getenv('XAI_API_KEY', '')
                    default_model = os.getenv('XAI_MODEL', 'xai/grok-2-vision-1212')

                    api_key = gr.Textbox(
                        label="Google API Key",
                        placeholder="sk-...",
                        value=default_api_key,
                        type="password",
                        visible=False
                    )
                    model = gr.Textbox(
                        label="モデル名",
                        placeholder="xai/grok-2-vision-1212",
                        value=default_model,
                        visible=False
                    )
                    caption_prompt = gr.Textbox(
                        label="キャプション生成プロンプト",
                        placeholder="この画像に写っている動物を簡潔に説明してください。動物の種類と特徴を含めてください。",
                        visible=False,
                        value="この画像の英語のキャプションを作成して"
                    )
                    
                    # APIキーとプロンプトの表示/非表示を切り替える
                    def toggle_gemini_options(use_gemini):
                        return {
                            api_key: gr.update(visible=use_gemini),
                            model: gr.update(visible=use_gemini),
                            caption_prompt: gr.update(visible=use_gemini)
                        }
                    
                    use_gemini.change(
                        fn=toggle_gemini_options,
                        inputs=[use_gemini],
                        outputs=[api_key, model, caption_prompt]
                    )
                
                # SVG変換設定
                with gr.Group():
                    gr.Markdown(f"## {EMOJI['settings']} SVG変換設定")
                    with gr.Accordion(f"{EMOJI['settings']} 詳細設定", open=False):
                        color_mode = gr.Radio(
                            choices=["color", "binary"],
                            value="color",
                            label="カラーモード"
                        )
                        hierarchical = gr.Radio(
                            choices=["stacked", "cutout"],
                            value="stacked",
                            label="階層モード"
                        )
                        mode = gr.Radio(
                            choices=["spline", "polygon", "none"],
                            value="spline",
                            label="トレースモード"
                        )
                        filter_speckle = gr.Slider(
                            minimum=0, maximum=128, value=10, step=1,
                            label="ノイズフィルタ (0-128)"
                        )
                        color_precision = gr.Slider(
                            minimum=1, maximum=8, value=6, step=1,
                            label="色精度 (1-8)"
                        )
                        corner_threshold = gr.Slider(
                            minimum=0, maximum=180, value=60, step=1,
                            label="角度閾値 (0-180)"
                        )
                
                # 処理ボタン
                process_btn = gr.Button(f"{EMOJI['magic']} 処理開始", variant="primary")
            
            with gr.Column():
                # 出力セクション
                with gr.Group():
                    gr.Markdown(f"## {EMOJI['split']} 分割結果")
                    overview_image = gr.Image(
                        label=f"{EMOJI['image']} 分割されたイラスト",
                        type="filepath"
                    )
                
                with gr.Group():
                    gr.Markdown(f"## {EMOJI['vector']} SVG変換結果")
                    output_text = gr.Textbox(
                        label=f"{EMOJI['processing']} 処理状況",
                        placeholder="処理結果がここに表示されます",
                        lines=5
                    )
                    
                    output_files = gr.File(
                        label=f"{EMOJI['download']} 変換されたSVGファイル",
                        file_count="multiple"
                    )
        
        def process_image(image_path, rows_val, cols_val, remove_bg_val, bg_method_val, remove_rectangle_val,
                         use_gemini_val, api_key_val, model_val, caption_prompt_val,
                         color_mode_val, hierarchical_val, mode_val,
                         filter_speckle_val, color_precision_val, corner_threshold_val):
            """
            画像処理のメイン関数
            """
            if not image_path:
                return None, "画像がアップロードされていません。", []
            
            try:
                # 一時ディレクトリを作成
                temp_dir = tempfile.mkdtemp()
                output_dir = os.path.join(temp_dir, "output")
                
                # グリッド分割処理
                result = process_grid_image(
                    image_path=image_path,
                    output_base_dir=output_dir,
                    rows=rows_val,
                    cols=cols_val
                )
                
                refined_paths = result['refined_paths']
                
                # 背景除去処理（オプション）
                if remove_bg_val:
                    bg_removed_dir = os.path.join(output_dir, "bg_removed")
                    os.makedirs(bg_removed_dir, exist_ok=True)
                    
                    bg_removed_paths = []
                    for img_path in refined_paths:
                        filename = os.path.basename(img_path)
                        output_path = os.path.join(bg_removed_dir, filename)
                        
                        if bg_method_val == "simple":
                            processed_path = remove_background_simple(img_path, output_path)
                        else:
                            processed_path = remove_background_advanced(img_path, output_path)
                        
                        if processed_path:
                            bg_removed_paths.append(processed_path)
                    
                    # 背景除去された画像を使用
                    if bg_removed_paths:
                        refined_paths = bg_removed_paths
                
                # Geminiによるキャプション生成とファイル名変更（オプション）
                if use_gemini_val and api_key_val:
                    captioner = ImageCaptioner(api_key=api_key_val, model=model_val)
                    
                    # プロンプトが空の場合はデフォルトを使用
                    prompt = caption_prompt_val if caption_prompt_val else None
                    
                    captioned_dir = os.path.join(output_dir, "captioned")
                    os.makedirs(captioned_dir, exist_ok=True)
                    
                    captioned_results = {}
                    for img_path in refined_paths:
                        new_filename, caption = captioner.generate_filename(img_path, "animal", prompt)
                        output_path = os.path.join(captioned_dir, new_filename)
                        
                        # ファイルをコピー
                        shutil.copy2(img_path, output_path)
                        captioned_results[img_path] = (output_path, caption)
                    
                    # キャプションが生成された画像を使用
                    if captioned_results:
                        refined_paths = [result[0] for result in captioned_results.values()]
                
                # SVG変換パラメータの設定
                svg_params = {
                    'COLORMODE': color_mode_val,
                    'HIERARCHICAL': hierarchical_val,
                    'MODE': mode_val,
                    'FILTER_SPECKLE': filter_speckle_val,
                    'COLOR_PRECISION': color_precision_val,
                    'CORNER_THRESHOLD': corner_threshold_val
                }
                
                # SVG変換処理
                svg_output_dir = os.path.join(output_dir, "svg_output")
                os.makedirs(svg_output_dir, exist_ok=True)
                
                svg_files = process_images_to_svg(
                    refined_paths,
                    svg_output_dir,
                    svg_params
                )
                
                # SVGから最大の長方形を削除（オプション）
                if remove_rectangle_val and svg_files:
                    rectangle_removed_dir = os.path.join(output_dir, "rectangle_removed")
                    os.makedirs(rectangle_removed_dir, exist_ok=True)
                    
                    rectangle_removed_files = []
                    for svg_file in svg_files:
                        filename = os.path.basename(svg_file)
                        output_path = os.path.join(rectangle_removed_dir, filename)
                        
                        processed_path = find_and_remove_largest_rectangle(svg_file, output_path)
                        if processed_path:
                            rectangle_removed_files.append(processed_path)
                    
                    # 長方形が削除されたSVGファイルを使用
                    if rectangle_removed_files:
                        svg_files = rectangle_removed_files
                
                # 結果テキストの作成
                result_text = f"{EMOJI['success']} 処理が完了しました！\n"
                result_text += f"{EMOJI['split']} 分割された画像: {len(result['refined_paths'])}個\n"
                
                if remove_bg_val:
                    result_text += f"{EMOJI['background']} 背景除去: {bg_method_val}モード\n"
                
                if remove_rectangle_val:
                    result_text += f"{EMOJI['background']} SVGから長方形を削除: {len(rectangle_removed_files)}個\n"
                
                if use_gemini_val and api_key_val:
                    result_text += f"{EMOJI['caption']} キャプション生成: {len(captioned_results)}個\n"
                
                result_text += f"{EMOJI['vector']} 変換されたSVG: {len(svg_files)}個\n"
                
                # 結果ファイルのリストを作成
                output_file_list = svg_files.copy()
                if result['overview_path']:
                    output_file_list.append(result['overview_path'])
                
                # 一時ディレクトリのクリーンアップは行わない（Gradioがファイルを参照するため）
                
                return result['overview_path'], result_text, output_file_list
                
            except Exception as e:
                import traceback
                error_text = f"{EMOJI['error']} エラーが発生しました: {str(e)}\n"
                error_text += traceback.format_exc()
                return None, error_text, []
        
        # イベントの設定
        process_btn.click(
            fn=process_image,
            inputs=[
                input_image, rows, cols, remove_bg, bg_method, remove_rectangle,
                use_gemini, api_key, model, caption_prompt,
                color_mode, hierarchical, mode, filter_speckle, color_precision, corner_threshold
            ],
            outputs=[overview_image, output_text, output_files]
        )
        
    return app

if __name__ == "__main__":
    app = create_interface()
    app.launch()
