"""
Event handlers for Animal Grid Vectorizer.
"""

import os
import tempfile
import shutil
from .components import EMOJI
from utils.grid_splitter import process_grid_image
from utils.svg_vectorizer import process_images_to_svg
from utils.background_removal import (
    remove_background_simple,
    remove_background_advanced,
    find_and_remove_largest_rectangle
)
from utils.image_captioner import ImageCaptioner

def process_image(image_path, rows_val, cols_val, remove_bg_val, bg_method_val, remove_rectangle_val,
                 use_gemini_val, api_key_val, model_val, caption_prompt_val,
                 color_mode_val, hierarchical_val, mode_val,
                 filter_speckle_val, color_precision_val, corner_threshold_val):
    """
    Main processing function for the application.

    Args:
        image_path (str): Path to the input image
        rows_val (int): Number of rows in the grid
        cols_val (int): Number of columns in the grid
        remove_bg_val (bool): Whether to remove background
        bg_method_val (str): Background removal method ('simple' or 'advanced')
        remove_rectangle_val (bool): Whether to remove largest rectangle from SVG
        use_gemini_val (bool): Whether to use Gemini for captioning
        api_key_val (str): Google API Key for Gemini
        model_val (str): Model name for Gemini
        caption_prompt_val (str): Prompt for caption generation
        color_mode_val (str): SVG color mode
        hierarchical_val (str): SVG hierarchy mode
        mode_val (str): SVG trace mode
        filter_speckle_val (int): Noise filter value
        color_precision_val (int): Color precision value
        corner_threshold_val (int): Corner threshold value

    Returns:
        tuple: (overview_image_path, result_text, output_file_list)
    """
    if not image_path:
        return None, "画像がアップロードされていません。", []
    
    try:
        # Create temporary directory
        temp_dir = tempfile.mkdtemp()
        output_dir = os.path.join(temp_dir, "output")
        
        # Grid splitting process
        result = process_grid_image(
            image_path=image_path,
            output_base_dir=output_dir,
            rows=rows_val,
            cols=cols_val
        )
        
        refined_paths = result['refined_paths']
        
        # Background removal process (optional)
        if remove_bg_val:
            refined_paths = handle_background_removal(
                refined_paths, output_dir, bg_method_val
            )
        
        # Gemini caption generation and file renaming (optional)
        if use_gemini_val and api_key_val:
            refined_paths = handle_caption_generation(
                refined_paths, output_dir, api_key_val, model_val, caption_prompt_val
            )
        
        # SVG conversion parameters
        svg_params = {
            'COLORMODE': color_mode_val,
            'HIERARCHICAL': hierarchical_val,
            'MODE': mode_val,
            'FILTER_SPECKLE': filter_speckle_val,
            'COLOR_PRECISION': color_precision_val,
            'CORNER_THRESHOLD': corner_threshold_val
        }
        
        # SVG conversion process
        svg_files = handle_svg_conversion(
            refined_paths, output_dir, svg_params, remove_rectangle_val
        )
        
        # Create result text
        result_text = create_result_text(
            result, remove_bg_val, bg_method_val, remove_rectangle_val,
            use_gemini_val, api_key_val, svg_files
        )
        
        # Create output file list
        output_file_list = svg_files.copy()
        if result['overview_path']:
            output_file_list.append(result['overview_path'])
        
        return result['overview_path'], result_text, output_file_list
        
    except Exception as e:
        import traceback
        error_text = f"{EMOJI['error']} エラーが発生しました: {str(e)}\n"
        error_text += traceback.format_exc()
        return None, error_text, []

def handle_background_removal(image_paths, output_dir, method):
    """Handle background removal process."""
    bg_removed_dir = os.path.join(output_dir, "bg_removed")
    os.makedirs(bg_removed_dir, exist_ok=True)
    
    bg_removed_paths = []
    for img_path in image_paths:
        filename = os.path.basename(img_path)
        output_path = os.path.join(bg_removed_dir, filename)
        
        if method == "simple":
            processed_path = remove_background_simple(img_path, output_path)
        else:
            processed_path = remove_background_advanced(img_path, output_path)
        
        if processed_path:
            bg_removed_paths.append(processed_path)
    
    return bg_removed_paths if bg_removed_paths else image_paths

def handle_caption_generation(image_paths, output_dir, api_key, model, prompt=None):
    """Handle Gemini caption generation process."""
    captioner = ImageCaptioner(api_key=api_key, model=model)
    
    captioned_dir = os.path.join(output_dir, "captioned")
    os.makedirs(captioned_dir, exist_ok=True)
    
    captioned_paths = []
    for img_path in image_paths:
        new_filename, _ = captioner.generate_filename(img_path, "animal", prompt)
        output_path = os.path.join(captioned_dir, new_filename)
        
        # Copy file
        shutil.copy2(img_path, output_path)
        captioned_paths.append(output_path)
    
    return captioned_paths if captioned_paths else image_paths

def handle_svg_conversion(image_paths, output_dir, svg_params, remove_rectangle=False):
    """Handle SVG conversion process."""
    svg_output_dir = os.path.join(output_dir, "svg_output")
    os.makedirs(svg_output_dir, exist_ok=True)
    
    svg_files = process_images_to_svg(
        image_paths,
        svg_output_dir,
        svg_params
    )
    
    if remove_rectangle and svg_files:
        rectangle_removed_dir = os.path.join(output_dir, "rectangle_removed")
        os.makedirs(rectangle_removed_dir, exist_ok=True)
        
        rectangle_removed_files = []
        for svg_file in svg_files:
            filename = os.path.basename(svg_file)
            output_path = os.path.join(rectangle_removed_dir, filename)
            
            processed_path = find_and_remove_largest_rectangle(svg_file, output_path)
            if processed_path:
                rectangle_removed_files.append(processed_path)
        
        return rectangle_removed_files if rectangle_removed_files else svg_files
    
    return svg_files

def create_result_text(result, remove_bg, bg_method, remove_rectangle,
                      use_gemini, api_key, svg_files):
    """Create result text message."""
    result_text = f"{EMOJI['success']} 処理が完了しました！\n"
    result_text += f"{EMOJI['split']} 分割された画像: {len(result['refined_paths'])}個\n"
    
    if remove_bg:
        result_text += f"{EMOJI['background']} 背景除去: {bg_method}モード\n"
    
    if remove_rectangle:
        result_text += f"{EMOJI['background']} SVGから長方形を削除\n"
    
    if use_gemini and api_key:
        result_text += f"{EMOJI['caption']} キャプション生成完了\n"
    
    result_text += f"{EMOJI['vector']} 変換されたSVG: {len(svg_files)}個\n"
    
    return result_text

def toggle_gemini_options(use_gemini):
    """Toggle visibility of Gemini options."""
    import gradio as gr
    return {
        "api_key": gr.update(visible=use_gemini),
        "model": gr.update(visible=use_gemini),
        "caption_prompt": gr.update(visible=use_gemini)
    }
