# from asyncio.windows_events import NULL
import struct
from datetime import datetime
from collections import namedtuple
from hashlib import *
import uuid
from os.path import exists

def add(path, case_id, item_id):
    FORMAT_HEADER = struct.Struct("20s d 16s I 11s I")
    FORMAT_DATA = struct.Struct("14s")
    TUPLE_FOR_HEADER = namedtuple("header", "sha1 timestamp case_id item_id state length")
    temp = []
    for i in item_id:
        for j in i:
            temp.append(j)
    item_id = temp

    # Remove dashes in case_id
    case_id = case_id.replace("-", "")

    # Reverse the case_id
    case_id = "".join(reversed([case_id[i:i+2] for i in range (0, len(case_id), 2)]))
    
    # If no block has been created, create one with an initial block
    if not exists(path):
        header = FORMAT_HEADER.pack(*(str.encode(""), datetime.timestamp(datetime.now()), str.encode(""), 0, str.encode("INITIAL"), 14))
        data = FORMAT_DATA.pack((str.encode("Initial block")))
        with open(path, 'wb') as f:
            f.write(header + data)
    
    ids = []
    # Save all previous item_ids to an array. Array will be used to see if new item_ids are duplicates of old ones 
    previous_hash = 0
    previous_hash = previous_hash.to_bytes(128, 'little')
    with open(path, "rb") as f:
        while True:
            try:
                header_content = f.read(68)
                header = TUPLE_FOR_HEADER._make(FORMAT_HEADER.unpack_from(header_content))
                data = f.read(header.length)
                if header.state.decode('utf-8').rstrip('\x00') == "INITIAL":
                    previous_hash = sha1(header_content+data).digest()
                ids.append(header.item_id)
            except:
                break
    FORMAT_DATA = struct.Struct("0s")
    for item in item_id:
        if int(item) in ids:
            print("DUPLICATE FOUND!!")
            exit(1)
        timestamp = datetime.timestamp(datetime.now())
        state = "CHECKEDIN"
        data_length = 0
        header = FORMAT_HEADER.pack(*(previous_hash, timestamp, uuid.UUID(case_id).bytes, int(item), str.encode(state), data_length))
        data = FORMAT_DATA.pack(b'')
        combined = header + data
        previous_hash = sha1(combined).digest()
        
        with open(path, "ab") as f:
            f.write(header)
            f.write(data)
            