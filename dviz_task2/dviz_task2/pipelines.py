import sqlite3

class DvizTask2Pipeline:

    def __init__(self):
        self.initialize_database()

    def initialize_database(self):
        self.conn = sqlite3.connect("task2.db")
        self.curr = self.conn.cursor()

        self.curr.execute("""DROP TABLE IF EXISTS products""")
        self.curr.execute("""create table products(
        product text,
        sub_category text,
        name text,
        description
        )""")

        self.conn.commit()

    def process_item(self, item, spider):
        self.store_data(item)
        return item

    def store_data(self, item):
        product = item['product']
        sub_cat = item['sub_category']
        names = item['prod_names']
        descriptions = item['descriptions']

        for i in range(len(names)):
            name = names[i]
            desc = descriptions[i]
            self.curr.execute("""insert into products values (?, ?, ?, ?)""", (product, sub_cat, name, desc))

        self.conn.commit()