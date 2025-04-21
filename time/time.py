import pytz
import time 
from datetime import datetime, timedelta

def time_at_location(timezone_str):
        est = pytz.timezone("America/New_York")
        timezone = pytz.timezone(timezone_str)
        loc_dt = est.localize(datetime.now())
        print("loc_dt:", loc_dt)
        timezone_dt = loc_dt.astimezone(timezone)
        print("timezone_dt:", timezone_dt)
        
        return {
            "time": timezone_dt.strftime("%Y-%m-%d %H:%M:%S"),
            "utc_offset": timezone_dt.strftime("%z"),
        }
    
print(time_at_location("Europe/London"))