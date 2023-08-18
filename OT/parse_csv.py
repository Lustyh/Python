import csv
from chinese_calendar import is_workday
from datetime import datetime

class OT_calculate():

    @staticmethod
    def parse_csv(csv_file):
        ot_mins = 0
        ot_hours = 0
        
        with open(csv_file,newline='')as cv:
            row = cv.readlines()
        for x in row[1:]:
            x = x.split(',')
            if x[4] != 'None' and x[5] != 'None':


                if is_workday(datetime.strptime(x[3],"%Y%m%d")):
                    #   Work day
                    #   The over time will start at 1730
                    if int(x[5]) < 1730:
                        continue
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
                    ot_mins += ( (int(x[5][0:2]) * 60) + int(x[5][2:]) ) - 1050 - late_time

                else:

                    #   holiday
                    if  0 <= int(x[4][2:]) < 30 and 0 <= int(x[5][2:]) < 30 :
                        x[4] = x[4][0:2] + '00'
                        x[5] = x[5][0:2] + '00'
                    elif 30 <= int(x[4][2:]) <= 59 and 30 <= int(x[5][2:]) <= 59:
                        x[4] = x[4][0:2] + '30'
                        x[5] = x[5][0:2] + '30'


                    print('--holiday overtime day--  ' + x[3] + '  start time: '+ x[4] + ' end time: ' + x[5]) 
                    # ot_mins = end(60 * h + mins) - start(60 * h + mins)  
                    if int(x[5][0:2]) >= 13:
                        break_time = 60
                    else:
                        break_time = 0

                    if 30 <= int(x[6]) <=59:
                        late_time = 60
                    elif 0 < int(x[6]) <=30:
                        late_time = 30
                    else:
                        late_time = int(x[6])
                    ot_mins += ( (int(x[5][0:2]) * 60) + int(x[5][2:]) ) - ( (int(x[4][0:2]) * 60) + int(x[4][2:]) ) - break_time - late_time
        
        ot_hours = ot_mins/60
        print('total OT Mins: ' + str(ot_mins) + ' mins')
        print('total OT Hours: ' + str(ot_hours) + ' H')


if __name__ == '__main__':
    OT_calculate.parse_csv('overtime_A907A919_20230817_1500.csv')