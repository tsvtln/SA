#! /bin/sh
 
# for each permission, find the longest token
PERMISSIONS=`ls /opsw/Permissions/info/`
PERMLEN=""
for P in "--------------- --------------- User Group" ${PERMISSIONS} ; do
        PERM=`echo $P | sed -e 's/\([A-Z]\)/ \1/g'`
        L=`echo $PERM | \
                awk '
                        BEGIN {
                                L=0
                        }
                        {
                                for (n=1 ; n<=NF ; n++) {
                                        if (length($n) > L) L=length($n)
                                }
                        }
                        END { print L }'`
        PERMLEN="${PERMLEN} ${P}:${L}"
done
 
# find the number of rows (ROWCOUNT) to print for the header
ROWCOUNT=0
for P in ${PERMISSIONS} ; do
        PERM=`echo $P | sed -e 's/\([A-Z]\)/ \1/g'`
        WC=`echo $PERM | wc -w`
        [ $WC -gt $ROWCOUNT ] && ROWCOUNT=$WC
done
 
# print the header
ROW=1
while [ ${ROW} -le ${ROWCOUNT} ] ; do
        for P in "--------------- --------------- User Group" ${PERMISSIONS} ; do
                PERM=`echo $P | sed -e 's/\([A-Z]\)/ \1/g'`
                WC=`echo $PERM | wc -w`
                [ $WC -gt $ROWCOUNT ] && ROWCOUNT=$WC
                echo $PERM | \
                        awk '
                                BEGIN {
                                        L=0
                                        RC='"${ROWCOUNT}"'
                                        R='"${ROW}"'
                                }
                                {
                                        if (R > RC-NF) TOKEN=$(R-(RC-NF))
                                        for (n=1 ; n<=NF ; n++) {
                                                if (length($n) > L) L=length($n)
                                        }
                                }
                                END { printf("| %-"L"s ", TOKEN) }'
        done
        ROW=`expr $ROW + 1`
        echo "|"
done
 
# terminate the header
for P in "--------------- --------------- User Group" ${PERMISSIONS} ; do
        PERM=`echo $P | sed -e 's/\([A-Z]\)/ \1/g'`
        echo $PERM | \
                awk '
                        BEGIN {
                                L=0
                        }
                        {
                                for (n=1 ; n<=NF ; n++) {
                                        if (length($n) > L) L=length($n)
                                }
                        }
                        END { printf(substr("-----------------------------------------",1,L+3)) }'
done
echo "-"
 
# give me a check mark for each permission granted to each group
for G in `ls /opsw/Permissions/UserGroups | sed -e 's/ /|/'` ; do
        GRP=`echo $G | sed -e 's/|/ /g'`
        echo "$GRP" | awk '{ printf("| %15-s |",substr($0,1,15))}'
        for P in ${PERMISSIONS} ; do
                W=`echo "$PERMLEN" | grep "^${P}" | sed -e "s/${P}://"`
                if [ -f "/opsw/Permissions/UserGroups/${GRP}/operations/$P" ] ; then
                        X="x"
                else
                        X=" "
                fi
                echo ${X} | awk '{ printf(" %-'${W}'s |", $0) }'
        done
        echo ""
done
