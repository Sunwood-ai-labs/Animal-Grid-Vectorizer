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
from .handlers import process_image, toggle_gemini_options

# Load environment variables
load_dotenv()

def create_interface():
    """Create the Gradio interface for Animal Grid Vectorizer."""
    
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
                # Input components
                input_image = create_input_components()
                
                # Grid settings
                rows, cols = create_grid_components()
                
                # Background removal settings
                remove_bg, bg_method, remove_rectangle = create_background_components()
                
                # Caption generation settings
                use_gemini, api_key, model, caption_prompt = create_caption_components()
                
                # SVG conversion settings
                color_mode, hierarchical, mode, filter_speckle, color_precision, corner_threshold = create_svg_components()
                
                # Process button
                process_btn = gr.Button(f"{EMOJI['magic']} 処理開始", variant="primary")
            
            with gr.Column():
                # Output components
                overview_image, output_text, output_files = create_output_components()
        
        # Event handlers
        process_btn.click(
            fn=process_image,
            inputs=[
                input_image, rows, cols, remove_bg, bg_method, remove_rectangle,
                use_gemini, api_key, model, caption_prompt,
                color_mode, hierarchical, mode, filter_speckle, color_precision, corner_threshold
            ],
            outputs=[overview_image, output_text, output_files]
        )
        
        use_gemini.change(
            fn=toggle_gemini_options,
            inputs=[use_gemini],
            outputs=[api_key, model, caption_prompt]
        )
    
    return app

if __name__ == "__main__":
    app = create_interface()
    app.launch()
