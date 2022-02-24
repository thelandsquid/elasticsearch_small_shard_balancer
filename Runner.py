from collections import defaultdict
from http.client import CONTINUE
import re
import random
import json
import argparse
import copy
from config.DataStore import DataStore

from ActiveShards import *
from modes.CommandLine import user_commands
from modes.GUI import GUI






def main():
    if args.cmd:
        user_commands()
    else:
        GUI()


parser = argparse.ArgumentParser(description='Output moves to balance shards')
parser.add_argument('-c', '--cmd', action='store_true', help='Use command line')

args = parser.parse_args()

main()