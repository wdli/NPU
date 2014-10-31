#ifndef _SQLITE_DB_H_
#define _SQLITE_DB_H_

#include <sqlite3.h>
#include <string.h>


#define DB_NAME "CS535.db"
#define TABLE_NAME "CS535_FALL14"

//
// opent the db
//
int open_db(sqlite3 **db, char * name);

//
// close the db
// 
void close_db(sqlite3 *db);

//
// execute the sql query 
//

int exec_sql_db(sqlite3 *db, char * sql);


#endif
