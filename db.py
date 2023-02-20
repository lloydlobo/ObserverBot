import sqlite3


class DBHelper:
    def __init__(self, dbname="database_oberverbot.db"):
        self.dbname = dbname
        self.conn = sqlite3.connect(self.dbname)
        # self.conn = None

    def create_connection(self):
        return sqlite3.connect(self.dbname)

    def close(self):
        if self.conn:
            self.conn.close()

    def setup(self):
        with self.conn:
            c = self.conn.cursor()
            c.execute(
                """
                CREATE TABLE IF NOT EXISTS db_observe (
                    user_id INTEGER, 
                    task TEXT, 
                    focus INTEGER, 
                    date TEXT
                )
            """
            )
            c.execute(
                """
                CREATE TABLE IF NOT EXISTS db_reflect (
                    user_id INTEGER, 
                    score REAL, 
                    date TEXT
                )
            """
            )
        pass

    # date variable will not be overwritten by the datetime('now', 'localtime') function call, as the latter is used as a default value for the date column in case no value is provided for it in the SQL INSERT statement.
    #
    # In this case, if the date parameter is not provided when calling the add_observe method, the date column in the db_observe table will be populated with the current date and time as returned by the datetime('now', 'localtime') function call. On the other hand, if a date value is provided, it will be used instead of the default value.
    def add_observe(
        self,
        user_id,
        task,
        focus,
    ):
        with self.conn:
            c = self.conn.cursor()
            c.execute(
                "INSERT INTO db_observe (user_id, task, focus, date) VALUES (?, ?, ?, datetime('now', 'localtime'))",
                (user_id, task, focus),
            )

    def add_reflect(self, user_id, score):
        with self.conn:
            c = self.conn.cursor()
            c.execute(
                "INSERT INTO db_reflect (user_id, score, date) VALUES(?, ?, datetime('now', 'localtime')) ",
                (user_id, score),
            )

    def get_observe(self, user_id):
        with self.conn:
            c = self.conn.cursor()
            c.execute("SELECT * FROM db_observe WHERE user_id=?", (user_id,))
            return c.fetchall()

    def get_reflect(self, user_id):
        with self.conn:
            c = self.conn.cursor()
            c.execute("SELECT * FROM db_reflect WHERE user_id=?", (user_id,))
            return c.fetchall()
