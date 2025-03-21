import numpy as np
from PIL import Image

# Create a sample grid image (3x6 grid)
img = np.ones((600, 1200, 3), dtype=np.uint8) * 255

# Add some colored rectangles to simulate animal illustrations
for r in range(3):
    for c in range(6):
        if (r+c) % 2 == 0:  # Checkerboard pattern
            # Create a colored rectangle
            img[r*200:(r+1)*200, c*200:(c+1)*200] = np.random.randint(100, 200, (200, 200, 3))

# Save the image
Image.fromarray(img.astype('uint8')).save('sample_grid.jpg')
print("Sample grid image created: sample_grid.jpg")
