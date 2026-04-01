import sqlite3
from app.core.database import get_connection

class BookService:
    """Quản lý các thao tác tương tác với dữ liệu Sách."""
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
