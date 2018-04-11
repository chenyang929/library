from table_init.store import Store, MYSQL_CONFIG

book_store = Store(**MYSQL_CONFIG)

sql_insert = "insert into book_book(book, inventory, remain, add_date)values(%s,1,1,CURDATE())"

book_set = set()
with open('books', encoding='utf-8') as f:
    for line in f:
        line = line.replace('《', '').replace('》', '').strip()
        if line:
            book_set.add(line)

for book in book_set:
    book_store.execute_sql(sql_insert, book)
