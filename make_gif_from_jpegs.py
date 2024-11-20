from PIL import Image
import pathlib


# File paths

path = pathlib.Path("C:/Users/matze/Desktop/export/Kinder/hannes_spukt_feuer")


jpeg_files = list(path.rglob("*.jpg"))



output_gif = path / "output.gif"

# Create a list of images
images = [Image.open(jpeg) for jpeg in jpeg_files]

# Save as GIF
images[0].save(output_gif, save_all=True, append_images=images[1:], duration=100, loop=0)