#!/bin/bash

read -p "Update? [Local/Server]: " location

if [[ "$location" = "Local" ]];then
	cp -r ~/Dotfiles/* ~/.config/
else 
	cp -r ~/.config/* ~/Dotfiles/
fi

echo "------DONE------"
