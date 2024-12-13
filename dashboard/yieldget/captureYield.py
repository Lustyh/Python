import sqlite3

def search_by_keyword(keyword, db_path="./yieldget/file_index.db"):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # 使用 LIKE 查找包含特定关键字的路径
    query = "SELECT path FROM files WHERE path LIKE ?"
    c.execute(query, (f"%{keyword}%",))
    results = [row[0] for row in c.fetchall()]
    conn.close()
    return results

# 示例: 搜索包含 WIP4B02MYJ7X01ES2 的文件
# keyword = "WIP4C05MYJ7X02CVK"
# results = search_by_keyword(keyword)
# print("搜索结果:")
# for result in results:
#     print(result)