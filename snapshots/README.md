# 🔒 snapshots/ — đầu ra BẤT BIẾN

```
snapshots/<as_of_date>/<promo_id>.json
# vd: snapshots/2026-10-07/P-03.json
```

## Vì sao thư mục này tồn tại

Snapshot là **điểm bàn giao DUY NHẤT** giữa lõi tất định và mọi thành phần còn lại
(agent, dashboard, hồ sơ chênh lệch).

→ Dashboard và agent **cùng đọc một file**, nên những gì người dùng **thấy** và những gì agent
**nói** **không thể lệch nhau**. Đó là cả lý do thiết kế.

## 🔒 Luật

1. **CHỈ ĐƯỢC GHI THÊM.** Không bao giờ ghi đè một snapshot đã tồn tại.
2. **Tái lập được.** Cùng đầu vào + cùng code → **cùng `content_hash`**.
   Hash khác nhau mà đầu vào giống nhau = **có lỗi**, phải báo rõ ràng.
3. Đầu vào thay đổi → sinh snapshot **mới**, không sửa cái cũ.
4. **Dashboard chỉ ĐỌC**, không bao giờ tự tính lại chỉ số.

## Truy vết

Mỗi snapshot mang:

| Trường | Dùng để |
|---|---|
| `snapshot_id` | `"P-03@2026-10-07#9f2c1e7a"` — định danh người đọc được |
| `schema_version` | Biết cấu trúc nào đang dùng |
| `metric_version` | **git SHA của code tính chỉ số** — con số trông lạ thì truy được code nào tính ra nó |
| `content_hash` | sha256 nội dung đã chuẩn hóa |

## ⏱️ "Du hành thời gian" trong demo

Thanh trượt ngày chốt trên dashboard **chỉ đơn giản là nạp snapshot của ngày cũ hơn**.
Không tính lại gì cả. Nhờ vậy nó vừa nhanh vừa không thể sai.

```
snapshots/2026-10-03/P-03.json   ROI 0.907x
snapshots/2026-10-04/P-03.json   ROI 0.837x   <- DISCOUNT_NOT_APPLIED phát lần đầu
snapshots/2026-10-05/P-03.json   ROI 0.794x   <- STOCKOUT_SUSPECTED phát lần đầu
snapshots/2026-10-07/P-03.json   ROI 0.743x   <- ROI_BEHIND_PLAN xác nhận -> phân bổ lại
```

> `snapshots/` của bản demo **nên được commit** để pitch chạy được kể cả khi pipeline hỏng.
