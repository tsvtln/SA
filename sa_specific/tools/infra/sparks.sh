#!/bin/sh

usage() {
  cat <<EOF
Command line sparks utility.  Is built around the 'curl' utility.  Maintains
session state using the following two special files:

  o ~/.sparks_cookies
  o ~/.sparks_trans

Usage:

  $0 login <username>
    Logs into sparks.  Will prompt for username/password if not otherwise 
    provided.  Can use env vars SPARKS_USERNAME and SPARKS_PASSWORD.

  $0 logout
    Logs out of sparks.

  $0 query -p <product name>
    Submits a search query to sparks.

  $0 dump_all_items
    Dumps a printout of each item in the results set of a previous call to 
    "query".

Example:

> ./sparks login
username: david.west@hp.com
password: 
Login Successful
> ./sparks query -p "server automation"
> ./sparks dump_all_items
1 2 3 4 5 6 7 8 ^C
> ./sparks logout
Logout Successful
> 

EOF
}

eval COOKIE_FILE=~'/.sparks_cookies'
eval TRANS_FILE=~'/.sparks_trans'
eval OUT_FILE=~'/.sparks_last_out'
eval HEADERS_FILE=~'/.sparks_last_out_headers'

submit_post() {
#  echo "$1" 
  rm "$OUT_FILE" 2>/dev/null
  echo -n "$1" | curl -s -L -H 'Expect:' -D "$HEADERS_FILE" -b "$COOKIE_FILE" -c "$COOKIE_FILE" -d @- 'http://hpsw-support-web.austin.hp.com/sc/detail.do' -o "$OUT_FILE"
#  echo DEBUG: $?
  if { [ $? -ne 0 ]; } then {
    echo Error:
    echo last headers:
    cat "$HEADERS_FILE"
  } fi
}

submit_get() {
  rm "$OUT_FILE" 2>/dev/null
  curl -e ';auto' -L -s -D "$HEADERS_FILE" -b "$COOKIE_FILE" -c "$COOKIE_FILE" "$1" -o "$OUT_FILE"
  if { [ $? -ne 0 ]; } then {
    echo Error:
    echo last headers:
    cat "$HEADERS_FILE"
  } fi
}

echo_off() {
  stty -echo
}

echo_on() {
  stty echo
}

inc_trans() {
  if { [ -e "$TRANS_FILE" ]; } then {
    TRANS=`cat "$TRANS_FILE"`
  } else {
    TRANS=0
  } fi
  TRANS=$(($TRANS+1))
  echo -n $TRANS > "$TRANS_FILE"
}

login() {
  # Check for in progress login session.
  if { [ -e "$TRANS_FILE" ]; } then {
    echo $0: Login session already in progress.  invoke '"'$0 logout'"' first.
    exit 1
  } fi

  if { [ "$1" ]; } then {
    SPARKS_USERNAME="$1"
  } fi
  if { [ \! "$SPARKS_USERNAME" ]; } then {
    echo -n 'username: '
    read SPARKS_USERNAME
  } fi
  trap echo_on 3
  if { [ \! "$SPARKS_PASSWORD" ]; } then {
    echo_off
    echo -n 'password: '
    read SPARKS_PASSWORD
    echo ''
  } fi
#  echo DEBUG: $SPARKS_USERNAME, $SPARKS_PASSWORD

  SPARKS_USERNAME="`echo $SPARKS_USERNAME | perl -pe 's/@/%40/g'`"

  submit_get 'http://hpsw-support-web.austin.hp.com/sc/index.do'

  inc_trans

  login_post="row=&__x=&essuser=false&event=0&transaction=${TRANS}&type=detail&focus=var%2Fold.password&focusContents=&focusId=X11&focusReadOnly=false&start=&count=&window=&close=&_blankFields=&_uncheckedBoxes=&formchanged=&formname=login.prompt.g&var%2Fuser.id=${SPARKS_USERNAME}&var%2Fold.password=${SPARKS_PASSWORD}&=&="

  submit_post "$login_post"

  if { [ "`grep 'Main Menu' $OUT_FILE`" ]; } then {
    echo Login Successful
  } else {
    echo $0: Login Failed
    rm "$TRANS_FILE"
  } fi
}

assert_logged_in() {
  # If there isn't a currently active session.
  if { [ \! -e "$TRANS_FILE" ]; } then {
    echo $0: No current login session detected.  invoke '"'$0 login'"' first.
    exit 1
  } fi
}

assert_out_file() {
  if { [ \! -e "$OUT_FILE" ]; } then {
    echo $0: Previous HTTP request had no output.  Login session may have timed out.
    exit 1
  } fi
}

logout() {
  assert_logged_in

  inc_trans

  logout_post1="row=&__x=&essuser=false&event=3&transaction=${TRANS}&type=detail&focus=&focusContents=&focusId=&focusReadOnly=&start=&count=&window=&close=&_blankFields=&_uncheckedBoxes=&formchanged=&formname=hpsw.menu.gui.user.g"

  submit_post "$logout_post1"

  inc_trans

  logout_post2="row=&__x=&essuser=false&event=3&transaction=${TRANS}&type=detail&focus=var%2Fold.password&focusContents=&focusId=&focusReadOnly=&start=&count=&window=&close=&_blankFields=&_uncheckedBoxes=&formchanged=&formname=menu.gui.logout&=&="

  submit_post "$logout_post2"

  if { [ "`grep 'Logout Successful' $OUT_FILE 2>/dev/null | perl -pe 's/(Logout Successful)/\1/'`" ]; } then {
    echo Logout Successful
  } else {
    echo $0: Error occured during logout, flushing client-side session state anyway.
  } fi

  # Remove the current session file.
  rm "$TRANS_FILE"
}

