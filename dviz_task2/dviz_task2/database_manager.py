import sqlite3

conn = sqlite3.connect("task2.db")
curr = conn.cursor()

curr.execute("""create table products(
products text,
sub_category text,
name text,
description
)""")

conn.commit()
conn.close()