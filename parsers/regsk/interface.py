import sys
import os
import json
import parsers.regsk.regsk as rs
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
        #res = rs.main(infile)
        res = rs.get_single_plugin(infile,  parser)
        if kuiper:
            res
        else:
            # regskewer is a special case where multiple results are returned for each plugin:
            # looping all results:
            
            uniq = 0
            plofile = os.path.join(os.path.dirname(outfile), \
                    (parser + '_' + os.path.splitext(os.path.basename(outfile))[0] +\
                    '_' + str(uniq) + '_' + os.path.splitext(os.path.basename(outfile))[1]))

            uniq += 1
            with open(plofile, 'w') as of:
                if res is not None:
                    for i in res:
                        write_entry(of , i , parser , infile)
                return plofile
    except Exception as e:
        raise e
        # exc_type, exc_obj, exc_tb = sys.exc_info()
        # msg = "[-] [Error] regsk Parser: " + str(exc_obj) + " - Line No. " + str(exc_tb.tb_lineno)
        # print(msg)
        # print(traceback.format_exc())
        # if kuiper:
        #     return (None , msg)