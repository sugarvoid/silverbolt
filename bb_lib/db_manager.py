
import sqlite3
from sqlite3 import Error
from bb_lib.logger import Logger

class DbManager():
    _connection = None
    _db_file_name: str = "data/courses.db"
    
    @staticmethod
    def connect():
        """ Create a database connection to the SQLite database specified by db_file """
        try:
            DbManager._connection = sqlite3.connect(DbManager._db_file_name)
            Logger.info("connected to db")
            print(f"Connected to {DbManager._db_file_name}")
        except Error as e:
            print(e)

    @staticmethod
    def disconnect():
        """ Close the database connection """
        if DbManager._connection:
            DbManager._connection.close()
            DbManager._connection = None
            print("Database connection closed.")

    @staticmethod
    def execute_query(query, params=None):
        """ Execute a single query """
        if not DbManager._connection:
            raise Error("Database is not connected.")
        
        try:
            cursor = DbManager._connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            DbManager._connection.commit()
            return cursor
        except Error as e:
            print(e)
            return None

    @staticmethod
    def fetch_all(query, params=None):
        """ Fetch all results from a query """
        cursor = DbManager.execute_query(query, params)
        return cursor.fetchall() if cursor else []

    @staticmethod
    def fetch_one(query, params=None):
        """ Fetch a single result from a query """
        cursor = DbManager.execute_query(query, params)
        return cursor.fetchone() if cursor else None

    @staticmethod
    def execute_sql_file(file_path):
        """ Execute a SQL script from a file """
        if not DbManager._connection:
            raise Error("Database is not connected.")

        try:
            with open(file_path, 'r') as sql_file:
                sql_script = sql_file.read()
            cursor = DbManager._connection.cursor()
            cursor.executescript(sql_script)
            DbManager._connection.commit()
            print(f"Executed SQL script from {file_path}")
        except Error as e:
            print(e)
        except FileNotFoundError:
            print(f"File {file_path} not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    @staticmethod
    def create_tables():
        """ Create tables for courses and jobs """
        copies_table = """
        CREATE TABLE IF NOT EXISTS copies (
            job_id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id TEXT NOT NULL,
            course_name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        user_creation_table = """
        CREATE TABLE IF NOT EXISTS user_creations (
            job_id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id INTEGER,
            job_details TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (course_id) REFERENCES courses (course_id)
        );
        """

        user_enrolls_table = """
        CREATE TABLE IF NOT EXISTS user_enrolls (
            job_id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id INTEGER,
            job_details TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (course_id) REFERENCES courses (course_id)
        );
        """
        DbManager.execute_query(copies_table)
        DbManager.execute_query(user_creation_table)
        DbManager.execute_query(user_enrolls_table)
        print("Tables created.")

# Example usage
if __name__ == "__main__":
    DbManager.connect()
   # DbManager.create_tables()
    
    # Insert example data
    DbManager.execute_query("INSERT INTO user_enrolls (course_name) VALUES (?)", ('Python Programming',))
    DbManager.execute_query("INSERT INTO jobs (course_id, job_details) VALUES (?, ?)", (1, 'Lecture on data structures'))
    
    # Fetch and print data
    #courses = DbManager.fetch_all("SELECT * FROM courses")
   # print("Courses:", courses)
    
    #jobs = DbManager.fetch_all("SELECT * FROM jobs")
    #print("Jobs:", jobs)

    # Execute the SQL file
    DbManager.execute_sql_file('test_script.sql')
    
    # Fetch and print data after executing the SQL script
    courses = DbManager.fetch_all("SELECT * FROM courses")
    print("Courses:", courses)
    
    jobs = DbManager.fetch_all("SELECT * FROM jobs")
    print("Jobs:", jobs)
    
    DbManager.disconnect()


    
    DbManager.disconnect()
