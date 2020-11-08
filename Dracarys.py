from Rhaegal.RhaegalLib import Event,Rhaegal
import Rhaegal.RhaegalLib as RhaegalLib
import argparse
import logging
import time
import glob
import sys
import os
from DracarysLib import Dracarys,InitLogger
import json

__author__ = "AbdulRhman Alfaifi"
__version__ = "1.1"
__maintainer__ = "AbdulRhman Alfaifi"
__license__ = "GPL"
__status__ = "Development"                


if "__main__" == __name__:
    parser = argparse.ArgumentParser(description='Dracarys, Detect malicious activities using Rhaegal rules')
    parser.add_argument("-i","--input", help='Path that contains CSV,IIS logs or JSONL files to be parsed (Accept glob)',required=True)
    parser.add_argument("-rp","--rulesPath", help='Path that contains Rhaegal rules',required=True)
    parser.add_argument("--no-log", help='Do not create log file',action="store_true",default=False)
    parser.add_argument("--log-file", help='Log file path',default="Dracarys.log")
    parser.add_argument("--log-level",choices=['CRITICAL','ERROR','WARNING','INFO','DEBUG'], help='Logging level (Defaults to INFO)',default="INFO")
    parser.add_argument("-v","--version", help='Print version number',action="store_true",default=False)
    args = parser.parse_args()
    if args.version:
        print(f"Dracarys v{__version__}")
        print(f"RhaegalLib v{RhaegalLib.__version__}")
        sys.exit()
    if args.input:
        files = glob.glob(args.input, recursive=True)
    if not args.no_log:
        logger = InitLogger(logName=args.log_file,log_level=args.log_level)
    else:
        logger=None

    rhaegal = Rhaegal(rulesDir=args.rulesPath,logger=logger)

    
    mapper = None
    rd = Dracarys(rhaegal,mapper)

    for path in files:
        path = os.path.abspath(path)
        for rule, record, matchedStr in rd.Scan(path):
            print(json.dumps(record.EventData))
