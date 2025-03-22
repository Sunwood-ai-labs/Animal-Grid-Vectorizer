"""
Image refinement functionality.
"""

import os
import cv2
import numpy as np
from loguru import logger
from .splitter import create_output_directory

def refine_animal_illustrations(input_dir='split_animals', refined_dir='refined_animals'):
    """
    Refine the extracted animal illustrations by removing excess whitespace.

    Args:
        input_dir (str): Directory containing the initially split animal images
        refined_dir (str): Directory where refined animal images will be saved
    
    Returns:
        list: Paths to the refined animal images
    """
    # Create refined output directory
    refined_dir = create_output_directory(refined_dir)
    refined_paths = []

    # Process each file in the input directory
    for filename in os.listdir(input_dir):
        if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue

        file_path = os.path.join(input_dir, filename)
        
        try:
            # Read image
            img = cv2.imread(file_path)
            if img is None:
                logger.warning(f"Could not read image: {file_path}")
                continue

            # Process image
            refined_img = remove_excess_whitespace(img)
            
            # Save refined image
            refined_path = os.path.join(refined_dir, filename)
            cv2.imwrite(refined_path, refined_img)
            refined_paths.append(refined_path)
            logger.info(f"Refined: {refined_path}")
            
        except Exception as e:
            logger.error(f"Error processing {file_path}: {str(e)}")
            continue

    logger.info(f"Refinement complete. Images saved to {refined_dir}")
    return refined_paths

def remove_excess_whitespace(img, padding=10):
    """
    Remove excess whitespace around the main content of an image.
    
    Args:
        img (numpy.ndarray): Input image
        padding (int): Padding to add around content
        
    Returns:
        numpy.ndarray: Cropped image
    """
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply threshold to separate content from background
    _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return img

    # Find largest contour (assumed to be the main content)
    largest_contour = max(contours, key=cv2.contourArea)

    # Get bounding rectangle
    x, y, w, h = cv2.boundingRect(largest_contour)

    # Add padding
    x = max(0, x - padding)
    y = max(0, y - padding)
    w = min(img.shape[1] - x, w + 2 * padding)
    h = min(img.shape[0] - y, h + 2 * padding)

    # Crop image
    return img[y:y+h, x:x+w]

def calculate_content_bounds(gray_img, threshold=240):
    """
    Calculate content boundaries in grayscale image.
    
    Args:
        gray_img (numpy.ndarray): Grayscale image
        threshold (int): Brightness threshold
        
    Returns:
        tuple: (min_x, min_y, max_x, max_y)
    """
    # Create binary mask
    _, mask = cv2.threshold(gray_img, threshold, 255, cv2.THRESH_BINARY_INV)
    
    # Find non-zero points
    points = cv2.findNonZero(mask)
    
    if points is None:
        return None
        
    # Calculate bounds
    x, y, w, h = cv2.boundingRect(points)
    return (x, y, x + w, y + h)
