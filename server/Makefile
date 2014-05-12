client: 
	gcc -g -o ssl_client -lssl ssl_common.c ssl_client.c

server:
	gcc -g -o ssl_server -lssl ssl_common.c ssl_server.c

all: client server

.PHONY: all

clean:
	rm -f ssl_client ssl_server
