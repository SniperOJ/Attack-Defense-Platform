#!/bin/bash

# Change root password
echo "root:__ROOT_PASSWORD__" | chpasswd

# Change ctf password
useradd -d /home/ctf/ -m -p ctf -s /bin/bash ctf
echo "ctf:__CTF_PASSWORD__" | chpasswd

# Add ssh key of ctf
mkdir /home/ctf/.ssh/
echo '__SSH_PUBLIC_KEY__' > /home/ctf/.ssh/authorized_keys
chmod 644 /home/ctf/.ssh/authorized_keys

# start server
service apache2 start
service ssh start
/bin/bash
