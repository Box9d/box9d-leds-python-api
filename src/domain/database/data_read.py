class DataRead:
    def __init__(self, rows, last_row_number, total_rows):
        self.rows = rows
        self.total_rows = total_rows
        self.more_rows = last_row_number > total_rows