import sqlite3
import os, time
import yaml
import threading
from multiprocessing import Process, Manager

configs = yaml.safe_load(open('config.yaml', mode='r').read())

def add_to_index(path_list, db_path="file_index.db"):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS files (id INTEGER PRIMARY KEY AUTOINCREMENT, path TEXT UNIQUE, mtime REAL)")
    for directory in path_list:
        for root, _, files in os.walk(directory):
            for file in files:
                if '.html' in file:
                    print(file)
                    file_path = os.path.join(root, file)
                    mtime = os.path.getmtime(file_path)
                    print(file_path)
                    print(mtime)
                    try:
                        c.execute("INSERT OR IGNORE INTO files (path, mtime) VALUES (?, ?)", (file_path, mtime))
                    except Exception as e:
                        print(f"插入索引时出错: {file_path}, 错误: {e}")
                    # finally:
                        # conn.commit()
    conn.commit()
    conn.close()

def create_and_index_single_path(path, db_path):
    """为单个路径创建数据库并进行文件索引"""
    # 根据路径生成数据库名
    
    # 创建数据库连接
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    c.execute("CREATE TABLE IF NOT EXISTS files (id INTEGER PRIMARY KEY AUTOINCREMENT, path TEXT UNIQUE, mtime REAL)")
    for root, _, files in os.walk(path):
        for file in files:
            if '.html' in file:
                # print(file)
                file_path = os.path.join(root, file)
                mtime = os.path.getmtime(file_path)
                print(file_path)
                # print(mtime)
                try:
                    c.execute("INSERT OR IGNORE INTO files (path, mtime) VALUES (?, ?)", (file_path, mtime))
                except Exception as e:
                    print(f"插入索引时出错: {file_path}, 错误: {e}")
                # finally:
                    # conn.commit()
    conn.commit()
    conn.close()

def process_path_in_thread(path, db_path):
    """启动单独线程处理单个路径"""
    thread = threading.Thread(target=create_and_index_single_path, args=(path, db_path))
    thread.start()
    # thread.join()  # 如果

# 使用示例
# {}_Test_Logs

# 示例调用
# db_file = "file_index.db"
# search_paths = [
#     r"\\10.97.1.49\SEL_Monitor\YJ7_Test_Logs",
#     r"\\10.97.1.49\SEL_Monitor\Another_Path"
# ]
# result = multi_process_search(db_file, search_paths)
# for path, files in result.items():
#     print(f"查询路径: {path}, 结果: {len(files)} 个文件")

# directory_to_index = "\\\\10.97.1.49\\SEL_Monitor\\YJ7_Test_Logs\\YJ7"
# # add_to_index(directory_to_index)
# path_list = []
# for folder in os.listdir('\\\\10.97.1.49\\SEL_Monitor'):
#     if 'Test_Logs' in folder and 'zip' not in folder and '-' not in folder:
#         # print(folder)
#         path_list.append('\\\\10.97.1.49\\SEL_Monitor\\'+folder + '\\')
# print(path_list)
# add_to_index(path_list)

for project in configs['Project']:
    # print(project)
    for target in configs['Project'][project]['path']:
        # print(target)
        # print(f"{project}.db")
        process_path_in_thread(target, f"{project}.db")