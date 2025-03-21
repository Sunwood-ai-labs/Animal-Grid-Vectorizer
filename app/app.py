"""
Main application file for Animal Grid Vectorizer.
"""

from dotenv import load_dotenv
import gradio as gr
from .components import (
    EMOJI,
    create_input_components,
    create_grid_components,
    create_background_components,
    create_caption_components,
    create_svg_components,
    create_output_components
)
from .handlers import process_image
from .components import toggle_gemini_opts

# Load environment variables
load_dotenv()


# カスタムCSS：カラーパレット、Kaisei Decolフォント、Font Awesomeを含む
custom_css = """
/* Kaisei Decolフォントのインポート */
@import url('https://fonts.googleapis.com/css2?family=Kaisei+Decol:wght@700&display=swap');
/* Font Awesomeのインポート */
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');

html, body, .root {
  max-width: 100%;
  overflow-x: hidden;
}

/* カラーパレットをCSS変数として定義 */
:root {
  --teal-1: #025259;
  --teal-2: #007172;
  --orange-3: #F29325;
  --orange-4: #D94F04;
  --cream-5: #F4E2DE;
}

/* Gradioコンテナ全体のスタイリング */
.gradio-container {
  background-color: var(--cream-5);
  font-family: 'Kaisei Decol', serif;
  max-width: 100%;
  overflow-x: hidden;
}

/* 見出しのスタイリング */
h1, h2, h3 {
  font-family: 'Kaisei Decol', serif;
  font-weight: 700;
  color: var(--teal-1);
  text-align: center;
  line-height: 1.4;
}

/* ボタンのカスタムスタイル */
button.gr-button {
  background-color: var(--orange-3) !important;
  border: none !important;
  color: white !important;
  font-family: 'Kaisei Decol', serif;
  font-weight: 700;
  border-radius: 15px !important;
  padding: 10px 20px !important;
  transition: all 0.3s ease !important;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  gap: 8px !important;
}

button.gr-button:hover {
  background-color: var(--orange-4) !important;
  transform: translateY(-2px) !important;
  box-shadow: 0 6px 8px rgba(0,0,0,0.15) !important;
}

button.gr-button i {
  margin-right: 6px !important;
}

/* 入力要素のカスタムスタイル */
.gr-input, .gr-form, .gr-box {
  border: 2px solid var(--teal-2) !important;
  border-radius: 12px !important;
  padding: 10px !important;
  background-color: white !important;
  transition: all 0.3s ease !important;
}

.gr-input:focus {
  box-shadow: 0 0 0 3px rgba(242, 147, 36, 0.3) !important;
  border-color: var(--orange-3) !important;
}

/* ラベルのカスタムスタイル */
label {
  font-family: 'Kaisei Decol', serif;
  font-weight: 700;
  color: var(--teal-2);
  margin-bottom: 8px !important;
}

/* Kaisei Decolボールドクラスの適用 */
.kaisei-decol-bold {
  font-family: 'Kaisei Decol', serif;
  font-weight: 700;
}

/* カラーパレット表示のスタイリング */
#color-palette .color-box {
  transition: all 0.3s ease !important;
  margin: 5px !important;
  padding: 0 !important;
  overflow: hidden !important;
  border: 2px solid var(--teal-2) !important;
  border-radius: 12px !important;
  background-color: white !important;
}

#color-palette .color-box:hover {
  transform: translateY(-5px) !important;
  box-shadow: 0 10px 15px rgba(0,0,0,0.1) !important;
}

.color-swatch {
  width: 100%;
  height: 60px;
  margin-bottom: 5px;
  border-radius: 5px 5px 0 0 !important;
}

.palette-text {
  padding: 8px;
  text-align: center;
}

/* アイコンのスタイリング */
.icon-container {
  text-align: center;
  margin: 20px 0;
}

.icon-container i {
  font-size: 2rem;
  color: var(--teal-1);
  margin: 0 10px;
  transition: all 0.3s ease;
}

.icon-container i:hover {
  color: var(--orange-3);
  transform: scale(1.2);
}

.white-text, .white-text * {
  color: white !important;
}

/* かわいいヘッダースタイル */
.cute-header {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 20px;
  background: linear-gradient(45deg, var(--teal-1), var(--teal-2));
  padding: 25px;
  border-radius: 15px;
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
  position: sticky;
  top: 0;
  z-index: 1000;
  width: 100%;
  min-height: 80px;
  overflow: hidden;
}

.cute-header h1 {
  margin: 0 10px;
  font-size: 1.8rem;
}

/* 装飾的な要素 */
.decoration {
  position: relative;
  height: 30px;
}

.decoration::before {
  content: "";
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, var(--cream-5), var(--orange-3), var(--cream-5));
}

/* フッタースタイル */
.footer {
  text-align: center;
  margin-top: 30px;
  padding: 10px;
  font-size: 0.9rem;
  color: var(--teal-2);
  border-top: 1px dashed var(--orange-3);
}
"""

# フォントとFont Awesomeを追加するカスタムヘッダー
custom_head = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Kaisei+Decol:wght@700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
"""

def create_interface():
    """Create the Gradio interface for Animal Grid Vectorizer."""
    
    with gr.Blocks(title=f"{EMOJI['animal']} Animal Grid Vectorizer {EMOJI['vector']}",
                   css=custom_css, 
                   head=custom_head) as app:
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
                # Input components
                input_image = create_input_components()
                
                # Grid settings
                rows, cols = create_grid_components()
                
                # Background removal settings
                remove_bg, bg_method, remove_rectangle, area_threshold = create_background_components()
                
                # Caption generation settings
                use_gemini, api_key, model, caption_prompt = create_caption_components()
                
                # SVG conversion settings
                color_mode, hierarchical, mode, filter_speckle, color_precision, corner_threshold = create_svg_components()
                
                # Process button
                process_btn = gr.Button(f"{EMOJI['magic']} 処理開始", variant="primary")
            
            with gr.Column():
                # Output components
                overview_image, output_text, output_files, grid_display, svg_preview, zip_download = create_output_components()
        
        # Event handlers
        process_btn.click(
            fn=process_image,
            inputs=[
                input_image, rows, cols, remove_bg, bg_method, remove_rectangle, area_threshold,
                use_gemini, api_key, model, caption_prompt,
                color_mode, hierarchical, mode, filter_speckle, color_precision, corner_threshold,
                grid_display
            ],
            outputs=[overview_image, output_text, output_files, svg_preview, zip_download]
        )
        
        # Event handlers for UI components
        use_gemini.change(
            fn=toggle_gemini_opts,
            inputs=[use_gemini],
            outputs=[api_key, model, caption_prompt]
        )
    
    return app

if __name__ == "__main__":
    app = create_interface()
    app.launch()
