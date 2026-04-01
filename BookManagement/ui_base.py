import tkinter as tk
from tkinter import ttk, messagebox

# Thiết kế màu sắc (Rich Aesthetics)
COLORS = {
    'primary': '#2C3E50',    # Dark Blue-Grey
    'secondary': '#E74C3C',  # Vibrant Red
    'background': '#F4F7F6', # Soft Light Grey
    'text': '#333333',
    'accent': '#3498DB',     # Bright Blue
    'white': '#FFFFFF',
    'success': '#27AE60'     # Green
}

def center_window(window, width, height):
    """Căn giữa cửa sổ trên màn hình."""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

class BaseFrame(tk.Frame):
    """Frame cơ sở với các thiết lập giao diện chung."""
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLORS['background'])
        self.controller = controller
        self.parent = parent
        self.create_widgets()

    def create_widgets(self):
        """Phương thức này sẽ được ghi đè ở các lớp con."""
        pass

    def show_error(self, message):
        messagebox.showerror("Lỗi", message)

    def show_info(self, message):
        messagebox.showinfo("Thông báo", message)
