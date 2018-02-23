#!/bin/bash

function init(){
    WEBHOME="/home/xxx/overview"
    WEBSOURCE="${WEBHOME}/overview_agent.py"
    WEBLOGDIR="${WEBHOME}/log"
    WEBLOGFILE="${WEBLOGDIR}/web.log"
    WEBTEMPDIR="${WEBHOME}/tmp"
    PIDFILE="${WEBTEMPDIR}/pidfile"
    [ ! -d ${WEBHOME} ] && {
        mkdir ${WEBHOME}
    }
    [ ! -d ${WEBTEMPDIR} ] && {
        mkdir ${WEBTEMPDIR}
    }
    [ ! -d ${WEBLOGDIR} ] && {
        mkdir ${WEBLOGDIR}
    }
}

function start(){
   if [ -f "$PIDFILE" ];then
       echo "$0 is running!"
       exit 1
   fi
   nohup /usr/bin/python "$WEBSOURCE" &> /dev/null &
   touch $PIDFILE
   [ $? -eq 0 ] && {
       echo "$0 start !"
   }
}

function stop(){
    if [ ! -f "$PIDFILE" ];then
       echo "$0 not running!"
       exit 1
    else
        ps -ef | grep "overview_agent.py" | egrep -v "egrep" | awk '{print $2}' | xargs kill -9
        /bin/rm -f "$PIDFILE"
        [ $? -eq 0 ] && {
           echo "$0 stop !"
       }
    fi
}

function restart(){
    stop
    sleep 1
    start
}

function main(){
    init
    [ $# -ne 1 ] && {
        echo "args error"
        exit 3
    }
    case "$1" in
        start)
            start
        ;;
        stop)
                stop
        ;;
        restart)
            restart
        ;;
        *)
            echo "{$0 USE:start|stop|restart}"
        ;;
    esac
}
main "$@"
