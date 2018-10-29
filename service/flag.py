#!/usr/bin/env python
# encoding: utf-8

import os
import uuid
import time
import hashlib
import sys

flag_salt = "c3944cd0-0f77-4f85-a561-ca9fd57c5c0e"
spanning = 1 * 60
playground = "../playground"

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

def update_flag(spanning, team_id, start_time):
    path = "%s/%s" % (playground, team_id)
    token = open("%s/token" % (path)).read()
    data = "%s|%s|%s" % (token, start_time, flag_salt)
    flag = "flag{%s}" % md5(data)
    print("set team %d flag to %s" % (team_id, flag))
    with open("%s/flag" % (path), "w") as f:
        f.write(flag)

def update_all_flag():
    ticks = int(time.time())
    start_time = ticks / spanning * spanning
    print "round: %s" % (time.asctime( time.localtime(start_time)))
    for i in os.listdir(playground):
        if i != ".gitkeep":
            update_flag(spanning, int(i), start_time)

def get_token_by_team_id(team_id):
    return open("%s/%s/token" % (playground, team_id)).read().strip()

def get_flag_by_team_id(team_id):
    return open("%s/%s/flag" % (playground, team_id)).read().strip()

def get_team_by_token(token):
    for i in os.listdir(playground):
        if i != ".gitkeep":
            correct_token = get_token_by_team_id(i)
            if token == correct_token:
                return i
    return None

def get_team_by_flag(flag):
    for i in os.listdir(playground):
        if i != ".gitkeep":
            correct_flag = get_flag_by_team_id(i)
            if flag == correct_flag:
                return i
    return None

def check_flag(token, flag):
    attacker_team = get_team_by_token(token)
    if attacker_team == None:
        return False
    victim_team = get_team_by_flag(flag)
    if victim_team == None:
        return False
    return (attacker_team, victim_team)

def main():
    update_all_flag()

if __name__ == "__main__":
    main()
