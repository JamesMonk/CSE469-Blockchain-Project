from datetime import *
from collections import namedtuple

from init import init
from common import *

def checkin(item_id, path):
    init(path)
    str_check = "CHECKEDIN"
    block_structure(path, int(item_id[0]), str_check)
    

def checkout(item_id, path):
    str_check = "CHECKEDOUT"
    block_structure(path, int(item_id[0]), str_check)
