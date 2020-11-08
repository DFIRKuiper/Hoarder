import json
import logging
import traceback
from collections import OrderedDict
from parsers.regsk.lib.helper import convert_datetime
from parsers.regsk.lib.helper import ComplexEncoder
from parsers.regsk.lib.hive_yarp import get_hive
from yarp import *


class PortForwading():

    def __init__(self,prim_hive,log_files):
        self.prim_hive = prim_hive
        self.log_files = log_files

    def run(self):
        hive = get_hive(self.prim_hive,self.log_files)
        select_key = hive.find_key(u'Select')
        current_path=''
        if select_key:
            current_value = select_key.value(name=u"Current")
            current_path = u"ControlSet{:03d}".format(current_value.data())
        else:
            current_path ='ControlSet001'
        lst =[]
        PortForwading_user_settings_path = u"\\".join([current_path,u"Services\\PortProxy\\v4tov4"])
        hive = get_hive(self.prim_hive,self.log_files)
        PortForwading_user_settings_key = hive.find_key(PortForwading_user_settings_path)
        if PortForwading_user_settings_key:
            for sk in PortForwading_user_settings_key.subkeys():
	              lst.append(sk)
            return lst
        # print('Found a key: {}'.format(PortForwading_user_settings_key.path()))
        # if PortForwading_user_settings_key:
        #     for sid_key in PortForwading_user_settings_key.subkeys():
        #         sid_name = sid_key.name()
        #         # version_value = sid_key.value(name=u"Version")
        #         # version = None
        #         # if version_value:
        #         #     version = version_value.data()
        #         #
        #         # sequence_value = sid_key.value(name=u"SequenceNumber")
        #         # sequence = None
        #         # if sequence_value:
        #         #     sequence = version_value.data()
        #
        #         sid_key_values = iter(sid_key.values())
        #
        #         while True:
        #             try:
        #                 value = next(sid_key_values)
        #             except StopIteration:
        #                 break
        #             except Exception as error:
        #                 # logging.error(u"Error getting next value: {}".format(error))
        #                 continue
        #
        #             print (value)
        #             # value_name = value.name()
        #             # value_data = value.data_raw()
        #             #
        #             # if value_name not in [u"Version", u"SequenceNumber"]:
        #             #     timestamp = convert_datetime(value_data[0:8])
        #             #
        #             #     record = OrderedDict([
        #             #         ("name", value_name),
        #             #         ("@timestamp", timestamp),
        #             #         ("sid", sid_name),
        #             #         ("version", version),
        #             #         ("sequence", sequence)
        #             #     ])
        #             #
        #             #     lst.append(u"{}".format(json.dumps(record, cls=ComplexEncoder)))
        #     return lst
        # else:
        #     # logging.info(u"[{}] {} not found.".format('PortForwading', PortForwading_user_settings_path))