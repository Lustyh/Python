

import requests,time,csv
from chinese_calendar import is_workday
from datetime import datetime
from lxml import etree
from requests.auth import HTTPBasicAuth
from requests.auth import HTTPDigestAuth
from requests_ntlm import HttpNtlmAuth
from pyquery import PyQuery as pq
import parse_csv


class Overtime():
    def __init__(self,user,password) -> None:
        # self.url = 'http://10.17.36.87/QSMCHR2005/Attn/Modify_Attandence_assistant_min.aspx?Flag=4&languageType=zh-CN'
        # self.url = 'http://10.17.36.87/QSMCHR2005/Attn/Modify_Attandence_assistant_min.aspx?Flag=4&languageType=zh-CN'
        # self.url = 'http://hr.rsquanta.com/QSMCHR2005/Attn/Modify_Attandence_assistant_min.aspx?Flag=4&languageType=zh-CN'
        self.url = 'http://hr.rsquanta.com/HROldPages/Attn/Modify_Attandence_assistant_min.aspx?Site=QMB&Flag=4&languageType=zh-CN'
        self.user = user #'A907A919'
        self.pd = password #'LH!1234567890'
    
    def LogInUrl(self):
        """Login request"""
        self.response = requests.get(url=self.url,
                                     auth=HttpNtlmAuth(self.user,
                                                       self.pd
                                                       )
                                    )
        
        # only continue when the return code is 200.
        if 200 == self.response.status_code:
            print('connect successfully!')
            # print(self.response.headers)
        else:
            print('connect failed')
            print('[error code]: '+ str(self.response.status_code))
    

    def SaveHTML(self):
        """Save HTML page at local"""
        self.text = pq(self.response.text)
        with open('html.txt','w+',encoding='utf-8')as f:
            f.write(str(self.text))
    
    def ListPyquery(self,keyword):
        # print(self.text)
        create = list(self.text.find(keyword))
        # print(create)
        self.final = []
        for x,v in enumerate(create):
            # color = list(self.text.find('tr'))
            # for x in color:
                # print(x.text)
            v = v.text
            # print(v)
            try:
                self.final.append(v)
            except:
                pass
        self.final = str(self.final[5:]).split("'QMB'")
        result = dict()
        
        for x in self.final:
            # print('='*20)
            x = x.replace('[','').replace(']','').split(',')
            # print(x)
            if len(x) < 2:
                continue
            if len(x[0]) >0:
                result[x[0].replace("'",'').strip()] = str(x).replace("'",'').strip()
            else:
                result[x[1].replace("'",'').strip()] = str(x[1:-1]).replace("'",'').strip()
        # print(result)
        return result
    
    def WriteToCSV(self,content):
        title = ['NO','工号','姓名','日期','上班时间','下班时间','迟到','班别','前段','后段','全段','多次刷卡','请假','补登上班','补登下班','加班开始','加班结束','1.5倍','2倍','3倍','补假日加班差额','总分钟数','总时数','补登事由','加班事由','补登签核','加班签核','加班明细','修改人','早退','报餐','旷职','预报时数','厂区']
        csv_file = 'overtime_'+self.user+'_%s.csv'%datetime.now().strftime("%Y%m%d")
        target_file = csv.writer(open(csv_file,'w+',newline='', encoding='utf-8'))
        target_file.writerow(title) #write title
        print(content)
        for x in range(2,len(content)+1):
            result = content[str(x)].replace('[','').replace(']','').replace('"','').split(',')
            # print(result)
            result = [str(x.strip()) for x in result]
            target_file.writerow(result)
        return csv_file

    def main(self,keyword):
        self.LogInUrl()
        self.SaveHTML()
        result = self.ListPyquery(keyword)
        csv_file = self.WriteToCSV(result)
        parse_csv.OT_calculate.parse_csv(csv_file)


if __name__ == '__main__':
    import sys
    user = sys.argv[1]  #"A907A919"#input('Please enter your username:').upper()
    password = sys.argv[2]  #'LH$1234567890'#input('Please enter your Password:')
    print('userID:', user)
    VERSION = '2.0.0'
    print('Cal_OT_Version: ' + VERSION)
    test = Overtime(user,password)
    test.main('span')






