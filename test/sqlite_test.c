#include <stdio.h>
#include <time.h>
#include <sqlite3.h>
#include <string.h>

#define DB_NAME "test.db"
#define TABLE_NAME "CS535_STUDENT_FALL14"

static int callback(void *notused, int argc, char **argv, char **azColName)
{
	int i;
        for (i=0; i<argc; i++) {
	     
             fprintf(stderr, "%s = %s\n", azColName[i], argv[i] ? argv[i]: "NULL");
         }
         fprintf(stderr, "\n");
         return 0;
}


static int exec_sql_db(sqlite3 *db, char * sql)
{
   	char * errmsg;
	int rc;
        
	fprintf(stderr,"SQL statement: %s\n", sql);
	if (sqlite3_exec(db, sql, callback, 0, &errmsg) != SQLITE_OK) {
		fprintf(stderr, "%s SQL error: %s\n", __FUNCTION__,errmsg);
		sqlite3_free(errmsg);
		return -1;
	}
        else {
                fprintf(stderr, "SQL statement executed OK!\n");
        }
        return 0;

}

static int open_db(sqlite3 **db, char * name)
{

	char *zErrMsg = 0;
	int rc;
	rc = sqlite3_open(name,db);
	if (rc ){
		fprintf(stderr, "Can't open database: %s\n", sqlite3_errmsg(*db));
	        return -1;	
        }
	else {
                fprintf(stderr, "Database opened!\n");
        }
        return 0;
}


static void close_db(sqlite3 *db)
{

	sqlite3_close(db);
        fprintf(stderr, "Database closed\n");
}


int main(int argc, char* argv[])
{
	sqlite3 *db;
        int rc;
        
	// fake records
	int id1 = 1234;
	int id2 = 4556;
        time_t now;
		
        char sql_statement[256];

        // open DB 
        if (open_db(&db, DB_NAME) < 0 ) {
                 fprintf(stderr, "open_db failed\n");
        }

        /* create SQL table if the table doesn't exist in the db*/
        sprintf(sql_statement, "CREATE TABLE IF NOT EXISTS " TABLE_NAME  "(ID INT PRIMARY KEY NOT NULL,TIME CHAR(128));");
      
        if (exec_sql_db(db, sql_statement) < 0 ) {
               return 0;
        }
        // Insert into the table
        time(&now);
        char* ins_time = ctime(&now);

        memset(sql_statement, 0, 256);
	sprintf(sql_statement, "INSERT INTO " TABLE_NAME " (ID, TIME)  VALUES ( %d , '%s' );", id1, ins_time ); 	
        exec_sql_db(db, sql_statement);

	// Close DB 
        close_db(db);

        return 0;
}
