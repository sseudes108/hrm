import hashlib

def get_hash_key(id1:str, id2:str):
    id2_hash = hashlib.md5(id2.encode('utf-8')).hexdigest()[:6]
    key = f"{id1}_{id2_hash}"
    return key

def get_hash(str:str):
    str_hash = hashlib.md5(str.encode('utf-8')).hexdigest()[:6]
    return str_hash