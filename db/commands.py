import sqlite3
from db import queries
import asyncio
class Database:
    def __init__(self):
        self.connection = sqlite3.connect("db.sqlite3", check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.loop = asyncio.get_running_loop()

    def sql_create_db(self):
        if self.connection:
            print("Database connected successfully")
        self.connection.execute(queries.CREATE_ANNOUNCEMENT_TABLE_QUERY)
        self.connection.commit()

    def sql_insert_user_form(self ,username, hash, text, phone_address, photo):
        self.cursor.execute(queries.INSERT_ANNO_QUERY,
                            (None, username, hash, text, phone_address, photo)
                            )
        self.connection.commit()
    def sql_select_user_form_by_telegram_id(self, hash):
        self.cursor.row_factory = lambda cursor, row: {
            "id": row[0],
            "username": row[1],
            "hash": row[2],
            "text": row[3],
            "phone_num_address": row[4],
            "photo" : row[5]
        }
        return self.cursor.execute(
            queries.SELECT_ANNO_QUERY, (hash,)
        ).fetchall()
