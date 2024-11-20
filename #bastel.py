from PIL import Image
import glob

# File paths
jpeg_files = sorted(glob.glob("path/to/jpegs/*.jpg"))
output_gif = "output.gif"

# Create a list of images
images = [Image.open(jpeg) for jpeg in jpeg_files]

# Save as GIF
images[0].save(output_gif, save_all=True, append_images=images[1:], duration=500, loop=0)