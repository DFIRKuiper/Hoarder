# Master parser allows calling all parsers in a moduler way by specifying:
# 1- The parser
# 2- The input file/folder
# 3- The output file

import argparse
import traceback
import pkgutil
import sys
import parsers
import os
import psutil
import json
# from Mapper import Mapper
import importlib
from Rhaegal.RhaegalLib import Event,Rhaegal
from DracarysLib import Dracarys,InitLogger
import zipfile

__version__ = "1.3"

# get the current path
def get_current_path():
	if hasattr(sys, 'frozen') and hasattr(sys, '_MEIPASS'):
		return sys._MEIPASS
	else:
		return os.getcwd()

def frozen_iter_imps():
	mods = set()
	for imp in pkgutil.iter_importers('parsers'):
		if hasattr(imp, 'toc'):
			for mod in imp.toc:
				if mod.startswith('parsers.'):
					mods.add(mod.split('.')[1])
	return list(mods)

def get_lparsers():
	parsers_list = {}

	# get the configuration information for all parsers
	for root, dirs, files in os.walk(os.path.join(get_current_path() , 'parsers')): 
		for d in dirs:

			# if starts with "_" (for __pycache__) or "." then skip the folder
			if d.startswith("_") or d.startswith("."):
				continue

			try:
				path = os.path.join(root, d) 
				with open(os.path.join(path , 'configuration.json') , 'r') as json_file:
					p_config = json.load(json_file)
					for c in p_config:
						if c['name'] in parsers_list.keys():
							raise Exception("duplicate parser ["+c['name']+"]")

						parsers_list[c['name']] = c
			except Exception as e:
				raise Exception("parser ["+d+"] failed getting parser information: " + str(e))
		break

	# get the modules for each parser
	if hasattr(sys, 'frozen') and hasattr(sys, '_MEIPASS'): # if running from frozen app
		for parser in parsers_list.keys():
			for imp in pkgutil.iter_importers('parsers'):
				if hasattr(imp, 'toc'):
					#imp.toc[]
					#for mod in imp.toc:
					#if mod.startswith('parsers.' + parsers_list[parser]['parser_folder']):
					parsers_list[parser]['parser_module'] = getattr(sys.modules["parsers."+parsers_list[parser]['parser_folder']+".interface"], "imain")
					
					if parsers_list[parser]['parser_module'] is None:
						raise Exception("Could not find the interface of parser (parsers." + parser + ".interface)")

	else: # if running from script
		for parser in parsers_list.keys():
			parsers_list[parser]['parser_module'] = getattr(sys.modules["parsers."+parsers_list[parser]['parser_folder']+".interface"], "imain")
			
			if parsers_list[parser]['parser_module'] is None:
				raise Exception("Could not find the interface of parser (parsers." + parser + ".interface)")

	return parsers_list



