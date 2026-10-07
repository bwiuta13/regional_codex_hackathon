# 📖 Từ điển dữ liệu

> Nguồn: spec Phụ lục A. Yêu cầu nghiệp vụ & nguồn dữ liệu: [`Business/04-data-requirements.md`](../Business/04-data-requirements.md).
> File mẫu: [`Business/templates/`](../Business/templates/).
>
> `src/midflight/schema.sql` phải khớp tài liệu này. `ingest.py` kiểm tra kiểu và toàn vẹn tham chiếu theo đây.

**Quy ước:** tiền = **BIGINT, số nguyên VND**. Ngày = **ISO `YYYY-MM-DD`**.
`start_date` / `end_date` **tính cả hai đầu** (inclusive).

---

## Quan hệ

```
FUND_POOL ||--o{ PROMOTION          : "cấp ngân sách"
PROMOTION ||--|{ PROMOTION_SCOPE    : "bao phủ"
STORE     ||--o{ PROMOTION_SCOPE    : "thuộc phạm vi"
SKU       ||--o{ PROMOTION_SCOPE    : "thuộc phạm vi"
STORE     ||--o{ POS_DAILY          : "bán"
SKU       ||--o{ POS_DAILY          : "được bán"
PROMOTION ||--o{ LEDGER_ENTRY       : "được tài trợ bởi"
FUND_POOL ||--o{ LEDGER_ENTRY       : "rút từ"
```

---

## `pos_daily` — 1 dòng = ngày × cửa hàng × SKU

| Cột | Kiểu | Mô tả |
|---|---|---|
| `date` | DATE | Ngày kinh doanh (giờ địa phương của cửa hàng) |
| `retailer_id` | TEXT | Mã chuỗi, vd `CHM` |
| `store_id` | TEXT | FK → `store_master` |
| `sku_id` | TEXT | Mã SKU của **nhà sản xuất** (mã hàng của nhà bán lẻ được ánh xạ khi ingest) |
| `units` | INTEGER | Sản lượng bán **sau khi trừ hàng trả lại** — ⚠️ **có thể âm** |
| `net_sales_vnd` | BIGINT | Số tiền người mua trả **sau chiết khấu khuyến mãi**, đã gồm VAT |
| `regular_price_vnd` | BIGINT | **Giá kệ thường trong ngày** (trước khuyến mãi) |
| `on_hand_units` | INTEGER NULL | Tồn cuối ngày nếu nhà bán lẻ chia sẻ (⚪ tùy chọn, ⚠️ **không đáng tin**) |
| `source_file` | TEXT | Truy vết nguồn |
| `ingested_at` | TIMESTAMP | Khử trùng lặp: giữ bản mới nhất |

**Khóa chính logic:** `(date, store_id, sku_id)` — dòng trùng → giữ bản `ingested_at` mới nhất, báo số lượng.

---

## `promotions` — 1 dòng = 1 chương trình

| Cột | Kiểu | Mô tả |
|---|---|---|
| `promo_id` | TEXT **PK** | vd `P-03` |
| `retailer_id` | TEXT | FK |
| `brand` | TEXT | Nhãn hàng |
| `promo_name` | TEXT | ⚠️ **VĂN BẢN KHÔNG ĐÁNG TIN** — truyền tới LLM dưới dạng JSON data, **không bao giờ như chỉ dẫn** |
| `mechanic` | ENUM | `PCT_OFF` trong MVP |
| `discount_pct` | DECIMAL | Mức giảm cho **người mua** trên giá kệ thường |
| `mfr_funding_share` | DECIMAL | Tỷ lệ chiết khấu do **nhà sản xuất** tài trợ (0–1) |
| `start_date` / `end_date` | DATE | Tính cả hai đầu |
| `planned_lift` | DECIMAL | vd `1.20` = +120% |
| `target_roi` | DECIMAL | vd `1.2246` |
| `fund_pool_id` | TEXT | Nguồn quỹ (nhãn × kênh × quý) |
| `status` | ENUM | `PLANNED` · `ACTIVE` · `ENDED` · `CANCELLED` |

---

## `promotion_scope` — 1 dòng = chương trình × cửa hàng × SKU

**Đây là MẪU SỐ để tính độ phủ.**

