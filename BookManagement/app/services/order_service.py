import sqlite3
from app.core.database import get_connection

class OrderService:
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
