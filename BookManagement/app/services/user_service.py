import sqlite3
from app.core.database import get_connection

class UserService:
    """Quản lý các thao tác liên quan tới Người dùng."""
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
            return False
        finally:
            conn.close()
