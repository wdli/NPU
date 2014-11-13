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

//#define CLIENTCERT "studentcert.pem"

//#define CAFILE "cacertRSA.pem"
//#define CAFILE "cacertRsaFall14.pem"

/* CS535 Fall Project */
#define CLIENTCERT "cs535_student_cert_fall14.pem"
#define CAFILE "cs535_CA_cert_fall14.pem"

#define CADIR NULL

/*
 * setup_client_txt
 */
static SSL_CTX * setup_client_ctx(void)
{

  SSL_CTX * ctx;
  
  ctx = SSL_CTX_new(SSLv23_method());
  if (!ctx) {
    int_error("Error in creating client SSL CTX\n");
  }

  fprintf(stderr,"Loading CA certificate %s\n",CAFILE);
  if (SSL_CTX_load_verify_locations(ctx, CAFILE, CADIR) != 1) {
    int_error("Error loading CA file");
  }
  
  
  fprintf(stderr,"Loading client certificate %s\n",CLIENTCERT);
  if (SSL_CTX_use_certificate_chain_file(ctx, CLIENTCERT) != 1) {
    int_error("Error in loading client cert file");
  }

  fprintf(stderr,"Loading client key\n");
  if (SSL_CTX_use_PrivateKey_file(ctx, CLIENTCERT, SSL_FILETYPE_PEM) != 1){
    int_error("Error in loading client key");
  }

  // how to verify
  //
  fprintf(stderr,"Set server verification policy\n");
  SSL_CTX_set_verify(ctx, SSL_VERIFY_PEER /* |SSL_VERIFY_FAIL_IF_NO_PEER_CERT */,
		     verify_callback);
  
  SSL_CTX_set_verify_depth(ctx, 4);
    

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
  char server_IP[20];

  if (!argv[1]) {
    printf ("No server IP address\n");
    return -1;
  }
  memset(server_IP,0,10);
  strcpy(server_IP, argv[1]);
  printf (" Server IP is %s\n", server_IP);
  
  /* Init SSL and CTX*/
  init_OpenSSL();
  ctx = setup_client_ctx();

  strcat(server_IP,":");
  strcat(server_IP,PORT);
  printf ("Connecting to %s\n", server_IP);

  conn = BIO_new_connect(server_IP);

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

  // TBD: post connection check

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
