import tkinter as tk
from tkinter import ttk, messagebox
from ui_base import BaseFrame, COLORS
from models import BookManager, OrderManager

class UserDashboard(BaseFrame):
    """Giao diện dành cho người mua hàng (Người dùng thường)."""
    def create_widgets(self):
        # Tiêu đề trên
        header = tk.Frame(self, bg=COLORS['accent'], height=60)
        header.pack(fill="x", side="top")
        
        tk.Label(header, text="CỬA HÀNG SÁCH TRỰC TUYẾN", 
                 font=("Helvetica", 18, "bold"), bg=COLORS['accent'], 
                 fg=COLORS['white']).pack(pady=15)

        # Tab control (Shop / Giỏ hàng / Lịch sử)
        style = ttk.Style()
        style.configure("TNotebook", background=COLORS['background'])
        
        self.tabs = ttk.Notebook(self)
        self.tabs.pack(fill="both", expand=True, padx=20, pady=10)

        # 1. TAB: CỬA HÀNG
        self.shop_frame = tk.Frame(self.tabs, bg=COLORS['white'])
        self.tabs.add(self.shop_frame, text=" Cửa Hàng ")
        self.create_shop_tab()

        # 2. TAB: LỊCH SỬ MUA HÀNG
        self.history_frame = tk.Frame(self.tabs, bg=COLORS['white'])
        self.tabs.add(self.history_frame, text=" Lịch Sử Đã Mua ")
        self.create_history_tab()

        # Nút Đăng xuất đặt riêng biệt dưới Tabs
        tk.Button(self, text="ĐĂNG XUẤT", bg=COLORS['secondary'], fg="white", 
                  command=self.controller.logout, bd=0, padx=20, pady=10, 
                  cursor="hand2").pack(pady=(0, 20))

    def create_shop_tab(self):
        """Xây dựng nội dung cho Tab Cửa Hàng."""
        # Top Search
        search_frame = tk.Frame(self.shop_frame, bg=COLORS['white'])
        search_frame.pack(fill="x", padx=10, pady=15)
        
        tk.Label(search_frame, text="Tìm sách:", bg=COLORS['white']).pack(side="left")
        self.ent_search = ttk.Entry(search_frame)
        self.ent_search.pack(side="left", fill="x", expand=True, padx=10)
        ttk.Button(search_frame, text="Tìm", command=self.load_books_shop).pack(side="left")

        # Table hiển thị sách cho người dùng mua
        columns = ("ID", "Title", "Author", "Genre", "Price", "Stock")
        self.tree_shop = ttk.Treeview(self.shop_frame, columns=columns, show="headings")
        titles = ["ID", "Tên sách", "Tác giả", "Thể loại", "Giá", "Tồn kho"]
        for col, title in zip(columns, titles):
            self.tree_shop.heading(col, text=title)
            self.tree_shop.column(col, width=100 if col != "Title" else 250, anchor="center")
        self.tree_shop.pack(fill="both", expand=True, padx=10)

        # Nút Mua Hàng
        buy_frame = tk.Frame(self.shop_frame, bg=COLORS['white'])
        buy_frame.pack(fill="x", pady=20)
        
        tk.Label(buy_frame, text="Số lượng:", bg=COLORS['white']).pack(side="left", padx=(10, 5))
        self.ent_qty = ttk.Entry(buy_frame, width=10)
        self.ent_qty.insert(0, "1")
        self.ent_qty.pack(side="left")
        
        btn_buy = tk.Button(buy_frame, text="ĐẶT MUA NGAY", bg=COLORS['success'], 
                             fg=COLORS['white'], font=("Helvetica", 10, "bold"), 
                             bd=0, padx=20, pady=5, cursor="hand2", command=self.place_order)
        btn_buy.pack(side="left", padx=20)

        self.load_books_shop()

    def create_history_tab(self):
        """Xây dựng nội dung cho Tab Lịch sử."""
        columns = ("Title", "Qty", "Total", "Date")
        self.tree_history = ttk.Treeview(self.history_frame, columns=columns, show="headings")
        titles = ["Tên Sách", "Số Lượng", "Thành Tiền", "Ngày Mua"]
        for col, title in zip(columns, titles):
            self.tree_history.heading(col, text=title)
            self.tree_history.column(col, width=150, anchor="center")
        self.tree_history.pack(fill="both", expand=True, padx=10, pady=10)
        
        ttk.Button(self.history_frame, text="LÀM MỚI LỊCH SỬ", 
                   command=self.load_order_history).pack(pady=10)

    def load_books_shop(self):
        """Tải danh sách sách hoặc kết quả tìm kiếm vào shop."""
        self.tree_shop.delete(*self.tree_shop.get_children())
        query = self.ent_search.get().strip()
        books = BookManager.search_books(query) if query else BookManager.get_all_books()
        for book in books:
            self.tree_shop.insert("", "end", values=book)

    def load_order_history(self):
        """Tải lịch sử mua hàng của người dùng hiện tại."""
        self.tree_history.delete(*self.tree_history.get_children())
        orders = OrderManager.get_user_orders(self.controller.current_user[0])
        for order in orders:
            self.tree_history.insert("", "end", values=order)

    def place_order(self):
        """Xử lý đặt hàng."""
        selected_items = self.tree_shop.selection()
        if not selected_items:
            self.show_error("Vui lòng chọn một quyển sách để mua!")
            return
        
        item_values = self.tree_shop.item(selected_items[0], 'values')
        book_id = item_values[0]
        try:
            qty = int(self.ent_qty.get().strip())
            if qty <= 0: raise ValueError
            
            success, msg = OrderManager.place_order(self.controller.current_user[0], book_id, qty)
            if success:
                self.show_info(msg)
                self.load_books_shop() # Cập nhật tồn kho
                self.load_order_history() # Cập nhật lịch sử
                self.ent_qty.delete(0, tk.END)
                self.ent_qty.insert(0, "1")
            else:
                self.show_error(msg)
        except ValueError:
            self.show_error("Số lượng phải là số nguyên dương!")
