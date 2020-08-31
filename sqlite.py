"""Import sqlite3."""
import sqlite3
from products import Product

DATABASE = './database.db'

conn = sqlite3.connect('database.db')

c = conn.cursor()

# c.execute("""CREATE TABLE artwork (
#             title text,
#             description text,
#             price real,
#             media text,
#             size text
#             )""")


teeth = Product('Teeth', 'Sacred Change', 'Oil on Canvas', '30x40', 3000.00)
redegeneration = Product('Redegeneration', 'Rebirth', 'Oil on Canvas', '24x36', 2300.00)

c.execute("INSERT INTO artwork VALUES (:title, :description, :price, :media, :size)",
          {'title': teeth.title,
           'description': teeth.description,
           'price': teeth.price,
           'media': teeth.media, 'size': teeth.size,
           })


conn.commit()

# c.execute("SELECT * FROM paintings WHERE title='Teeth'")

# print(c.fetchone())

conn.commit()
