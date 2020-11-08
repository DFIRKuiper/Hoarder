import sys
import json
import parsers.UsnJrnl_parser.usn as usn
def write_entry(hOutFile , jEntry , DataType , DataPath ):
    data = {
        "Data" : jEntry, 
        "data_type" : DataType , 
        "data_source" : DataType , 
        "data_path" : DataPath
    }
    hOutFile.write(json.dumps(data) + "\n")

def imain(infile, outfile,parser, kuiper = False):
	try:
		res = usn.parserusn(infile)
		if kuiper:
			return [res]
		else:
			with open(outfile, 'w') as of:
				for i in [res]:
					write_entry(of , i , parser , infile)
			return outfile
	except Exception as e:
		raise e
		# exc_type, exc_obj, exc_tb = sys.exc_info()
		# msg = "[-] [Error] usnjrnl Parser: " + str(exc_obj) + " - Line No. " + str(exc_tb.tb_lineno)
		# if kuiper:
		# 	return (None , msg)

# def UsnJrnl_interface(file , parser):
#     try:
#         return_data = usn.parserusn(file)
#         return return_data

#     except Exception as e:
#         exc_type, exc_obj, exc_tb = sys.exc_info()
#         msg = "[-] [Error] " + parser + " Parser: " + str(exc_obj) + " - Line No. " + str(exc_tb.tb_lineno)
#         return (None , msg)