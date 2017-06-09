import sqlite3
from domain.database.data_read import DataRead

class DataAccess:
    def __init__(self, sqlite_connection_string, video_id, buffer_row_count):
        self.sqlite_connection_string = sqlite_connection_string
        self.video_id = video_id
        self.buffer_row_count = buffer_row_count

        try:
            conn = sqlite3.connect(sqlite_connection_string)
            self.conn = conn
        except Exception as ex:
            print(ex)
            raise

        self.rows_fetched = 0

        cur = self.conn.cursor()
        self.number_of_rows = cur.execute("SELECT Count(*) FROM VideoFrame WHERE videoid =?", (self.video_id,)).fetchone()[0]
        print("Video has " + str(self.number_of_rows) + " frames")

    def read_next_rows(self):
        cur = self.conn.cursor()
        cur.execute("SELECT binarydata FROM VideoFrame WHERE videoid =? ORDER BY position ASC LIMIT ? OFFSET ?", \
        (self.video_id, \
        self.buffer_row_count, \
        self.rows_fetched))

        rows = cur.fetchall()

        self.rows_fetched = self.rows_fetched + len(rows)
        print("Database read completed. Have now fetched a total of " + str(self.rows_fetched) + " rows")
        return DataRead(rows, self.rows_fetched, self.number_of_rows)
