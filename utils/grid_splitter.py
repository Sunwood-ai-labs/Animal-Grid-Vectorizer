import cv2
import numpy as np
import os
from matplotlib import pyplot as plt

def create_output_directory(output_dir):
    """Create output directory if it doesn't exist."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")
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
    print(f"Reading image from: {image_path}")
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Could not read image from {image_path}")
        return extracted_paths

    # Convert to grayscale for processing
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Get image dimensions
    height, width = img.shape[:2]

    # Calculate the size of each cell in the grid
    cell_height = height // rows
    cell_width = width // cols

    # Extract and save each animal illustration
    count = 0
    for row in range(rows):
        for col in range(cols):
            # Calculate coordinates for current cell
            x1 = col * cell_width
            y1 = row * cell_height
            x2 = x1 + cell_width
            y2 = y1 + cell_height

            # Extract the region
            animal_img = img[y1:y2, x1:x2]

            # Check if the image contains significant content
            gray_animal = cv2.cvtColor(animal_img, cv2.COLOR_BGR2GRAY)
            if np.mean(gray_animal) > 240:  # Skip nearly blank images
                continue

            # Save the extracted animal
            count += 1
            output_path = os.path.join(output_dir, f"animal_{count:02d}.png")
            cv2.imwrite(output_path, animal_img)
            extracted_paths.append(output_path)
            print(f"Saved: {output_path}")

    print(f"Extraction complete. {count} animals extracted to {output_dir}")
    return extracted_paths

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
        if not filename.endswith(('.png', '.jpg', '.jpeg')):
            continue

        file_path = os.path.join(input_dir, filename)
        img = cv2.imread(file_path)

        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Apply threshold to separate animal from background
        _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)

        # Find contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            # Find the largest contour (assuming it's the animal)
            largest_contour = max(contours, key=cv2.contourArea)

            # Get bounding rectangle
            x, y, w, h = cv2.boundingRect(largest_contour)

            # Add some padding
            padding = 10
            x = max(0, x - padding)
            y = max(0, y - padding)
            w = min(img.shape[1] - x, w + 2 * padding)
            h = min(img.shape[0] - y, h + 2 * padding)

            # Crop the image
            cropped = img[y:y+h, x:x+w]

            # Save the refined image
            refined_path = os.path.join(refined_dir, filename)
            cv2.imwrite(refined_path, cropped)
            refined_paths.append(refined_path)
            print(f"Refined: {refined_path}")

    print(f"Refinement complete. Images saved to {refined_dir}")
    return refined_paths

def create_overview_image(refined_dir='refined_animals', overview_filename='overview.png'):
    """
    Create an overview image showing all processed animal illustrations in a grid.
    
    Args:
        refined_dir (str): Directory containing the refined animal images
        overview_filename (str): Filename for the overview image
    
    Returns:
        str: Path to the overview image
    """
    image_files = [f for f in os.listdir(refined_dir)
                  if f.endswith(('.png', '.jpg', '.jpeg'))]

    if not image_files:
        print(f"No images found in {refined_dir}")
        return None

    # Sort the files to display them in order
    image_files.sort()

    # Calculate grid dimensions
    n_images = len(image_files)
    grid_size = int(np.ceil(np.sqrt(n_images)))
    rows = cols = grid_size

    # Create the figure
    plt.figure(figsize=(15, 15))

    for i, filename in enumerate(image_files):
        if i >= rows * cols:
            break

        # Read the image
        img_path = os.path.join(refined_dir, filename)
        img = cv2.imread(img_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert from BGR to RGB for display

        # Add to plot
        plt.subplot(rows, cols, i + 1)
        plt.imshow(img)
        plt.title(filename)
        plt.axis('off')

    plt.tight_layout()
    overview_path = os.path.join(refined_dir, overview_filename)
    plt.savefig(overview_path)
    plt.close()
    print(f"Overview image saved to {overview_path}")
    return overview_path

def process_grid_image(image_path, output_base_dir='output', rows=3, cols=6):
    """
    Process a grid image by splitting, refining, and creating an overview.
    
    Args:
        image_path (str): Path to the input grid image
        output_base_dir (str): Base directory for all output
        rows (int): Number of rows in the grid
        cols (int): Number of columns in the grid
    
    Returns:
        dict: Dictionary containing paths to split images, refined images, and overview
    """
    # Create base output directory
    output_base_dir = create_output_directory(output_base_dir)
    
    # Create subdirectories
    split_dir = os.path.join(output_base_dir, 'split_animals')
    refined_dir = os.path.join(output_base_dir, 'refined_animals')
    
    # Process the image
    split_paths = split_animal_illustrations(image_path, split_dir, rows, cols)
    refined_paths = refine_animal_illustrations(split_dir, refined_dir)
    overview_path = create_overview_image(refined_dir)
    
    return {
        'split_paths': split_paths,
        'refined_paths': refined_paths,
        'overview_path': overview_path,
        'split_dir': split_dir,
        'refined_dir': refined_dir
    }
