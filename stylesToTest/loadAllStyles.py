import os
import glob
import json

LAYERS_KEY = "layers"
LAYER_ID_KEY = "id"
LAYER_TYPE_KEY = "type"
PAINT_KEY = "paint"
FILL_COLOR_KEY = "fill-color"
LINE_WIDTH_KEY = "line-width"



# Get all JSON style files from the current directory
style_folder = os.path.dirname(os.path.abspath(__file__))
style_files = glob.glob(os.path.join(style_folder, "*.json"))
style_files = list(filter(lambda f:  "bm_web_col_new" in str(os.path.basename(f)), style_files))


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

            if LAYERS_KEY in content:
                for layer in content[LAYERS_KEY]:

                    if PAINT_KEY in layer:
                        if LINE_WIDTH_KEY in layer[PAINT_KEY]:
                            line_width = layer[PAINT_KEY][LINE_WIDTH_KEY]
                            if any(map(lambda x: isinstance(line_width, x), [int, float, str])):
                                layer_id = layer.get(LAYER_ID_KEY)
                                layer_type = layer.get(LAYER_TYPE_KEY)

                                print(
                                    f"\n{LAYERS_KEY}: {layer_id} (Type: {layer_type})")
                                print(
                                    f" {LINE_WIDTH_KEY}: {layer[PAINT_KEY][LINE_WIDTH_KEY]}")
            else:
                print("No 'layers' key found in this file")

        except json.JSONDecodeError as e:
            print(f"\nError parsing {os.path.basename(style_file)}: {e}")
