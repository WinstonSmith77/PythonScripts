import json
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


def list_all_fonts(items):
    results = []
    if (any(isinstance(item, list) for item in fonts)):
        results.extend([str(fonts[3][1][0]), str(fonts[4][1][0])])
    else:
        results.extend        using System;
        using System.Numerics;
        using System.Text;
        
        static string ToBinaryString<T>(T value, int maxFractionBits = 32)
            where T : IFloatingPointIeee754<T>
        {
            if (T.IsNaN(value) || T.IsInfinity(value))
                throw new ArgumentOutOfRangeException(nameof(value));
        
            string sign = T.IsNegative(value) ? "-" : string.Empty;
            T absValue = T.Abs(value);
        
            T integerPartT = T.Truncate(absValue);
            T fractionPart = absValue - integerPartT;
        
            string integerBits = BuildIntegerBits(integerPartT);
            string fractionBits = BuildFractionBits(fractionPart, maxFractionBits);
        
            return sign + integerBits + fractionBits;
        }
        
        static string BuildIntegerBits<T>(T integerPartT)
            where T : IFloatingPointIeee754<T>
        {
            if (T.IsZero(integerPartT))
                return "0";
        
            BigInteger integerPart = BigInteger.CreateTruncating(integerPartT);
            var sb = new StringBuilder();
            while (integerPart > BigInteger.Zero)
            {
                sb.Insert(0, (integerPart & BigInteger.One) == BigInteger.Zero ? '0' : '1');
                integerPart >>= 1;
            }
            return sb.ToString();
        }
        
        static string BuildFractionBits<T>(T fractionPart, int maxFractionBits)
            where T : IFloatingPointIeee754<T>
        {
            if (maxFractionBits <= 0 || T.IsZero(fractionPart))
                return string.Empty;
        
            var sb = new StringBuilder(".");
            T two = T.CreateChecked(2);
        
            for (int i = 0; i < maxFractionBits; i++)
            {
                fractionPart *= two;
                if (fractionPart >= T.One)
                {
                    sb.Append('1');
                    fractionPart -= T.One;
                }
                else
                {
                    sb.Append('0');
                }
        
                if (T.IsZero(fractionPart))
                    break;
            }
        
            return sb.ToString();
        }
        
        // Usage
        Console.WriteLine(ToBinaryString<double>(0.4, 40));  // 0.0110011001100110011001100110011001100110
        Console.WriteLine(ToBinaryString<double>(6.4, 40));  // 110.0110011001100110011001100110011001100110(fonts)
    return results


allFonts = set()

style_folder = Path(__file__).parent
style_files = style_folder.glob("*.json")

style_files = [
    style_file for style_file in style_files if style_file.is_file and "" in str(style_file)]

print(f"Found {len(style_files)} style file(s):")
for style_file in style_files:
    print(f" {style_file.parts[-1]}", end='; ')
print(f"\n")


for style_file in style_files:
    try:
        with style_file.open() as f:
            content = json.load(f)
        print(f"\n{'=' * 60}")
        print(f"File: {style_file.parts[-1]}")
        print('=' * 60)

        layer_names = (layer[LAYER_ID_KEY] for layer in content[LAYERS_KEY])

        layer_names = sorted(
            layer_names, key=lambda s: len(s), reverse=True)

        # pprint(layer_names)

        if LAYERS_KEY in content:
            for layer in content[LAYERS_KEY]:
                if LAYOUT_KEY in layer and TEXT_FONT in layer[LAYOUT_KEY]:
                    fonts = layer[LAYOUT_KEY][TEXT_FONT]
                    print(f"{layer[LAYER_ID_KEY]} {fonts}", end='; ')
                    allFonts.update(list_all_fonts(fonts))

    except json.JSONDecodeError as e:
        print(f"\n\nError parsing {style_file.parent}: {e}")

print(f'\nAlle Fonts:\n')
for font in sorted(allFonts):
    print(font)
