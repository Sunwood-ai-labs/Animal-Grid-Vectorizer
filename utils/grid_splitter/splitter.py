"""
Grid splitting functionality.
"""

import os
import cv2
import numpy as np
from loguru import logger

def create_output_directory(output_dir):
    """
    Create output directory if it doesn't exist.
    
    Args:
        output_dir (str): Path to output directory
        
    Returns:
        str: Path to created directory
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        logger.info(f"Created output directory: {output_dir}")
    return output_dir

def split_animal_illustrations(image_path, output_dir='split_animals', rows=3, cols=6):
    """
    Split a grid of animal illustrations into individual images.

    Args:
        image_path (str): Path to the input image with multiple animal illustrations
        output_dir (str): Directory where individual animal images will be saved
        rows (int): Number of rows in the grid
        cols (int): Number of columns in the grid
    
    Returns:
        list: Paths to the extracted animal images
    """
    # Create output directory
    output_dir = create_output_directory(output_dir)
    extracted_paths = []

    # Read the image
    logger.info(f"Reading image from: {image_path}")
    img = cv2.imread(image_path)
    if img is None:
        logger.error(f"Could not read image from {image_path}")
        return extracted_paths

    # Convert to grayscale for processing
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Get image dimensions
    height, width = img.shape[:2]

    # Calculate cell dimensions
    cell_height = height // rows
    cell_width = width // cols

    # Extract each cell
    count = 0
    for row in range(rows):
        for col in range(cols):
            # Calculate coordinates
            x1 = col * cell_width
            y1 = row * cell_height
            x2 = x1 + cell_width
            y2 = y1 + cell_height

            # Extract the region
            cell_img = img[y1:y2, x1:x2]

            # Check if cell contains significant content
            gray_cell = cv2.cvtColor(cell_img, cv2.COLOR_BGR2GRAY)
            if np.mean(gray_cell) > 240:  # Skip nearly blank cells
                logger.debug(f"Skipping blank cell at row {row+1}, col {col+1}")
                continue

            # Save the extracted image
            count += 1
            output_path = os.path.join(output_dir, f"animal_{count:02d}.png")
            cv2.imwrite(output_path, cell_img)
            extracted_paths.append(output_path)
            logger.info(f"Saved: {output_path}")

    logger.info(f"Extraction complete. {count} images extracted to {output_dir}")
    return extracted_paths

def is_blank_image(image, threshold=240):
    """
    Check if an image is mostly blank (white).
    
    Args:
        image (numpy.ndarray): Image array
        threshold (int): Brightness threshold (0-255)
        
    Returns:
        bool: True if image is mostly blank
    """
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    return np.mean(gray) > threshold
