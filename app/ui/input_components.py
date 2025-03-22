"""
Input components for the UI.
"""

import os
import gradio as gr
from app.ui.components_common import EMOJI, toggle_gemini_opts

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
            lambda x: gr.update(visible=x),
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
