import os
import sys
import json
import subprocess
import platform
from mft import PyMftParser, PyMftAttributeX10, PyMftAttributeX30, PyMftAttributeX90, PyMftAttributeX80, PyMftAttributeOther

def write_entry(hOutFile , jEntry , DataType , DataPath ):
    data = {
        "Data" : jEntry, 
        "data_type" : DataType , 
        "data_source" : DataType , 
        "data_path" : DataPath
    }
    hOutFile.write(json.dumps(data) + "\n")


def imain(infile, outfile , parser, mapper=None, kuiper = False):
    try:
        # init parser
        MFTParser = PyMftParser(infile)

        with open(outfile, 'w') as of:
            for entry in MFTParser.entries():
                # check if runtime error:
                if isinstance(entry, RuntimeError):
                    continue
                
                # empty field
                if entry.full_path == '[Unknown]':
                    continue
                    
                
                entry_dict = {}
                entry_dict["EntryId"]             = entry.entry_id
                entry_dict["Sequence"]          = entry.sequence
                entry_dict["BaseEntryId"]       = entry.base_entry_id
                entry_dict["BaseEntrySequence"] = entry.base_entry_sequence
                entry_dict["HardLinkCount"]     = entry.hard_link_count
                entry_dict["Flags"]             = entry.flags
                entry_dict["UsedEntrySize"]     = entry.used_entry_size
                entry_dict["TotalEntrySize"]    = entry.total_entry_size
                entry_dict["FullPath"]          = entry.full_path
                entry_dict["SIFlags"]           = ""
                entry_dict["SILastModified"]    = "1970-01-01T00:00:00.000000Z"
                entry_dict["SILastAccess"]      = "1970-01-01T00:00:00.000000Z"
                entry_dict["SICreated"]         = "1970-01-01T00:00:00.000000Z"
                entry_dict["SIMFTModified"]     = "1970-01-01T00:00:00.000000Z"
                # loop attributes:
                for attribute in entry.attributes():
                    # check if runtime error:
                    if isinstance(attribute, RuntimeError):
                        continue

                    # get resident content:
                    resident = attribute.attribute_content
                    if resident:
                        if isinstance(resident, PyMftAttributeX10): #SI
                            entry_dict["SIFlags"]               = resident.file_flags
                            entry_dict["SILastModified"]        = resident.modified.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                            entry_dict["SILastAccess"]          = resident.accessed.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                            entry_dict["SICreated"]             = resident.created.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                            entry_dict["SIMFTModified"]         = resident.mft_modified.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                        if isinstance(resident, PyMftAttributeX30) and 'parent_entry_sequence' not in entry_dict.keys(): #FN
                            # the check for parent_entry_sequence to see if the FN record stored before, this will take only the first FN attribute
                            entry_dict["IsADirectory"]          = "TRUE" if "FILE_ATTRIBUTE_IS_DIRECTORY" in resident.flags else "FALSE"
                            entry_dict["IsHidden"]              = "TRUE" if "FILE_ATTRIBUTE_HIDDEN" in resident.flags else "FALSE"

                            entry_dict["FileSize"]              = resident.logical_size

                            entry_dict["parent_entry_sequence"] = resident.parent_entry_sequence
                            entry_dict["parent_entry_id"]       = resident.parent_entry_id
                            
                            entry_dict["FNFlags"]               = resident.flags
                            entry_dict["FNLastModified"]        = resident.modified.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                            entry_dict["FNLastAccess"]          = resident.accessed.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                            entry_dict["FNCreated"]             = resident.created.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                            entry_dict["FNMFTModified"]         = resident.mft_modified.strftime("%Y-%m-%dT%H:%M:%S.%fZ")



                if "FNFlags" not in entry_dict.keys():
                    entry_dict["FNFlags"]           = ""
                    entry_dict["FNLastModified"]    = entry_dict["SILastModified"]
                    entry_dict["FNLastAccess"]      = entry_dict["SILastAccess"]
                    entry_dict["FNCreated"]         = entry_dict["SICreated"]
                    entry_dict["FNMFTModified"]     = entry_dict["SIMFTModified"]
                    entry_dict["IsADirectory"]      = "FALSE"
                if "FileSize" not in entry_dict.keys():
                    entry_dict["FileSize"] = "-1" # non-resident
                entry_dict["@timestamp"] = entry_dict["FNCreated"]
                
                write_entry(of , entry_dict , parser , infile)
        return outfile    
      
    except Exception as e:
        if kuiper:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            msg = "[-] [Error] mft Parser: " + str(exc_obj) + " - Line No. " + str(exc_tb.tb_lineno)
            return (None , msg)
        else:
            raise e