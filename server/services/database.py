class Database:
    def __init__(self, connection):
        self.connection = connection

    def execute_query(self, query, params=None, fetch="none"):
        cursor = self.connection.cursor()

        try:
            cursor.execute(query, params or ())

            if fetch == "all":
                return cursor.fetchall()
            elif fetch == "one":
                return cursor.fetchone()

            self.connection.commit()
            return cursor.rowcount

        except Exception:
            self.connection.rollback()
            raise

        finally:
            cursor.close()

    def close(self):
        self.connection.close()