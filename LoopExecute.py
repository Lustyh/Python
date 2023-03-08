
import schedule
import time

def job():
    print("I'm working...")

schedule.every(1).seconds.do(job)
# seconds,minutes,hours

while True:
    schedule.run_pending()
    time.sleep(1)
