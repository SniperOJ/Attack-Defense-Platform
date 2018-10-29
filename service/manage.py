#!/usr/bin/env python

import sys
import os
import sqlite3
import random
import string

from Crypto.PublicKey import RSA

def generate_rsa_key_pair(length=2048):
    key = RSA.generate(length)
    private_key = key.exportKey("PEM")
    public_key = key.publickey().exportKey("OpenSSH")
    return str(public_key), str(private_key)

def random_string(length=0x10):
    charset = string.letters + string.digits
    return "".join([random.choice(charset) for i in range(length)])

class Manager(object):
    def __init__(self, playground, template, name):
        self.playground = playground
        self.template = template
        self.subnet = "172.100.1.0/24"
        self.gateway = "172.100.1.254"
        self.name = name

    def init_db(self):
        db_filename = "db.sqlite3"
        try:
            os.remove("%s" % (db_filename))
        except Exception as e:
            pass
        os.system("sqlite3 %s < db.sql" % (db_filename))

    def create_network(self):
        os.system(
            "docker network create \
            --driver=bridge \
            --subnet=%s \
            --ip-range=%s \
            --gateway=%s \
            %s" % (self.subnet, self.subnet, self.gateway, self.name)
        )

    def create_team(self):
        '''
        Create team
            create_team src dst
        '''
        # Assign team id
        team_id = self.available_team_id()
        team_folder = "%s/%d" % (self.playground, team_id)
        print("Assigned team id: %d" % (team_id))
        # Assign access cred
        ctf_password = random_string(0x20)
        root_password = random_string(0x20)
        public_key, private_key = generate_rsa_key_pair()
        token = random_string(0x20)
        # Assign IP address
        ip = "%s.%d" % (self.subnet.split(".0/")[0], team_id)
        name = self.name
        # Assign ports
        base_port = 60000
        service_port = base_port + team_id * 5
        ssh_port = base_port + team_id * 5 + 1
        config = {
            # Common
            "team_id": team_id,
            "team_folder":team_folder,
            # Auth
            "ctf_password":ctf_password,
            "root_password":root_password,
            "public_key":public_key,
            "private_key":private_key,
            "token":token,
            # Net
            "ip":ip,
            "name":name,
            # Service
            "service_port":service_port,
            "ssh_port":ssh_port,
        }
        # Create team folder
        command = "cp -r %s %s" % (self.template, team_folder)
        code = os.system(command)
        if code != 0:
            print("Error while executing command: %s" % (command))
            return
        print("team folder created")
        print("configuring vaiables")
        self.config_team(team_id, config)
        print("Create db")
        db = sqlite3.connect('db.sqlite3')
        db.execute("INSERT INTO team (name, score) VALUES ('%d', %d)" % (team_id, 1000))
        db.commit()
        db.close()
        print("create team envrionment finished")

    def config_team(self, team_id, config):
        print("Modifying team %d => \n%s" % (team_id, config))
        # Docker-compose
        filename = "%s/docker-compose.yml" % (config['team_folder'])
        content = open(filename, "r").read()
        content = content.replace(
            "__SERVICE_EXTERNAL_PORT___", str(config['service_port'])
        )
        content = content.replace(
            "__SSH_EXTERNAL_PORT___", str(config['ssh_port'])
        )
        content = content.replace(
            "__NAME__", config['name']
        )
        content = content.replace(
            "__IP__", config['ip']
        )
        with open(filename, "w") as f:
            f.write(content)
        # Run.sh
        filename = "%s/run.sh" % (config['team_folder'])
        content = open(filename, "r").read()
        content = content.replace(
            "__ROOT_PASSWORD__", str(config['root_password'])
        )
        content = content.replace(
            "__CTF_PASSWORD__", config['ctf_password']
        )
        content = content.replace(
            "__SSH_PUBLIC_KEY__", config['public_key']
        )
        with open(filename, "w") as f:
            f.write(content)
        # SSH key
        with open("%s/ssh/id_rsa.pub" % (config['team_folder']), "w+") as f:
            f.write(config['public_key'])
        with open("%s/ssh/id_rsa" % (config['team_folder']), "w+") as f:
            f.write(config['private_key'])
        with open("%s/token" % (config['team_folder']), "w+") as f:
            f.write(config['token'])

    def available_team_id(self):
        folder_list = os.listdir(self.playground)
        ID = 0
        while True:
            if "%d" % (ID) not in folder_list:
                print("Current team number: %d" % (number))
                return ID
            else:
                ID += 1
        
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
    manager = Manager("../playground", "../challenges/2018-Jinan-Train/zblog", "ctf")
    manager.dispatcher(*sys.argv[1:])

if __name__ == "__main__":
    main()

