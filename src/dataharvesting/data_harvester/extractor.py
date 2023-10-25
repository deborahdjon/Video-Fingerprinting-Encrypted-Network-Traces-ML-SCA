#!/usr/bin/env python3

"""
Central location for application settings.
"""

__author__ = "Darragh Connaughton"
__copyright__ = "Copyright (c) Darragh Connaughton, 2023"
__license__ = "MIT License"

import re
from datetime import datetime


# ========
# FEATURE:
# ========

# Analyse log to determine if the session was successful. A good check would be seeing if number of bytes gathered
# is greater than some threshold.

# ========


def extract_videotrace_from_stderr(raw_data, timestamped_data) -> dict:
    videotrace = {
        "timestamp": [],
        "data": []
    }

    for data in raw_data.decode("utf-8").split("\n"):
        data_bytes = ""
        data_timestamp = ""

        match = re.search(r"(\S+) bytes", data)
        if match:
            data_bytes = match.group(1)

        match = re.search(
            r"([0-9]+-[0-9]+-\w+ [0-9]+[0-9]:[0-9]+:[0-9]+,[0-9]+)[0-9]", data
        )
        if match:
            date_time_obj = datetime.strptime(match.group(1), "%Y-%m-%d %H:%M:%S,%f")
            data_timestamp = datetime.timestamp(date_time_obj)

        if data_timestamp != "" and data_bytes != "":
            videotrace["timestamp"].append(data_timestamp)
            videotrace["data"].append(data_bytes)

    # if len(videotrace["timestamp"]) < len(timestamped_data):
    #     videotrace["quality"] = timestamped_data[:len(videotrace["timestamp"])]

    videotrace["quality"] = timestamped_data
    return videotrace
