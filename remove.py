
from common import block_structure

def remove(item_id, reason, file_path, owner):
    block_structure(file_path, int(item_id[0]), reason, owner)
