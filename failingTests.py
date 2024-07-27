from  pathlib import Path
from pprint import pprint

path = Path("allFailedTests.txt")
test_lines = path.read_text(encoding='utf-8').splitlines()



def get_failing_tests(lines):
    block = None
    for line in lines:     
    
        if 'RequestsReturningResult (1;' in line:
            if block is not None:
                yield  (''.join(block))
            block = []
            block.append(line)  
        else:
            pass
            #if block is not None:
             #   block.append(line)          
                
blocks = list(get_failing_tests(test_lines))    
blocks = [block for block in blocks if 'Unchanged' in block]   
blocks = [block.split(';') for block in blocks]   
blocks = [block[4] for block in blocks]   
pprint(blocks) 

