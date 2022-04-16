import struct
import os
from datetime import datetime
from collections import namedtuple
from hashlib import *
import uuid
import array

def add(path, case_id, item_id):
    FORMAT_HEAD = struct.Struct("20s d 16s I 11s I")
    FORMAT_DATA = struct.Struct("14s")
    TUPLE_FOR_HEAD = namedtuple("Head", "hash timestamp case_id item_id state length")
    temp = []
    for i in item_id:
        for j in i:
            temp.append(j)
    item_id = temp
    case_id = case_id.replace("-", "")
    case_id = "".join(reversed([case_id[i:i+2] for i in range (0, len(case_id), 2)]))
    try:
        f = open(path, "r")
        f.close()
    except:
        head = FORMAT_HEAD.pack(*(str.encode(""), datetime.timestamp(datetime.now()), str.encode(""), 0, str.encode("INITIAL"), 14))
        data = FORMAT_DATA.pack((str.encode("Initial block")))
        with open(path, 'wb') as f:
            f.write(head + data)
    ids = []
    with open(path, "rb") as f:
        while True:
            try:
                head = TUPLE_FOR_HEAD._make(FORMAT_HEAD.unpack(f.read(68)))
                data = f.read(head.length)
                ids.append(head.item_id)
            except:
                break
    previous_hash = 0
    previous_hash = previous_hash.to_bytes(128, 'little')
    FORMAT_DATA = struct.Struct("0s")
    for item in item_id:
        if int(item) in ids:
            print("DUPLICATE FOUND!!")
            exit(1)
        timestamp = datetime.timestamp(datetime.now())
        state = "CHECKEDIN"
        data_length = 0
        head = FORMAT_HEAD.pack(*(previous_hash, timestamp, uuid.UUID(case_id).bytes, int(item), str.encode(state), data_length))
        data = FORMAT_DATA.pack(b'')
        combined = head + data
        previous_hash = sha1(combined).digest()

        with open(path, "ab") as f:
            f.write(head)
            f.write(data)
            