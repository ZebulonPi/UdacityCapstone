import configparser
import psycopg2
from sql_queries import insert_table_queries


def insert_tables(cur, conn):
    '''
    Executes queries in list [insert_table_queries] against the Redshift back-end. This will load fact and dimension tables from staging tables.

            Parameters:
                    cur (psycopg2 connection object): Allows Python code to execute PostgreSQL command in a database session
                    conn (psycopg2 connection object): Handles the connection to a PostgreSQL database instance. It encapsulates a database session.

            Returns:
                    None
    '''
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    '''
    Reads configuration file, makes connection to Redshift backend, executes required queries
    '''
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()