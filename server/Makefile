client: 
	gcc sqlite_db.c ssl_common.c ssl_client.c -g -o ssl_client -lssl -lcrypto -ldl -lsqlite3

server:
	gcc sqlite_db.c ssl_common.c ssl_server.c -g -o ssl_server -lssl -lcrypto -ldl -lpthread -lsqlite3

all: client server


clean:
	rm -f ssl_client ssl_server


.PHONY: all clean client server

