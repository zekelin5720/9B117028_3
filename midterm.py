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
            data = json.load(file)
            for book in data.get('books', []):
                books.append(book)
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
        confirm_username = username
        confirm_password = password
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

def add_record(db_path, json_file_path):
    title = input("請輸入要新增的標題：")
    author = input("請輸入要新增的作者：")
    publisher = input("請輸入要新增的出版社：")
    year = input("請輸入要新增的年份：")

    insert_book(db_path, title, author, publisher, year)
    print("記錄已成功新增")

def add_record(db_path, json_file_path):
    title = input("請輸入要新增的標題：")
    author = input("請輸入要新增的作者：")
    publisher = input("請輸入要新增的出版社：")
    year = input("請輸入要新增的年份：")

    # 讀取並列印 JSON 檔案中的記錄
    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
            json_books = json_data.get('books', [])
            if json_books:
                print("異動 1 記錄")
                print("|　　　　書名　　　　|　　　　作者　　　　|　　　出版社　　　　| 年份 |")
                for json_book in json_books:
                    print(f"|{json_book.get('title', ''):<18}|{json_book.get('author', ''):<18}|{json_book.get('publisher', ''):<18}|{json_book.get('year', ''):<6}|")
            else:
                print("JSON 檔案中沒有任何記錄")
    except FileNotFoundError:
        print("找不到 JSON 檔案")
    except Exception as e:
        print("讀取 JSON 檔案時發生錯誤：", e)

    # 將資料新增至資料庫
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("INSERT INTO books (title, author, publisher, year) VALUES (?, ?, ?, ?)",
              (title, author, publisher, year))
    conn.commit()

    # 列印資料庫中的所有記錄
    c.execute("SELECT title, author, publisher, year FROM books")
    db_records = c.fetchall()
    if db_records:
        for record in db_records:
            print(f"|{record[0]:{18}}|{record[1]:{18}}|{record[2]:{18}}|{record[3]:{6}}|")
    else:
        print("資料庫中沒有任何記錄")

    conn.close()


def modify_record(db_path, json_file_path):
    book_id = input("請問要修改哪一本書的標題？：")
    new_title = input("請輸入要更改的標題：")
    new_author = input("請輸入要更改的作者：")
    new_publisher = input("請輸入要更改的出版社：")
    new_year = input("請輸入要更改的年份：")

    conn = sqlite3.connect(db_path, json_file_path)
    c = conn.cursor()
    if new_title:
        c.execute("SELECT title, author, publisher, year FROM books")
    if new_author:
        c.execute("SELECT title, author, publisher, year FROM books")
    if new_publisher:
        c.execute("SELECT title, author, publisher, year FROM books")
    if new_year:
        c.execute("SELECT title, author, publisher, year FROM books")
    conn.commit()
    conn.close()
    print("記錄已成功修改")

def query_record(db_path, json_file_path):
    keyword = input("請輸入想查詢的關鍵字：")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ? OR publisher LIKE ? OR year LIKE ?",
              ('%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%'))
    records = c.fetchall()
    conn.close()
    if records:
        print("查詢結果：")
        for record in records:
            print("|{}　　　　　　　　|{}　　　　|{}　　　|{}  |"
                  .format(record[0], record[1], record[2], record[3]))
    else:
        print("|　　　　書名　　　　|　　　　作者　　　　|　　　出版社　　　　| 年份 |")

    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
            json_books = json_data.get('books', [])
            found = False
            for json_book in json_books:
                if keyword.lower() in json_book.get('title', '').lower() or keyword.lower() in json_book.get('author', '').lower() \
                        or keyword.lower() in json_book.get('publisher', '').lower() or keyword.lower() in str(json_book.get('year', '')).lower():
                    print("|{}　　　　　　　　|{}　　　　|{}　　　|{}  |"
                          .format(json_book.get('title', ''), json_book.get('author', ''), json_book.get('publisher', ''), json_book.get('year', '')))
                    found = True
            if not found:
                print("|　　　　書名　　　　|　　　　作者　　　　|　　　出版社　　　　| 年份 |")
    except FileNotFoundError:
        print("找不到 JSON 檔案")
    except Exception as e:
        print("讀取 JSON 檔案時發生錯誤：", e)



def list_data(db_path, json_file_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT * FROM books")
    db_records = c.fetchall()
    conn.close()
    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
            json_books = json_data.get('books', [])
            print("|　　　　書名　　　　|　　　　作者　　　　|　　　出版社　　　　| 年份 |")
            for json_book in json_books:
                print(f"|{json_book.get('title', ''):<18}|{json_book.get('author', ''):<18}|{json_book.get('publisher', ''):<18}|{json_book.get('year', ''):<6}|")
    except FileNotFoundError:
        print("找不到 JSON 檔案")
    except Exception as e:
        print("讀取 JSON 檔案時發生錯誤：", e)

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
    db_path = "library.sqlite"
    json_file_path = "books.json"  # JSON 檔案的路徑

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
                add_record(db_path, json_file_path)
            elif choice == "2":
                delete_record(db_path, json_file_path)
            elif choice == "3":
                modify_record(db_path, json_file_path)
            elif choice == "4":
                query_record(db_path, json_file_path)  # 將 json_file_path 參數傳遞給 query_record 函數
            elif choice == "5":
                list_data(db_path, json_file_path)
            else:
                print("無效的選擇")
                break
        else:
            print("帳號或密碼錯誤，請重新輸入。")

if __name__ == "__main__":
    main()

