import sys
import uuid
import struct
import hashlib
from datetime import datetime
from collections import namedtuple
from actions import *
def log(path="./output.txt", reverse=False, n=None, case_id=None, item_id=None):
    FORMAT_HEADER = struct.Struct("20s d 16s I 11s I")
    TUPLE_FOR_HEADER = namedtuple("header", "sha1 timestamp case_id item_id state length")
    blocks = []
    if n != None:
        n = int(n)
    with open(path, "rb") as f:
        while True:
            try:
                if n == 0 and n != None:
                    break
                header = TUPLE_FOR_HEADER._make(FORMAT_HEADER.unpack_from(f.read(68)))
                f.read(header.length)
                current_case_id = b''
                for i in range(0,len(header.case_id)):
                    current_case_id = bytes([header.case_id[i]]) + current_case_id
                if case_id and (uuid.UUID(bytes=current_case_id) != uuid.UUID(case_id)):
                    continue
                if item_id and int(header.item_id) != int(item_id[0]):
                    continue
                blocks.append([uuid.UUID(bytes=current_case_id), header.item_id, header.state.decode('utf-8').rstrip('\x00'), str(datetime.fromtimestamp(header.timestamp)).split()[0] + "T" + str(datetime.fromtimestamp(header.timestamp)).split()[1] + "Z"])
                if n != None:
                    n = n - 1
            except:
                break
        if reverse:
            for i in range(len(blocks)-1, -1, -1):
                print("Case:", blocks[i][0])
                print("Item:", blocks[i][1])
                print("Action:", blocks[i][2])
                print("Time:", blocks[i][3])
                print()
        else:
            for i in range(0, len(blocks)):
                print("Case:", blocks[i][0])
                print("Item:", blocks[i][1])
                print("Action:", blocks[i][2])
                print("Time:", blocks[i][3])
                print()