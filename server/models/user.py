class User:
    def __init__(self, database):
        self.database = database

    def create(self, email, password, username):
        self.database.execute_query(
            "INSERT INTO users(email, password, username) VALUES(?, ?, ?)",
            (email, password, username)
        )

    def get(self, email):
        self.database.execute_query(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        )

    def update(self, email, params):

        set_chunk = ""

        for i, (key, value) in enumerate(params.items()):
            set_chunk += f"{key}=?"

            if i < len(params) - 1:
                set_chunk += ", "

        statement = f"UPDATE users SET {set_chunk} WHERE email = ? LIMIT 1"

        final_params = list(params.values())
        final_params.append(email)

        self.database.execute_query(
            statement,
            tuple(final_params)
        )

    def delete(self, email):
        self.database.execute_query(
            "DELETE FROM users WHERE email = ?",
            (email,)
        )
