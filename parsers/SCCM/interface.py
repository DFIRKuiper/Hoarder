import sys
import json
import parsers.SCCM.sccmparser as sp
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
        res = sp.parse_sccm(infile)
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
        # msg = "[-] [Error] sccmparser Parser: " + str(exc_obj) + " - Line No. " + str(exc_tb.tb_lineno)
        # print(msg)
        # print(traceback.format_exc())
        # if kuiper:
        #     return (None , msg)

# import os
# import sys
# import subprocess
# import json
# import ast

# def auto_interface(file,parser):
#     try:
#         CurrentPath=os.path.dirname(os.path.abspath(__file__))
#         command = 'python3 "'+ CurrentPath+'/sccmparser.py" "' + file + '"'
#         proc = subprocess.Popen(command, shell=True ,stdout=subprocess.PIPE)
#         res = proc.communicate()[0].split('\n')

#         data = ""
#         for line in res:
#             if line.startswith('['):
#                 data += line
#         if data == "":
#             return []
#         d = []
#         for i in ast.literal_eval(data):
#             if type(i) == dict:
#                 if len(i.keys()):
#                     d.append(i)
#                 else:
#                     continue
#             else:
#                 d.append(json.loads(i) )
#         return d
#     except Exception as e:
#         exc_type,exc_obj,exc_tb = sys.exc_info()
#         msg = "[-] [Error] " + str(parser) + " Parser: " + str(exc_obj) + " - Line No. " + str(exc_tb.tb_lineno)
#         print msg
#         return (None , msg)

