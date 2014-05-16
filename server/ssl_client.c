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
 * setup_client_txt
 */
static SSL_CTX * setup_client_ctx(void)
{

  SSL_CTX * ctx;
  
  ctx = SSL_CTX_new(SSLv23_method());
  
  // For now we don't ask client to use certificate
  return ctx;

}


/* 
 * do_client_loop
 */

static int
do_client_loop(SSL * ssl)
{
  int err, nwritten;
  char buf[80];

  for (;;) {

    memset(buf,0, sizeof(buf));

    if (!fgets(buf, sizeof(buf), stdin))
      break;

    fprintf(stderr, "Done input: len %d, %s", strlen(buf), buf);

    for (nwritten = 0; nwritten < strlen(buf); nwritten += err){

      err = SSL_write(ssl, buf + nwritten, strlen(buf) - nwritten);

      printf("Done sending\n");

      if (err < 0){
	fprintf(stderr, "Error in SSL write\n");
	return 0;
      }

    }
  }

  return 1;
}


/* 
 * main
 */

int main(int argc, char* argv[])
{

  BIO * conn;
  SSL * ssl;
  SSL_CTX * ctx;

  init_OpenSSL();
  ctx = setup_client_ctx();
  
  conn = BIO_new_connect("127.0.0.1" ":" PORT);

  if (!conn) {
    int_error("Error creating connection BIO");
  }

  if (BIO_do_connect(conn) <= 0) {
    int_error("Error connecting to the remote machine");
  }

  if (!(ssl = SSL_new(ctx))) {
    int_error("Error creating new SSL object");
  }

  SSL_set_bio(ssl, conn, conn);

  //
  // SSL handshake
  //
  if (SSL_connect(ssl) <= 0) {
    int_error("Error creating SSL connection");
  }
    
  fprintf(stderr, "Connection from client opened\n");
  if (do_client_loop(ssl)) {
    SSL_shutdown(ssl);
  }
  else {
    SSL_clear(ssl);
  }

  fprintf(stderr, "Connection from client closed\n");

  SSL_free(ssl);
  SSL_CTX_free(ctx);

  BIO_free(conn);

  return 0;

}
