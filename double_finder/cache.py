import pathlib
import json


class PassThroughCache:
    def __init__(self, name) -> None:
        pass

    def lookup(self, key, toCall):
        return toCall()

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        pass


class Cache:
    def __init__(self, name) -> None:
        self._isDirty = False
        self._path = pathlib.Path(pathlib.Path(__file__).parent, f'{name}.cache.json')

        if self._path.exists():
            try:
                with self._path.open(mode='r', encoding='utf-8') as f:
                    self._innerCache = json.load(f)
                return
            except:
                pass

        self._innerCache = {}
       

    def add_result(self, *key_parts, value):
        key = self._make_key(*key_parts)
        self._innerCache[key] = value
        self._isDirty = True
        return value

    def _make_key(self, *key_parts):
        return ",".join(key_parts)

    def lookup(self, *key_parts, callIfMissing):
        key = self._make_key(*key_parts)

        if key in self._innerCache:
            return self._innerCache[key]
        else:
            new_entry = callIfMissing()
            self._innerCache[key] = new_entry
            self._isDirty = True
            return new_entry

    def __enter__(self):
        self._isDirty = False
        return self

    def __exit__(self, type, value, tb):
        if self._isDirty:
            with self._path.open(mode='w', encoding='utf-8') as f:
                json.dump(self._innerCache, f, indent=2)


class CacheGroup:
    def __init__(self, *names, factory = Cache) -> None:
        self._caches : dict[str, Cache] = {name: factory(name) for name in names}

    def __enter__(self):
        for cache in self._caches.values():
            cache.__enter__()
        return self

    def __exit__(self, type, value, tb):
        for cache in self._caches.values():
            cache.__exit__(type, value, tb)

    def __getitem__(self, name : str):
        return self._caches[name]
    
    def close_and_remove(self, name:str):
        item = self.__getitem__(name)
        item.__exit__(None, None, None)
        del self._caches[name]