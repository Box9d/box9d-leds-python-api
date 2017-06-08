from domain.database.data_access import DataAccess

class Playback:
    def __init__(self, sqlite_connection_string, video_id, frame_rate):

        buffer_seconds = 10

        self.frame_rate = frame_rate
        self.data_access = DataAccess(sqlite_connection_string, video_id, frame_rate * buffer_seconds)
        self.rows = None
        self.next_rows = None

    def load_buffer(self):
        self.rows = self.data_access.read_next_rows()
        self.next_rows = self.load_next_rows()

    def play(self, start_time):
        pass

    def stop(self):
        pass

    def load_next_rows(self):
        if not self.next_rows and self.rows.more_rows:
            self.next_rows = self.data_access.read_next_rows()