#include <stdio.h>
#include <sqlite3.h>


#define DB_NAME "test.db"


static int callback(void *notused, int argc, char **argv, char **azColName)
{
	int i;
        for (i=0; i<argc; i++) {
	     
             fprintf(stderr, "%s = %s\n", azColName[i], argv[i] ? argv[i]: "NULL");
         }
         fprintf(stderr, "\n");
         return 0;
}


static int create_db_table(sqlite3 *db, char * sql)
{
   	char * errmsg;

	if (sqlite3_exec(db, sql, callback, 0, &errmsg) != SQLITE_OK) {
		fprintf(stderr, "%s SQL error %s\n", __FUNCTION__,errmsg);
		sqlite3_free(errmsg);
		return -1;
	}
        else {
                fprintf(stderr, "Table created OK!\n");
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

        char * sql_statement;

        // open DB 
        if (open_db(&db, DB_NAME) < 0 ) {
                 fprintf(stderr, "open_db failed\n");
        }

        /* create SQL statement */
        sql_statement = "CREATE TABLE CS535_STUDENT_FALL14(" \
                        "ID INT PRIMARY KEY NOT NULL," \
                        "TIME REAL);";
      
        create_db_table(db, sql_statement); 

	// Close DB 
        close_db(db);

        return 0;
}
