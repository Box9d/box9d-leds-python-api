class DataRead:
    def __init__(self, rows, total_rows_fetched, total_rows):
        self.rows = rows
        self.total_rows = total_rows
        self.more_rows = total_rows_fetched < total_rows