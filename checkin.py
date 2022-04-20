from init import init
from common import block_structure

def checkin(item_id, path):
    to_initiate = init(path)
    str_check = "CHECKEDIN"
    block_structure(path, int(item_id[0]), str_check)
