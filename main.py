import re
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import json


def parse_defender_log(log_line):
    match = re.match(r'(?P<date>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (?P<action>\w+): (?P<message>.+)', log_line)
    if match:
        date = match.group('date')
        action = match.group('action')
        message = match.group('message')

        to_json = {'Date': date, 'Action': action, 'Message': message}

        with open('log_analysis.json', 'w') as f:
            json.dump(to_json, f, sort_keys=True, indent=2)

        with open('log_analysis.json') as f:
            print(f.read())

        print(f'Date: {date}, Action: {action}, Message: {message}')


class LogHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        with open(event.src_path, 'r') as file:
            for line in file.readlines():
                parse_defender_log(line)


if __name__ == "__main__":
    path = "C:\\path\\to\\defender_logfile.txt"

    event_handler = LogHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)

    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
