#!/usr/bin/env python
# encoding: utf-8

import os
import uuid
import time
import hashlib

flag_salt = "c3944cd0-0f77-4f85-a561-ca9fd57c5c0e"

def md5(data):
    return hashlib.md5(data).hexdigest()

'''
def update_flag(playground, team_id):
    path = "%s/%d" % (playground, team_id)
    flag = str(uuid.uuid4())
    print("set team %d flag to %s" % (team_id, flag))
    with open("%s/flag" % (path), "w") as f:
        f.write(flag)
'''

def update_flag(playground, spanning, team_id):
    path = "%s/%d" % (playground, team_id)
    token = open("%s/token" % (path)).read()
    ticks = int(time.time())
    start_time = ticks / spanning * spanning
    data = "%s|%s|%s" % (token, start_time, flag_salt)
    flag = "flag{%s}" % md5(data)
    print("set team %d flag to %s" % (team_id, flag))
    with open("%s/flag" % (path), "w") as f:
        f.write(flag)

def update_all_flag():
    playground = "../playground"
    spanning = 3
    for i in os.listdir(playground):
        if i != ".gitkeep":
            update_flag(playground, spanning, int(i))

def main():
    update_all_flag()

if __name__ == "__main__":
    main()
