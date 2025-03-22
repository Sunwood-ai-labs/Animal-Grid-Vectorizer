"""
Batch processing functionality for SVG vectorization.
"""

import os
import glob
from loguru import logger
from .core import convert_image_to_svg
from .params import DEFAULT_PARAMS

def batch_convert_folder(input_folder, output_folder, params=None):
    """
    Convert all images in a folder to SVG.

    Args:
        input_folder (str): Input directory containing images
        output_folder (str): Output directory for SVG files
        params (dict, optional): Conversion parameters
        
    Returns:
        list: Paths to generated SVG files
    """
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        logger.info(f"Created output folder: {output_folder}")

    # Image file extensions to process
    image_extensions = ('*.jpg', '*.jpeg', '*.png', '*.bmp', '*.tiff')

    # List for converted files
    converted_files = []

    # List all image files
    image_files = []
    for ext in image_extensions:
        image_files.extend(glob.glob(os.path.join(input_folder, ext)))
        image_files.extend(glob.glob(os.path.join(input_folder, ext.upper())))

    total_files = len(image_files)
    logger.info(f"Found {total_files} images to convert")

    # Process each image
    for i, img_path in enumerate(image_files, 1):
        # Generate output filename
        file_name = os.path.splitext(os.path.basename(img_path))[0]
        output_path = os.path.join(output_folder, f"{file_name}.svg")

        logger.info(f"Processing {i}/{total_files}: {img_path}")

        # Convert image to SVG
        result = convert_image_to_svg(img_path, output_path, params)
        if result:
            converted_files.append(result)

    logger.info(f"Batch processing complete. Success: {len(converted_files)}/{total_files}")
    return converted_files

def process_images_to_svg(image_paths, output_folder, params=None):
    """
    Convert multiple images to SVG.
    
    Args:
        image_paths (list): List of input image paths
        output_folder (str): Output directory for SVG files
        params (dict, optional): Conversion parameters
        
    Returns:
        list: Paths to generated SVG files
    """
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        logger.info(f"Created output folder: {output_folder}")
        
    converted_files = []
    total_files = len(image_paths)
    
    # Use default parameters if none provided
    if params is None:
        params = DEFAULT_PARAMS.copy()
    
    for i, img_path in enumerate(image_paths, 1):
        # Generate output filename
        file_name = os.path.splitext(os.path.basename(img_path))[0]
        output_path = os.path.join(output_folder, f"{file_name}.svg")

        logger.info(f"Processing {i}/{total_files}: {img_path}")

        # Convert image to SVG
        result = convert_image_to_svg(img_path, output_path, params)
        if result:
            converted_files.append(result)
            
    logger.info(f"Processing complete. Success: {len(converted_files)}/{total_files}")
    return converted_files
