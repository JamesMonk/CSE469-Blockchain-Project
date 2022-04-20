from collections import namedtuple
import datetime
import hashlib
import struct
import sys



def set_block_tuple():
    head_format = struct.Struct('20s d 16s I 11s I')
    head = namedtuple(
        'Block_Head', 'hash timestamp case_id item_id state length')
    data = namedtuple('Block_Data', 'data')
    return head_format, head, data


def get_timestamp():
    curr_time = datetime.datetime.now()
    timestamp = datetime.datetime.timestamp(curr_time)
    return timestamp, curr_time


def write_to_file(path, packed_head, packed_data):
    with open(path, 'ab') as f:
        f.write(packed_head)
        f.write(packed_data)


def block_structure(path, item_id, str_check, own=False):
    state = ''
    case_id = ''
    last_hash = b''
    

    head_format, head, data = set_block_tuple()
    
    with open(path, 'rb') as f:
        while True:
            try:
                block_size = head_format.size
                header_bytes = f.read(block_size)
                unpack_head = head_format.unpack(header_bytes)
                header = head._make(unpack_head)
                data_size = header.length
                data_bytes = f.read(data_size)
                last_hash = hashlib.sha1(header_bytes+data_bytes).digest()
                if item_id == header.item_id:
                    case_id = header.case_id
                    state = header.state
            except:
                break
    try:
        
        arg = state.decode('utf-8').rstrip('\x00')
        if (arg == "CHECKEDOUT" and str_check == "CHECKEDIN") or (arg == "CHECKEDIN" and str_check == "CHECKEDOUT") or (arg == "CHECKEDIN" and not(str_check[0] not in ["DISPOSED", "DESTROYED", "RELEASED"])):
            if not(str_check[0] not in ["DISPOSED", "DESTROYED", "RELEASED"]):
                str_check = str_check[0]
            timestamp, curr_time = get_timestamp()
            
            if own:
                if str_check not in ["DISPOSED", "DESTROYED", "RELEASED"]:
                    sys.exit(2)

                data_val = " ".join(own)

                head_val = (last_hash, timestamp, case_id,
                    item_id, str.encode(str_check), len(data_val)+1)
                
                block_data_format = struct.Struct(str(len(data_val)+1) + 's')
                
                packed_data = block_data_format.pack(
                    str.encode(data_val))
                
            else:
                
                data_val = b''
                head_val = (last_hash, timestamp, case_id,
                        item_id, str.encode(str_check), 0)
                data_format = struct.Struct('0s')
                packed_data = data_format.pack(data_val)
            
            packed_head = head_format.pack(*head_val)
            
            write_to_file(path, packed_head, packed_data)
        else:
            sys.exit(2)  # Remove de to Incorrect State
            
    except:
        sys.exit(3)  # Item ID not found
        
    sys.exit(0)
