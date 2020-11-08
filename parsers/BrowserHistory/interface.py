import os
import sys
import json
import parsers.BrowserHistory.BrowserHistory_ELK as bhe
import traceback

# this function used to write the entry in output file
def write_entry(hOutFile , jEntry , DataType , DataPath ):
    data = {
        "Data" : jEntry, 
        "data_type" : DataType , 
        "data_source" : DataType , 
        "data_path" : DataPath
    }
    hOutFile.write(json.dumps(data) + "\n")


def auto_browser_history(file):
	try:
		filename = os.path.basename(file)
		if filename == "History":
			h = bhe.extract_chrome_history(file)
		elif filename == "WebCacheV01.dat":
			h = bhe.extract_webcachev01_dat(file)
		elif filename == "places.sqlite":
			h = bhe.extract_firefox_history(file)
		else:
			h = []
		return h
		
	except Exception as e:
		raise e


def imain(infile, outfile, parser, kuiper = False):
	try:
		res = auto_browser_history(infile)
		if kuiper:
			return res
		else:
			with open(outfile, 'w') as of:
				for jentry in res:
					write_entry(of , jentry , parser , infile)
			return outfile

	except Exception as e:
		raise e
		# exc_type, exc_obj, exc_tb = sys.exc_info()
		# msg = "[-] [Error] browserhistory Parser: " + str(exc_obj) + " - Line No. " + str(exc_tb.tb_lineno)
		# print(msg)
		# print(traceback.format_exc())
		# if kuiper:
		# 	return (None , msg)
