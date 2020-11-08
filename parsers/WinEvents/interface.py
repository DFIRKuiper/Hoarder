import os
import subprocess
import json 
import sys
import evtx
import glob
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
        with open(outfile, 'w') as of:
            files = []
            if os.path.isdir(infile):
                files = glob.glob(infile + '/**/*.evtx', recursive=True)
            else:
                files.append(infile)
            for file in files:
                rec_parser = evtx.PyEvtxParser(file)
                for record in rec_parser.records_json():
                    res = process_event(record["data"].strip())
                    res["event_record_id"] = record["event_record_id"]
                    write_entry(of , res , parser , file)
        return outfile
        
    except Exception as e:
        if kuiper:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            msg = "[-] [Error] winevents Parser: " + str(exc_obj) + " - Line No. " + str(exc_tb.tb_lineno)
            return (None , msg)
        else:
            raise e

def delete_null(json):
    
    if isinstance( json , dict ):
        for j in json.keys():
            if json[j] is None:
                del json[j]
                continue
            delete_null(json[j])

def remove_attributes_field(json):
    if not isinstance(json , dict):
        return json

    if "#text" in json.keys() and isinstance(json['#text'] , list):
        try:
            json['#text'] = '\n'.join(  json['#text'] )
        except Exception as e:
            pass
    # rename  the #attributes to @ + attr name 
    if "#attributes" in json.keys():
        for attr in json["#attributes"].keys():
            json["@"+attr] = json["#attributes"][attr]
        del json["#attributes"]
    
    for i in json.keys():
        # if there is a . in the field name, replace it with "_"
        remove_attributes_field(json[i])
        if i.find(".") != -1:
            json[i.replace("." , "_")] = json[i]
            del json[i]
    return json

def process_event(event):
    if event == '':
        return {}
    rec = json.loads(event)

    # set @timestamp
    try:
        rec['@timestamp'] = rec['Event']['System']['TimeCreated']['#attributes']['SystemTime']
    except Exception as e:
        rec['@timestamp'] = "1700-01-01T00:00:00"
        
    # fix the event id issue
    if type(rec['Event']['System']['EventID']) == int:
        rec['Event']['System']['EventID'] = {'#text' : rec['Event']['System']['EventID']}

    # fix the correlation issue
    if 'Correlation' in rec['Event']['System'].keys():
        if rec['Event']['System']['Correlation'] is None:
            del rec['Event']['System']['Correlation']

    # fix the EventData null value 
    if 'EventData' in rec['Event']:
        if rec['Event']['EventData'] is None:
            del rec['Event']['EventData']

    # if the Data field string, change the field name to DataText
    # some records have Data as json and some has text, which confuse elasticsearch
    if 'EventData' in rec['Event']:
        if 'Data' in rec['Event']['EventData']:
            if isinstance(rec['Event']['EventData']['Data'] , str):
                rec['Event']['EventData']['DataText'] = rec['Event']['EventData']['Data']
                del rec['Event']['EventData']['Data']

    # this will delete all fields of null value to avoid issue on data field mapping 
    # delete_null(rec['Event'])
    remove_attributes_field(rec)
    return rec