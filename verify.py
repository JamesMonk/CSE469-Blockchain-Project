# from sre_parse import State
import struct
from collections import namedtuple
from hashlib import *
from os.path import exists

def verify(path):
    FORMAT_HEADER = struct.Struct("20s d 16s I 11s I")
    FORMAT_DATA = struct.Struct("14s")
    TUPLE_FOR_HEADER = namedtuple("header", "sha1 timestamp case_id item_id state length")
    print("Verifying!!")
    ids = {}
    hashes = []
    success = True
    count = 0
    last_hash = None
    with open(path, "rb") as f:
        while True:
            try:
                header_bytes = f.read(68)
                header = TUPLE_FOR_HEADER._make(FORMAT_HEADER.unpack_from(header_bytes))
                data = f.read(header.length)
                state = header.state.decode('utf-8').rstrip('\x00')
                if state not in ["CHECKEDIN", "CHECKEDOUT", "DESTROYED", "DISPOSED", "RELEASED", "INITIAL"]:
                    success = False
                    exit(1)
                if state == "INITIAL" and data.decode('utf-8').rstrip('\x00') != "Initial block":
                    success = False
                    exit(1)
                if state == "RELEASED" and header.length == 0:
                    success = False
                    exit(1)  
                if (last_hash != None) and (header.sha1 != last_hash):
                    success = False
                    exit(1)
                if header.item_id in ids:
                    if state == "CHECKEDIN" and ids[header.item_id] == "CHECKEDIN":
                        success = False
                        exit(1)
                    if state == "CHECKEDOUT" and ids[header.item_id] == "CHECKEDOUT":
                        success = False
                        exit(1)
                    if state in ["DESTROYED", "DISPOSED", "RELEASED"] and ids[header.item_id] in ["DESTROYED", "DISPOSED", "RELEASED"]: 
                        success = False
                        exit(1)
                    if state in ["CHECKEDIN", "CHECKEDOUT"] and ids[header.item_id] in ["DESTROYED", "DISPOSED", "RELEASED"]: 
                        success = False
                        exit(1)
                else:
                    if state in ["DESTROYED", "DISPOSED", "RELEASED"]:
                        success = False
                        exit(1)

                count = 1
                ids[header.item_id] = state
                hashes.append(header.sha1)
                last_hash = sha1(header_bytes + data).digest()
                print()
            except:
                if success == False:
                    exit(1)
                if count == 0:
                    exit(1)
                break
