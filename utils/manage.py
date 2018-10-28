#!/usr/bin/env python

import sys
import os

class Manager(object):
    def __init__(self):
        pass

    def create_team(self, template, team_name, target_folder):
        '''
        Create team
            create_team template team_name target_folder
        '''
        os.system("cp -r %s %s/%s" % (template, team_name, target_folder))

    def help(self, func):
        try:
            print("%s: " % (func))
            print(getattr(self, func).__doc__)
        except AttributeError as e:
            print("No such command: %s" % (func))
        except TypeError as e:
            print("Type error: %s" % (repr(e)))


    def dispatcher(self, func, *args):
        try:
            getattr(self, func)(*args)
        except AttributeError as e:
            print("No such command: %s" % (func))
        except TypeError as e:
            print("Type error: %s" % (repr(e)))
        


def main():
    manager = Manager()
    manager.dispatcher(*sys.argv[1:])

if __name__ == "__main__":
    main()
