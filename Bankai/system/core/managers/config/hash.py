import hashlib

def get_hash(str:str):
    str_hash = hashlib.md5(str.encode('utf-8')).hexdigest()[:6]
    return str_hash