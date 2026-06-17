class Database:
    def __init__(self, connection):
        self.connection = connection

    def execute_query(self, query, params=None, fetch=False):
        cursor = self.connection.cursor()

        try:
            cursor.execute(query, params or ())

            if fetch:
                return cursor.fetchall()

            self.connection.commit()
            return cursor.rowcount

        except Exception:
            self.connection.rollback()
            raise

        finally:
            cursor.close()

    def close(self):
        self.connection.close()