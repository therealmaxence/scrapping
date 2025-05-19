import sqlite3
import os
from datetime import datetime

class DB:
    def __init__(self, folder="", database=None):
        self.folder = folder
        self.file = database

    def reconnect(self):
        self.close()
        self.connect()

    def connect(self):
        self.conn = sqlite3.connect(self.folder + self.file)
        self.cursor = self.conn.cursor()

    def close(self):
        self.conn.close()

    def executeFile(self, sqlFile, args=()):
        self.connect()
        with open(sqlFile, 'r') as sql:
            request = sql.read()
            for arg in args:
                request = request.replace('?', arg, 1)
            self.cursor.executescript(request)
        self.conn.commit()
        self.close()

    def execute(self, query, args=(), type="all"):
        self.cursor.execute(query, args)
        if type == "one":
            return self.cursor.fetchone()
        else :
            return self.cursor.fetchall()