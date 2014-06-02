/*
 * ssl_server.c
 *
 * Simple SSL server
 *
 * Create 5/14/14
 *
 * Usage:
 *
 *
 */

#include "ssl_common.h"


#define SERVERCERT "servercert2.pem"
#define CAFILE "root.pem"
#define CADIR NULL

/*
 * setup_server_ctx
 */
static SSL_CTX * setup_server_ctx(void)
{
  SSL_CTX *ctx;

  ctx = SSL_CTX_new(SSLv23_method()); // handle only SSL v2 and v3
  if (!ctx) {
    int_error("Error in creating SSL ctx\n");
    return 0;
  }
  
  // loading CA
  //
  fprintf(stderr,"Loading CA certificate %s\n", CAFILE);
  if (SSL_CTX_load_verify_locations(ctx, CAFILE, CADIR) != 1) {
    int_error("Error loading CA file");
  }

  /*
  if (SSL_CTX_set_default_verify_paths(ctx) != 1){
    int_error("Error loading default CA ");
  }
  */

  // loading server cert
  // 
  fprintf(stderr,"Loading server certificate %s\n", SERVERCERT);
  if (SSL_CTX_use_certificate_chain_file(ctx,SERVERCERT) != 1) {
    int_error("Error loading server certificate");
  }
  
  fprintf(stderr,"Loading server private key\n");
  if (SSL_CTX_use_PrivateKey_file(ctx, SERVERCERT, SSL_FILETYPE_PEM) != 1) {
    int_error("Error Loading server private key");
  }

  // how to verify
  //
  fprintf(stderr,"Set client verification policy\n");
  SSL_CTX_set_verify(ctx, SSL_VERIFY_PEER /* |SSL_VERIFY_FAIL_IF_NO_PEER_CERT */,
		     verify_callback);
  
  SSL_CTX_set_verify_depth(ctx, 4);
  
  return ctx;

}


/*
 * server loop
 */

static int  do_server_loop(SSL * ssl)
{
  int done, err, nread;
  char buf[80];

  fprintf(stderr, "server loop\n");

  do {
    for (nread = 0; nread < sizeof(buf); nread += err) {

      err = SSL_read(ssl, buf+nread, sizeof(buf) - nread);

      if (err <= 0) {
	break;
      }

      fwrite(buf, 1, nread, stdout);
      fflush(stdout);

    } 
  } while (err > 0);

  return (SSL_get_shutdown(ssl) & SSL_RECEIVED_SHUTDOWN) ? 1:0;
}



/*
 * server_thread
 */
void * ssl_server_thread(void * arg)
{
  // BIO * client = (BIO*) arg;
  SSL * client = (SSL*) arg;

  //
  // SSL handshake
  // 
  if (SSL_accept(client) <= 0) {
    int_error("Error accepting SSL connection");
  }

  fprintf(stderr, "Post connection check\n");
  post_connection_check(client, "localhost");

  // TBD post_connection_check
  
  fprintf(stderr,"SSL server connection opened\n");
  
  if (do_server_loop(client)) {
    SSL_shutdown(client);
  }
  else {
    SSL_clear(client);
  }

  fprintf(stderr,"SSL server connection closed\n");

  // BIO_free(client);
  SSL_free(client);
  ERR_remove_state(0);// free a current thread error queue

}


/*
 * main
 */

int main(int argc, char * argv[])
{
  
  BIO * acc, * client;
  SSL *ssl;
  SSL_CTX *ctx;
  THREAD_TYPE tid;
  
  char * port = PORT; // BIO_new_accept takes only a string for port number


  init_OpenSSL();

  // set up server's SSL context  
  ctx = setup_server_ctx();

  // create ssl socket
  acc = BIO_new_accept(port);
  if (!acc) {
    int_error("Error creating SSL server socket");
  }
  
  // bind the ssl socket to the port
  if (BIO_do_accept(acc) <= 0) {
    int_error("Error binding SSL server socket");
  }

  // forever loop
  for (;;) {

    if (BIO_do_accept(acc) <= 0 ) {
      int_error("Error SSL server accepting connection");
    }
    fprintf(stderr,"Accepted a connection from client\n");

    client = BIO_pop(acc);
    if ( !(ssl = SSL_new(ctx))) {
      int_error("Error creating SSL object");
    }
    fprintf(stderr,"Popped a client BIO object\n");

    SSL_set_accept_state(ssl);
    SSL_set_bio(ssl, client, client);

    fprintf(stderr,"Creating a server thread to handle client request\n");
    THREAD_CREATE(tid, &ssl_server_thread, ssl);
    
    
  }

  SSL_CTX_free(ctx);
  BIO_free(acc);
  return 0;

}
