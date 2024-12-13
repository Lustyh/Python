import os
import yaml
import json
import csv
from datetime import datetime, timedelta



class GetFailItem():
    @staticmethod
    def countFailItemToCSV(project, station_list, path, date):
        print(station_list)
        print(path)
        given_date = datetime.strptime(date, "%Y%m%d")
        past_seven_days = [(given_date - timedelta(days=i-1)).strftime("%Y_%m_%d") for i in range(0, 8)]
        fail_item = {}
        ''' fail_item = {
            day1 : {
            station1: {
                item1: 5
                item2: 9
                item3: 10
                }
            }
        }
        '''
        
        for station in station_list:
            for day in past_seven_days:
                if not os.path.exists(f'./retest_cache/{project}/'):
                    os.makedirs(f'./retest_cache/{project}/')
                item_count = {}
                station_dict = {f"{station}": item_count}
                day_station = {f'{day}':station_dict}   
                
                try:
                    with open(f"{path}{station}\\{day}.csv", 'r')as f:
                        for line in f.readlines():
                            if project in line and station in line:
                                line = line.split(',')
                                
                                # print(line)
                                item = line[-1].strip().replace('"', '')
                                if item in item_count:
                                    item_count[item] += 1
                                else:
                                    item_count[item] = 1
                                # print(day_station)
                except Exception as e:
                    print(e)
                    continue
            with open(f'./retest_cache/{project}/{day}.csv', 'a+', newline='')as f:
                f.write(json.dumps(day_station) + '\n')
            print(day_station)

    @staticmethod
    def checkRetestOrFail(path, csvfile):
        with open(csvfile, 'r')as f:
            for station_item in f.readlines():
                station_item = json.loads(station_item.strip())
                for day, v in station_item.items():
                    for station, total in v.items():
                        with open (f"{path}{station}\\{day}.csv", 'r')as f:
                            print(f.read().split('\n'))
                                


if __name__ == '__main__':
    configs = yaml.safe_load(open('config.yaml', mode='r').read())
    project = 'YJ3DHM3'
    # path = configs['Project'][project]['FailItem_Path']
    # station_list = configs['Project'][project]['stations']
    # GetFailItem.countFailItemToCSV(project, station_list, path, '20241210')
    path = configs['Project'][project]['FPY_Path']
    GetFailItem.checkRetestOrFail(path, f'./retest_cache/{project}/2024_12_10.csv')