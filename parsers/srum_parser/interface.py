import sys
import json
import parsers.srum_parser.srum as sr
import traceback
def write_entry(hOutFile , jEntry , DataType , DataPath ):
    data = {
        "Data" : jEntry, 
        "data_type" : DataType , 
        "data_source" : DataType , 
        "data_path" : DataPath
    }
    hOutFile.write(json.dumps(data) + "\n")

def SRUM_interface(file, parser):
	try:
		srum_obj = sr.SRUM_Parser(file)
		return_data = []
		if srum_obj.ApplicationResourceUsage is not None:
			return_data += srum_obj.ApplicationResourceUsage
		if srum_obj.ApplicationResourceUsage is not None:
			return_data += srum_obj.NetworkDataUsageMonitor
		if srum_obj.ApplicationResourceUsage is not None:
			return_data += srum_obj.NetworkConnectivityUsageMonitor
		return return_data

	except Exception as e:
		raise e

def imain(infile, outfile, parser, kuiper = False):
	try:
		res = SRUM_interface(infile, "SRUM")
		if kuiper:
			return res
		else:
			with open(outfile, 'w') as of:
				for i in res:
					write_entry(of , i , parser , infile)
			return outfile
	except Exception as e:
		raise e
		# exc_type, exc_obj, exc_tb = sys.exc_info()
		# msg = "[-] [Error] SRUM Parser: " + str(exc_obj) + " - Line No. " + str(exc_tb.tb_lineno)
		# print(msg)
		# print(traceback.format_exc())
		# if kuiper:
		# 	return (None , msg)