import tkinter as tk
import importlib
import sys
from app.core.database import init_db
from app.ui.base import center_window

# Danh sách các module cần nạp lại khi nhấn Ctrl+R
UI_MODULES = [
    'app.core.database',
    'app.services.user_service',
    'app.services.book_service',
    'app.services.order_service',
    'app.ui.base',
    'app.ui.views.login_view',
    'app.ui.views.admin_dashboard',
    'app.ui.views.user_dashboard'
]

class BookApp(tk.Tk):
    """Lớp điều khiển chính của ứng dụng."""
    def __init__(self):
        super().__init__()
        self.title("Hệ thống Quản lý Sách (Nâng cao) - Antigravity")
        center_window(self, 1000, 700)
        self.current_user = None 
        
        # Khởi tạo Database (Tạo folder data và file .db nếu chưa có)
        init_db()

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.bind("<Control-r>", lambda event: self.reload_ui())
        self.show_login()

    def reload_ui(self):
        """Tính năng Hot Reload: Nạp lại mã nguồn mà không cần tắt app."""
        print("Đang nạp lại mã nguồn từ các folder dịch vụ...")
        try:
            for module_name in UI_MODULES:
                if module_name in sys.modules:
                    importlib.reload(sys.modules[module_name])
            
            for widget in self.container.winfo_children():
                widget.destroy()
            
            if self.current_user:
                self.show_dashboard()
            else:
                self.show_login()
            print("🚀 Đã cập nhật mã nguồn mới thành công!")
        except Exception as e:
            print(f"❌ Lỗi nạp lại: {e}")

    def show_login(self):
        from app.ui.views.login_view import LoginFrame
        self.current_user = None
        frame = LoginFrame(self.container, self)
        frame.grid(row=0, column=0, sticky="nsew")

    def on_login_success(self, user):
        self.current_user = user 
        self.show_dashboard()

    def show_dashboard(self):
        role = self.current_user[2]
        if role == 'admin':
            from app.ui.views.admin_dashboard import AdminDashboard
            frame = AdminDashboard(self.container, self)
        else:
            from app.ui.views.user_dashboard import UserDashboard
            frame = UserDashboard(self.container, self)
        
        frame.grid(row=0, column=0, sticky="nsew")

    def logout(self):
        self.current_user = None
        self.show_login()

if __name__ == "__main__":
    app = BookApp()
    app.mainloop()
