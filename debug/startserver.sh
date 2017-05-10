#!/bin/sh


help="Please use command 'sudo startserver.sh localip(default is 192.168.1.1 using '-' instead) port_for_distribute_app(default is 5000 \ 
using '-' instead) managerip(default is 192.168.1.2, port for sign in and out:5050 using '-' instead) port_for_user_request(default is 6\
	000 using '-' instead)'"

localip=$1
if [ "$localip" == "" ]
then
	localip="192.168.1.1"
fi

port_for_distribute_app=$2
