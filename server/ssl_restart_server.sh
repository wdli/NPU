#!/bin/bash
#


SSL_SERVER_PID=$(pidof ssl_server)
[ -z ${SSL_SERVER_PID} ] && { echo "No ssl_server running"; exit; }

echo "ssl_server id is: ${SSL_SERVER_PID}"

kill -s SIGTERM ${SSL_SERVER_PID}
sleep 10 

SSL_SERVER_PID=$(pidof ssl_server)
[ -z ${SSL_SERVER_PID} ] && { echo "ssl_server killed"; exit; }
echo "For some reason it's still running: ${SSL_SERVER_PID}"

 
