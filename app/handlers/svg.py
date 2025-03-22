"""
SVG handling functionality.
"""

import os
import zipfile
from loguru import logger
from utils.svg_vectorizer import process_images_to_svg
from utils.background_removal import find_and_remove_large_paths
from utils.grid_splitter import create_grid_layout

def handle_svg_conversion(image_paths, output_dir, svg_params, remove_rectangle=False, 
                        area_threshold=0.9, grid_display=True, rows=3, cols=6):
    """
    Handle SVG conversion process.
    
    Args:
        image_paths (list): List of paths to input images
        output_dir (str): Directory for output SVG files
        svg_params (dict): SVG conversion parameters
        remove_rectangle (bool): Whether to remove background from SVGs
        area_threshold (float): Area ratio threshold for background detection
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

def create_svg_grid(svg_files, rows, cols, output_dir):
    """
    Create a single SVG file with grid layout.
    
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
