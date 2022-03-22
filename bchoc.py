import argparse
import os
from add import add
from checkout import checkout
from checkin import checkin
from log import log
from remove import remove
from init import init
from verify import verify
def syntax_error(reason):
    print("SYNTAX ERROR!! Cause:", reason+ ". Use \"-h\" to see usage information")
    # print("")
    exit(1)

parser = argparse.ArgumentParser()
parser.add_argument("action", help="The action you want to perform: [add, checkout, checkin, log, remove, init, verify]")
parser.add_argument("-c", help="case id")
parser.add_argument("-i", nargs="+", help="item id")
parser.add_argument("-r", "--reverse", action="store_true", help="reverse log order")
parser.add_argument("-n", help="number of items to log")
parser.add_argument("-y", "--why", nargs="+", help="why are you removing a block")
parser.add_argument("-o", nargs="+", help="owner")
args = parser.parse_args()

path = os.getenv("BCHOC_FILE_PATH")

if args.action:
    if args.action == "add":
        if not args.c:
            syntax_error("missing case_id")
        if not args.i:
            syntax_error("missing item_id")
        add(path, args.c, args.i)
    
    elif args.action == "checkout":
        if not args.i:
            syntax_error("missing item_id")
        if len(args.i) != 1:
            print("[note] only first item id will be checked out")
        checkout(args.i[0])
        
    elif args.action == "checkin":
        if not args.i:
            syntax_error("missing item_id")
        if len(args.i) != 1:
            print("[note] only first item id will be checked in")
        checkin(args.i[0])

    elif args.action == "log":
        log(args.reverse, args.n, args.c, args.i[0])

    elif args.action == "remove":
        if not args.i:
            syntax_error("missing item_id")
        if not args.why:
            syntax_error("missing reason")
        if len(args.i) != 1:
            print("[note] only first item id will be removed")
        why = ""
        for word in args.why:
            why += word + " "
        why = why[:-1]
        owner = ""
        for word in args.o:
            owner += word + " "
        owner = owner[:-1]
        remove(args.i[0], why, owner)

    elif args.action == "init":
        init()

    elif args.action == "verify":
        verify()
    
    else:
        syntax_error("unrecognized action \"" + args.action + "\"")
    

