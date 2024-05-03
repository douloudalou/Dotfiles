#!/bin/bash

read -p "tar file: " tarFile

read -p "$tarFile CONFIRM:[Y/n] " fileCheck

if [[ "$fileCheck" == "" || "${fileCheck^^}" == "Y" ]] 
	then
		sudo mkdir ~/Downloads/tmp/
		tar -xvf ~/Downloads/$tarFile.tar.gz -C ~/Download/tmp/
		folder=("~/Downloads"/*)
		echo $folder
		rm -rf ~/Downloads/tmp/
fi
