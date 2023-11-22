import requests
import traceback
import sys
import yaml
import re
import time


class SFC(object):
    """
    Shopfloor control Process/Data Tansfer
    """
    config = yaml.safe_load(open('shopfloor.yaml',mode='r').read())
    API_CONNECT = 'Connect'
    API_CONNECT_FINAL = 'ConnectFinal'
    API_GET_DEVICE_DATA = 'GetDeviceData'
    API_SEND_RECV_DATA_SFC = 'SendRecvDataSFC'

    FIELD_RESULT = 'result'
    FIELD_MESSAGE = 'message'
    FIELD_DATA = 'data'

    RESPONSE_PASS = 'PASS'
    RESPONSE_FAIL = 'FAIL'

    TIMEOUT_SECOND = 10
    DATA_TYPE_DIR = {'GET_BUILD_PHASE': 'BUILD',
                    'GET_DUT_CONFIG': 'SKU',
                    'GET_DUT_DATA': 'data',
                    'CHECK_SCOF': 'SCOF',
                    'GET_SF_TIME_MILLIS':'sf_time',
                    'GET_ASSEMBLY_DATA': 'data'}



    def __init__(self,project_id,station_id):
        self.project_id = project_id
        self.station_id = station_id

    def httpPost(self,api,data):
        try:
            req = requests.post('http://%s:%s/%s' % (self.config['ip'], self.config['port'], api),
                                json=data,
                                timeout=30)
            req.raise_for_status()
            res = req.json()
            return res
        except:
            return {'result': 'FAIL',
                    'message': ''.join(
                        traceback.format_exception_only(sys.exc_info()[0], sys.exc_info()[1])).strip()}

    def Connect(self, dut_id):
            """ Connect to ShopFloor server before starting a test.
            Arg:
            dut_id: dut serial number

            Return:
            result: Connect result: PASS/FAIL
            message: shopfloor return message.
            """
            data = {
            'dut_id': dut_id,
            'station_id': self.station_id,
            }

            response = self.httpPost(self.API_CONNECT, data)
            result = response.get(self.FIELD_RESULT, self.RESPONSE_FAIL)
            message = response.get(self.FIELD_MESSAGE, '\nConnect: No message from Shopfloor!\n')

            return result, message

    def SendRecvDataSFC(self, data_type, dut_id=None, name=None,
                      value=None, data=None ):
        """ Get various info data from shopfloor
        Arg:
        data_type:  info data type, defined on DATA_TYPE list,
        dut_id: dut serial number
        name: key name
        value: key value
        data:  any data for a special SFC

        Return:
        result: connection result: PASS/FAIL
        message: info data
        """

        result = 'FAIL'
        message = 'GetDeviceData: data_type is not supported.'
        response = None
        http_post_api = self.API_SEND_RECV_DATA_SFC
        http_post_data = {
        'data_type': data_type,
        'dut_id': dut_id,
        'project_id': self.project_id,
        'station_id': self.station_id,
        'data': data
        }

        if data_type in list(self.DATA_TYPE_DIR.keys()):
            response = self.httpPost(http_post_api, http_post_data) # response is a dict
            result = response.get(self.FIELD_RESULT, self.RESPONSE_FAIL)
            if result == self.RESPONSE_PASS:
                message = response.get(self.FIELD_DATA, {})
                if message:
                    if data_type != 'GET_DUT_DATA':
                        message = message.get(self.DATA_TYPE_DIR[data_type], '')
                    if not message:
                        result = 'FAIL'
                        message = 'No message returned from SF'
                else:
                    result = 'FAIL'
                    message = 'No data returned from SF.'
            else:
                message = response.get(self.FIELD_MESSAGE, 'GetDeviceData: No message from Shopfloor.')

        return result, message

    def ConnectFinal(self, dut_id=None, test_result=None):
        """ final connect to shopfloor after a test completed.
        Arg:
        test_result: final test result.

        Return:
        result: Connect result: PASS/FAIL
        message: shopfloor return message.
        """

        dut_id = dut_id
        test_result = test_result
        print(test_result)
        pvs_upload_list = self.config['upload_list']
        illegal_char = '[\s\r\n\'\",;:$*]'
        description = dict()
        final_result = 'PASS'
        
        # Check final result PASS/FAIL
        for item,value in test_result.items():
            try:
                if 'PASS' not in value[1]:
                    description[item] = value[1] # ERROR Code
                    final_result = 'FAIL'
            except:
                pass
        
        # Check PASS item whether in upload lists
        if final_result != 'FAIL':
            for item,value in test_result.items():
                try:
                    if item in pvs_upload_list:
                        # replace illegal char to '' empty.
                        description[item] = re.sub(illegal_char,'',value[0])
                except:
                    pass

        # default is ok when PASS and no upload items.
        if len(description) == 0:
            description = "OK"

        # if 'PASS' not in test_result:
        #     test_result = 'FAIL'

        data = {
        'dut_id': dut_id,
        'station_id': self.station_id,
        'status': final_result,
        'description': description,
        }
        print(data)
        # return 'PASS',{'dut_id': 'WIP3327105HA010C9', 'station_id': 'K6_P3-M29_FATP-PROV_03', 'status': 'PASS', 'description': 'OK'}
        # TODO
        for i in range(2):
            try:
                response = self.httpPost(self.API_CONNECT_FINAL, data)
                result = response.get(self.FIELD_RESULT, self.RESPONSE_FAIL)
                message = response.get(self.FIELD_MESSAGE, 'ConnectFinal: No message from Shopfloor.')
                if 'requests.exceptions' in message:
                    print('retry ConnectionFinal')
                    continue
                else:
                    break
            except:
                pass
        return result, message
    



