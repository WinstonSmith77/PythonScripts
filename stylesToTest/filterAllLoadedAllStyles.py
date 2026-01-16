import glob
import json
from pprint import pprint
from pathlib import Path


LAYERS_KEY = "layers"
LAYER_ID_KEY = "id"
LAYER_TYPE_KEY = "type"
PAINT_KEY = "paint"
LAYOUT_KEY = "layout"
FILL_COLOR_KEY = "fill-color"
LINE_WIDTH_KEY = "line-width"
LINE_COLOR_KEY = "line-color"
LINE_DASH_ARRAY = "line-dasharray"
TEXT_FONT = "text-font"


def dash_fits(dash: dict | list):
    if isinstance(dash, dict):
        if 'stops' in dash:
            interpolation = dash['stops']
            found_near_zero = False
            for step in interpolation:
                found_near_zero |= any(True for x in step[1] if x < 0.01)
            if found_near_zero:
                return interpolation
    return False

def extractFonts(fonts: dict | list):
    pprint(fonts)
    result = [ str(fonts[3][1][0]), str(fonts[4][1][0])] 
    return result


allFonts = set()

def addFont(toAdd):
    allFonts.add(toAdd)




# Get all JSON style files from the current directory
style_folder = Path(__file__).parent
print(style_folder)
style_files = list(style_folder.glob("*.json"))

style_files = [
    style_file for style_file in style_files if style_file.is_file and "" in str(style_file)]

print(style_files)

# Print all found style files
print(f"Found {len(style_files)} style file(s):")
for style_file in style_files:
    print(f"  - {style_file.parts[-1]}")



# Extract paint properties from layers
for style_file in style_files:
    try:
        content = json.loads(style_file.read_text())
        print(f"\n{'=' * 60}")
        print(f"File: {style_file.parts[-1]}")
        print('=' * 60)

        layer_names = (x[LAYER_ID_KEY] for x in content[LAYERS_KEY])

        layer_names = sorted(
            layer_names, key=lambda s: len(s), reverse=True)

        # pprint(layer_names)

        if LAYERS_KEY in content:
            for layer in content[LAYERS_KEY]:

                if LAYOUT_KEY in layer:
                    if TEXT_FONT in layer[LAYOUT_KEY]:
                        fonts = layer[LAYOUT_KEY][TEXT_FONT]
                        print(f"{layer[LAYER_ID_KEY]} {fonts}")
                        for font in fonts:
                            if (isinstance(font, list)):
                               for fontInner in (extractFonts(fonts)):
                                   addFont(fontInner)
                                   continue
                            else:
                                addFont(font)

        else:
            print("No 'layers' key found in this file")
   

    except json.JSONDecodeError as e:
        print(f"\nError parsing {style_file.parent}: {e}")

pprint(allFonts)



