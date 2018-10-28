#!/usr/bin/env python

import sys
import os

class Manager(object):
    def __init__(self, playground, template):
        self.playground = playground
        self.template = template

    def create_team(self):
        '''
        Create team
            create_team src dst
        '''
        # Assign team id
        team_id = self.count_team()
        print("Assigned team id: %d" % (team_id))
        # Assign IP address
        subnet = "172.100.1.0/24"
        gateway = "172.100.1.1"
        ip = "%s.%d" % (subnet.split(".0/24")[0], team_id)
        print("subnet: %s" % (subnet))
        print("gateway: %s" % (gateway))
        print("ip: %s" % (ip))
        # Create team folder
        command = "cp -r %s %s/%d" % (self.template, self.playground, team_id)
        code = os.system(command)
        if code != 0:
            print("Error while executing command: %s" % (command))
            return
        print("team folder created")
        print("setting vaiables")
        print("create team envrionment finished")

    def count_team(self):
        number =  len(os.listdir(self.playground))
        print("Current team number: %d" % (number))
        return number

        
    def help(self, func):
        try:
            print("%s: " % (func))
            print(getattr(self, func).__doc__)
        except AttributeError as e:
            print("%r" % e)
            print("No such command: %s" % (func))
        except TypeError as e:
            print("Type error: %s" % (repr(e)))


    def dispatcher(self, func, *args):
        try:
            getattr(self, func)(*args)
        except AttributeError as e:
            print("%r" % e)
            print("No such command: %s" % (func))
        except TypeError as e:
            print("Type error: %s" % (repr(e)))
        


def main():
    manager = Manager("../playground", "../challenge/template")
    manager.dispatcher(*sys.argv[1:])

if __name__ == "__main__":
    main()
