from datetime import datetime

import pytz
from tzlocal import get_localzone

# Get the current time in UTC
time_in_utc = datetime.utcnow()

# Detect the local timezone
local_timezone = get_localzone()

# Convert time to the local timezone
time_in_local_timezone = time_in_utc.replace(tzinfo=pytz.UTC).astimezone(local_timezone)

print("UTC time:", time_in_utc)
print("Time in local timezone:", time_in_local_timezone)