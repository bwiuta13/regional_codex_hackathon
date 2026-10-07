# 📄 File CSV mẫu

Header chuẩn + vài dòng mẫu cho 6 bộ dữ liệu. Dùng để:

1. 📊 **Data Science** đối chiếu khi viết `src/midflight/mockdata.py`
2. 👔 **Business** thấy rõ mỗi cột trông như thế nào bằng dữ liệu thật
3. 🧪 Làm fixture nhỏ cho test ingest

**Đặc tả đầy đủ từng cột:** [`../04-data-requirements.md`](../04-data-requirements.md)

```bash
# Khi đã điền xong, copy sang thư mục fixture của repo
cp Business/templates/*.csv data/fixtures/
```

| File | Độ chi tiết | Ai sinh ra |
|---|---|---|
| `pos_daily.sample.csv` | ngày × cửa hàng × SKU | Nhà bán lẻ / `midflight generate` |
| `promotions.sample.csv` | chương trình | Trade marketing / TPM |
| `promotion_scope.sample.csv` | chương trình × cửa hàng × SKU | Trade marketing + KAM |
| `trade_spend_ledger.sample.csv` | dòng sổ cái | Tài chính / TPM |
| `sku_master.sample.csv` | SKU | Nhà sản xuất 🔒 |
| `store_master.sample.csv` | cửa hàng | Nhà bán lẻ |

> ⚠️ **Quy ước:** tiền là **số nguyên VND** (không dùng float, không dấu phân cách).
> Ngày theo **ISO `YYYY-MM-DD`**. `start_date` / `end_date` **tính cả hai đầu**.
