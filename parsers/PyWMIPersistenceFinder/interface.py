
import parsers.PyWMIPersistenceFinder.PyWMIPersistenceFinder as pwf
import sys
import json
import traceback
def write_entry(hOutFile , jEntry , DataType , DataPath ):
    data = {
        "Data" : jEntry, 
        "data_type" : DataType , 
        "data_source" : DataType , 
        "data_path" : DataPath
    }
    hOutFile.write(json.dumps(data) + "\n")

def imain(infile, outfile, parser, kuiper = False):
	try:
		res = pwf.main(infile)
		if kuiper:
			return [res]
		else:
			with open(outfile, 'w') as of:
				for i in res:
					write_entry(of , i , parser , infile)
			return outfile
	except Exception as e:
		raise e
		# exc_type, exc_obj, exc_tb = sys.exc_info()
		# msg = "[-] [Error] wmipersistence Parser: " + str(exc_obj) + " - Line No. " + str(exc_tb.tb_lineno) + "\n" + traceback.format_exc()
		# if kuiper:
		# 	return (None , msg)