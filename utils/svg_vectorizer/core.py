"""
Core SVG vectorization functionality.
"""

import os
import tempfile
import shutil
from PIL import Image
import vtracer
from loguru import logger
from .params import DEFAULT_PARAMS, validate_params

def convert_image_to_svg(input_path, output_path, params=None):
    """
    Convert an image to SVG format.

    Args:
        input_path (str): Path to input image
        output_path (str): Path for output SVG
        params (dict, optional): Conversion parameters
        
    Returns:
        str: Path to generated SVG file, or None on failure
    """
    # Validate input
    if not input_path or not os.path.exists(input_path):
        logger.error(f"Input file not found: {input_path}")
        return None

    # Set up parameters
    if params is None:
        params = DEFAULT_PARAMS.copy()
    else:
        # Validate parameters
        is_valid, error_msg = validate_params(params)
        if not is_valid:
            logger.error(f"Invalid parameters: {error_msg}")
            return None

    # Create temporary directory for processing
    temp_dir = tempfile.mkdtemp()
    temp_input = os.path.join(temp_dir, "temp_input.jpg")

    try:
        # Process input image
        logger.info(f"Processing input image: {input_path}")
        img = Image.open(input_path)

        # Save as temporary file
        img.save(temp_input, "JPEG")
        logger.info(f"Created temporary file: {temp_input}")

        # Get absolute paths
        abs_output_path = os.path.abspath(output_path)

        logger.info(f"Starting conversion... Input: {temp_input}, Output: {abs_output_path}")

        # Convert image to SVG using VTracer
        vtracer.convert_image_to_svg_py(
            temp_input,
            abs_output_path,
            # Color settings
            colormode=params['COLORMODE'],
            hierarchical=params['HIERARCHICAL'],
            
            # Tracing settings
            mode=params['MODE'],
            filter_speckle=params['FILTER_SPECKLE'],
            color_precision=params['COLOR_PRECISION'],
            layer_difference=params['LAYER_DIFFERENCE'],
            
            # Path settings
            corner_threshold=params['CORNER_THRESHOLD'],
            length_threshold=params['LENGTH_THRESHOLD'],
            max_iterations=params['MAX_ITERATIONS'],
            splice_threshold=params['SPLICE_THRESHOLD'],
            path_precision=params['PATH_PRECISION']
        )

        logger.info(f"Conversion complete: '{input_path}' → '{abs_output_path}'")
        return abs_output_path

    except Exception as e:
        logger.error(f"Error during conversion: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return None

    finally:
        # Clean up temporary directory
        try:
            shutil.rmtree(temp_dir)
            logger.info("Cleaned up temporary files")
        except Exception as e:
            logger.warning(f"Error cleaning up temporary files: {str(e)}")

def process_single_image(input_path, output_path=None, params=None):
    """
    Process a single image with optional parameter overrides.
    
    Args:
        input_path (str): Path to input image
        output_path (str, optional): Path for output SVG
        params (dict, optional): Parameter overrides
        
    Returns:
        str: Path to generated SVG file
    """
    # Generate output path if not provided
    if output_path is None:
        output_dir = os.path.dirname(input_path)
        filename = os.path.splitext(os.path.basename(input_path))[0]
        output_path = os.path.join(output_dir, f"{filename}.svg")

    # Merge with default parameters
    actual_params = DEFAULT_PARAMS.copy()
    if params:
        actual_params.update(params)

    return convert_image_to_svg(input_path, output_path, actual_params)
