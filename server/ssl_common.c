#include "ssl_common.h"

static MUTEX_TYPE *mutex_buf;

/*
 * handle_error
 */
void handle_error(const char* file, int lineno, const char* msg)

{
  fprintf(stderr, "%s %i, %s\n", file, lineno, msg);
  ERR_print_errors_fp(stderr);

}


/*
 * init_openSSL
 */
void init_OpenSSL(void)
{

  //  where is THREAD_SETUP? 
  if(!THREAD_SETUP){
    fprintf(stderr, "Pthread init failed\n");
    exit(-1);
  }
  OPENSSL_init_library();
  SSL_load_error_strings();
}


/*
 * locking_function callback
 *
 * mode - CRYPTO_LOCK
 * n    - nth mutex
 *
 */
static void locking_function(int mode, int n, const char* file, int lineno)
{
  if (mode & CRYPTO_LOCK) {
    MUTEX_LOCK(mutex_buf[n]);
  }
  else {
    MUTEX_UNLOCK(mutex_buf[n]);
  }
}


/*
 * id_function callback
 */
static unsigned long id_function(void)
{
  return ((unsigned long)THREAD_ID);
}



/*
 * THREAD_setup
 */
int THREAD_setup(void)
{

  int i;
  int numlocks;
  
  numlocks  = CRYPTO_num_locks();
  mutex_buf = (MUTEX_TYPE *)malloc(numlocks * sizeof(MUTEX_TYPE));

  if (!mutex_buf)
    return 0;

  for ( i = 0; i < numlocks; i++) {
    MUTEX_SETUP(mutex_buf[i]);
  }

  CRYPTO_set_id_callback(id_function);
  CRYPTO_set_locking_callback(locking_function);
  
  return 1;
}


/* 
 * THREAD_cleanup
 */

int THREAD_cleanup(void)
{
  int i;

  if (!mutex_buf)
    return 0;

  CRYPTO_set_id_callback(NULL);
  CRYPTO_set_locking_callback(NULL);
  
  for (i = 0; i < CRYPTO_num_locks(); i++) {
    MUTEX_CLEANUP(mutex_buf[i]);
  }
  free(mutex_buf);
  mutex_buf = NULL;
  return 1;
}
