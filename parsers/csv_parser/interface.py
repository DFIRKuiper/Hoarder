import csv  
import json  
import sys

def write_entry(hOutFile , jEntry , DataType , DataPath ):
    data = {
        "Data" : jEntry, 
        "data_type" : DataType , 
        "data_source" : DataType , 
        "data_path" : DataPath
    }
    hOutFile.write(json.dumps(data) + "\n")

def auto_csv_parser(file , parser):
	# Open the CSV  
	try:
		f = open( file, 'r' )  
		# Change each fieldname to the appropriate field name. I know, so difficult.  
		reader = csv.DictReader( f )  
		records = [ row for row in reader ]	
		return records
	except Exception as e:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		
		msg = "[-] [Error] " + parser + " Parser: " + str(exc_obj) + " - Line No. " + str(exc_tb.tb_lineno)
		print(msg)
		return (None , msg)

def imain(infile, outfile, parser, kuiper = False):
	try:
		res = auto_csv_parser(infile, "csvparser")
		if kuiper:
			return res
		else:
			with open(outfile, 'w') as of:
				for i in res:
					write_entry(of , j , parser , infile)
			return outfile
			
	except Exception as e:
		raise e
		# exc_type, exc_obj, exc_tb = sys.exc_info()
		# msg = "[-] [Error] jumplist Parser: " + str(exc_obj) + " - Line No. " + str(exc_tb.tb_lineno)
		# print(msg)
		# if kuiper:
		# 	return (None , msg)