import sqlite3
import os

DB_NAME = "book_inventory.db"

def init_db():
    """Khởi tạo cơ sở dữ liệu SQLite và các bảng cần thiết."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Bảng Người dùng
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL CHECK(role IN ('admin', 'user'))
    )
    ''')

    # Bảng Sách
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        genre TEXT,
        price REAL NOT NULL,
        stock INTEGER NOT NULL
    )
    ''')

    # Bảng Đơn hàng
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        book_id INTEGER,
        order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        quantity INTEGER NOT NULL,
        total_price REAL NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (book_id) REFERENCES books (id)
    )
    ''')

    # Thêm tài khoản admin mặc định nếu chưa có
    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                       ("admin", "admin123", "admin"))
    except sqlite3.IntegrityError:
        pass # Admin đã tồn tại

    conn.commit()
    conn.close()

def get_connection():
    """Trả về kết nối tới database."""
    return sqlite3.connect(DB_NAME)

if __name__ == "__main__":
    init_db()
    print("Cơ sở dữ liệu đã được khởi tạo thành công!")
