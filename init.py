import struct
from datetime import datetime
from collections import namedtuple
from hashlib import *
from os.path import exists
def init(path):
    print("Initializing!!")
    FORMAT_HEADER = struct.Struct("20s d 16s I 11s I")
    FORMAT_DATA = struct.Struct("14s")
    TUPLE_FOR_HEADER = namedtuple("header", "sha1 timestamp case_id item_id state length")
    TUPLE_FOR_DATA = namedtuple("Data", "data")
    
    if not exists(path):
        print("Block not found. Creating one")

        head = FORMAT_HEADER.pack(*(str.encode(""), datetime.timestamp(datetime.now()), str.encode(""), 0, str.encode("INITIAL"), 14))
        data = FORMAT_DATA.pack((str.encode("Initial block")))
        with open(path, 'wb') as f:
            f.write(head + data)
    try:
        with open(path, "rb") as f:
            head = TUPLE_FOR_HEADER._make(FORMAT_HEADER.unpack_from(f.read(68)))
            data = TUPLE_FOR_DATA._make(FORMAT_DATA.unpack_from(f.read(head.length)))
    except:
        exit(1)