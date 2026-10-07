# 📐 Phương pháp tính ROI — NGUỒN SỰ THẬT

> **Vai trò A (Dữ liệu & chỉ số) + 📊 Data Science sở hữu file này.**
>
> 🔴 `src/midflight/evaluate.py` và `alert.py` **PHẢI** khớp chính xác tài liệu này.
> Khi lệch nhau: tài liệu đúng, code sai. `make drift` kiểm tra tự động, CI báo lỗi nếu có lệch.
>
> Nguồn: spec §4.4. Golden test mã hóa ví dụ ở `Business/05-demo-scenario-numbers.md`.

**Ký hiệu:** chương trình *p* · cửa hàng *s* · SKU *k* · ngày *d* · ngày chốt *t*.
**Tiền: số nguyên VND.** Không dùng float cho tiền ở bất kỳ đâu.

---

## 1 · Baseline — doanh số lẽ ra có nếu không khuyến mãi

Baseline theo **"ngày sạch" + thứ trong tuần**, giống cách các hãng đo lường syndicated xây baseline:
bỏ các giai đoạn có khuyến mãi, rồi ước lượng mức nền và tính mùa vụ ở cấp cửa hàng × mặt hàng.

```
ngày sạch   = SKU không khuyến mãi
              VÀ không nằm trong 14 ngày sau một đợt khuyến mãi
              VÀ ngoài khung ngày lễ (Tết căn theo ÂM LỊCH)
              VÀ không phải ngày nghi hết hàng
              rồi cắt bỏ 2.5% số ngày cao nhất và thấp nhất

w(k)        = chỉ số thứ trong tuần
            = sản lượng TB ngày sạch rơi vào thứ k ÷ sản lượng TB ngày sạch
              (ước lượng ở cấp cửa hàng × NGÀNH HÀNG cho ổn định; cần ≥ 8 tuần ngày sạch)

L[s,k]      = mức nền = trung bình của (units_d ÷ w(dow_d)) trên 28–56 ngày sạch gần nhất

baseline_d  = L[s,k] × w(dow_d) × trend_d

trend_d     = Σ thực tế cửa hàng đối chứng_d ÷ Σ baseline đối chứng_d , kẹp trong [0.8, 1.2]
              đối chứng = cùng chuỗi, NGOÀI phạm vi chương trình, ≥ 10 cửa hàng
              không đủ → trend = 1.0

dự phòng    = không có lịch sử dùng được
            → tốc độ bán trung vị của SKU trong cụm (chuỗi × định dạng × vùng) × chỉ số quy mô cửa hàng
            → gắn cờ BASELINE_FALLBACK  (hoặc MISSING_BASELINE và loại khỏi tính toán)
```

Tham số: [`config/thresholds.yaml`](../config/thresholds.yaml) → `baseline:`

> 🚫 **Chủ động KHÔNG làm ở MVP:** baseline hồi quy, CausalImpact (Bayesian structural time series),
> synthetic control. Chúng cần giai đoạn trước dài & sạch cùng nhóm đối chứng, trong khi
> **tờ rơi toàn chuỗi thường làm nhiễu các nhóm này**. Để v2 — và nói rõ lý do khi pitch.

<!-- TODO(DS): xác nhận danh sách ngày lễ loại trừ theo âm lịch 2026-2027 -->
<!-- TODO(DS): xác nhận có loại trừ nào đặc thù VN khác không (ngày lương về, Rằm...) -->

---

## 2 · Sản lượng

```
incremental_units = actual_units − baseline_units
lift              = actual_units ÷ baseline_units − 1
```

---

## 3 · Lợi nhuận gộp tăng thêm (iGP) — góc nhìn NHÀ SẢN XUẤT

```
unit_margin = net_price_to_retailer − unit_COGS
iGP         = incremental_units × unit_margin
```

**Giả định (ghi rõ):** sản lượng bán ra tăng thêm chuyển **1:1** thành sản lượng giao hàng trong
chu kỳ khuyến mãi. **Loại trừ** việc nhà bán lẻ gom hàng trước (forward-buying).

---

## 4 · Chi phí trade ghi nhận lũy kế

```
variable    = discounted_units × regular_shelf_price × discount_pct × mfr_funding_share   # scan rebate
fixed       = Σ khoản trọn gói cho sự kiện (trưng bày, feature, tờ rơi)
              × tỷ lệ SẢN LƯỢNG KẾ HOẠCH lũy kế
discretion  = Σ các dòng MDF ghi nhận theo kỳ dịch vụ
trade_spend = variable + fixed + discretion
```

