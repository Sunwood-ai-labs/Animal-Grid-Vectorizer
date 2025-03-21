"""
Gradio UI components for Animal Grid Vectorizer.
"""

import gradio as gr
import os

def toggle_area_threshold(x):
    """Event handler for area threshold visibility."""
    return gr.update(visible=x)

def toggle_gemini_opts(x):
    """Event handler for Gemini options visibility."""
    return [
        gr.update(visible=x),  # api_key
        gr.update(visible=x),  # model
        gr.update(visible=x)   # caption_prompt
    ]

# Emoji definitions
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

def create_input_components():
    """Create input components for the interface."""
    with gr.Group():
        gr.Markdown(f"## {EMOJI['upload']} 入力")
        input_image = gr.Image(
            label=f"{EMOJI['image']} グリッド画像をアップロード",
            type="filepath"
        )
    return input_image

def create_grid_components():
    """Create grid setting components."""
    with gr.Group():
        gr.Markdown(f"## {EMOJI['grid']} グリッド設定")
        with gr.Row():
            rows = gr.Slider(
                minimum=1, maximum=10, value=3, step=1,
                label=f"行数"
            )
            cols = gr.Slider(
                minimum=1, maximum=10, value=5, step=1,
                label=f"列数"
            )
    return rows, cols

def create_background_components():
    """Create background removal components."""
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
            label=f"SVGから背景を削除する",
            value=False,
            info="SVGファイルから最大の面積を持つ要素（通常は背景）を削除し、自動的にリサイズします"
        )
        area_threshold = gr.Slider(
            minimum=0.1, maximum=0.99, value=0.35, step=0.01,
            label="背景判定の面積閾値 (0.5-0.99)",
            info="全体面積に対する比率がこの値を超える要素を背景として扱います",
            visible=False
        )
    # Rectangle removal checkbox event
    remove_rectangle.change(
        toggle_area_threshold,
        inputs=[remove_rectangle],
        outputs=[area_threshold]
    )
    
    return remove_bg, bg_method, remove_rectangle, area_threshold

def create_caption_components():
    """Create Gemini caption generation components."""
    with gr.Group():
        gr.Markdown(f"## {EMOJI['caption']} キャプション生成設定")
        use_gemini = gr.Checkbox(
            label=f"{EMOJI['ai']} Geminiを使って画像キャプションを生成",
            value=False
        )

        # Get default values from environment
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
    
        # Gemini checkbox event
        use_gemini.change(
            fn=toggle_gemini_opts,
            inputs=[use_gemini],
            outputs=[api_key, model, caption_prompt]
        )
    
    return use_gemini, api_key, model, caption_prompt

def create_svg_components():
    """Create SVG conversion components."""
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
    
    return color_mode, hierarchical, mode, filter_speckle, color_precision, corner_threshold

def create_output_components():
    """Create output components."""
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
        
        grid_display = gr.Checkbox(
            label=f"{EMOJI['grid']} グリッド表示",
            value=True,
            info="SVGをグリッド状に配置して表示"
        )
        
        with gr.Row():
            svg_preview = gr.HTML(
                label=f"{EMOJI['art']} SVGプレビュー",
                value="<div style='text-align:center'>SVGがここに表示されます</div>"
            )
        
        with gr.Row():
            output_files = gr.File(
                label=f"{EMOJI['download']} 個別SVGファイル",
                file_count="multiple"
            )
            zip_download = gr.File(
                label=f"{EMOJI['folder']} ZIPアーカイブ",
                file_count="single"
            )
    
    return overview_image, output_text, output_files, grid_display, svg_preview, zip_download
