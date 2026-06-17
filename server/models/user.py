class User:
    def __init__(self, database):
        self.database = database

    def create(self, email, password, username):
        self.database.execute_query(
            "INSERT INTO users(email, password, username) VALUES(?, ?, ?)",
            (email, password, username)
        )
