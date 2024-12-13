import os
import sqlite3
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import yaml
import threading
from datetime import datetime


configs = yaml.safe_load(open('config.yaml', mode='r').read())

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, db_name):
        self.db_name = db_name

    def on_created(self, event):
        if not event.is_directory:
            self.update_db(event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            self.update_db(event.src_path)

    def update_db(self, file_path):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        mtime = os.path.getmtime(file_path)
        try:
            c.execute("SELECT mtime FROM files WHERE path = ?", (file_path,))
            result = c.fetchone()
            if result is None:
                c.execute("INSERT INTO files (path, mtime) VALUES (?, ?)", (file_path, mtime))
                print(f"新增文件: {file_path}")
            elif result[0] < mtime:
                c.execute("UPDATE files SET mtime = ? WHERE path = ?", (mtime, file_path))
                print(f"更新文件: {file_path}")
            conn.commit()
        except sqlite3.Error as e:
            print(f"更新文件 {file_path} 时出错: {e}")
        finally:
            conn.close()

def perform_incremental_scan(path, db_name):
    """增量扫描，补充监听中断期间的文件变化"""
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    # 确保表结构存在
    c.execute("""
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT UNIQUE,
            mtime REAL
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS metadata (
            key TEXT PRIMARY KEY,
            value REAL
        )
    """)
    conn.commit()

    # 获取上次更新的时间
    c.execute("SELECT value FROM metadata WHERE key = 'last_update_time'")
    result = c.fetchone()
    last_update_time = result[0] if result else 0
    print(last_update_time)
    # 遍历路径，增量更新
    current_time = time.time()
    for root, _, files in os.walk(path):
        for file in files:
            if '.html' in file:
                file_path = os.path.join(root, file)
                try:
                    mtime = os.path.getmtime(file_path)
                    if mtime > last_update_time:
                        c.execute("SELECT mtime FROM files WHERE path = ?", (file_path,))
                        file_record = c.fetchone()
                        if file_record is None:
                            c.execute("INSERT INTO files (path, mtime) VALUES (?, ?)", (file_path, mtime))
                            print(f"新增文件: {file_path}")
                        elif file_record[0] < mtime:
                            c.execute("UPDATE files SET mtime = ? WHERE path = ?", (mtime, file_path))
                            print(f"更新文件: {file_path}")
                except Exception as e:
                    print(f"处理文件 {file_path} 时出错: {e}")

    # 更新 last_update_time
    c.execute("INSERT OR REPLACE INTO metadata (key, value) VALUES ('last_update_time', ?)", (current_time,))
    conn.commit()
    conn.close()

def start_monitoring(path, db_name):
    """启动文件系统监听并结合定期扫描"""
    # observer = Observer()
    # event_handler = FileChangeHandler(db_name)
    # observer.schedule(event_handler, path=path, recursive=True)
    # observer.start()
    print(f"开始监控路径: {path}")

    try:
        while True:
            time.sleep(60)  # 定期扫描，时间间隔可调整
            print("执行定期扫描...")
            perform_incremental_scan(path, db_name)
    except KeyboardInterrupt:
        pass
    #     observer.stop()
    # observer.join()

# 启动监听


def process_path_in_thread(path, db_path):
    """启动单独线程处理单个路径"""
    thread = threading.Thread(target=start_monitoring, args=(path, db_path))
    thread.start()

for project in configs['Project']:
    print(project)
    for target in configs['Project'][project]['path']:
        print(target)
        print(f"{project}.db")
        process_path_in_thread(target, f"{project}.db")
