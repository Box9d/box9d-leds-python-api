import codecs
import queue
import time
import json
import requests
from domain.timer import Timer
from domain.database.data_access import DataAccess
from websocket import create_connection
from dateutil import parser

class Playback:
    def __init__(self, sqlite_connection_string, video_id, frame_rate):

        self.buffer_seconds = 45
        self.frame_rate = frame_rate
        self.buffer_frame_count = round(self.frame_rate * self.buffer_seconds)
        self.sqlite_connection_string = sqlite_connection_string
        self.video_id = video_id
        self.row_queue = queue.Queue(-1)
        self.total_seconds = 0
        self.loaded = False
        self.stop_requested = False

    def load_buffer(self):
        if self.loaded:
            return

        producer = queue.threading.Thread(target=self.buffer_producer)
        producer.daemon = True
        producer.start()

        self.stop_requested = False
        self.loaded = True

    def buffer_producer(self):
        data_access = DataAccess(self.sqlite_connection_string, self.video_id, self.buffer_frame_count)
        self.total_seconds = data_access.number_of_rows / self.frame_rate

        print("Loading buffer")
        print("Video length: " + str(self.total_seconds) + "s")

        while True:
            if self.row_queue.qsize() <= self.buffer_frame_count:
                new_rows = data_access.read_next_rows()
                for new_row in new_rows.rows:
                    self.row_queue.put(new_row[0])

                print("Added " + str(len(new_rows.rows)) + " frames to buffer")
                if not new_rows.more_rows or self.stop_requested:
                    print("Buffer has finished")
                    break

                print("Waiting to add to buffer...")
            else:
                time.sleep(1)

    def buffer_consumer(self, play_at, time_reference_url):
        web_socket = create_connection("ws://localhost:7890")

        response = requests.get(time_reference_url).json()

        server_time = parser.parse(response['Result'])
        wait = (parser.parse(play_at) - server_time).total_seconds()
        print("Video starts in " + str(wait) + " seconds")
        time.sleep(wait)

        timer = Timer()
        timer.start()

        frames_played = 0
        print("Starting video!")
        while timer.elapsed() < self.total_seconds \
        and not self.row_queue.empty() \
        and not self.stop_requested:
            frame = self.row_queue.get()
            while timer.elapsed() * self.frame_rate < frames_played:
                web_socket.send_binary(frame)
            frames_played = frames_played + 1

        timer = None
        black_out = self.get_black_out(3000)
        web_socket.send_binary(black_out)
        web_socket.send_binary(black_out)
        web_socket.close()

    def play(self, play_at, time_reference_url):
        consumer = queue.threading.Thread(target=self.buffer_consumer, args=(play_at, time_reference_url))
        consumer.daemon = True
        consumer.start()

    def stop(self):
        print("Stopping video ")
        self.stop_requested = True

    def get_black_out(self, number_of_pixels):
        frame = bytearray()

        counter = 0
        while counter < number_of_pixels:
            frame.append(0x00)
            counter += 1

        return frame
        