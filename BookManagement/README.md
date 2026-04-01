# 📚 Ứng Dụng Quản Lý Sách (Service-Oriented Architecture)

Chào mừng bạn đến với phiên bản nâng cấp của ứng dụng Quản lý Sách. Phiên bản này được tổ chức theo **Kiến trúc hướng dịch vụ (Service-Oriented)**, giúp tách biệt rõ ràng giữa Giao diện (UI) và Logic nghiệp vụ (Services).

## 📂 Cấu trúc thư mục chuyên nghiệp
Dự án hiện tại được chia thành các package:
- **`app/core/`**: Chứa cấu hình cốt lõi (Database).
- **`app/services/`**: Chứa logic xử lý (BookService, UserService, OrderService).
- **`app/ui/views/`**: Chứa các màn hình giao diện riêng biệt.
- **`data/`**: Thư mục an toàn để lưu trữ cơ sở dữ liệu SQLite.
- **`main.py`**: Tệp khởi chạy chính tại thư mục gốc.

## 🚀 Cách khởi chạy
1. Đảm bảo bạn đang ở thư mục `BookManagement`.
2. Chạy lệnh:
   ```bash
   python main.py
   ```

## 🧑‍💻 Tài khoản đăng nhập
- **Admin:** `admin` / `admin123`
- **Người dùng:** Đăng ký trực tiếp trong ứng dụng.

## ✨ Tính năng Hot Reload
Bạn có thể chỉnh sửa bất kỳ tệp nào trong `app/ui/views` hoặc `app/services` và nhấn **`Ctrl + R`** để cập nhật ngay lập tức mà không cần tắt ứng dụng!
