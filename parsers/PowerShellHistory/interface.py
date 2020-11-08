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

def pshist(file):
    # Open the CSV
    try:
        f = open( file, 'r' )  
        # Change each fieldname to the appropriate field name. I know, so difficult.  
        data = []
        for l in f.readlines():
            data.append({"command" : l.strip()})
        return data
    except Exception as e:
        raise e

def imain(infile, outfile, parser, kuiper = False):
    try:
        res = pshist(infile)
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
        # msg = "[-] [Error] pshistory Parser: " + str(exc_obj) + " - Line No. " + str(exc_tb.tb_lineno)
        # print(msg)
        # print(traceback.format_exc())
        # if kuiper:
        #     return (None , msg)