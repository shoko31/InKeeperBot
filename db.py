import os
import psycopg2
from dotenv import load_dotenv


class DB:
    def __init__(self, host='localhost', port=5432, database='postgres', user='postgres', password='postgres', credentials=None):
        self.conn = None
        self.credentials = credentials
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password

    def connect(self):
        if self.credentials is not None:
            self.conn = psycopg2.connect(self.credentials, sslmode='require')
        else:
            self.conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password,
                sslmode='require')

    def disconnect(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None

    def __create_server_table(self, disconnect=True):
        if self.conn is None:
            self.connect()
        cur = self.conn.cursor()
        cur.execute('''CREATE TABLE SERVER
        (ID BIGINT PRIMARY KEY     NOT NULL,
        VALUE           JSON    NOT NULL);''')
        self.conn.commit()
        print('SERVER TABLE CREATED')
        if disconnect:
            self.disconnect()

    def update_server(self, id, value):
        if self.conn is None:
            self.connect()
        cur = self.conn.cursor()
        cur.execute('''INSERT INTO SERVER (id, value)
        VALUES ({}, '{}') ON CONFLICT (id)
        DO
         UPDATE
         SET value = EXCLUDED.value;
        '''.format(id, value))
        self.conn.commit()
        self.disconnect()

    def get_server(self, id):
        if self.conn is None:
            self.connect()
        cur = self.conn.cursor()
        try:
            cur.execute(f'SELECT * FROM SERVER WHERE id = {str(id)}')
        except psycopg2.errors.UndefinedTable:
            print('NO TABLE')
            self.conn.reset()
            self.__create_server_table(False)
            cur = self.conn.cursor()
            cur.execute(f'SELECT * FROM SERVER WHERE id = {str(id)}')
        rows = cur.fetchall()
        self.disconnect()
        if len(rows) < 1:
            return None
        return rows[0][1]


load_dotenv()
#db = DB(host=os.getenv('DB_URL'), port=5432, database=os.getenv('DB_NAME'), user=os.getenv('DB_USER'), password=os.getenv('DB_PWD'))
db = DB(credentials=os.getenv('DATABASE_URL'))