get_messages() {
  assert_logged_in

  submit_get "http://hpsw-support-web.austin.hp.com/sc/service.do?name=getMessages&timestamp='"

  assert_out_file

  cat $OUT_FILE
  echo ''
}

query() {
  assert_logged_in
#  echo DEBUG: '$1:' "$1"
  while [ "$1" ]
  do
    arg="$1"
    shift
    val="$1"
    shift
#    echo DEBUG: $arg, $val
    val="`echo $val | perl -pe 's/ /+/g'`"
    case "$arg" in
      -p)
        PRODUCT="$val"
        ;;
      *)
        echo $0: arg=$arg, val=$val: argument pair not recognized, skipping
        ;;
    esac
  done

#  p0="event=3"

  p1="row=&__x=&essuser=false&event=2&transaction=${TRANS}&type=detail&focus=&focusContents=&focusId=&focusReadOnly=&start=&count=&window=&close=&_blankFields=&_uncheckedBoxes=&formchanged=&formname=hpsw.menu.gui.user.g"

  p2="row=&__x=&essuser=false&event=7&transaction=${TRANS}&type=list&focus=&focusContents=&focusId=&focusReadOnly=&start=0&count=1&window=&close=&_blankFields=&_uncheckedBoxes=&formchanged=&formname=hpsw.sc.manage.incident.g&var%2FL.inbox=Open+Incidents+Owned+by+or+Assigned+To+Me"

  p3="row=&__x=&essuser=false&event=6&transaction=${TRANS}&type=detail&focus=var%2Fsearch.open.flag&focusContents=open&focusId=X10&focusReadOnly=false&start=&count=&window=&close=&_blankFields=&_uncheckedBoxes=&formchanged=&formname=apm.search.probsummary.g&var%2Fsearch.open.flag=either&instance%2Fhpsw.wfm.id=&instance%2Fnumber=&instance%2Fhpsw.tam=&instance%2Fcompany=&instance%2Fticket.owner=&instance%2Fhpsw.said.no=&instance%2Fcontact.name=&instance%2Fassignment=&instance%2Fcontact.email=&instance%2Fassignee.name=&instance%2Falternate.contact=&instance%2Fhpsw.level1.group=&instance%2Fhpsw.product=${PRODUCT}&instance%2Fhpsw.level1.assignee=&instance%2Fversion=&instance%2Fhpsw.level2.group=&instance%2Fhpsw.subproduct=&instance%2Fhpsw.level2.assignee=&instance%2Fhpsw.product.extension=&instance%2Fhpsw.level3.group=&instance%2Fhpsw.level3.assignee=&instance%2Fproblem.status=&instance%2Fhpsw.level4.group=&instance%2Fstatus=&instance%2Fhpsw.level4.assignee=&instance%2Fseverity=&instance%2Fhpsw.ele.status=&instance%2Fcause.code=&instance%2Fhpsw.ele.cs.followup.mgr=&instance%2Fresolution.code=&instance%2Fhpsw.external.system.id=&instance%2Foperating.system=&var%2Fsmart.search=true&var%2Fpmc.open.after=&var%2Fpmc.open.before=&instance%2Fopened.by=&var%2Fpmc.update.after=&var%2Fpmc.update.before=&instance%2Fupdated.by=&var%2Fpmc.close.after=&var%2Fpmc.close.before=&instance%2Fclosed.by="

  # Cancel any previous search.  (This can only occur after a search has already occured.)
#  submit_post "$p0"

  # Load search page.
  inc_trans
  submit_post "$p1"
  inc_trans
  submit_post "$p2"

  # Submit search query.
  inc_trans
  submit_post "$p3"

#  echo Num of records returned:
#  count
#  echo ''
}

count() {
  assert_logged_in

  inc_trans
  submit_get "http://hpsw-support-web.austin.hp.com/sc/detail.do?row=0&essuser=false&event=5100&transaction=${TRANS}&type=detail&start=0&count=32"

  nCount=`cat $OUT_FILE | grep 'records in this list' | perl -pe '/ are (\d+) records /;$_="$1"'`

  echo -n $nCount
}

get_item() {
  assert_logged_in

  submit_get "http://hpsw-support-web.austin.hp.com/sc/printDetail.do?row=${1}"
  cat $OUT_FILE
}

dump_all_items() {
  assert_logged_in

  n=1
  cont=1
  while [ $cont ]
  do
    if { [ $n -gt 2 ]; } then {
      if { [ \! "`diff $(($n-2)).html $(($n-1)).html`" ]; } then {
        cont=''
      } fi
    } fi
    echo -n "$n "
    get_item $n | perl -pe 's/&amp;/&/g' > "${n}.html"
    n=$(($n+1))
  done
}

case "$1" in
  login)
    shift
    login "$@"
  ;;
  logout)
    logout
  ;;
  get_messages)
    get_messages
  ;;
  query)
    shift
    query "$@"
  ;;
  count)
    count
  ;;
  get_item)
    shift
    get_item "$@"
  ;;
  dump_all_items)
    dump_all_items
  ;;
  *)
    usage
  ;;
esac

