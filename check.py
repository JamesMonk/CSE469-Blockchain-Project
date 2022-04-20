import sys
import uuid
import struct
import hashlib
from datetime import datetime
from collections import namedtuple

from init import init
from common import *

# def set_block_tuple():
#     head_format = struct.Struct('20s d 16s I 11s I')
#     head = namedtuple('Block_Head', 'hash timestamp case_id item_id state length')
#     data = namedtuple('Block_Data', 'data')
#     return head_format, head, data

# def get_timestamp():
#     curr_time = datetime.now()
#     timestamp = datetime.timestamp(curr_time)
#     return timestamp, curr_time

# def write_to_file(path, packed_head, packed_data):
#     with open(path, 'ab') as f:
#         f.write(packed_head)
#         f.write(packed_data)

# def printout(case_id, item_id, curr_time, str_check):
    
#     print("Case:", str(uuid.UUID(bytes=case_id)))
#     print("Checked in item:", item_id)
#     print("\tStatus:", str_check)
#     print("\tTime of action:", curr_time.strftime(
#         '%Y-%m-%dT%H:%M:%S.%f') + 'Z')

# def block_structure(path, item_id, str_check):
#     state = ''
#     case_id = ''
#     last_hash = b''
#     data_val = b''
    
#     head_format, head, data = set_block_tuple()
#     # print("before")
#     with open(path, 'rb') as f:
#         # print("after")
#         while True:
#             try:
                
#                 block_size = head_format.size
#                 content = f.read(block_size)
                
#                 unpack_head = head_format.unpack(content)
#                 curr_head = head._make(unpack_head)
                
#                 data_size = curr_head.length
#                 len_str = str(data_size) + 's'
#                 # print("HERE:", len_str)
#                 data_format = struct.Struct(len_str)
#                 data_content = f.read(data_size)
                
#                 unpack_data = data_format.unpack(data_content)
#                 curr_data = data._make(unpack_data)
                
#                 last_hash = hashlib.sha1(content+data_content).digest()
#                 # print("try")
#                 # print("item_id", item_id)
#                 # print("HERE", type(item_id))
#                 if item_id == curr_head.item_id:
#                     case_id = curr_head.case_id
#                     state = curr_head.state
#                     # print("Here:", state)
#             except:
#                 break
    
    
    
#     # print("HERE:", arg=="CHECKEOUT")
#     try:
#         arg = state.decode('utf-8').rstrip('\x00')
#         if (arg == "CHECKEDOUT" and str_check == "CHECKEDIN") or (arg == "CHECKEDIN" and str_check== "CHECKEDOUT"):
#             timestamp, curr_time = get_timestamp()
#             print("HERE: ", timestamp)
#             # print("HERE in Printout", arg)
#             head_val = (last_hash, timestamp, case_id, item_id, str.encode(str_check), 0)
            
#             data_format = struct.Struct('0s')
            
#             packed_head = head_format.pack(*head_val)
#             packed_data = data_format.pack(data_val)
#             unpack_head = head_format.unpack(packed_head)
#             curr_head = head._make(unpack_head)
#             unpack_data = data_format.unpack(packed_data)
#             curr_data = data._make(unpack_data)

#             write_to_file(path, packed_head, packed_data)
#             printout(case_id, item_id, curr_time, str_check)
#         else:
#             sys.exit(2)  # Remove de to Incorrect State
#     except:
#         sys.exit(3)  # Item ID not found

def checkin(item_id, path):
    to_initiate = init(path)
    str_check = "CHECKEDIN"
    block_structure(path, int(item_id[0]), str_check)
    

def checkout(item_id, path):
    str_check = "CHECKEDOUT"
    block_structure(path, int(item_id[0]), str_check)
