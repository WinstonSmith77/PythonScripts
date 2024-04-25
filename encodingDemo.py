from pprint import pprint

text = "Hänger am Škoda. Mit øl!"

def format_byte_array(bytes):
    if len(bytes) == 1:
        return hex(bytes[0])
    return [hex(c) for c in bytes]

output = [
            (c,
              format_byte_array(bytes(c, encoding = "cp1252")),
              format_byte_array(bytes(c, encoding = 'utf-8')),
              format_byte_array(bytes(c, encoding = "utf-16")[2:]),
            ) 
              
              for c in text]

for item in output:
    pprint(item)