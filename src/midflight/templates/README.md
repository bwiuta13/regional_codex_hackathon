# 📄 templates/ — mẫu Jinja2

| File | Dùng cho | Vai trò |
|---|---|---|
| `variance_dossier.md.j2` | Hồ sơ chênh lệch (Markdown → PDF) | D |

## Luật

- Mẫu **chỉ hiển thị** giá trị lấy từ snapshot và nhật ký quyết định. **Không tính toán trong mẫu.**
- Mọi con số đã được renderer định dạng trước khi vào mẫu (`0,74x` · `37,9 tr` · `19,1%`).
- Phần **"Giới hạn đã biết"** là **bắt buộc**, không phải tùy chọn — hồ sơ này đưa cho đối tác đọc.
