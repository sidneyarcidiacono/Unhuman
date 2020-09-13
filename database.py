"""Import sqlite3."""
import sqlite3


class Database:
    """Define class Database."""

    def __init__(self):
        """Initialize properties for db."""
        self.DATABASE = './database.db'
        self.conn = sqlite3.connect('database.db', check_same_thread=False)
        self.c = self.conn.cursor()

# c.execute("""CREATE TABLE artwork (
#             title text,
#             description text,
#             price real,
#             media text,
#             size text
#             )""")

    def insert_product(self, title, description, price, media, size):
        """Insert product dynamically into db."""
        self.c.execute("INSERT INTO artwork VALUES (:title, :description, :price, :media, :size)",
                       {'title': title,
                        'description': description,
                        'price': price,
                        'media': media, 'size': size,
                        })
        self.conn.commit()
