import csv
import json
import sqlite3

def check_database_exists(db_path):
    try:
        with open(db_path):
            pass
        return True
    except FileNotFoundError:
        return False

def create_database(db_path):
    conn = sqlite3.connect(db_path)
    conn.close()

def create_tables(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL
                )''')

    c.execute('''CREATE TABLE IF NOT EXISTS books (
                    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    publisher TEXT NOT NULL,
                    year INTEGER NOT NULL
                )''')

    conn.commit()
    conn.close()

def import_data_from_files(db_path):
    users = read_users_file("users.csv")
    for username, password in users.items():
        insert_user(db_path, username, password)

    books = read_books_file("books.json")
    for book in books:
        insert_book(db_path, book['title'], book['author'], book['publisher'], book['year'])

def read_users_file(file_path):
    users = {}
    try:
        with open(file_path, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                users[row['username']] = row['password']
    except FileNotFoundError:
        print('找不到使用者檔...')
    except Exception as e:
        print(f'開啟使用者檔時發生錯誤：{file_path}')
        print(f'錯誤訊息：{e}')
    return users

def read_books_file(file_path):
    books = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            books = json.load(file)
    except FileNotFoundError:
        print('找不到圖書檔...')
    except Exception as e:
        print('開啟圖書檔時發生錯誤...')
        print(f'錯誤訊息：{e}')
    return books

def get_login_credentials():
    username = input("請輸入帳號：")
    password = input("請輸入密碼：")
    return username, password

def verify_login(db_path, username, password):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    result = c.fetchone()
    conn.close()
    return result is not None

def display_menu():
    print("-------------------")
    print("    資料表 CRUD")
    print("-------------------")
    print("1. 增加記錄")
    print("2. 刪除記錄")
    print("3. 修改記錄")
    print("4. 查詢記錄")
    print("5. 資料清單")
    print("-------------------")

def menu_choice():
    return input("選擇要執行的功能(Enter離開)：")

def add_record(db_path):
    print("執行增加記錄功能...")

def delete_record(db_path):
    print("執行刪除記錄功能...")

def modify_record(db_path):
    print("執行修改記錄功能...")

def query_record(db_path):
    print("執行查詢記錄功能...")

def list_data(db_path):
    print("執行資料清單功能...")

def insert_user(db_path, username, password):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

def insert_book(db_path, title, author, publisher, year):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("INSERT INTO books (title, author, publisher, year) VALUES (?, ?, ?, ?)", (title, author, publisher, year))
    conn.commit()
    conn.close()