if __name__ == '__main__':
    sf = SFC(project_id='Z7B',station_id='Z7B_F4-E24_FT1_01')
    # data = {"dut_id": "WIP3803MZ7BX00025", "station_id": "Z7B_F4-E24_FT1_01", "status": "PASS", "description": "OK"}#{"CPUID": "00000000c9384b21", "EMMC_MFG_DATE": "07/2023", "SB_CPUID": "0000000B08000000DE62B0829F682621"}}
    # print(sf.httpPost('ConnectFinal',data))
    result,message = sf.SendRecvDataSFC(data_type='GET_DUT_DATA',
                                        dut_id='WIP3803MZ7BX00025',
                                        )
    print(result)
    print(message)
    # import json
    # test = '{"result": "PASS", "message": "OK", "data": { "Work_Order": "335763548", "Station": "YX6MS_F4-L19_BFT_01", "ErrorCode": "", "MBSN": "ZZ99999", "BTMAC": "", "WIFIMAC": "", "ModelDesc": "YX6ESMB", "BMac": "", "WMac": "", "EMac": "", "WIFI2G": "C09879A4753C", "Wifi5G": "C09879A4753B", "Wifi6G": "C09879A4753D", "EMAC0": "C09879A4753F", "EMAC1": "C09879A4753E", "Config": "MP", "ACCE": "", "BIN": "" , "BUILD": "MP", "Line": "E34", "Hwid": "0100", "EmmcName": "004GA1;SM0000", "PJID": "00", "CPUType": "", "MLBRepair": "", "Image": "MP"}}'
    # print(json.loads(test))
    # result,message = sf.Connect(dut_id='F3BYJ3ME3AWM0091')
    # print(result)
    # print(message)
    # sp_return = []
    # sp_return.extend(message)
    # print(sp_return)
    """

    Estimation value get from BU10 program.
    dict[item] = [value, ErrorCode]

    {'power_off_12v': ['', 'PASS'], 'power_off_5v': ['', 'PASS'], 
    'delay_some_seconds': ['', 'PASS'], 'power_on_12v': ['', 'PASS'], 
    'off_mode_current': ['', 'PASS'], 'power_on_5v': ['', 'PASS'], 
    'power_on_current': ['', 'PASS'], 'ping_test': ['FAIL', 'BCPNM'], 
    'get_info_from_sf': ['LAN_PROT2_PASS LAN_PROT3_PASS LAN_PROT4_PASS', 'PASS'], 'write_2g_mac': ['', 'PASS']}

    """

    # test_result = {'power_off_12v': ['', 'PASS'], 'power_off_5v': ['LAN_PROT2_PASS LAN_PROT3_PASS LAN_PROT4_PASS', 'fail'], 'delay_some_seconds': ['', 'fail'], 'power_on_12v': ['', 'PASS'], 'off_mode_current': ['', 'PASS'], 'power_on_5v': ['', 'PASS'], 'power_on_current': ['', 'PASS'], 'ping_test': ['FAIL', 'PASS'], 'get_info_from_sf': ['', 'PASS'], 'write_2g_mac': ['', 'PASS']}
    # print(sf.ConnectFinal(dut_id='WIP3803MZ7BX00025',test_result=test_result))