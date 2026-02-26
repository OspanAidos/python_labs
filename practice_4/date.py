#1
from datetime import datetime, timedelta
current_date = datetime.now()
five_days_ago = current_date - timedelta(days=5)
print(f"Current Date: {current_date.strftime('%Y-%m-%d')}")
print(f"Five days ago: {five_days_ago.strftime('%Y-%m-%d')}")


#2
from datetime import datetime, timedelta
today = datetime.now()
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)
print(f"Yesterday: {yesterday.strftime('%Y-%m-%d')}")
print(f"Today:     {today.strftime('%Y-%m-%d')}")
print(f"Tomorrow:  {tomorrow.strftime('%Y-%m-%d')}")


#3
from datetime import datetime
dt_with_ms = datetime.now()
dt_no_ms = dt_with_ms.replace(microsecond=0)
print(f"With microseconds:    {dt_with_ms}")
print(f"Without microseconds: {dt_no_ms}")


#4
from datetime import datetime
date1 = datetime(2026, 2, 24, 15, 0, 0)
date2 = datetime(2026, 2, 23, 15, 0, 0) 
difference = date1 - date2
seconds_diff = difference.total_seconds()
print(f"Date 1: {date1}")
print(f"Date 2: {date2}")
print(f"Difference in seconds: {int(seconds_diff)} seconds")