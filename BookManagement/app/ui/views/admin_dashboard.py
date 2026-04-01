import tkinter as tk
from tkinter import ttk, messagebox
from app.ui.base import BaseFrame, COLORS
from app.services.book_service import BookService

class AdminDashboard(BaseFrame):
    """Giao diện dành cho người quản trị (Admin)."""
    def create_widgets(self):
        self.config(bg=COLORS['background'])
        
        header = tk.Frame(self, bg=COLORS['primary'], height=60)
        header.pack(fill="x", side="top")
        
        tk.Label(header, text="HỆ THỐNG QUẢN LÝ KHO SÁCH (ADMIN)", 
                 font=("Helvetica", 18, "bold"), bg=COLORS['primary'], 
                 fg=COLORS['white']).pack(pady=15)

        main_body = tk.Frame(self, bg=COLORS['background'])
        main_body.pack(fill="both", expand=True, padx=20, pady=20)

        form_frame = tk.LabelFrame(main_body, text="Thông tin Sách", 
                                   font=("Helvetica", 12, "bold"), padx=20, pady=20,
                                   bg=COLORS['white'])
        form_frame.pack(side="left", fill="y", padx=(0, 20))

        fields = ["Tên Sách", "Tác Giả", "Thể Loại", "Giá Bán", "Số Lượng Tồn"]
        self.entries = {}
        for idx, field in enumerate(fields):
            tk.Label(form_frame, text=f"{field}:", bg=COLORS['white']).pack(anchor="w", pady=(10, 0))
            entry = ttk.Entry(form_frame, width=30)
            entry.pack(pady=(0, 5))
            self.entries[field] = entry

        btn_frame = tk.Frame(form_frame, bg=COLORS['white'])
        btn_frame.pack(fill="x", pady=20)

        ttk.Button(btn_frame, text="THÊM MỚI", command=self.add_book).pack(fill="x", pady=2)
        ttk.Button(btn_frame, text="CẬP NHẬT", command=self.update_book).pack(fill="x", pady=2)
        ttk.Button(btn_frame, text="XÓA SÁCH", command=self.delete_book).pack(fill="x", pady=2)
        ttk.Button(btn_frame, text="LÀM MỚI FORM", command=self.clear_form).pack(fill="x", pady=2)
        
        tk.Button(form_frame, text="Đăng Xuất", bg=COLORS['secondary'], fg="white", 
                  command=self.controller.logout, cursor="hand2", bd=0, pady=5).pack(fill="x", pady=(20, 0))

        table_frame = tk.Frame(main_body, bg=COLORS['white'])
        table_frame.pack(side="right", fill="both", expand=True)

        search_frame = tk.Frame(table_frame, bg=COLORS['white'])
        search_frame.pack(fill="x", pady=(0, 10))
        tk.Label(search_frame, text="Tìm kiếm (Tên/Tác giả):", bg=COLORS['white']).pack(side="left")
        self.ent_search = ttk.Entry(search_frame)
        self.ent_search.pack(side="left", fill="x", expand=True, padx=10)
        ttk.Button(search_frame, text="Tìm", command=self.search_books).pack(side="left")
        ttk.Button(search_frame, text="Tất cả", command=self.load_all_books).pack(side="left", padx=5)

        columns = ("ID", "Title", "Author", "Genre", "Price", "Stock")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)
        
        titles = ["ID", "Tên sách", "Tác giả", "Thể loại", "Giá", "Tồn kho"]
        for col, title in zip(columns, titles):
            self.tree.heading(col, text=title)
            self.tree.column(col, width=100 if col != "Title" else 200, anchor="center")

        self.tree.pack(side="left", fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.selected_id = None
        self.load_all_books()

    def load_all_books(self):
        self.tree.delete(*self.tree.get_children())
        books = BookService.get_all_books()
        for book in books:
            self.tree.insert("", "end", values=book)

    def search_books(self):
        query = self.ent_search.get().strip()
        if not query:
            self.load_all_books()
            return
        self.tree.delete(*self.tree.get_children())
        books = BookService.search_books(query)
        for book in books:
            self.tree.insert("", "end", values=book)

    def on_select(self, event):
        selected_items = self.tree.selection()
        if not selected_items: return
        item_values = self.tree.item(selected_items[0], 'values')
        self.selected_id = item_values[0]
        fields = ["Tên Sách", "Tác Giả", "Thể Loại", "Giá Bán", "Số Lượng Tồn"]
        for i, field in enumerate(fields):
            self.entries[field].delete(0, tk.END)
            self.entries[field].insert(0, item_values[i+1])

    def add_book(self):
        data = [self.entries[f].get().strip() for f in ["Tên Sách", "Tác Giả", "Thể Loại", "Giá Bán", "Số Lượng Tồn"]]
        if not all(data):
            self.show_error("Vui lòng điền đủ mọi thông tin!")
            return
        try:
            BookService.add_book(data[0], data[1], data[2], data[3], data[4])
            self.show_info("Thêm sách thành công!")
            self.clear_form()
            self.load_all_books()
        except ValueError:
            self.show_error("Dữ liệu nhập phải là số!")

    def update_book(self):
        if not self.selected_id:
            self.show_error("Vui lòng chọn một dòng!")
            return
        data = [self.entries[f].get().strip() for f in ["Tên Sách", "Tác Giả", "Thể Loại", "Giá Bán", "Số Lượng Tồn"]]
        try:
            BookService.update_book(self.selected_id, data[0], data[1], data[2], data[3], data[4])
            self.show_info("Cập nhật thành công!")
            self.load_all_books()
        except ValueError:
            self.show_error("Dữ liệu nhập không hợp lệ!")

    def delete_book(self):
        if not self.selected_id:
            self.show_error("Vui lòng chọn dòng!")
            return
        if messagebox.askyesno("Xác nhận", "Xóa sách này?"):
            BookService.delete_book(self.selected_id)
            self.selected_id = None
            self.clear_form()
            self.load_all_books()

    def clear_form(self):
        self.selected_id = None
        for entry in self.entries.values():
            entry.delete(0, tk.END)
