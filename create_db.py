import sqlite3

# 連接到資料庫（如果不存在，則會自動建立一個新的資料庫）
conn = sqlite3.connect('library.db')

# 建立游標
cursor = conn.cursor()

# 建立 users 資料表
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
)
''')

# 建立 books 資料表
cursor.execute('''
CREATE TABLE IF NOT EXISTS books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    publisher TEXT NOT NULL,
    year INTEGER NOT NULL
)
''')

# 插入使用者資料
users_data = [
    ('Alice', 'password1'),
    ('Bob', 'password2'),
    ('Charlie', 'password3')
]

cursor.executemany('INSERT INTO users (username, password) VALUES (?, ?)', users_data)

# 插入書籍資料
books_data = [
    ('簡愛', '夏綷蒂。姍蒂', '上海譯文出版社', 1847),
    ('紅樓夢', '曹雪芹', '人民文學出版社', 1792),
    ('西遊記', '吳承恩', '古典文學出版社', 1592)
]

cursor.executemany('INSERT INTO books (title, author, publisher, year) VALUES (?, ?, ?, ?)', books_data)

# 提交變更並關閉連線
conn.commit()
conn.close()

print("Database created successfully!")
