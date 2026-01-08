import os
import glob
import json
from pprint import pprint

LAYERS_KEY = "layers"
LAYER_ID_KEY = "id"
LAYER_TYPE_KEY = "type"
PAINT_KEY = "paint"
FILL_COLOR_KEY = "fill-color"
LINE_WIDTH_KEY = "line-width"
LINE_DASH_ARRAY = "line-dasharray"


# Get all JSON style files from the current directory
style_folder = os.path.dirname(os.path.abspath(__file__))
style_files = glob.glob(os.path.join(style_folder, "*.json"))
style_files = list(
    filter(lambda f:  "bm_web_col_new" in str(os.path.basename(f)), style_files))


# Print all found style files
print(f"Found {len(style_files)} style file(s):")
for style_file in style_files:
    print(f"  - {os.path.basename(style_file)}")

# Extract paint properties from layers
for style_file in style_files:
    with open(style_file, 'r', encoding='utf-8') as f:
        try:
            content = json.load(f)
            print(f"\n{'=' * 60}")
            print(f"File: {os.path.basename(style_file)}")
            print('=' * 60)

            layer_names = map(lambda x: x[LAYER_ID_KEY], content[LAYERS_KEY])
            layer_names = sorted(
                layer_names, key=lambda s: len(s), reverse=True)

            # pprint(layer_names)

            def dash_fits(dash):
                if isinstance(dash, dict):
                    if 'stops' in dash:
                        interpolation = dash['stops']
                        return True
                return False

            if LAYERS_KEY in content:
                for layer in content[LAYERS_KEY]:
                   # if layer[LAYER_ID_KEY] == "Gewaesser_L_Durchlass_Dueker":

                        if PAINT_KEY in layer:
                            if LINE_DASH_ARRAY in layer[PAINT_KEY]:
                                dash = layer[PAINT_KEY][LINE_DASH_ARRAY]
                                if dash_fits(dash):
                                    print(f"{layer[LAYER_ID_KEY]} {dash}")

            else:
                print("No 'layers' key found in this file")

        except json.JSONDecodeError as e:
            print(f"\nError parsing {os.path.basename(style_file)}: {e}")
