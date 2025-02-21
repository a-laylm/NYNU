from datetime import datetime
date = "2024-12-07 17:00:00"
date= datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
timestamp = date.timestamp()
print(timestamp)