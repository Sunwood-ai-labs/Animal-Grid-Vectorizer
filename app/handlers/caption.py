"""
Image captioning handling functionality.
"""

import os
from utils.image_captioner import ImageCaptioner

def handle_caption_generation(image_paths, output_dir, api_key, model, prompt=None):
    """
    Handle Gemini caption generation process.
    
    Args:
        image_paths (list): List of paths to input images
        output_dir (str): Directory for output
        api_key (str): API key for Gemini
        model (str): Model name for Gemini
        prompt (str, optional): Prompt for caption generation
        
    Returns:
        list: Paths to processed images with captions as filenames
    """
    captioner = ImageCaptioner(api_key=api_key, model=model)
    
    captioned_dir = os.path.join(output_dir, "captioned")
    os.makedirs(captioned_dir, exist_ok=True)
    
    captioned_paths = []
    for img_path in image_paths:
        new_filename, _ = captioner.generate_filename(img_path, "animal", prompt)
        output_path = os.path.join(captioned_dir, new_filename)
        
        # Copy file
        with open(img_path, 'rb') as src_file:
            with open(output_path, 'wb') as dst_file:
                dst_file.write(src_file.read())
        captioned_paths.append(output_path)
    
    return captioned_paths if captioned_paths else image_paths