class MasterParser:
	parser_information = [] # this contains the parser information to be parsed (parser, inFile, outFile)

	def __init__(self, lparsers , priority=2 , inFile=None, outFile=None, Parser=None, parser_file=None, rulesPath=None):
		self.parsers_list 	= lparsers
		self.priority 		= priority

		# if parser information file provided then use it
		if parser_file is not None:
			if not os.path.exists(parser_file):
				raise Exception("File not found ("+inFile+") ")
			try:
				with open(parser_file , 'r') as pFile:
					parser_file_lines = pFile.readlines()
					for l in parser_file_lines:
						p = json.loads(l)
						if 'inFile' not in p.keys() or 'outFile' not in p.keys() or 'parser' not in p.keys():
							raise Exception("Invalid parser information, some of the keys not provided in record: " + l)
						
						if not os.path.exists(p["inFile"]):
							raise Exception("File not found ("+p["inFile"]+") ")
						elif p["parser"] not in self.parsers_list.keys():
							raise Exception("Invalid parser ("+p["parser"]+") ")
						self.parser_information.append( p )
			except Exception as e:
				raise Exception("Failed to read MasterParser parser configration file: " + parser_file + ", error: " + str(e))
					
		else:
			# if parser information file not provided then use the parameters (parser, inFile, outFile)
			self.parser_information.append({
				"parser" : Parser,
				"inFile" : inFile,
				"outFile": outFile
			})
			if not os.path.exists(inFile):
				raise Exception("File not found ("+inFile+") ")
			elif Parser not in self.parsers_list.keys():
				raise Exception("Invalid parser ("+Parser+") ")

		if len(self.parser_information) == 0:
			raise Exception("No parser information provided")
		
		
		# initiate Rhaegal object
		if rulesPath is not None:
			# if the rule files compressed in zip file
			if rulesPath.endswith(".zip"):
				with zipfile.ZipFile(rulesPath, 'r') as zip_ref:
					rulesPath = rulesPath.rstrip(".zip")
					zip_ref.extractall(rulesPath)
					

			self.enable_detection = True
			rhaegal = Rhaegal(rulesDir=rulesPath, logger=None )
			self.rd = Dracarys(rhaegal,None)
		else:
			self.enable_detection = False
			self.rd = None

		

		# Set Process Priority:
		p = psutil.Process(os.getpid())
		if priority == 1:
			p.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
		elif priority == 2:
			p.nice(psutil.IDLE_PRIORITY_CLASS)
		elif priority == 3:
			p.nice(psutil.NORMAL_PRIORITY_CLASS)
		elif priority == 4:
			p.nice(psutil.ABOVE_NORMAL_PRIORITY_CLASS)
		elif priority == 5:
			p.nice(psutil.HIGH_PRIORITY_CLASS)
		elif priority == 6:
			p.nice(psutil.REALTIME_PRIORITY_CLASS)
		else:
			raise ValueError("Invalid priority.")



	# this function run the interface of the parser
	def parse(self):
		for p in self.parser_information:
			# if folder of output file not exists, then create the file
			if not os.path.exists(os.path.dirname(p['outFile'])):
				os.makedirs(os.path.dirname(p['outFile']))
			# call parser interface
			output_file = self.parsers_list[p["parser"]]['parser_module'](p["inFile"], p["outFile"], p["parser"])

			# run the Rhaegal rules detection for output file
			if self.rd is not None:
				oFile = output_file if output_file is not None else p["outFile"]
				if os.path.exists(oFile):
					tmp_file = oFile + ".gh"
					# scan the file by rhaegal rules, and write the results to temp file
					with open(tmp_file , 'w') as tmp_file_handle:
						for rule, krecord, matchedStr in self.rd.Scan(oFile):
							tmp_file_handle.write( json.dumps(krecord.EventData) + "\n")
					
					# replace the tmp file with output file
					os.remove(oFile)
					os.rename(tmp_file, oFile)

				else:
					raise Exception("file to be scanned not found: " + oFile)

def main():
	try:
		# Get the list of available parsers:
		lparsers = get_lparsers()
		lparsers_names = []
		for pk in lparsers.keys():
			lparsers_names.append(pk)
	except Exception as e:
		print("Exception: failed getting parsers' modules [" + str(e) + "]\n" + traceback.format_exc())
		return 

	try:
		# Compose arguments:
		priority = """
				1: BELOW_NORMAL_PRIORITY_CLASS
				2: IDLE_PRIORITY_CLASS (default)
				3: NORMAL_PRIORITY_CLASS
				4: ABOVE_NORMAL_PRIORITY_CLASS
				5: HIGH_PRIORITY_CLASS
				6: REALTIME_PRIORITY_CLASS
				"""
		ap = argparse.ArgumentParser("Master Parser V" + __version__)
		ap.add_argument('-sp', '--set_priority', choices=[1, 2, 3, 4, 5, 6], default=2, type=int, help='Will run MasterParser process with the selected priority. ' + priority)
		ap.add_argument('-v', '--verbose', action="store_true", help='Enable verbose mode')
		ap.add_argument('-r', '--rulesPath', help='Folder path containing all Rhaegal rules')
		reqgrp = ap.add_argument_group("required arguments for single parser")
		reqgrp.add_argument('-p', dest='parser', help='Parser to use. Available parsers: ' + ', '.join(lparsers_names))
		reqgrp.add_argument('-i', dest='infile', help='input file/folder')
		reqgrp.add_argument('-o', dest='outfile', help='output file')
		
		reqgrp = ap.add_argument_group("required arguments for multiple parsers (provided by file)")
		reqgrp.add_argument('-pf', dest='parser_file', help='file containing the list of parsers, input files, output files')


		args = ap.parse_args()
		if args.infile is not None and args.outfile is not None and args.parser is not None:
			m = MasterParser(lparsers , inFile=args.infile, outFile=args.outfile, Parser=args.parser , priority=args.set_priority, rulesPath=args.rulesPath)
			m.parse()
		elif args.parser_file is not None:
			m = MasterParser(lparsers , priority=args.set_priority , parser_file=args.parser_file, rulesPath=args.rulesPath)
			m.parse()
		else:
			raise Exception("You have to provide parameter (parser_file) or (infile and outfile and parser)")

	except Exception as e:
		if args.verbose:
			print("Exception: failed parsing provided files [" + str(e) + "]\n" + traceback.format_exc())
		else:
			pass

if __name__ == "__main__":
	main()