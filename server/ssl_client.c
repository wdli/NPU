/*
 * ssl_client.c
 *
 * Simple SSL client
 *
 * Create 5/12/14
 *
 * Usage:
 *      
 *
 * Bug: Need to press Enter twice for the server to display messages
 *
 */

#include "ssl_common.h"

/* 
 * do_client_loop
 */

static void 
do_client_loop(BIO* conn)
{
  int err, nwritten;
  char buf[80];

  for (;;) {

    memset(buf,0, sizeof(buf));

    if (!fgets(buf, sizeof(buf), stdin))
      break;

    fprintf(stderr, "Done input: len %d, %s", strlen(buf), buf);

    for (nwritten = 0; nwritten < strlen(buf); nwritten += err){

      err = BIO_write(conn, buf + nwritten, strlen(buf) - nwritten);
      BIO_flush(conn);
      printf("Done sending\n");

      if (err < 0){
	fprintf(stderr, "Error in bio write\n");
	return;
      }

    }
  }

}


/* 
 * main
 */

int main(int argc, char* argv[])
{

  BIO * conn;

  init_OpenSSL();
  
  conn = BIO_new_connect("127.0.0.1" ":" PORT);

  if (!conn) {
    int_error("Error creating connection BIO");
  }

  if (BIO_do_connect(conn) <= 0) {
    int_error("Error connecting to the remote machine");
  }
  
  fprintf(stderr, "Connection from client opened\n");
  do_client_loop(conn);
  fprintf(stderr, "Connection from client closed\n");
  
  BIO_free(conn);

  return 0;

}
