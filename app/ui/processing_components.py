"""
Processing-related UI components.
"""

import gradio as gr
from app.ui.components_common import EMOJI

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
    
    return (
        color_mode, hierarchical, mode,
        filter_speckle, color_precision, corner_threshold
    )

def create_process_button():
    """Create process button component."""
    return gr.Button(
        f"{EMOJI['magic']} 処理開始",
        variant="primary"
    )

def create_grid_display_option():
    """Create grid display option component."""
    return gr.Checkbox(
        label=f"{EMOJI['grid']} グリッド表示",
        value=True,
        info="SVGをグリッド状に配置して表示"
    )
