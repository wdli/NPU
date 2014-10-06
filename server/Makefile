client: 
	gcc ssl_common.c ssl_client.c -g -o ssl_client -lssl -lcrypto -ldl 

server:
	gcc ssl_common.c ssl_server.c -g -o ssl_server -lssl -lcrypto -ldl -lpthread

all: client server


clean:
	rm -f ssl_client ssl_server


.PHONY: all clean client server

