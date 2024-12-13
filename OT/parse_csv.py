import csv
# from chinese_calendar import is_workday
from datetime import datetime

holiday_list = ['20241014', '20241023', '20241205', '20241231']

class OT_calculate():

    @staticmethod
    def is_workday(date):
        if date in holiday_list:
            return False
        day_of_week = datetime.strptime(date,"%Y%m%d").weekday()
        if day_of_week == 5 or day_of_week == 6:
            return False
        return True

    @staticmethod
    def parse_csv(csv_file):
        ot_mins = 0
        ot_hours = 0
        with open(csv_file,newline='',encoding='utf-8')as cv:
            row = cv.readlines()
        for x in row[1:-1]:
            try:
                x = x.split(',')
                # ['18', 'A907A919', '黄俊霖', '20230901', '0758', '2107', '0', 'D', 'None', 'None', 'None', 'N', 'N', 'None', 'None', 'None', 'None', '0', '0', '0', '0', '0', '0.00', 'None', 'None', '', 'None', '明细', 'A7359568', '0', 'N', '0.00', '0.00\r\n']
                if x[4] != 'None' and x[5] == 'None':
                    print('makeup offwork time')
                    x[5] = x[14]
            
                if x[4] == 'None' and x[5] != 'None':
                    print('makeup onwork time')
                    x[4] = x[13]

                if x[4] != 'None' and x[5] != 'None':

                    if OT_calculate.is_workday(x[3]):
                        #   Work day
                        #   The over time will start at 1730
                        if int(x[5]) < 1830:
                            continue
                        # if int(x[5]) < 1730 and int(x[3]) < 20240905:
                        #     continue
                        elif 0 <= int(x[5][2:]) < 30:
                            x[5] = x[5][0:2] + '00' 
                        elif 30 <= int(x[5][2:]) <= 59:
                            x[5] = x[5][0:2] + '30'
                        # late_time
                        
                        if 30 <= int(x[6]) <=59:
                            late_time = 60
                        elif 0 < int(x[6]) <=30:
                            late_time = 30
                        else:
                            late_time = int(x[6])

                        print('--normal working day--  ' + x[3] + '  start time: '+ x[4] + ' end time: ' + x[5]) 
                        # Normal day start from 1050
                        # 1050 mins mean 0am ~ 8am 480mins + 8am ~ 1730pm : 570mins
                        # in QMB it\s 8am ~ 1830pm then is 480 + 630 = 1110
                        if int(x[3]) > 20240905:
                            offtime_mins = 1110
                        else:
                            offtime_mins = 1050
                        print(( (int(x[5][0:2]) * 60) + int(x[5][2:]) ) - offtime_mins - late_time)
                        ot_mins += ( (int(x[5][0:2]) * 60) + int(x[5][2:]) ) - offtime_mins - late_time
                        # print(ot_mins)
                    else:
                        # print('holiday')
                        #   holiday
                        

                        if 0 <= int(x[4][2:]) < 30:
                            x[4] = x[4][0:2] + '30'
                        else:
                            if len(str(int(x[4][0:2]) + 1) ) == 1:
                                x[4] = '0' + str(int(x[4][0:2]) + 1) + '00'
                            else:
                                x[4] = str(int(x[4][0:2]) + 1) + '00'

                        if 0 <= int(x[5][2:]) < 30 :
                            x[5] = x[5][0:2] + '00'
                        else:
                            x[5] = x[5][0:2] + '30'

                        print('--holiday overtime day--  ' + x[3] + '  start time: '+ x[4] + ' end time: ' + x[5]) 
                        # ot_mins = end(60 * h + mins) - start(60 * h + mins)  
                        
                        if int(x[4][0:2]) <= 12 and int(x[5][0:2]) >= 13:
                            break_time = 60
                        else:
                            break_time = 0

                        if int(x[5]) > 1800:
                            break_time += 30

                        if 30 <= int(x[6]) <=59:
                            late_time = 60
                        elif 0 < int(x[6]) <=30:
                            late_time = 30
                        else:
                            late_time = int(x[6])
                        print(( (int(x[5][0:2]) * 60) + int(x[5][2:]) ) - ( (int(x[4][0:2]) * 60) + int(x[4][2:]) ) - break_time - late_time)
                        ot_mins += ( (int(x[5][0:2]) * 60) + int(x[5][2:]) ) - ( (int(x[4][0:2]) * 60) + int(x[4][2:]) ) - break_time - late_time
            except Exception as e:
                print(e)
        ot_hours = ot_mins/60
        print('total OT Mins: ' + str(ot_mins) + ' mins')
        print('total OT Hours: ' + str(ot_hours) + ' H')


if __name__ == '__main__':
    # OT_calculate.parse_csv('overtime_A907A919_20230817_1500.csv')
    # print(datetime.strptime(x[3],"%Y%m%d"))
    x = '20241014'
    # OT_calculate.is_workday(datetime.strptime(x,"%Y%m%d"))
    print(OT_calculate.is_workday(x))