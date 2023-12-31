import sys
import re
import os
import logging
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv


class Database:
    """PostgreSQL Database class."""

    def __init__(self, which="uk"):
        load_dotenv('.env')
        if which in ["eu", "xi", "xitest"]:
            self.database_url = os.getenv('DATABASE_EU')
        else:
            self.database_url = os.getenv('DATABASE_UK')

        self.conn = None

    def open_connection(self):
        """Connect to a Postgres database."""
        try:
            if self.conn is None:
                self.conn = psycopg2.connect(self.database_url)
        except psycopg2.DatabaseError as e:
            logging.error(e)
            sys.exit()
        finally:
            logging.info('Connection opened successfully.')

    def close_connection(self):
        self.conn = None

    def run_query(self, query, params=None):
        query = query.replace("\n", " ")
        query = re.sub("\s+", " ", query)
        """Run a SQL query."""
        try:
            self.open_connection()
            with self.conn.cursor() as cur:
                # with self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                if 'SELECT' in query.upper():
                    records = []
                    if params is None:
                        cur.execute(query)
                    else:
                        cur.execute(query, params)
                        a = 1
                    result = cur.fetchall()
                    for row in result:
                        records.append(row)
                    cur.close()
                    return records
                else:
                    result = cur.execute(query)
                    self.conn.commit()
                    affected = f"{cur.rowcount} rows affected."
                    cur.close()
                    return affected
        except psycopg2.DatabaseError as e:
            print(e)
        finally:
            if self.conn:
                self.conn.close()
                logging.info('Database connection closed.')
