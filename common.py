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


# def printout(case_id, item_id, curr_time, str_check):

#     print("Case:", str(uuid.UUID(bytes=case_id)))
#     print("Checked in item:", item_id)
#     print("\tStatus:", str_check)
#     print("\tTime of action:", curr_time.strftime(
#         '%Y-%m-%dT%H:%M:%S.%f') + 'Z')


# def print_remove(data_value, item_id, curr_time, str_check):
#     # print("HERE in print")
#     print("Removed item:", item_id)
#     print("\tStatus:", str_check)
#     print("\tOwner info:", data_value)
#     print("\tTime of action:", curr_time.strftime(
#                 '%Y-%m-%dT%H:%M:%S.%f') + 'Z')


def block_structure(path, item_id, str_check, own=False):
    state = ''
    case_id = ''
    last_hash = b''
    

    head_format, head, data = set_block_tuple()
    
    # print("before")
    with open(path, 'rb') as f:
        # print("after")
        while True:
            try:

                block_size = head_format.size
                content = f.read(block_size)

                unpack_head = head_format.unpack(content)
                curr_head = head._make(unpack_head)

                data_size = curr_head.length
                len_str = str(data_size) + 's'
                data_format = struct.Struct(len_str)
                data_content = f.read(data_size)

                unpack_data = data_format.unpack(data_content)
                curr_data = data._make(unpack_data)

                last_hash = hashlib.sha1(content+data_content).digest()
                if item_id == curr_head.item_id:
                    case_id = curr_head.case_id
                    state = curr_head.state
            except:
                break
    try:
        
        arg = state.decode('utf-8').rstrip('\x00')
        # print("arg:", str_check)
        if (arg == "CHECKEDOUT" and str_check == "CHECKEDIN") or (arg == "CHECKEDIN" and str_check == "CHECKEDOUT") or (arg == "CHECKEDIN" and not(str_check[0] not in ["DISPOSED", "DESTROYED", "RELEASED"])):
            if not(str_check[0] not in ["DISPOSED", "DESTROYED", "RELEASED"]):
                str_check = str_check[0]
            timestamp, curr_time = get_timestamp()
            
            if own:
                # print("Owner:", own)
                if str_check not in ["DISPOSED", "DESTROYED", "RELEASED"]:
                    sys.exit(2)

                data_val = " ".join(own)
                # print("IN if", data_val)

                head_val = (last_hash, timestamp, case_id,
                    item_id, str.encode(str_check), len(data_val)+1)
                
                block_data_format = struct.Struct(str(len(data_val)+1) + 's')
                
                # print(str(len(own)) + 's', data_val, len(data_val))

                packed_data = block_data_format.pack(
                    str.encode(data_val))
                
            else:
                
                data_val = b''
                head_val = (last_hash, timestamp, case_id,
                        item_id, str.encode(str_check), 0)
                # print("HERE in Printout", arg)
                data_format = struct.Struct('0s')
                packed_data = data_format.pack(data_val)
            
            packed_head = head_format.pack(*head_val)
            
            unpack_head = head_format.unpack(packed_head)
           
            curr_head = head._make(unpack_head)
            
            # unpack_data = data_format.unpack(packed_data)
            print("owner: ", own)
            # curr_data = data._make(unpack_data)
            
            write_to_file(path, packed_head, packed_data)
            # if not(str_check not in ["DISPOSED", "DESTROYED", "RELEASED"]):
                
            #     print_remove(data_val, item_id, curr_time, str_check)
            # else:
            #     printout(case_id, item_id, curr_time, str_check)
        else:
            sys.exit(2)  # Remove de to Incorrect State
            
    except:
        sys.exit(3)  # Item ID not found
        
    sys.exit(0)
