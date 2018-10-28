#!/usr/bin/env python
# encoding: utf-8

import web
from flag_service.flag import check_flag

urls = (
    '/submit', 'submit'
)
db = web.database(dbn='sqlite', db='db.sqlite3')

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
