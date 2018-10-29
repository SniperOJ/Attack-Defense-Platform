#!/usr/bin/env python

import time
import sqlite3


db = sqlite3.connect('/root/Abattoir/service/db.sqlite3')
c = db.cursor()

spanning = 1 * 60
ticks = int(time.time())
start_time = ticks / spanning * spanning - spanning
end_time = start_time + spanning
print("%s => %s" % (time.asctime( time.localtime(start_time)), time.asctime( time.localtime(end_time))))

cursor = c.execute("SELECT * FROM attack_log WHERE timestamp > datetime(%s, 'unixepoch', 'localtime') AND timestamp < datetime(%s, 'unixepoch', 'localtime')" % (start_time, end_time))
attacks = set()
for row in cursor:
    print row
    ID = row[0]
    ip = row[1]
    attacker = row[2]
    victim = row[3]
    timestamp = row[4]
    print(ID, ip, attacker, victim, timestamp)
    attack = (attacker, victim)
    attacks.add(attack)

for attack in attacks:
    attacker = attack[0]
    victim = attack[1]
    # punish
    price = 5
    print("punishing victim: team %s (-%d points)" % (victim, price))
    c.execute("UPDATE team SET score=score-%d WHERE name='%s'" % (price, victim))
    db.commit()
    # award
    print("awarding attacker: team %s (+%d points)" % (attacker, price))
    c.execute("UPDATE team SET score=score+%d WHERE name='%s'" % (price, attacker))
    db.commit()


db.close()

