# 📌 data/fixtures/ — dữ liệu cố định (commit vào git)

Tập dữ liệu **nhỏ**, dùng cho test và để vai trò C dựng dashboard trước khi engine xong.

```bash
# Khởi tạo từ file mẫu Business đã điền
cp ../../Business/templates/*.csv .
```

| Nên có | Dùng cho |
|---|---|
| 6 CSV cơ bản (pos_daily, promotions, promotion_scope, trade_spend_ledger, sku_master, store_master) | test ingest "đường đi hạnh phúc" |
| Biến thể có **dòng trùng** | `test_deduplicates_by_latest_ingested_at` |
| Biến thể có **FK lỗi** | `test_quarantines_rows_with_broken_foreign_keys` |
| Biến thể có **units âm** | `test_keeps_negative_units_as_returns` |
| Biến thể **chồng lấn / thiếu độ phủ / thiếu baseline** | 3 test DQ của bài dự thi |

> 💡 Giữ file **nhỏ** (vài chục dòng). Test phải chạy trong vài giây.
> Dữ liệu đầy đủ 6 chương trình × 3 chuỗi × 77 ngày thuộc về `midflight generate`, không phải ở đây.
