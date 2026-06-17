class Report:
    def __init__(self, database):
        self.database = database

    def create(self, claim, score, reason, confidence, user_id):
        self.database.execute_query(
            "INSERT INTO reports(claim, score, reason, confidence, user_id) VALUES(?, ?, ?, ?, ?)",
            (claim, score, reason, confidence, user_id)
        )