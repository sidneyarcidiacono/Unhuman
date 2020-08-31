"""Import sqlite3."""
import sqlite3
from products import Product

DATABASE = './database.db'

conn = sqlite3.connect('database.db')

c = conn.cursor()

# c.execute("""CREATE TABLE paintings (
#             title text,
#             description text,
#             price real
#             )""")
 #TODO: add media and size to paintings TABLE

# c.execute("INSERT INTO paintings VALUES ('Teeth', 'Sacred', 2000.00)")
teeth = Product('Teeth', 'Sacred Change', 'Oil on Canvas', '30x40', 3000.00)
redegeneration = Product('Redegeneration', 'Rebirth', 'Oil on Canvas', '24x36', 2300.00)

c.execute("INSERT INTO paintings VALUES (:title, :description, :media, :size, :price)",
          (teeth.title, teeth.description, teeth.price))


conn.commit()

c.execute("SELECT * FROM paintings WHERE title='Teeth'")

print(c.fetchone())

conn.commit()
