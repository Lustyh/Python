import xml.etree.ElementTree as ET

class xml_parse():


    @staticmethod
    def programmer_xml(filename):
        # xml_data = '''
        # <Data formatVersion="2.0" type="TS4-H Programmer">
        #     <Station config="1.0" SW="1.2" HW="1" Location="Tigo" ID="1"/>
        #     <DateTime TimeZone="Central Standard Time">2022-11-11_11-36-15</DateTime>
        #     <TotalTestTime>18.7</TotalTestTime>
        #     <DUT Num_of_retries="1" hex_file_name="Mnode_H9_0012.bin" Hw_str_for_user_data="ESO080V800W-H511.4.50" SW_ver="9.0012" HW_ver="4.50" Model="511" Short_MAC="4-21B0F36R" MAC="04C05B40021B0F36" SN="00511T3322045009001212345"/>
        #     <Result Code="PASS"/>
        # </Data>
        #            '''

        tree = ET.parse(filename)
        root = tree.getroot()

        # 提取数据
        format_version = root.attrib["formatVersion"]
        data_type = root.attrib["type"]

        station_config = root.find("Station").attrib["config"]
        station_sw = root.find("Station").attrib["SW"]
        station_hw = root.find("Station").attrib["HW"]
        station_location = root.find("Station").attrib["Location"]
        station_id = root.find("Station").attrib["ID"]

        date_time = root.find("DateTime").text

        total_test_time = root.find("TotalTestTime").text

        dut = root.find("DUT")
        dut_retries = dut.attrib["Num_of_retries"]
        dut_hex_file_name = dut.attrib["hex_file_name"]
        dut_hw_str = dut.attrib["Hw_str_for_user_data"]
        dut_sw_ver = dut.attrib["SW_ver"]
        dut_hw_ver = dut.attrib["HW_ver"]
        dut_model = dut.attrib["Model"]
        dut_short_mac = dut.attrib["Short_MAC"]
        dut_mac = dut.attrib["MAC"]
        dut_sn = dut.attrib["SN"]

        result_code = root.find("Result").attrib["Code"]

        # 打印提取的数据
        print("Format Version:", format_version)
        print("Data Type:", data_type)
        print("Station Config:", station_config)
        print("Station SW:", station_sw)
        print("Station HW:", station_hw)
        print("Station Location:", station_location)
        print("Station ID:", station_id)
        print("Date Time:", date_time)
        print("Total Test Time:", total_test_time)
        print("DUT Retries:", dut_retries)
        print("DUT Hex File Name:", dut_hex_file_name)
        print("DUT HW Str:", dut_hw_str)
        print("DUT SW Version:", dut_sw_ver)
        print("DUT HW Version:", dut_hw_ver)
        print("DUT Model:", dut_model)
        print("DUT Short MAC:", dut_short_mac)
        print("DUT MAC:", dut_mac)
        print("DUT SN:", dut_sn)
        print("Result Code:", result_code)

    @staticmethod
    def tester_xml(filename):

        tree = ET.parse(filename)
        root = tree.getroot()

        format_version = root.attrib["formatversion"]
        data_type = root.attrib["type"]
        test_name = root.find('TestName').text
        cycle_time = root.find('TotalTestTime').text
        lmu_sw = root.find('LMU').attrib['SW']
        lmu_hw = root.find('LMU').attrib['HW']
        lmu_cable_length = root.find('LMU').attrib['Cable_length']
        lmu_swc = root.find('LMU').attrib['SWC']
        result_code = root.find("Result").attrib["Code"]

        for result_item in root.find("Result"):
            # 获取子元素的标签名
            item_name = result_item.tag
            # 获取子元素的属性
            item_attributes = result_item.attrib
            # 获取子元素的文本内容
            item_text = result_item.text

            # 输出子元素的信息
            print("Item Name:", item_name)
            print("Item Attributes:", item_attributes)
            # if 'step' in item_attributes:
            #     print("Item Attributes:", item_attributes['step'])
            # elif 'name' in item_attributes: 
            #     print("Item Attributes:", item_attributes['name'])
            # else:
            #     print("Item Attributes:", item_attributes)
            print("Item Text:", item_text)
            print("\n")
        
        # 打印提取的数据
        print("Format Version:", format_version)
        print("Data Type:", data_type)
        print("Test Name:",test_name)
        print("Cycle time: %ss"%cycle_time)
        print(lmu_sw, lmu_hw, lmu_cable_length, lmu_swc)
        print("Result Code:", result_code)
        

if __name__ == '__main__':
    # xml_parse.programmer_xml('programer.xml')
    xml_parse.tester_xml('tester.xml')