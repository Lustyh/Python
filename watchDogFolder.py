import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        print(f"发现新文件: {event.src_path}")
        # you can deal with the file in here

# functon for monitor folder
def watch_folder(folder_path):
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, folder_path, recursive=False)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    
    observer.join()

if __name__ == '__main__':
    folder_path = "C:\\Users\\A907A919\\MarsLog"
    watch_folder(folder_path)