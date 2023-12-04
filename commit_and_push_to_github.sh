#!/bin/bash

# this is the file to use in order to commit new changes to the github repo. 
# The reason I made this file, is because the log files need to be excluded using the git option
# git reset -- logs/*

function helpFunction() {
    echo ""
    echo "Use: $0 -m commit_message"
    echo ""
    echo "Description: This script is used to update the gatewa-services code to Github while avoiding to upload the log files."
    echo ""
    echo "Options:"
    echo "-m commit_message      Message to save with the commit."
    echo ""
    exit 1
}


echo "enter a message that describes the commit:"
read commit_msg
git add .
git reset -- single_transport/backend/logs/*
git commit -m "$commit_msg"
git push 

# this gets the version number stored in the variable "GATEWAY_VERSION" in the python script.
version=$(grep "GATEWAY_VERSION" single_transport/backend/global_vars.py  |  tr '="' "\n" | head -n 3 | tail -n 1)
if [[ $(git tag | grep $version | wc -l) -eq 0 ]]; then 
    # now it means that the release or tag is new, and should be sent.
    release=false

    if [[ $(git tag | grep ${version:0:6} |wc -l) -eq 0 ]]; then
        release=true  # it is a new tag, okay. But it is a new release? Are the first 3 numbers really new?
        echo "enter a message that describes the new release"
    else
        echo "enter a message that describes the new tag"
    fi

    
    read rel_msg
    git tag -a "v$version" -m "$rel_msg"
    git push origin --tags       

    if [ $release = true ]; then
        gh release create "v$version" -t "v$version" -p -n "$rel_msg"
    fi
    
fi



