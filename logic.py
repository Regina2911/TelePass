import sqlite3


class DatabaseManager:

    def __init__(self, database):
        self.database = database

    def create_tables(self):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARYы KEY AUTOINCREMENT,
            service TEXT,
            username TEXT,
            password TEXT
        )
        """)

        conn.commit()
        conn.close()

    def add_password(self, service, username, password):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO passwords (service, username, password) VALUES (?, ?, ?)",
            (service, username, password)
        )

        conn.commit()
        conn.close()

    def get_passwords(self):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()

        cursor.execute("SELECT service, username, password FROM passwords")

        data = cursor.fetchall()

        conn.close()

        return data
            