| Quy tắc | Lý do |
|---|---|
| ✅ Chỉ tính phần chiết khấu **do nhà sản xuất tài trợ** | Phần nhà bán lẻ thuộc P&L của nhà bán lẻ |
| ❌ **Loại phí niêm yết (`LISTING_FEE`)** khỏi ROI chương trình | Nó mua **độ phủ phân phối**, không mua sự kiện → theo dõi riêng |
| 📊 Khoản trọn gói phân bổ theo **tỷ lệ sản lượng kế hoạch lũy kế** | Một trong các phương án trích trước chuẩn của hệ RGM. Khi kế hoạch đều theo ngày thì bằng tỷ lệ thời gian đã qua |
| 👁️ Song song có **"góc nhìn cam kết"** ghi nhận toàn bộ khoản trọn gói từ ngày 1 | Dự phóng cuối kỳ **luôn dùng toàn bộ số tiền** |
| 🚫 Cửa hàng-ngày chỉ tính là *có chiết khấu* khi chiết khấu thực tế ≥ **50% kế hoạch** | Ngược lại → gắn cờ không tuân thủ và **không phát sinh scan rebate** |

---

## 5 · ROI

```
ROI     = iGP ÷ trade_spend          # x; 1.0x = hòa vốn
net     = iGP − trade_spend           # VND
ROI_gap = ROI_to_date ÷ plan_ROI_to_date − 1
```

⚠️ **Đường kế hoạch lũy kế áp dụng CÙNG công thức trên sản lượng kế hoạch theo ngày.**
Không được dùng công thức khác cho kế hoạch và thực tế.

Lãi ròng tăng thêm cũng viết được là:

```
net = I × (m − d_m) − B × d_m − F
```

Số hạng `B × d_m` là **tiền chiết khấu trả cho những sản phẩm baseline vốn dĩ vẫn bán được**,
và thường chính nó làm chương trình lỗ.

> 📌 Ngành **chưa có một công thức ROI chuẩn duy nhất.** MidFlight gọi tên rõ định nghĩa của mình
> và áp dụng y hệt cho cả kế hoạch lẫn thực tế. Đó là điều phải nói khi giám khảo hỏi "ROI của các bạn là gì".

---

## 6 · Tỷ lệ chiết khấu thực tế & tuân thủ giá

```
realized_discount = 1 − Σ net_sales ÷ Σ (units × regular_shelf_price)

trạng thái cửa hàng (gộp ngày cho tới khi ≥ 5 sản phẩm):
  NOT_APPLIED   thực tế < max(5%, 50% × kế hoạch)
  PARTIAL       thực tế < kế hoạch − 2 điểm %
  OK            trong khoảng ±2 điểm % quanh kế hoạch
  STACKED       thực tế > kế hoạch + 2 điểm %     ← có bên đang giảm thêm: AI tài trợ phần đó?
```

- Tính ở **cả 3 cấp**: chuỗi, cửa hàng, ngày. ⚠️ Vấn đề thường **chỉ lộ ở cấp cửa hàng**.
- Giá kệ thường đối chiếu với **giá phổ biến nhất (mode) trong các ngày sạch**.
- **Ngày bắt đầu thực tế** của chương trình xác định từ **giá thực tế** — nhà bán lẻ đôi khi
  bắt đầu sớm hoặc muộn một tuần so với master data.

---

## 7 · Dự phóng đến cuối chương trình

```
lift_recent     = min( lift lũy kế , lift của 3 ngày gần nhất )   # lift đã hiệu chỉnh thứ-trong-tuần
projected_units = lũy kế + Σ baseline_d (ngày còn lại) × (1 + lift_recent)
projected_spend = sản lượng có chiết khấu dự phóng × rebate
                  + TOÀN BỘ khoản trọn gói
                  + chi phí tùy nghi còn lại
band            = P10–P90 từ 500 lần bootstrap theo cửa hàng   ← MỤC CẮT ĐẦU TIÊN nếu thiếu thời gian
```

**Vì sao lấy `min`:** bắt được cả hiện tượng khuyến mãi **"hụt hơi"** (lift thường đạt đỉnh tuần đầu)
lẫn các **cú gãy** như một làn sóng hết hàng.

⚠️ **Tên phương pháp phải ghi vào snapshot:** `projection.method = "trailing_3d_run_rate"`.

---

## 8 · Nghi hết hàng CHỈ TỪ POS (không cần dữ liệu tồn kho)

> 65% bản ghi tồn kho tại cửa hàng không chính xác (DeHoratius & Raman 2008)
> → **không tin tồn kho hệ thống**, suy ra từ POS.

```
λ_d = baseline_d × (1 + min(lift quan sát ở các cửa hàng BÌNH THƯỜNG cùng cụm, lift kế hoạch))

gắn cờ cửa hàng × SKU khi CẢ BA:
  (1) k ≥ 2 ngày liên tiếp không bán được
  (2) VÀ cửa hàng vẫn có doanh số các SKU KHÁC trong những ngày đó   (đang mở, dữ liệu vẫn về)
  (3) VÀ P = exp(−Σ λ_d) < 0.001       (tương đương Σ λ_d > 6.9 sản phẩm kỳ vọng)

sau đó: sản lượng mất ≈ Σ λ_d trên các ngày bị gắn cờ
        các ngày này bị LOẠI khỏi baseline về sau
```

