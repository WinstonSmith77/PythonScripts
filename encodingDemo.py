from pprint import pprint

text = "Hänger am Škoda. Mit øl! 早上好"


def format_byte_array(bytes_to_encode, encoding):
    try:
        encoded = bytes(bytes_to_encode, encoding)
        if len(encoded) == 1:
            return hex(encoded[0])
        return [hex(c) for c in encoded]
    except UnicodeEncodeError:
        return "ERROR"


output = [
    (
        c,
        format_byte_array(c, encoding="cp1252"),
        format_byte_array(c, encoding="utf-8"),
        format_byte_array(c, encoding="utf-16"),
    )
    for c in text
]

for item in output:
    pprint(item)
