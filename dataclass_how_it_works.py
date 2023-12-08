import dataclasses
import json

_original_create_fn = dataclasses._create_fn

def _new_create_fn(name, args, body, **kwargs):
    args_str = ', '.join(args)
    body_str = '\n'.join('  ' + l for l in body)
    print(f'def {name}({args_str}):\n{body_str}\n')
    return _original_create_fn(name, args, body, **kwargs)

dataclasses._create_fn = _new_create_fn

@dataclasses.dataclass(frozen=True, order= True)
class Adress:
    Street: str
    ZipCode: int
    City : str

address = Adress("Zülpe", 56984, "Köln")    

@dataclasses.dataclass(frozen=True, order= True)
class User:
    Name: str
    Vorname: str
    Data : ()
    Adress : Adress
   
   
user = User('a', 'b', (56,  56, True), address)

print(hash(user))




# class EnhancedJSONEncoder(json.JSONEncoder):
#         def default(self, o):
#             if dataclasses.is_dataclass(o):
#                 dict = dataclasses.asdict(o)
#                 #dict['___dataClass___'] = None
#                 return dict
#             return super().default(o)

# dump = json.dumps(user, indent= 2)

# dedump =  json.loads(dump)

# print(dump)
# print(dedump)