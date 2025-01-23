from PIL import Image
import pathlib
import pprint


# File paths

path = pathlib.Path("/Volumes/Matze/matze/Desktop/rutsche/")




jpeg_files = list(path.rglob("*.jpg"))
jpeg_files = sorted(jpeg_files, key=lambda item: item.name)
pprint.pprint(jpeg_files)
#first = jpeg_files[0]
#second = jpeg_files[1]
#jpeg_files = jpeg_files[2:] + [first, second, first, second,first, second, first, second, ]






output_gif = path / "output.gif"

# Create a list of images
images = [Image.open(files) for files in jpeg_files]

# Save as GIF
images[0].save(output_gif, save_all=True, append_images=images[1:], duration=150, loop=0)