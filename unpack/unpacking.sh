#!/bin/bash

helpInform="This script requires a name of tar file to load container.i.e. ./unpacking.sh 514yie3"
tarName=$1
if [ "$tarName" == "" ] 
then echo $helpInform
else
	echo "Loading "${tarName}"..."
	cat ${tarName}.tar | docker import - ${tarName}:latest
	echo "Loading "${tarName}" finished"
fi
