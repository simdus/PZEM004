#!/bin/bash

NAME=power.py
START=/root/power.sh
GREP=/bin/grep
PS=/bin/ps
NOP=/bin/true
DATE=/bin/date
RM=/bin/rm

$PS -ef|$GREP -v grep|$GREP $NAME >/dev/null 2>&1

case "$?" in
   0)
   # Sluzba funguje neni co delat.
   $NOP
   ;;
   1)
   echo "$NAME =Power= prestala pracovat. Startuji $NAME a posilam zpravu."
   NOTICE=/tmp/watchdog.txt
   echo "$NAME =Hermes= prestala pracovat, byla nastartovana `$DATE`" > $NOTICE
   sendEmail -f watchdog@watchdog.cz -t mail@domain.cz -u "Power crash" -s smtp.gmail.com:587 -xu user@daomain.cz -xp heslo -m < $NOTICE
   $RM -f $NOTICE
   $START 
   ;;
esac

exit

