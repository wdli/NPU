#include <openssl/bio.h>
#include <openssl/err.h>
#include <openssl/rand.h>
#include <openssl/ssl.h>
#include <openssl/x509v3.h>
#include <openssl/crypto.h>

#include <pthread.h>


// pthread stuff

#define MUTEX_TYPE pthread_mutex_t
#define MUTEX_SETUP(x) pthread_mutex_init(&(x), NULL)
#define MUTEX_CLEANUP(x) pthread_mutex_destroy(&(x))
#define MUTEX_LOCK(x) pthread_mutex_lock(&(x))
#define MUTEX_UNLOCK(x) pthread_mutex_unlock(&(x))
#define THREAD_ID pthread_self()




#define THREAD_SETUP THREAD_setup()
#define THREAD_CLEANUP THREAD_cleanup()

#define THREAD_TYPE pthread_t
#define THREAD_CREATE(tid, entry, arg) pthread_create(&(tid), NULL, (entry), (arg))

// port server, client addresses

#define PORT "6001"
#define SERVER localhost
#define CLIENT localhost

#define int_error(msg) handle_error(__FILE__,__LINE__,msg)

void handle_error(const char * file, int lineno, const char* msg);

void init_OpenSSL(void);

int THREAD_setup(void);
int THREAD_cleanup(void);
