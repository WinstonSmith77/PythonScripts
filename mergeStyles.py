from pathlib import Path
from pprint import pprint
import json


pathStyles = Path(r'C:\Users\henning\source\LinqScripts\stylesToTest')

styles = (list(pathStyles.glob("*.json")))

jsons = [json.loads(style.read_text(encoding="utf-8")) for style in styles]
layers = [style  for content in jsons for style in content['layers'] if 'filter' in style]


sorted(layers, key=lambda x: x['id'])



