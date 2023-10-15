#!/bin/bash
#This script completely revokes all permissions that have been
#granted with the aaa shell-perm grant command

#IFS is a bash environment variable that tells bash how to delineate
#this tells them to delineate ‘line feed’, ‘carriage return’
#use this because the usergroups include spaces and whitespace is
#part of the default dilineater in BASH
IFS=$'\x0A'$'\x0D'
grouplist=`ls /opsw/Permissions/UserGroups`
permslist=`ls /opsw/Permissions/info`

for K in $grouplist
do
    for L in $permslist
    do
       aaa shell-perm revoke -o $L -u "$K"
    done
done
