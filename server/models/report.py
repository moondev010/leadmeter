class Report:
    def __init__(self, database):
        self.database = database

    def create(self, claim, score, reason, confidence, user_email):
        self.database.execute_query(
            "INSERT INTO reports(claim, score, reason, confidence, user_email) VALUES(?, ?, ?, ?, ?)",
            (claim, score, reason, confidence, user_email)
        )