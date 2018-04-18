import MySQLdb
import MySQLdb.cursors
import traceback

MYSQL_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'passwd': 'My1qaz2wsx',
    'db': 'library',
    'charset': 'utf8mb4',
    'cursorclass': MySQLdb.cursors.DictCursor
    }


class Store:
    def __init__(self, **kwargs):
        try:
            self.conn = MySQLdb.connect(**kwargs)
        except:
            traceback.print_exc()

    def execute_sql(self, _sql, *args):
        if 'select' in _sql:
            cur = self.conn.cursor()
            cur.execute(_sql, args)
            return cur.fetchall()
        else:
            if 'insert' in _sql or 'where' in _sql:
                cur = self.conn.cursor()
                cur.execute(_sql, args)
                self.conn.commit()
            else:
                print('no where')

    def close(self):
        cursor = self.conn.cursor()
        cursor.close()
        self.conn.close()


book_store = Store(**MYSQL_CONFIG)

sql_insert = "insert into storage_storage(book, inventory, remain, add_date, is_delete)values(%s,1,1,CURDATE(),0)"

book_set = set()
with open('books', encoding='utf-8') as f:
    for line in f:
        line = line.replace('《', '').replace('》', '').strip()
        if line:
            book_set.add(line)

for book in book_set:
    book_store.execute_sql(sql_insert, book)
