#include "ssl_common.h"
#include <time.h>
#include "sqlite_db.h"

static MUTEX_TYPE *mutex_buf;
static sqlite3 * db;




static int record_in_db(char* id, char* ins_time)
{
  char sql_statement[256];

  memset(sql_statement, 0, 256);
  sprintf(sql_statement, "INSERT INTO " TABLE_NAME " (ID, TIME)  VALUES ( %d , '%s' );", atoi(id), ins_time ); 	

  // Try to insert a new record, if not then update
  if ( exec_sql_db(db, sql_statement) < 0) {
    // update
    memset(sql_statement, 0, 256);
    sprintf(sql_statement,"UPDATE " TABLE_NAME " SET TIME = '%s' WHERE ID = %d;",  ins_time, id);
    exec_sql_db(db, sql_statement);
  }              

  display_db(db);
  
  return 0;
}

/*
 * post_connection_check
 */
long post_connection_check(SSL *ssl, const char *host)
{
  X509 *cert;
  X509_NAME * subj;
  char data[256];

  int extcount;
 
  if ( !(cert = SSL_get_peer_certificate(ssl)) || !host ) {
    int_error("Failed to get peer certificate or host");
  }

  //
  // get the extension in the certificate
  //
  if ( extcount = X509_get_ext_count(cert) > 0 ) {
    
    int i;
    for (i = 0; i < extcount; i++) {

      const char * extstr;
      X509_EXTENSION * ext;
      
      ext = X509_get_ext(cert, i);
      extstr = OBJ_nid2sn(OBJ_obj2nid(X509_EXTENSION_get_object(ext)));
      
      fprintf(stderr, " %s\n",extstr);
    }
    
  }// extension

  //
  // Get the CN
  //
  
  memset(data, 0, 256);
  if ((subj = X509_get_subject_name(cert)) &&
      (X509_NAME_get_text_by_NID(subj, NID_commonName, data, 256)) > 0) {
    
    time_t now;
    time(&now);

    data[255] = '\n';
    fprintf(stderr," CN = %s\n", data);
    // Record in file
    fprintf(student_file,"%s CN = %s\n", ctime(&now), data);
    // Record in db
    record_in_db(data, ctime(&now));

    fflush(student_file);
  }
  
  X509_free(cert);
  
  return SSL_get_verify_result(ssl);
}


/*
 * student login record init
 * 
 * We can use a file to store login record and 
 * use a sql database
 *
 */
int login_record_init(void)
{
  
  // Set up a file
   student_file = fopen(STUDENT_LOGIN_RECORD,"w");
   if (!student_file) {
        fprintf(stderr,"Error creating a login record file\n");
        exit(-1);
   }
   fprintf(stderr, "Student login records created %s\n", STUDENT_LOGIN_RECORD);

   // Set up a table in the database
   if (open_db(&db, DB_NAME) < 0 ) {
     fprintf(stderr, "open_db failed!\n");
     return -1;
   }
   fprintf(stderr, "Student login database created %s\n", DB_NAME);

   // Create a table for student records
   char sql_statement[256];
   sprintf(sql_statement, "CREATE TABLE IF NOT EXISTS " TABLE_NAME  "(ID CHAR(10) PRIMARY KEY NOT NULL,TIME CHAR(128));");

   if (exec_sql_db(db, sql_statement) < 0 ) {
     fprintf(stderr,"failed to create table\n");
     return -1;
   }
   fprintf(stderr, "Student login table created %s\n", TABLE_NAME);

   return;
} 

void login_record_cleanup(void)
{
  // clean up the file descriptor 
  fclose(student_file);

  // close the db
  close_db(db);

}

/*
 * verify_callback
 */

int verify_callback(int ok, X509_STORE_CTX *store)
{

  char data[256];
  
  if (!ok) {
    
    X509 *cert = X509_STORE_CTX_get_current_cert(store);
    int depth = X509_STORE_CTX_get_error_depth(store);
    int err = X509_STORE_CTX_get_error(store);
    fprintf(stderr, "Error with certificate at depth: %d\n", depth);

    X509_NAME_oneline(X509_get_issuer_name(cert), data, 256);
    fprintf(stderr," issuer = %s\n", data);

    X509_NAME_oneline(X509_get_subject_name(cert), data, 256);
    fprintf(stderr," subject = %s\n", data);
    fprintf(stderr," err %i:%s\n",err, X509_verify_cert_error_string(err));

  }
  
  return ok;

}

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

  OpenSSL_add_all_algorithms();
  SSL_library_init();
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