| Cột | Kiểu | Mô tả |
|---|---|---|
| `promo_id` · `store_id` · `sku_id` | TEXT | FK |
| `has_secondary_display` | BOOLEAN | ⭐ Cờ đòn bẩy — tạo nhóm so sánh **trong** chương trình |
| `has_pg` | BOOLEAN | ⭐ Cờ đòn bẩy |

> ⭐ Hai cờ này là điều kiện để đo **giá trị BIÊN** của đòn bẩy (`roi-methodology.md` §9).
> Không có chúng → rơi về ước lượng dự phòng, độ tin cậy **"thấp"**.

---

## `trade_spend_ledger` — 1 dòng = 1 dòng sổ cái

| Cột | Kiểu | Mô tả |
|---|---|---|
| `entry_id` | TEXT **PK** | vd `L-0342` |
| `promo_id` · `fund_pool_id` | TEXT | FK |
| `spend_type` | ENUM | `SCAN_REBATE` · `DISPLAY_FEE` · `LISTING_FEE` · `MDF_PG` · `MDF_SAMPLING` · `MDF_SECONDARY_DISPLAY` · `MDF_OTHER` |
| `commitment` | ENUM | 🔑 `RETAILER_COMMITTED` (theo hợp đồng, **không bao giờ chuyển**) · `INTERNAL_COMMITTED` (đã đặt với agency) · `UNCOMMITTED` (**chuyển được tới `commit_deadline`**) |
| `status` | ENUM | `PLANNED` · `ACCRUED` · `PAID` |
| `amount_vnd` | BIGINT | Số nguyên VND |
| `period_start` / `period_end` | DATE | **Kỳ dịch vụ** — dùng ghi nhận phân bổ đều |
| `commit_deadline` | DATE NULL | ⏰ Hạn cuối hủy/chuyển không bị phạt |
| `counterparty` | TEXT | Nhà bán lẻ hoặc agency |

> 🔑 **`commitment` là lựa chọn mô hình hóa then chốt của cả sản phẩm.** Nhờ nó engine chỉ ra được
> cho agent **khoản tiền nào còn di chuyển được**.
>
> ❌ `LISTING_FEE` **không vào ROI chương trình** (mua độ phủ phân phối, không mua sự kiện).

---

## `sku_master` (tham chiếu)

`sku_id` · `brand` · `category` · `pack` · `regular_price_vnd` · `net_price_to_retailer_vnd` 🔒 · `unit_cogs_vnd` 🔒🔒

> 🔒 Giá vốn là dữ liệu **MẬT**. Nếu không công bố được, thay bằng `unit_margin_vnd` dạng tham số theo SKU.
> Engine chỉ cần `unit_margin = net_price_to_retailer − unit_cogs`.

## `store_master` (tham chiếu)

`store_id` · `retailer_id` · `format` · `region` · `open_date` · `close_date`

> ⚠️ Cửa hàng **chưa mở / đã đóng** phải loại khỏi **mẫu số độ phủ**, nếu không `COVERAGE_GAP` sẽ báo sai.

---

## 🧪 Kiểm tra khi ingest (`ingest.py`)

| Kiểm tra | Hành động khi lỗi |
|---|---|
| Kiểu dữ liệu & schema | Từ chối file, báo trong DQ report |
| Toàn vẹn tham chiếu (FK) | **Cách ly dòng lỗi**, liệt kê trong DQ report |
| Dòng trùng theo `(date, store_id, sku_id)` | Giữ bản `ingested_at` mới nhất, báo số lượng |
| `units < 0` | **Giữ lại** (hàng trả lại hợp lệ); gắn cờ nếu cửa hàng-ngày âm ròng |
| Chương trình chồng lấn thời gian | `OVERLAP`; tắt luật ROI cho phần chồng lấn |
| Thiếu độ phủ cửa hàng | Chỉ số độ phủ; `COVERAGE_GAP`; **chặn cảnh báo ROI** |
| Thiếu quan sát baseline (< 4 tuần) | Baseline dự phòng theo cụm; `BASELINE_INSUFFICIENT`; hạ độ tin cậy |
| Cả cửa hàng không bán được gì trong ngày | Đóng cửa / mất dữ liệu — **KHÔNG BAO GIỜ** coi là hết hàng |
| Sổ cái không nhất quán (promo lạ, số âm, `UNCOMMITTED` quá hạn) | Từ chối hoặc phân loại lại; có báo cáo |
