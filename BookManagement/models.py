import sqlite3
from db_config import get_connection

class UserManager:
    """Quản lý thông tin và xác nhận người dùng."""
    @staticmethod
    def login(username, password):
        """Xác thực người dùng từ database."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, role FROM users WHERE username=? AND password=?", 
                       (username, password))
        user = cursor.fetchone()
        conn.close()
        return user

    @staticmethod
    def register(username, password, role='user'):
        """Tạo người dùng mới."""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                           (username, password, role))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False # Tài khoản đã tồn tại
        finally:
            conn.close()

class BookManager:
    """Quản lý các thao tác với bảng sách."""
    @staticmethod
    def get_all_books():
        """Lấy danh sách tất cả sách."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books")
        books = cursor.fetchall()
        conn.close()
        return books

    @staticmethod
    def add_book(title, author, genre, price, stock):
        """Thêm sách mới vào kho."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO books (title, author, genre, price, stock) VALUES (?, ?, ?, ?, ?)", 
                       (title, author, genre, float(price), int(stock)))
        conn.commit()
        conn.close()

    @staticmethod
    def update_book(book_id, title, author, genre, price, stock):
        """Cập nhật thông tin sách hiện có."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE books SET title=?, author=?, genre=?, price=?, stock=? WHERE id=?", 
                       (title, author, genre, float(price), int(stock), book_id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete_book(book_id):
        """Xóa sách dựa trên ID."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM books WHERE id=?", (book_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def search_books(query):
        """Tìm kiếm sách theo tiêu đề hoặc tác giả."""
        conn = get_connection()
        cursor = conn.cursor()
        search_query = f"%{query}%"
        cursor.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ?", 
                       (search_query, search_query))
        books = cursor.fetchall()
        conn.close()
        return books

class OrderManager:
    """Quản lý việc đặt hàng và lịch sử mua hàng."""
    @staticmethod
    def place_order(user_id, book_id, quantity):
        """Thực hiện một đơn hàng mới và cập nhật tồn kho."""
        conn = get_connection()
        cursor = conn.cursor()
        
        # Kiểm tra tồn kho
        cursor.execute("SELECT stock, price FROM books WHERE id=?", (book_id,))
        book = cursor.fetchone()
        
        if book and book[0] >= quantity:
            new_stock = book[0] - quantity
            total_price = book[1] * quantity
            
            # Cập nhật tồn kho
            cursor.execute("UPDATE books SET stock=? WHERE id=?", (new_stock, book_id))
            # Lưu đơn hàng
            cursor.execute("INSERT INTO orders (user_id, book_id, quantity, total_price) VALUES (?, ?, ?, ?)", 
                           (user_id, book_id, quantity, total_price))
            
            conn.commit()
            conn.close()
            return True, "Đặt hàng thành công!"
        else:
            conn.close()
            return False, "Sản phẩm không đủ số lượng tồn kho."

    @staticmethod
    def get_user_orders(user_id):
        """Lấy lịch sử mua hàng của một người dùng cụ thể."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT b.title, o.quantity, o.total_price, o.order_date 
            FROM orders o JOIN books b ON o.book_id = b.id 
            WHERE o.user_id = ? 
            ORDER BY o.order_date DESC
        ''', (user_id,))
        orders = cursor.fetchall()
        conn.close()
        return orders
