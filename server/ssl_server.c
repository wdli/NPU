#include "ssl_common.h"


/*
 * server loop
 */
static void do_server_loop(BIO * conn)
{
  int done, err, nread;
  char buf[80];

  do {
    for (nread = 0; nread < sizeof(buf); nread += err) {
      err = BIO_read(conn, buf+nread, sizeof(buf) - nread);
      
      if (err <= 0) {
	break;
      }

      fwrite(buf, 1, nread, stdout);
    } 
  }while (err > 0);

}



/*
 * server_thread
 */
void * ssl_server_thread(void * arg)
{
  BIO * client = (BIO*) arg;
  fprintf(stderr,"SSL server connection opened\n");
  
  do_server_loop(client);
  fprintf(stderr,"SSL server connection closed\n");

  BIO_free(client);
  ERR_remove_state(0);// free a current thread error queue

}


/*
 * main
 */

int main(int argc, char * argv[])
{
  
  BIO * acc, * client;
  THREAD_TYPE tid;
  
  char * port = PORT; // BIO_new_accept takes only a string for port number


  init_OpenSSL();
  
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
    
    client = BIO_pop(acc);
    THREAD_CREATE(tid, &ssl_server_thread, client);
    
  }

  BIO_free(acc);
  return 0;

}
