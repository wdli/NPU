client: 
	gcc -g -o ssl_client -lssl ssl_common.c ssl_client.c

server:
	gcc -g -o ssl_server -lssl ssl_common.c ssl_server.c

all: client server

clean:
	rm -f *.o
