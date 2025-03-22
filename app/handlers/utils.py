"""
Utility functions for handlers.
"""

from app.ui.components_common import EMOJI

def create_result_text(result, remove_bg, bg_method, remove_rectangle,
                      use_gemini, api_key, svg_files, grid_display, area_threshold=None):
    """
    Create result text message.
    
    Args:
        result (dict): Processing result info
        remove_bg (bool): Whether background was removed
        bg_method (str): Background removal method used
        remove_rectangle (bool): Whether rectangle was removed from SVG
        use_gemini (bool): Whether Gemini was used
        api_key (str): Gemini API key
        svg_files (list): List of processed SVG files
        grid_display (bool): Whether grid display is enabled
        area_threshold (float, optional): Area threshold used for background removal
    
    Returns:
        str: Formatted result message
    """
    result_text = f"{EMOJI['success']} 処理が完了しました！\n"
    result_text += f"{EMOJI['split']} 分割された画像: {len(result['refined_paths'])}個\n"
    
    if remove_bg:
        result_text += f"{EMOJI['background']} 背景除去: {bg_method}モード\n"
    
    if remove_rectangle:
        threshold_info = f" (面積比{area_threshold:.0%}以上の要素を削除)" if area_threshold else ""
        result_text += f"{EMOJI['background']} SVGから大きな背景要素を削除{threshold_info}\n"
    
    if use_gemini and api_key:
        result_text += f"{EMOJI['caption']} キャプション生成完了\n"
    
    result_text += f"{EMOJI['vector']} 変換されたSVG: {len(svg_files)}個\n"
    result_text += f"{EMOJI['folder']} SVGファイルをZIPアーカイブで提供\n"
    
    if grid_display:
        result_text += f"{EMOJI['grid']} グリッド表示のSVGを生成\n"
    
    return result_text
