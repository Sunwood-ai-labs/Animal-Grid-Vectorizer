"""
Output-related UI components.
"""

import gradio as gr
from app.ui.components_common import EMOJI

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
    
    return (
        overview_image,
        output_text,
        output_files,
        grid_display,
        svg_preview,
        zip_download
    )

def create_progress_display():
    """Create progress display component."""
    return gr.HTML(
        value="<div id='progress'></div>",
        visible=False
    )

def update_progress(value, status):
    """
    Update progress display.
    
    Args:
        value (float): Progress value (0-1)
        status (str): Status message
        
    Returns:
        dict: HTML update for progress display
    """
    percentage = int(value * 100)
    return {
        "value": f"""
        <div style="width:100%; background-color:#f0f0f0; border-radius:5px;">
            <div style="width:{percentage}%; background-color:var(--orange-3); 
                        height:20px; border-radius:5px;">
            </div>
        </div>
        <div style="text-align:center; margin-top:5px;">
            {status} ({percentage}%)
        </div>
        """
    }
