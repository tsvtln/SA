#!/bin/bash

for i in `grep "^mfg:.*DELL.*" */info | cut -d"/" -f1`;
do 

	/bin/echo -n "$i:  "; 
	grep "^serial_num:" $i/info | awk '{ print $2 }';

done
