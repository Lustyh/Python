import sqlite3
import os, time



def add_to_index(directory_to_index, db_path="file_index.db"):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS files (id INTEGER PRIMARY KEY AUTOINCREMENT, path TEXT UNIQUE, mtime REAL)")
    # for directory in path_list:
    for root, _, files in os.walk(directory_to_index):
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

# 使用示例
# {}_Test_Logs

directory_to_index = "\\\\10.97.1.49\\SEL_Monitor\\YJ7_Test_Logs\\YJ7"
add_to_index(directory_to_index)
# path_list = []
# for folder in os.listdir('\\\\10.97.1.49\\SEL_Monitor'):
#     if 'Test_Logs' in folder and 'zip' not in folder and '-' not in folder:
#         # print(folder)
#         path_list.append('\\\\10.97.1.49\\SEL_Monitor\\'+folder + '\\')
# print(path_list)
# add_to_index(path_list)