**Ví dụ:** λ = 3,0 × (1 + 100%) = 6,0 sp/ngày. Hai ngày không bán được → P = e^(−12) ≈ 6 × 10⁻⁶ → gắn cờ.
Nếu áp dụng cùng luật mà **bỏ qua lift** (λ = 3,0) → cần **3** ngày.

**Bằng chứng ủng hộ ngưỡng thận trọng:** gắn cờ **mọi** ngày không bán được → **37% báo động giả**.
Kiểm định dựa trên **2 ngày liên tiếp** → **7,7%**, đổi lại tỷ lệ phát hiện thấp hơn.
Các kiểm định "doanh số thấp bất thường nhưng khác 0" **phần lớn là báo động giả**
→ **MidFlight coi doanh số thấp là `LOW_LIFT`, KHÔNG phải hết hàng.**

---

## 9 · Logic phân bổ lại (tất định, CHẠY TRƯỚC LLM)

```
điều kiện: đã chạy ≥ 7 ngày (đủ 1 chu kỳ thứ-trong-tuần) VÀ ROI_BEHIND_PLAN đã được XÁC NHẬN

bên cho:   có lỗi thực thi HOẶC ROI dự phóng < 0.90 × kế hoạch
           và có dòng UNCOMMITTED chưa quá hạn commit_deadline

bên nhận:  cùng nguồn quỹ
           ROI dự phóng > 1.10 × kế hoạch
           không có cờ thực thi
           còn ≥ 7 ngày
           dư địa = chi phí của đòn bẩy còn thiếu (vd trưng bày phụ ở các cửa hàng chưa có)

amount = min( phần chưa cam kết của bên cho,
              dư địa bên nhận,
              30% × ngân sách trọn gói kế hoạch của bên nhận )

# GIÁ TRỊ BIÊN của đòn bẩy — ƯU TIÊN đo NGAY TRONG chương trình nhận:
uplift = lift(cửa hàng CÓ đòn bẩy) − lift(cửa hàng KHÔNG có)       [sp/cửa hàng/ngày]
value  = uplift × số cửa hàng-ngày được tài trợ × (unit_margin − rebate) × haircut − amount

# DỰ PHÒNG (không có nhóm so sánh) → độ tin cậy "thấp":
value  = amount × ROI dự phóng × haircut − amount

chọn phương án tốt nhất trong { giữ ở bên cho , hoãn , phân bổ lại }
CÔNG BỐ haircut hòa vốn kèm khuyến nghị
```

**⚠️ Vì sao luật này tồn tại — ROI *biên* thấp hơn ROI *bình quân*.**
Đồng tiền bỏ thêm vào chương trình tốt nhất mua được **ít hơn** những đồng đã có, vì:

1. phản ứng của thị trường **bão hòa dần**;
2. một phần lift đến từ **trưng bày đã trả tiền rồi**;
3. **tồn kho hoặc diện tích kệ** giới hạn phần sản lượng thêm.

Cộng thêm: chọn con số cao nhất trong nhiều ước lượng ROI nhiễu khiến bên thắng bị thổi phồng —
**"lời nguyền của người tối ưu"** (optimizer's curse, Smith & Winkler 2006).

Vì vậy MidFlight đo lợi ích của **đúng đòn bẩy mà khoản tiền sẽ mua**, dựa trên các cửa hàng
trong chương trình nhận **đã có** đòn bẩy đó. Kết quả nhân **haircut 0,70** để trừ thiên lệch chọn mẫu
(cửa hàng được làm trưng bày trước có thể vốn là cửa hàng tốt hơn), và **haircut hòa vốn được công bố kèm theo**.

**Kiểm chứng với ví dụ demo:** cửa hàng có trưng bày phụ bán thêm 10 sp/ngày.
Tài trợ thêm 20 cửa hàng trong 7 ngày → **27,3 tr** lợi nhuận đóng góp trước haircut, so với chi phí **14 tr**.
→ phân bổ lại tốt hơn hoãn **miễn là hiệu ứng thật đạt ≥ 51%** hiệu ứng đo được.

---

## 10 · ⚠️ Giới hạn đã biết — GHI RÕ, KHÔNG CHE GIẤU

| Chưa làm ở MVP | Ghi chú |
|---|---|
| Ăn mòn doanh số (cannibalisation) | v2 |
| Hiệu ứng lan tỏa (halo) | v2 |
| Sụt giảm sau khuyến mãi (post-promo dip) | Bằng 4–25% hiệu ứng khuyến mãi (van Heerde 2000) — ghi nhận, chưa trừ |
| Nhà bán lẻ gom hàng trước (forward-buying) | Giả định sell-out ≈ sell-in trong chu kỳ |
| Dự phóng chỉ dùng run-rate | Đơn giản, giải thích được, đủ cho quyết định giữa chừng |
| Khuyến mãi chồng lấn | **Gắn cờ `OVERLAP` thay vì phân bổ** — không đoán bừa |

Các giới hạn này phải hiện **trên UI và trong hồ sơ chênh lệch**, không giấu trong tài liệu.
