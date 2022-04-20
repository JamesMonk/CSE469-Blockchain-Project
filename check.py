import traceback
import sys
import uuid
import struct
import hashlib
from datetime import *
from collections import namedtuple
from actions import *

from init import init

def set_block_tuple():
    head_format = struct.Struct('20s d 16s I 11s I')
    head = namedtuple('Header', 'sha1 timestamp case_id item_id state length')
    data = namedtuple('Data', 'data')
    return head_format, head, data

def get_timestamp():
    curr_time = datetime.now()
    timestamp = datetime.timestamp(curr_time)
    return timestamp, curr_time

def write_to_file(path, packed_head, packed_data):
    with open(path, 'ab') as f:
        f.write(packed_head)
        f.write(packed_data)

def printout(case_id, item_id, curr_time, str_check):
    
    print("Case:", str(uuid.UUID(bytes=case_id)))
    print("Checked in item:", item_id)
    print("\tStatus:", str_check)
    print("\tTime of action:", curr_time)

def block_structure(path, item_id, str_check):
    state = ''
    case_id = ''
    last_hash = b''
    data_val = b''
    
    head_format, head, data = set_block_tuple()
    with open(path, 'rb') as f:
        while True:
            try:
                block_size = head_format.size
                header_content = f.read(block_size)
                header = head._make(head_format.unpack_from(header_content))
                data_content = f.read(header.length)                
                last_hash = hashlib.sha1(header_content+data_content).digest()
                if item_id == header.item_id:
                    case_id = header.case_id
                    state = header.state
            except:
                break
    try:
        print(state)
        arg = state.decode('utf-8').rstrip('\x00')
        if (arg == "CHECKEDOUT" and str_check == "CHECKEDIN") or (arg == "CHECKEDIN" and str_check== "CHECKEDOUT"):
            timestamp, curr_time = get_timestamp()
            head_val = (last_hash, timestamp, case_id, item_id, str.encode(str_check), 0)
            
            data_format = struct.Struct('0s')
            
            packed_head = head_format.pack(*head_val)
            packed_data = data_format.pack(data_val)

            write_to_file(path, packed_head, packed_data)
            printout(case_id, item_id, curr_time, str_check)
        else:
            sys.exit(2)  # Remove de to Incorrect State
    except:
        sys.exit(3)  # Item ID not found

def checkin(item_id, path):
    init(path)
    str_check = "CHECKEDIN"
    block_structure(path, int(item_id[0]), str_check)
    

def checkout(item_id, path):
    str_check = "CHECKEDOUT"
    block_structure(path, int(item_id[0]), str_check)
