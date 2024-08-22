import sqlite3
import pandas as pd
conn = sqlite3.connect('./apparel.db')
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS item;")
cur.execute("DROP TABLE IF EXISTS user;")
cur.execute("DROP TABLE IF EXISTS review;")
cur.execute("DROP TABLE IF EXISTS size;")

cur.execute('''
            CREATE TABLE item(
                id VARCHAR(10) NOT NULL,
                category VARCHAR(20),
                name VARCHAR(100),
                price INTEGER,
                img VARCHAR(150),
                link VARCHAR(150),
                PRIMARY KEY(id));''')

cur.execute('''
            CREATE TABLE user(
                id VARCHAR(10) NOT NULL,
                height VARCHAR(10),
                weight VARCHAR(10),
                size_id VARCHAR(1),
                PRIMARY KEY(id),
                FOREIGN KEY(size_id) REFERENCES size(id));''')

cur.execute('''
            CREATE TABLE review(
                id VARCHAR(10) NOT NULL,
                user_id VARCHAR(10),
                item_id VARCHAR(10),
                star INTEGER,
                comment VARCHAR(1000),
                size_id VARCHAR(1),
                color VARCHAR(10),
                PRIMARY KEY(id),
                FOREIGN KEY(user_id) REFERENCES user(id),
                FOREIGN KEY(item_id) REFERENCES item(id),
                FOREIGN KEY(size_id) REFERENCES size(id));''')

cur.execute('''
            CREATE TABLE size(
                id VARCHAR(1) NOT NULL,
                size VARCHAR(5));
            ''')
conn.commit()
cur.close()
conn.close()