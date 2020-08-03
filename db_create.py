import sqlite3

conn = sqlite3.connect("db.db")
cursor = conn.cursor()

cursor.execute("""CREATE TABLE Users
		        (
		    	 id INTEGER PRIMARY KEY AUTOINCREMENT,
		    	 cash real NOT NULL,
		    	 user_id int NOT NULL,
		    	 dt date NOT NULL
		        )
		        """)

cursor.execute("""CREATE TABLE History
		        (
		    	 id INTEGER PRIMARY KEY AUTOINCREMENT,
		    	 name varchar(31) NOT NULL,
		    	 num int NOT NULL,
		    	 price int NOT NULL,
		    	 dt datetime NOT NULL,
		    	 user_id int NOT NULL
		        )
		        """)

cursor.execute("""CREATE TABLE Coupons
		        (
		    	 id INTEGER PRIMARY KEY AUTOINCREMENT,
		    	 name varchar(31) NOT NULL,
		    	 cash real NOT NULL
		        )
		        """)

cursor.execute("""CREATE TABLE Comment
		        (
		    	 comment int NOT NULL
		        )
		        """)

conn.commit()