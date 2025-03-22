"""
Main processing functionality.
"""

import os
import tempfile
from loguru import logger
from utils.grid_splitter import process_grid_image
from .background import handle_background_removal
from .caption import handle_caption_generation
from .svg import (
    handle_svg_conversion,
    create_zip_archive
)
from .utils import create_result_text

def process_image(image_path, rows_val, cols_val, remove_bg_val, bg_method_val, 
                 remove_rectangle_val, area_threshold_val, use_gemini_val, api_key_val, 
                 model_val, caption_prompt_val, color_mode_val, hierarchical_val, mode_val,
                 filter_speckle_val, color_precision_val, corner_threshold_val,
                 grid_display_val):
    """
    Main processing function for the application.

    Args:
        image_path (str): Path to the input image
        rows_val (int): Number of rows in the grid
        cols_val (int): Number of columns in the grid
        remove_bg_val (bool): Whether to remove background
        bg_method_val (str): Background removal method ('simple' or 'advanced')
        remove_rectangle_val (bool): Whether to remove largest rectangle from SVG
        area_threshold_val (float): Area ratio threshold for background detection
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
        grid_display_val (bool): Whether to display grid layout

    Returns:
        tuple: (overview_image_path, result_text, output_file_list, svg_preview_html, zip_file)
    """
    logger.info("Starting image processing...")
    if not image_path:
        return None, "画像がアップロードされていません。", [], "", None
    
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
            'CORNER_THRESHOLD': corner_threshold_val,
            'LENGTH_THRESHOLD': 4.0,  # デフォルト値
            'MAX_ITERATIONS': 10,     # デフォルト値
            'SPLICE_THRESHOLD': 45,   # デフォルト値
            'PATH_PRECISION': 9,      # デフォルト値
            'LAYER_DIFFERENCE': 16    # デフォルト値を追加
        }
        
        # SVG conversion process
        logger.info("Starting SVG conversion...")
        svg_files = handle_svg_conversion(
            refined_paths, output_dir, svg_params,
            remove_rectangle=remove_rectangle_val,
            area_threshold=area_threshold_val,
            grid_display=grid_display_val,
            rows=rows_val,
            cols=cols_val
        )
        
        # Create result text
        result_text = create_result_text(
            result, remove_bg_val, bg_method_val, remove_rectangle_val,
            use_gemini_val, api_key_val, svg_files,
            grid_display_val
        )
        
        # Prepare output files
        individual_files = svg_files.copy()
        zip_file = None
        svg_preview_html = "<div style='text-align:center'>SVGが生成されていません</div>"
        
        # Create SVG preview if grid display is enabled
        if grid_display_val and svg_files:
            grid_file = os.path.join(output_dir, "grid_layout.svg")
            if os.path.exists(grid_file):
                try:
                    with open(grid_file, 'r', encoding='utf-8') as f:
                        svg_content = f.read()
                        svg_preview_html = f"<div style='text-align:center'>{svg_content}</div>"
                except Exception as e:
                    logger.error(f"Error reading grid SVG: {str(e)}")
                individual_files.append(grid_file)
        
        # Create ZIP archive
        if svg_files:
            zip_file = create_zip_archive(svg_files, output_dir)
            
        # Add overview image if available
        if result['overview_path']:
            individual_files.append(result['overview_path'])
        
        return result['overview_path'], result_text, individual_files, svg_preview_html, zip_file
        
    except Exception as e:
        import traceback
        error_text = f"エラーが発生しました: {str(e)}\n"
        error_text += traceback.format_exc()
        return None, error_text, [], "", None
