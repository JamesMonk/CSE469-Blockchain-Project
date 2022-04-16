import struct
from datetime import datetime
from collections import namedtuple
from hashlib import *
def init(path):
    print("Initializing!!")
    FORMAT_HEAD = struct.Struct("20s d 16s I 11s I")
    FORMAT_DATA = struct.Struct("14s")
    TUPLE_FOR_HEAD = namedtuple("Head", "hash timestamp case_id item_id state length")
    try:
        f = open(path, "r")
        f.close()
        print("Block found")
    except:
        print("Block not found. Creating one")

        head = FORMAT_HEAD.pack(*(str.encode(""), datetime.timestamp(datetime.now()), str.encode(""), 0, str.encode("INITIAL"), 14))
        data = FORMAT_DATA.pack((str.encode("Initial block")))
        with open(path, 'wb') as f:
            f.write(head + data)
    try:
        with open(path, "rb") as f:
            head = TUPLE_FOR_HEAD._make(FORMAT_HEAD.unpack(f.read(68)))
            data = f.read(head.length)
    except:
        exit(1)
    if "INITIAL" in head.state.decode('utf-8'):
        exit(0)
    else:
        head = FORMAT_HEAD.pack(*(str.encode(""), datetime.timestamp(datetime.now()), str.encode(""), 0, str.encode("INITIAL"), 14))
        data = FORMAT_DATA.pack((str.encode("Initial block")))
        with open(path, 'wb') as f:
            f.write(head + data)