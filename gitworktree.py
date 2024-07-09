import pathlib
from pprint import pprint

path = pathlib.Path(r'C:\Users\henning\source\easymapGit')

for file in (path.rglob('*.*', case_sensitive=False)):
    if file.is_file():
        
        if not file.suffix:
            
            try:
                content = file.read_text(encoding='utf-8')
                if 'c:' in content.lower():
                    pprint((file, content))
                    
            except Exception:
               pass