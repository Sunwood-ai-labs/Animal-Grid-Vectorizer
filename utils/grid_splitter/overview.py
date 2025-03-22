"""
Overview image generation functionality.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import cv2
from loguru import logger

def create_overview_image(refined_dir='refined_animals', overview_filename='overview.png'):
    """
    Create an overview image showing all processed animal illustrations in a grid.
    
    Args:
        refined_dir (str): Directory containing the refined animal images
        overview_filename (str): Filename for the overview image
    
    Returns:
        str: Path to the overview image
    """
    # Get list of image files
    image_files = [f for f in os.listdir(refined_dir)
                  if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    if not image_files:
        logger.warning(f"No images found in {refined_dir}")
        return None

    try:
        # Sort files for consistent display
        image_files.sort()

        # Calculate grid dimensions
        n_images = len(image_files)
        grid_size = int(np.ceil(np.sqrt(n_images)))
        rows = cols = grid_size

        # Create figure
        plt.figure(figsize=(15, 15))

        # Add each image to the grid
        for i, filename in enumerate(image_files):
            if i >= rows * cols:
                break

            # Read and process image
            img_path = os.path.join(refined_dir, filename)
            img = load_and_convert_image(img_path)

            if img is not None:
                # Add to plot
                plt.subplot(rows, cols, i + 1)
                plt.imshow(img)
                plt.title(filename)
                plt.axis('off')

        # Adjust layout and save
        plt.tight_layout()
        overview_path = os.path.join(refined_dir, overview_filename)
        plt.savefig(overview_path)
        plt.close()

        logger.info(f"Overview image saved to {overview_path}")
        return overview_path

    except Exception as e:
        logger.error(f"Error creating overview image: {str(e)}")
        return None

def load_and_convert_image(image_path):
    """
    Load and convert image for matplotlib display.
    
    Args:
        image_path (str): Path to image file
        
    Returns:
        numpy.ndarray: RGB image array or None on failure
    """
    try:
        # Read image
        img = cv2.imread(image_path)
        if img is None:
            logger.warning(f"Could not read image: {image_path}")
            return None

        # Convert from BGR to RGB
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    except Exception as e:
        logger.error(f"Error loading image {image_path}: {str(e)}")
        return None

def create_thumbnail(img, max_size=200):
    """
    Create thumbnail version of image.
    
    Args:
        img (numpy.ndarray): Input image
        max_size (int): Maximum dimension
        
    Returns:
        numpy.ndarray: Resized image
    """
    # Get current dimensions
    height, width = img.shape[:2]

    # Calculate new dimensions
    if height > width:
        new_height = max_size
        new_width = int(width * (max_size / height))
    else:
        new_width = max_size
        new_height = int(height * (max_size / width))

    # Resize image
    return cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)
