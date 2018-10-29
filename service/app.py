#!/usr/bin/env python
# encoding: utf-8

import web
import operator
from flag import check_flag

urls = (
    '/submit', 'submit',
    '/score', 'score',
)
db = web.database(dbn='sqlite', db='db.sqlite3')

class score:
    def GET(self):
        teams = db.select('team')
        score = dict()
        for team in teams:
            score[team.name] = team.score
        result = ""
        for i in sorted(score.items(), key=operator.itemgetter(1))[::-1]:
            result += "%s\t%s\n" % (i[0], i[1])
        return result

class submit:
    def POST(self):
        # Get input data
        i = web.input(token=None, flag=None)
        token = i.token
        if token == None:
            return "token please"
        flag = i.flag
        if flag == None:
            return "flag please"
        # Create submit log
        db.insert('submit_log', ip=web.ctx['ip'], flag=flag, token=token)
        # Check flag
        attack = check_flag(token, flag)
        if attack == False:
            return "Invalid flag"
        if attack[0] == attack[1]:
            return "Attack your self is usless"
        db.insert('attack_log', ip=web.ctx['ip'], attacker=attack[0], victim=attack[1])
        print "team %s => team %s" % (attack[0], attack[1])
        return "team %s => team %s" % (attack[0], attack[1])

if __name__ == "__main__":
    web.config.debug = False
    app = web.application(urls, globals())
    app.run()
