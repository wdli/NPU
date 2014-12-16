#!/bin/bash
#
# Monitor and restart the ssl_server if it's dead
#

LOG="./ssl_server_monitor.log"
SLEEP_TIME=60

function log()
{
    MSG=$1
    TIME=$(date)

    echo "$TIME Logging message: $MSG"
    echo ""
    echo "$TIME: $MSG">>$LOG
    
    return
}


function ssl_server_monitor()
{
    SSL_SERVER_PID=$(pidof ssl_server)
    if [ -z ${SSL_SERVER_PID} ]; then
	log "No ssl_server running, restart it"  
  	./ssl_server 
	wait
        log "New ssl_server id is: $(pidof ssl_server)" 
	return
    fi

    log "ssl_server id is runing: ${SSL_SERVER_PID}"
    return

    #kill -s SIGTERM ${SSL_SERVER_PID}
    #sleep 10 

    #SSL_SERVER_PID=$(pidof ssl_server)
    #[ -z ${SSL_SERVER_PID} ] && { echo "ssl_server killed"; ./ssl_server; exit; }
    #echo "For some reason it's still running: ${SSL_SERVER_PID}"
}



#
# Main
#
echo "start monitoring" > $LOG

while true
do
    ssl_server_monitor
    sleep $SLEEP_TIME
done

log "$FUNCNAME: end monitoring"

