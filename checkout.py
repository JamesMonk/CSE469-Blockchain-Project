from common import block_structure

def checkout(item_id, path):
    str_check = "CHECKEDOUT"
    block_structure(path, int(item_id[0]), str_check)
