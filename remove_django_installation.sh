#! /bin/bash

/etc/init.d/postgresql stop
rm -rf /home/roto/Project
deluser --remove-home postgres
apt-get --purge -y remove postgresql* libpq-dev python3-dev
apt autoremove -y
rm -rf /etc/postgresql*
rm -rf /var/lib/postgresql/

exit
