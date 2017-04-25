#!/bin/bash

helpInform="This script requires a variable as containerId to pack the container.
i.e.
./.packing.sh k2o573zu"
containerId=$1
if [ "$containerId" == "" ]
then 
	echo $helpInform
else
	echo "Packing "$containerId"..."
	docker export $containerId > ${containerId}.tar
	echo "Packing "$containerId" finished"
fi
