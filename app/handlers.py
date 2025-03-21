"""
Event handlers for Animal Grid Vectorizer.
"""

import os
import tempfile
import shutil
import zipfile
from loguru import logger
from .components import EMOJI
from utils.grid_splitter import process_grid_image, create_grid_layout
from utils.svg_vectorizer import process_images_to_svg
from utils.background_removal import (
    remove_background_simple,
    remove_background_advanced,
    find_and_remove_large_paths
)
from utils.image_captioner import ImageCaptioner

def process_image(image_path, rows_val, cols_val, remove_bg_val, bg_method_val, remove_rectangle_val, area_threshold_val,
                 use_gemini_val, api_key_val, model_val, caption_prompt_val,
                 color_mode_val, hierarchical_val, mode_val,
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
        area_threshold_val (float): Area ratio threshold for background detection (0.5-0.99)
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
    logger.info("Starting image processing...")
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
            grid_file = create_svg_grid(svg_files, rows_val, cols_val, output_dir)
            if grid_file:
                # Read the grid SVG file and create HTML preview
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

def create_svg_grid(svg_files, rows, cols, output_dir):
    """
    Create a single SVG file with grid layout of all SVG files.
    
    Args:
        svg_files (list): List of SVG file paths
        rows (int): Number of rows in grid
        cols (int): Number of columns in grid
        output_dir (str): Output directory
        
    Returns:
        str: Path to the grid SVG file
    """
    grid_output_path = os.path.join(output_dir, "grid_layout.svg")
    return create_grid_layout(svg_files, grid_output_path, rows, cols)

def create_zip_archive(files, output_dir):
    """
    Create ZIP archive containing the given files.
    
    Args:
        files (list): List of file paths to include
        output_dir (str): Output directory
        
    Returns:
        str: Path to the ZIP file
    """
    zip_path = os.path.join(output_dir, "svg_files.zip")
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for file in files:
            zipf.write(file, os.path.basename(file))
    return zip_path

def handle_svg_conversion(image_paths, output_dir, svg_params, remove_rectangle=False, area_threshold=0.9,
                         grid_display=True, rows=3, cols=6):
    """
    Handle SVG conversion process.
    
    Args:
        image_paths (list): List of image paths to convert
        output_dir (str): Output directory for SVG files
        svg_params (dict): SVG conversion parameters
        remove_rectangle (bool): Whether to remove background from SVGs
        area_threshold (float): Area ratio threshold for background detection
        save_option (str): "個別ファイル" or "ZIPアーカイブ"
        grid_display (bool): Whether to create grid layout
        rows (int): Number of rows in grid
        cols (int): Number of columns in grid
        
    Returns:
        list: Paths to output files (SVG files and/or ZIP archive)
    """
    logger.info(f"Converting {len(image_paths)} images to SVG...")
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
            
            logger.info(f"Processing SVG to remove large background paths: {svg_file}")
            processed_path = find_and_remove_large_paths(
                svg_file,
                output_path,
                area_threshold=area_threshold
            )
            if processed_path:
                rectangle_removed_files.append(processed_path)
        
        svg_files = rectangle_removed_files if rectangle_removed_files else svg_files
    
    # Process all SVG files
    output_files = svg_files.copy()
    
    # Create grid layout if requested
    if grid_display and svg_files:
        grid_file = create_svg_grid(svg_files, rows, cols, output_dir)
        if grid_file:
            output_files.append(grid_file)
    
    return output_files

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
        save_option (str): Save option selected ("個別ファイル" or "ZIPアーカイブ")
        grid_display (bool): Whether grid display is enabled
        area_threshold (float, optional): Area threshold used for background removal
    
    Returns:
        str: Formatted result message
    """
    logger.info("Creating result message...")
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

