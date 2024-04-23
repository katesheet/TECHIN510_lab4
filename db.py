import time
import psycopg2

class Database:
    def __init__(self, database_url) -> None:
        self.con = psycopg2.connect(database_url)
        self.cur = self.con.cursor()

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.con.close()

    def create_table(self):
        q = """
        CREATE TABLE IF NOT EXISTS books (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            rating INTEGER NOT NULL,
            price TEXT NOT NULL,
            stock TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        self.cur.execute(q)
        self.con.commit()

    def truncate_table(self):
        q = """
        TRUNCATE TABLE books
        """
        self.cur.execute(q)
        self.con.commit()
    
    def insert_book(self, book):
        q = """
        INSERT INTO books (title, rating, price, stock) VALUES (%s, %s, %s, %s)
        """
        self.cur.execute(q, (book['title'], book['rating'], book['price'], book['stock']))
        self.con.commit()


    def query_table(self, search_query=None, sort_column=None, sort_order=None, filter_in_stock=None):
        query = "SELECT * FROM books "
        if filter_in_stock:
            query += " WHERE stock = 'In stock'"
        if search_query:
            if filter_in_stock:
                query += " AND "
            else:
                query += " WHERE "
            query += "title LIKE %s"
            query += f" ORDER BY {sort_column} " if sort_column is not None else ""
            query += "DESC" if sort_order != "from low to high" else "ASC"
            print(query, search_query)
            self.cur.execute(query + ' ', ('%' + search_query + '%', ))
        elif sort_column:
            query += f" ORDER BY {sort_column} "
            query += "DESC" if sort_order != "from low to high" else "ASC"
            self.cur.execute(query + ' ')
        else:
            self.cur.execute(query + ' ')

        return self.cur.fetchall()