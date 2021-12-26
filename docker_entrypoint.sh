#!/bin/bash

# Update Data runs 4 times a year
# https://echo.epa.gov/resources/echo-data/about-the-data
echo "WB Data Updater container has been started"

declare -p | grep -Ev 'BASHOPTS|BASH_VERSINFO|EUID|PPID|SHELLOPTS|UID' > /container.env

echo "start" >> /var/log/cron.log 2>&1

# Setup a cron schedule
echo "SHELL=/bin/bash
BASH_ENV=/container.env

# 1st Quarter, At 00:00 on day-of-month 1 in February.
0 0 1 2 * cd /app && ./scripts/update_wb_data.sh >> /var/log/cron.log 2>&1

# 2nd Quarter, At 00:00 on day-of-month 1 in May.
0 0 1 5 * cd /app && ./scripts/update_wb_data.sh >> /var/log/cron.log 2>&1

# 3rd Quarter, At 00:00 on day-of-month 1 in August.
0 0 1 8 * cd /app && ./scripts/update_wb_data.sh >> /var/log/cron.log 2>&1

# 4th Quarter, At 00:00 on day-of-month 1 in November.
0 0 1 11 * cd /app && ./scripts/update_wb_data.sh >> /var/log/cron.log 2>&1
# This extra line makes it a valid cron" > scheduler.txt

crontab scheduler.txt
cron

touch /var/log/cron.log
echo "running....."
