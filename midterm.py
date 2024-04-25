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
    attempts = 0
    max_attempts = 2
    while attempts < max_attempts:
        username = input("請輸入帳號：")
        password = input("請輸入密碼：")
        confirm_username = username  # 使用第一次輸入的帳號值
        confirm_password = password  # 使用第一次輸入的密碼值
        if username == confirm_username and password == confirm_password:
            return username, password
        else:
            print("帳號或密碼輸入不一致，請重新輸入。")
            attempts += 1
    print("已達到最大嘗試次數，程式結束。")
    exit(1)

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
    title = input("請輸入書名：")
    author = input("請輸入作者：")
    publisher = input("請輸入出版社：")
    year = input("請輸入年份：")

    insert_book(db_path, title, author, publisher, year)
    print("記錄已成功新增")

def delete_record(db_path):
    book_id = input("請輸入要刪除的書籍ID：")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("DELETE FROM books WHERE book_id = ?", (book_id,))
    conn.commit()
    conn.close()
    print("記錄已成功刪除")

def modify_record(db_path):
    book_id = input("請輸入要修改的書籍ID：")
    new_title = input("請輸入新書名（若不修改請按Enter）：")
    new_author = input("請輸入新作者（若不修改請按Enter）：")
    new_publisher = input("請輸入新出版社（若不修改請按Enter）：")
    new_year = input("請輸入新年份（若不修改請按Enter）：")

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    if new_title:
        c.execute("UPDATE books SET title = ? WHERE book_id = ?", (new_title, book_id))
    if new_author:
        c.execute("UPDATE books SET author = ? WHERE book_id = ?", (new_author, book_id))
    if new_publisher:
        c.execute("UPDATE books SET publisher = ? WHERE book_id = ?", (new_publisher, book_id))
    if new_year:
        c.execute("UPDATE books SET year = ? WHERE book_id = ?", (new_year, book_id))
    conn.commit()
    conn.close()
    print("記錄已成功修改")

def query_record(db_path):
    book_id = input("請輸入要查詢的書籍ID：")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT * FROM books WHERE book_id = ?", (book_id,))
    record = c.fetchone()
    conn.close()
    if record:
        print("查詢結果：", record)
    else:
        print("未找到符合條件的記錄")

def list_data(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT * FROM books")
    records = c.fetchall()
    conn.close()
    print("資料清單：")
    print("|　　　　書名　　　　|　　　　作者　　　　|　　　出版社　　　　| 年份 |")
    for record in records:
        print(f"|{record[1]:<16}|{record[2]:<16}|{record[3]:<16}|{record[4]:<6}|")
    input("按 Enter 回到主選單...")

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

def main():
    db_path = "library.sqlite"  # 或者使用 ".db" 文件後綴

    if not check_database_exists(db_path):
        create_database(db_path)
        create_tables(db_path)
        import_data_from_files(db_path)


    while True:
        username, password = get_login_credentials()
        if verify_login(db_path, username, password):
            display_menu()
            choice = menu_choice()
            if choice == "1":
                add_record(db_path)
            elif choice == "2":
                delete_record(db_path)
            elif choice == "3":
                modify_record(db_path)
            elif choice == "4":
                query_record(db_path)
            elif choice == "5":
                list_data(db_path)
            else:
                print("無效的選擇")
                break
        else:
            print("帳號或密碼錯誤，請重新輸入。")

if __name__ == "__main__":
    main()
