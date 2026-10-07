# ⚙️ config/ — tham số nghiệp vụ

> **👔 Trade Marketing SỞ HỮU thư mục này, không phải engineering.**
>
> Đây là lý do các ngưỡng nằm trong YAML chứ không hard-code trong Python: người nghiệp vụ phải
> đọc được, review được và **đổi được qua pull request** mà không cần sửa code.

| File | Nội dung | Ai quyết | Codex được tự đổi? |
|---|---|---|---|
| `thresholds.yaml` | Ngưỡng cảnh báo, cửa sổ baseline, tham số dự phóng | 👔 Trade Marketing | ❌ **KHÔNG** |
| `policy.yaml` | Danh sách hành động đóng, đòn bẩy bị cấm, luật phân bổ lại, quy trình duyệt | 👔 Trade Marketing + ⚖️ Pháp chế | ❌ **KHÔNG** |

## Luật

1. ❌ **Codex không bao giờ tự sửa hai file này.** Nếu một thay đổi code cần ngưỡng khác → **hỏi người**.
2. ✅ Mọi thay đổi đi qua **pull request có review**, kèm lý do nghiệp vụ trong mô tả PR.
3. 🔒 `policy.yaml` → `permitted_actions` và `forbidden_levers` là **ràng buộc pháp lý**, không phải sở thích.
   Thêm một hành động vào `permitted_actions` = **cần pháp chế xem lại** (xem `Business/06-open-questions.md` Q3).
4. 🧪 Code **đọc** từ hai file này. Không được hard-code lại một con số nào trong `.py`.
   Test rào chắn kiểm tra điều đó.

## Chốt giá trị ở đâu

Các ô `⬜ CHƯA CHỐT` nằm ở [`Business/02-task-business.md`](../Business/02-task-business.md) §4 và §5.
Chốt xong thì cập nhật file YAML ở đây và tick vào checklist bên đó.
