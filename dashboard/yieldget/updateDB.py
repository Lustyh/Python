import os
import sqlite3
import time
import yaml
import threading
from datetime import datetime


configs = yaml.safe_load(open('config.yaml', mode='r').read())

def update_db_if_needed(db_name, file_path):
    # 获取文件的修改时间
    mtime = os.path.getmtime(file_path)
    
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    # 检查文件是否已经存在
    c.execute("SELECT mtime FROM files WHERE path = ?", (file_path,))
    result = c.fetchone()

    if result is None:
        # 文件不存在，插入新记录
        c.execute("INSERT INTO files (path, mtime) VALUES (?, ?)", (file_path, mtime))
        print(f"文件 {file_path} 被添加到数据库")
    else:
        # 文件存在，检查修改时间是否更新
        stored_mtime = result[0]
        if stored_mtime < mtime:
            # 修改时间有更新，进行更新操作
            c.execute("UPDATE files SET mtime = ? WHERE path = ?", (mtime, file_path))
            print(f"文件 {file_path} 的 mtime 被更新")
        else:
            print(f"文件 {file_path} 没有变化，无需更新")


def get_last_update_time(db_path="file_index.db"):
    """
    获取索引的上次更新时间。
    """
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS metadata (key TEXT UNIQUE, value TEXT)")
    c.execute("SELECT value FROM metadata WHERE key = 'last_update_time'")
    row = c.fetchone()
    print('xxxxxxxxx')
    conn.close()
    if row:
        return float(row[0])
    else:
        return 0  # 如果没有记录，返回0，表示需要全量更新

def update_last_update_time(db_path="file_index.db"):
    """
    更新索引的最后更新时间。
    """
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO metadata (key, value) VALUES ('last_update_time', ?)", (time.time(),))
    conn.commit()
    conn.close()

def update_index_incrementally(directory, db_path="file_index.db"):
    """
    增量更新索引，只添加最近新增或修改的文件。
    """
    last_update_time = get_last_update_time(db_path)
    dt_object = datetime.fromtimestamp(last_update_time)
    formatted_time = dt_object.strftime("%Y-%m-%d %H:%M:%S")
    print(formatted_time)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS files (path TEXT UNIQUE, mtime REAL)")
    for root, _, files in os.walk(directory + datetime.today().strftime("%Y%m%d")):
        for file in files:
            # print(file)
            if '.html' in file:
                # print(file)
                file_path = os.path.join(root, file)
                try:
                    mtime = os.path.getmtime(file_path)
                    # print(mtime)  # 获取文件修改时间
                    if mtime > last_update_time:  # 判断是否是新增或修改文件
                        c.execute("INSERT OR REPLACE INTO files (path, mtime) VALUES (?, ?)", (file_path, mtime))
                        print(f"索引已更新: {file_path}")
                    else:
                        c.execute("SELECT mtime FROM files WHERE path = ?", (file_path,))
                        result = c.fetchone()
                        if result is None:
                            # 文件不存在，插入新记录
                            c.execute("INSERT INTO files (path, mtime) VALUES (?, ?)", (file_path, mtime))
                            print(f"文件 {file_path} 被添加到数据库")
                except Exception as e:
                    print(f"处理文件时出错: {file_path}, 错误: {e}")

    conn.commit()
    conn.close()

    # for root, _, files in os.walk(directory):
    #     # if os.path.getatime(root) < last_update_time:
    #     #     print(root)
    #     #     continue
    #     for file in files:
    #         # print(file)
    #         if '.html' in file:
    #             # print(file)
    #             file_path = os.path.join(root, file)
    #             try:
    #                 mtime = os.path.getmtime(file_path)
    #                 # print(mtime)  # 获取文件修改时间
    #                 if mtime > last_update_time:  # 判断是否是新增或修改文件
    #                     c.execute("INSERT OR REPLACE INTO files (path, mtime) VALUES (?, ?)", (file_path, mtime))
    #                     print(f"索引已更新: {file_path}")
    #             except Exception as e:
    #                 print(f"处理文件时出错: {file_path}, 错误: {e}")

    # conn.commit()
    # conn.close()

    # 更新最后更新时间
    update_last_update_time(db_path)

# 定时任务
def periodic_index_update(path, db_path, interval=120,):
    """
    每隔一定时间增量更新索引。
    """
    while True:
        print(f"开始增量更新{db_path}索引...")
        # print(path)
        update_index_incrementally(path, db_path)
        print(f"{db_path}索引更新完成。")
        time.sleep(5)

def process_path_in_thread(path, db_path):
    """启动单独线程处理单个路径"""
    thread = threading.Thread(target=periodic_index_update, args=(path, db_path))
    thread.start()

# 使用示例
# directory_to_monitor = "\\\\10.97.1.49\\SEL_Monitor\\YJ7_Test_Logs\\YJ7"
# path_list = []
# for folder in os.listdir('\\\\10.97.1.49\\SEL_Monitor'):
#     if 'Test_Logs' in folder and 'zip' not in folder and '-' not in folder:
#         print(folder)
#         path_list.append('\\\\10.97.1.49\\SEL_Monitor\\'+folder + '\\')
# # print(path_list)
# # add_to_index(path_list)
# periodic_index_update(path_list, interval=60)  # 每隔60秒增量更新

for project in configs['Project']:
    print(project)
    for target in configs['Project'][project]['path']:
        print(target)
        print(f"{project}.db")
        # if project == 'YJ7':
        process_path_in_thread(target, f"{project}.db")