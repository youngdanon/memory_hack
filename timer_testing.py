import datetime
import time
hh, mm, ss = [int(i) for i in input().split()]
print(hh, mm, ss)
now = datetime.datetime.now()
deadline = now + datetime.timedelta(hours=hh, minutes=mm, seconds=ss)
print(deadline.hour, deadline.minute, deadline.second)
while True:
    time.sleep(1)
    now = datetime.datetime.now()
    if deadline.hour <= now.hour and deadline.minute <= now.minute and deadline.second <= now.second:
        print("Time is up")
        break
