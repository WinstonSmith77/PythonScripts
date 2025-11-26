import os
import glob
import json

# Get all JSON style files from the current directory
style_folder = os.path.dirname(os.path.abspath(__file__))
style_files = glob.glob(os.path.join(style_folder, "*.json"))
#style_files = list(filter(lambda f: 'neu' in str(os.path), style_files))

# Print all found style files 
print(f"Found {len(style_files)} style file(s):")
for style_file in style_files:
    print(f"  - {os.path.basename(style_file)}")

# Extract paint properties from layers
for style_file in style_files:
    with open(style_file, 'r', encoding='utf-8') as f:
        try:
            content = json.load(f)
            print(f"\n{'='*60}")
            print(f"File: {os.path.basename(style_file)}")
            print('='*60)
            
            if 'layers' in content:
                for layer in content['layers']:
                    layer_id = layer.get('id', 'unknown')
                    layer_type = layer.get('type', 'unknown')
                    
                    if 'paint' in layer:
                        if 'fill-color' in layer['paint']:
                            print(f"\nLayer: {layer_id} (Type: {layer_type})")
                           
                            print(f"  fill-color: {layer['paint']['fill-color']}")
            else:
                print("No 'layers' key found in this file")
                
        except json.JSONDecodeError as e:
            print(f"\nError parsing {os.path.basename(style_file)}: {e}")
