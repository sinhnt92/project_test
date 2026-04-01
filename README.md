# 📚 Ứng Dụng Quản Lý Sách

Chào mừng bạn đến với ứng dụng quản lý sách hoàn chỉnh. Đây là công cụ phục vụ mục đích học tập và thực hành Python với các tính năng chuyên nghiệp, giao diện trực quan và cấu trúc modular dễ bảo trì.

## 📁 Cấu trúc thư mục
Dự án được chia thành các tệp tin chuyên biệt:
- **`main.py`**: Điểm khởi đầu của ứng dụng, quản lý chuyển đổi màn hình và tính năng "Hot Reload".
- **`db_config.py`**: Cấu hình và khởi tạo cơ sở dữ liệu SQLite.
- **`models.py`**: Xử lý logic nghiệp vụ (Auth, CRUD Sách, Đặt hàng).
- **`ui_base.py`**: Định nghĩa giao diện cơ sở, màu sắc và phong cách chung.
- **`ui_login.py`**: Màn hình Đăng nhập & Đăng ký.
- **`ui_admin.py`**: Dashboard dành cho Admin (Quản lý kho sách, Thêm/Xóa/Sửa).
- **`ui_user.py`**: Dashboard dành cho Người dùng (Xem catalog, Đặt mua, Lịch sử).

## 🚀 Hướng dẫn khởi chạy
1. Đảm bảo bạn đã cài đặt Python (không cần thư viện bên ngoài).
2. Chạy tệp tin chính:
   ```bash
   python main.py
   ```

## 🧑‍💻 Tài khoản mặc định
Khi khởi chạy lần đầu, ứng dụng tự động tạo tài khoản Admin:
- **Tên đăng nhập:** `admin`
- **Mật khẩu:** `admin123`

Bạn cũng có thể sử dụng nút **"Đăng ký ngay"** trên màn hình đăng nhập để tạo tài khoản người dùng bình thường.

## ✨ Tính năng nổi bật: Hot Reload
Ứng dụng hỗ trợ tính năng **Hot Reload** độc đáo. Nếu bạn thay đổi mã nguồn trong các tệp UI (ví dụ thay đổi màu sắc trong `ui_base` hoặc layout trong `ui_admin`):
- Không cần tắt ứng dụng.
- Chỉ cần nhấn phím tắt **`Ctrl + R`** trên bàn phím.
- Ứng dụng sẽ tự động nạp lại mã mới và cập nhật giao diện ngay lập tức.

## 🛠️ Yêu cầu kỹ thuật
- **Ngôn ngữ:** Python 3.x
- **Giao diện:** Tkinter (Tích hợp sẵn)
- **Cơ sở dữ liệu:** SQLite (Tích hợp sẵn)
