#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AAC / M4A with chapters to text
"""

import sys
import re
import subprocess

if len(sys.argv) != 2:
    print("Usage: m4a-to-chapter M4A_FILENAME")
    sys.exit(1)


filename = sys.argv[1]
command = ["ffprobe", '-i', filename]

output = subprocess.check_output(command, stderr=subprocess.STDOUT, universal_newlines=True)


def chaps():
    current_chap = None
    chapters = []
    for line in iter(output.splitlines()):
        m = re.match(r".*Chapter #(\d+:\d+): start (\d+\.\d+), end (\d+\.\d+).*", line)
        num = 0
        if m is not None:
            current_chap = ({"name": m.group(1), "start": m.group(2), "end": m.group(3), "title": None})
            num += 1

        m_title = re.match(r"\s+title\s+:\s*(.*)", line)
        if m_title is not None and current_chap is not None:
            current_chap["title"] = m_title.group(1)
            current_chap["start"] = float(current_chap["start"])
            current_chap["end"] = float(current_chap["end"])
            chapters.append(current_chap)
    return chapters


all_chaps = chaps()

for chap in all_chaps:
    millis = int((chap["start"] % 1) * 1000)
    seconds = int(chap["start"]) % 60
    minutes = int(chap["start"]) // 60
    hours = int(chap["start"]) // 60 // 60
    print("{:02}:{:02}:{:02}.{:03} {}".format(hours, minutes, seconds, millis, chap["title"]))
