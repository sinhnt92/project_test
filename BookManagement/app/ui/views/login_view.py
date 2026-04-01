import tkinter as tk
from tkinter import ttk
from app.ui.base import BaseFrame, COLORS
from app.services.user_service import UserService

class LoginFrame(BaseFrame):
    """Giao diện đăng nhập và đăng ký người dùng."""
    def create_widgets(self):
        container = tk.Frame(self, bg=COLORS['white'], padx=40, pady=40, 
                             highlightthickness=2, highlightbackground=COLORS['accent'])
        container.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(container, text="QUẢN LÝ SÁCH", font=("Helvetica", 24, "bold"), 
                 bg=COLORS['white'], fg=COLORS['primary']).pack(pady=(0, 20))
        
        self.lbl_title = tk.Label(container, text="Đăng Nhập", font=("Helvetica", 16), 
                                 bg=COLORS['white'], fg=COLORS['text'])
        self.lbl_title.pack(pady=(0, 20))

        tk.Label(container, text="Tên đăng nhập:", bg=COLORS['white']).pack(anchor="w")
        self.ent_username = ttk.Entry(container, width=30)
        self.ent_username.pack(pady=(0, 20))

        tk.Label(container, text="Mật khẩu:", bg=COLORS['white']).pack(anchor="w")
        self.ent_password = ttk.Entry(container, width=30, show="*")
        self.ent_password.pack(pady=(0, 20))

        self.btn_submit = tk.Button(container, text="ĐĂNG NHẬP", bg=COLORS['accent'], 
                                   fg=COLORS['white'], font=("Helvetica", 12, "bold"), 
                                   command=self.handle_login, cursor="hand2", bd=0, padx=20, pady=10)
        self.btn_submit.pack(fill="x", pady=(0, 10))

        self.btn_toggle = tk.Button(container, text="Bạn chưa có tài khoản? Đăng ký ngay", 
                                   bg=COLORS['white'], fg=COLORS['accent'], bd=0, 
                                   command=self.toggle_mode, cursor="hand2")
        self.btn_toggle.pack()

        self.is_register_mode = False

    def toggle_mode(self):
        self.is_register_mode = not self.is_register_mode
        if self.is_register_mode:
            self.lbl_title.config(text="Đăng Ký Tài Khoản")
            self.btn_submit.config(text="ĐĂNG KÝ", bg=COLORS['success'])
            self.btn_toggle.config(text="Đã có tài khoản? Đăng nhập tại đây")
        else:
            self.lbl_title.config(text="Đăng Nhập")
            self.btn_submit.config(text="ĐĂNG NHẬP", bg=COLORS['accent'])
            self.btn_toggle.config(text="Chưa có tài khoản? Đăng ký ngay")

    def handle_login(self):
        user = self.ent_username.get().strip()
        pwd = self.ent_password.get().strip()

        if not user or not pwd:
            self.show_error("Vui lòng điền đầy đủ thông tin!")
            return

        if self.is_register_mode:
            if UserService.register(user, pwd):
                self.show_info("Đăng ký thành công! Đăng nhập ngay.")
                self.toggle_mode()
            else:
                self.show_error("Tài khoản đã tồn tại!")
        else:
            logged_user = UserService.login(user, pwd)
            if logged_user:
                self.controller.on_login_success(logged_user)
            else:
                self.show_error("Sai thông tin đăng nhập!")
