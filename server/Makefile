client: 
	gcc -g -o ssl_client -lssl -lcrypto ssl_common.c ssl_client.c

server:
	gcc -g -o ssl_server -lssl -lcrypto ssl_common.c ssl_server.c

all: client server


clean:
	rm -f ssl_client ssl_server


.PHONY: all clean client server

