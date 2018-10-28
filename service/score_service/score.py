#!/usr/bin/env python


import sqlite3

db = sqlite3.connect('../db.sqlite3')
c = conn.cursor()

cursor = c.execute("SELECT * from attack_log")
for row in cursor:
    ID = row[0]
    ip = row[1]
    attacker = row[2]
    victim = row[3]
    timestamp = row[4]
    print(ID, ip, attacker, victim, timestamp)

db.close()

