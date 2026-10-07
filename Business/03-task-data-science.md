# 03 · 📊 TASK CHO BẠN BÊN DATA SCIENCE

> Bạn chuyển định nghĩa nghiệp vụ (👔 `02-task-business.md`) thành **công thức kiểm chứng được**,
> rồi sinh bộ dữ liệu giả lập sao cho engine chạy ra **đúng từng đồng** số liệu Phụ lục B.
>
> ⚠️ **Bạn KHÔNG viết code production.** Codex viết `src/midflight/*.py` trong ngày thi,
> dựa trên `docs/roi-methodology.md` do bạn hoàn thiện. Việc của bạn là: **công thức + dữ liệu + số kỳ vọng.**

**Trạng thái tổng:** `⬜ 0 / 18 hạng mục đã chốt`

---

## §1 · 🔴 Deliverable chặn — 3 thứ phải có trước ngày thi

| # | Deliverable | File đích | Vì sao chặn |
|---|---|---|---|
| 1.1 | Bộ dữ liệu giả lập 6 chương trình × 3 chuỗi, có seed | `data/fixtures/*.csv` | Không có dữ liệu = không demo được |
| 1.2 | Bảng số kỳ vọng ngày 3/4/5/7 **tới từng đồng** | `05-demo-scenario-numbers.md` | Golden test viết TRƯỚC, Codex làm cho pass |
| 1.3 | `docs/roi-methodology.md` đã rà soát & điền hết `TODO(DS)` | `docs/roi-methodology.md` | Đây là nguồn sự thật Codex đọc |

---

## §2 · Baseline — phần khó nhất về mặt phương pháp

**Baseline = doanh số lẽ ra có nếu không khuyến mãi.** Sai baseline → sai lift → sai iGP → sai ROI.
Đây là baseline theo **"ngày sạch" + thứ trong tuần**, giống cách các hãng đo lường syndicated xây baseline.

```
ngày sạch   = SKU không khuyến mãi
              VÀ không nằm trong 14 ngày sau một đợt khuyến mãi   (tránh sụt giảm hậu khuyến mãi)
              VÀ ngoài khung ngày lễ (Tết căn theo ÂM LỊCH)
              VÀ không phải ngày nghi hết hàng
              rồi cắt bỏ 2.5% số ngày cao nhất và thấp nhất

w(k)        = chỉ số thứ trong tuần
            = sản lượng TB ngày sạch rơi vào thứ k ÷ sản lượng TB ngày sạch
              (ước lượng ở cấp cửa hàng × NGÀNH HÀNG cho ổn định; cần ≥ 8 tuần ngày sạch)

L[s,k]      = mức nền = trung bình của (units_d ÷ w(dow_d)) trên 28–56 ngày sạch gần nhất

baseline_d  = L[s,k] × w(dow_d) × trend_d

trend_d     = Σ thực tế cửa hàng đối chứng_d ÷ Σ baseline đối chứng_d , kẹp trong [0.8, 1.2]
              (đối chứng = cùng chuỗi, NGOÀI phạm vi chương trình, ≥ 10 cửa hàng;
               nếu không đủ → trend = 1.0)

dự phòng    = không có lịch sử dùng được
            → tốc độ bán trung vị của SKU trong cụm (chuỗi × định dạng × vùng) × chỉ số quy mô cửa hàng
            → gắn cờ BASELINE_FALLBACK  (hoặc MISSING_BASELINE và loại khỏi tính toán)
```

| # | Việc | Trạng thái |
|---|---|---|
| 2.1 | Rà lại định nghĩa "ngày sạch" — có loại trừ nào đặc thù VN không? (VD: ngày lễ, lương về, Rằm) | ⬜ |
| 2.2 | Xác nhận khung ngày lễ căn theo **âm lịch** (Tết). Danh sách ngày loại trừ 2026–2027? | ⬜ |
| 2.3 | Chốt cửa sổ `clean_days_lookback` = 56, `min_clean_weeks` = 8 có khả thi với dữ liệu giả lập không? | ⬜ |
| 2.4 | Dữ liệu giả lập phải có **56 ngày tiền-khuyến-mãi sạch** để baseline ổn định | ⬜ |
| 2.5 | Nhóm đối chứng: có đủ ≥ 10 cửa hàng cùng chuỗi **ngoài phạm vi** trong dữ liệu giả lập không? | ⬜ |

> 🚫 **Chủ động KHÔNG làm ở MVP:** baseline hồi quy, CausalImpact (Bayesian structural time series),
> synthetic control. Chúng cần giai đoạn trước dài & sạch cùng nhóm đối chứng, trong khi **tờ rơi
> toàn chuỗi thường làm nhiễu các nhóm này**. Để v2 — và **nói rõ điều này với giám khảo** là một điểm cộng
> về chiều sâu tư duy, không phải điểm trừ.

---

## §3 · Chuỗi công thức chỉ số (nguồn: spec §4.4)

```
# 2. Sản lượng
incremental_units = actual_units − baseline_units
lift              = actual_units ÷ baseline_units − 1

# 3. Lợi nhuận gộp tăng thêm (góc nhìn NHÀ SẢN XUẤT)
unit_margin = net_price_to_retailer − unit_COGS
iGP         = incremental_units × unit_margin
# Giả định: sản lượng bán ra tăng thêm chuyển 1:1 thành sản lượng giao hàng trong chu kỳ.
#           Loại trừ việc nhà bán lẻ gom hàng trước (forward-buying).

# 4. Chi phí trade ghi nhận lũy kế
variable    = discounted_units × regular_shelf_price × discount_pct × mfr_funding_share   # scan rebate
fixed       = Σ khoản trọn gói (trưng bày, feature, tờ rơi) × tỷ lệ SẢN LƯỢNG KẾ HOẠCH lũy kế
discretion  = Σ các dòng MDF ghi nhận theo kỳ dịch vụ
trade_spend = variable + fixed + discretion

# 5. ROI
ROI     = iGP ÷ trade_spend           # 1.0x = hòa vốn
net     = iGP − trade_spend           # VND
ROI_gap = ROI_to_date ÷ plan_ROI_to_date − 1
```

| # | Quy tắc tính toán cần DS kiểm chứng | Trạng thái |
|---|---|---|
| 3.1 | **Chỉ tính phần chiết khấu do nhà sản xuất tài trợ.** Phần nhà bán lẻ thuộc P&L của họ | ⬜ |
| 3.2 | **Loại phí niêm yết (listing fee) khỏi ROI chương trình** — nó mua độ phủ phân phối, không mua sự kiện | ⬜ |
| 3.3 | Khoản trọn gói phân bổ theo **tỷ lệ sản lượng kế hoạch lũy kế** (chuẩn trích trước của hệ RGM). Khi kế hoạch đều theo ngày thì bằng tỷ lệ thời gian đã qua | ⬜ |
| 3.4 | Song song có **"góc nhìn cam kết"** ghi nhận toàn bộ khoản trọn gói từ ngày 1; **dự phóng cuối kỳ luôn dùng toàn bộ số tiền** | ⬜ |
| 3.5 | Một cửa hàng-ngày chỉ tính là *có chiết khấu* khi chiết khấu thực tế ≥ **50%** kế hoạch. Ngược lại → gắn cờ không tuân thủ, **không phát sinh scan rebate** | ⬜ |
| 3.6 | Đường kế hoạch lũy kế dùng **cùng công thức** trên sản lượng kế hoạch theo ngày (không được dùng công thức khác) | ⬜ |

> 📌 **Ngành chưa có một công thức ROI chuẩn duy nhất.** MidFlight gọi tên rõ định nghĩa của mình
> và áp dụng **y hệt cho cả kế hoạch lẫn thực tế**. Đó là điều phải nói khi giám khảo hỏi "ROI của các bạn là gì".

---

## §4 · Tỷ lệ chiết khấu thực tế & tuân thủ giá

```
realized_discount = 1 − Σ net_sales ÷ Σ (units × regular_shelf_price)

trạng thái cửa hàng (gộp ngày cho tới khi ≥ 5 sản phẩm):
  NOT_APPLIED   thực tế < max(5%, 50% × kế hoạch)
  PARTIAL       thực tế < kế hoạch − 2 điểm %
  OK            trong khoảng ±2 điểm % quanh kế hoạch
  STACKED       thực tế > kế hoạch + 2 điểm %   ← có bên đang giảm thêm: AI tài trợ phần đó?
```

| # | Việc | Trạng thái |
|---|---|---|
| 4.1 | Tính ở **cả 3 cấp**: chuỗi, cửa hàng, ngày. ⚠️ Vấn đề thường **chỉ lộ ở cấp cửa hàng** | ⬜ |
| 4.2 | Giá kệ thường đối chiếu với **giá phổ biến nhất (mode) trong các ngày sạch** | ⬜ |
| 4.3 | **Ngày bắt đầu thực tế** của chương trình xác định từ GIÁ THỰC TẾ (nhà bán lẻ hay bắt đầu sớm/muộn 1 tuần) | ⬜ |

> 🎯 Đây là **cú twist của demo**: chiết khấu cấp chuỗi 19,1% trông bình thường so với kế hoạch 20%,
> nên mọi báo cáo tổng hợp sẽ **bỏ sót vấn đề**. Chỉ ở cấp cửa hàng mới thấy 27 cửa hàng không bán được
> gì từ ngày 3 và 9 cửa hàng vẫn bán nguyên giá. Hãy đảm bảo dữ liệu giả lập tái tạo đúng hiệu ứng này.

---

## §5 · Phát hiện hết hàng CHỈ TỪ POS (không cần dữ liệu tồn kho)

Vì **65% bản ghi tồn kho tại cửa hàng không chính xác** (DeHoratius & Raman 2008), ta không tin tồn kho hệ thống.

```
λ_d = baseline_d × (1 + min(lift quan sát ở các cửa hàng BÌNH THƯỜNG cùng cụm, lift kế hoạch))

gắn cờ cửa hàng × SKU khi CẢ BA điều kiện:
  (1) k ≥ 2 ngày liên tiếp không bán được
  (2) VÀ cửa hàng vẫn có doanh số các SKU KHÁC trong những ngày đó  (đang mở, dữ liệu vẫn về)
  (3) VÀ P = exp(−Σ λ_d) < 0.001        (tương đương Σ λ_d > 6.9 sản phẩm kỳ vọng)

sau đó: sản lượng mất ≈ Σ λ_d trên các ngày bị gắn cờ
        các ngày này bị LOẠI khỏi baseline về sau
```

**Kiểm chứng số của spec:** λ = 3,0 × (1 + 100%) = 6,0 sản phẩm/ngày.
2 ngày không bán được → P = e^(−12) ≈ 6,1 × 10⁻⁶ < 0,001 → **gắn cờ**.
Nếu bỏ qua lift (λ = 3,0): k=2 → e^(−6) = 2,5 × 10⁻³ → **chưa gắn cờ**, cần 3 ngày.

| # | Việc | Trạng thái |
|---|---|---|
| 5.1 | Verify lại phép tính trên bằng script, ghi vào `05-demo-scenario-numbers.md` | ⬜ |
| 5.2 | Điều kiện (2) rất quan trọng: **cả cửa hàng không bán được gì** = đóng cửa hoặc mất dữ liệu, **KHÔNG BAO GIỜ** là hết hàng | ⬜ |
| 5.3 | Đo tỷ lệ báo động giả của luật này trên dữ liệu giả lập | ⬜ |

> 📚 **Bằng chứng ủng hộ ngưỡng thận trọng:** trên dữ liệu POS bán lẻ, gắn cờ **mọi** ngày không bán được
> cho **37% báo động giả**. Kiểm định thống kê dựa trên **2 ngày liên tiếp** giảm còn **7,7%**, đổi lại
> tỷ lệ phát hiện thấp hơn. Các kiểm định "doanh số thấp bất thường nhưng khác 0" **phần lớn là báo động giả**
> → vì vậy MidFlight coi **doanh số thấp là LOW_LIFT, không phải hết hàng**.

---

## §6 · Dự phóng đến cuối chương trình

```
lift_recent     = min( lift lũy kế , lift của 3 ngày gần nhất )     # lift đã điều chỉnh theo thứ trong tuần
projected_units = lũy kế + Σ baseline_d (các ngày còn lại) × (1 + lift_recent)
projected_spend = sản lượng có chiết khấu dự phóng × rebate
                  + TOÀN BỘ khoản trọn gói
                  + chi phí tùy nghi còn lại
band            = P10–P90 từ 500 lần bootstrap theo cửa hàng    ← MỤC CẮT ĐẦU TIÊN nếu thiếu thời gian
```

| # | Việc | Trạng thái |
|---|---|---|
| 6.1 | Hiểu vì sao lấy `min`: bắt được cả **khuyến mãi "hụt hơi"** (lift đạt đỉnh tuần đầu) lẫn **cú gãy** như làn sóng hết hàng | ⬜ |
| 6.2 | **Tên phương pháp phải ghi vào snapshot** (`projection.method = "trailing_3d_run_rate"`) | ⬜ |
| 6.3 | Bootstrap band: chuẩn bị nhưng chấp nhận bị cắt | ⬜ |

---

## §7 · 💰 Giá trị biên của đòn bẩy — phần "chiều sâu tư duy" ăn điểm nhất

**Vì sao không dùng ROI bình quân:** đồng tiền bỏ thêm vào chương trình tốt nhất mua được **ít hơn**
những đồng đã có, vì (a) thị trường bão hòa dần, (b) một phần lift đến từ trưng bày **đã trả tiền rồi**,
(c) tồn kho/diện tích kệ giới hạn phần sản lượng thêm. Cộng thêm **"lời nguyền của người tối ưu"**:
chọn con số cao nhất trong nhiều ước lượng nhiễu làm bên thắng bị thổi phồng.

```
# ƯU TIÊN: đo NGAY TRONG chương trình nhận (within-promo split)
uplift = lift(cửa hàng CÓ đòn bẩy) − lift(cửa hàng KHÔNG có)      [sản phẩm/cửa hàng/ngày]
value  = uplift × số cửa hàng-ngày được tài trợ × (unit_margin − rebate) × haircut − amount

# DỰ PHÒNG (không có nhóm so sánh): độ tin cậy "thấp"
value  = amount × ROI dự phóng × haircut − amount

amount = min( phần chưa cam kết của bên cho,
              dư địa bên nhận,
              30% × ngân sách trọn gói kế hoạch của bên nhận )

chọn phương án tốt nhất trong { giữ ở bên cho , hoãn , phân bổ lại } ; CÔNG BỐ haircut hòa vốn
```

**Kiểm chứng với ví dụ demo:** cửa hàng có trưng bày phụ bán **+10 sản phẩm/ngày**.
Tài trợ thêm 20 cửa hàng × 7 ngày × 10 × (24.000 − 4.500) = **27,3 tr** lợi nhuận đóng góp trước haircut,
so với chi phí **14 tr**. → phân bổ lại tốt hơn hoãn **miễn là hiệu ứng thật đạt ≥ 51,3%** hiệu ứng đo được.

| # | Việc | Trạng thái |
|---|---|---|
| 7.1 | ⚠️ Dữ liệu giả lập **bắt buộc** có cờ `has_secondary_display` chia 20/20 ở P-05 để có nhóm so sánh | ⬜ |
| 7.2 | Verify `breakeven_haircut = 14 ÷ 27,30 = 0,513` | ⬜ |
| 7.3 | Giải thích được vì sao haircut 0,70 trừ **thiên lệch chọn mẫu** (cửa hàng được làm trưng bày trước có thể vốn đã là cửa hàng tốt hơn) | ⬜ |

---

## §8 · Giới hạn đã biết — GHI RÕ, KHÔNG CHE GIẤU

> Nói thẳng các giới hạn này trong pitch. Giám khảo sẽ đánh giá cao sự trung thực hơn là
> một mô hình tự nhận làm được mọi thứ.

| Chưa làm ở MVP | Vì sao chấp nhận được |
|---|---|
| Ăn mòn doanh số (cannibalisation) | Cần mô hình ngành hàng; v2 |
| Hiệu ứng lan tỏa (halo) | Như trên |
| Sụt giảm sau khuyến mãi (post-promo dip) | Bằng 4–25% hiệu ứng khuyến mãi (van Heerde 2000) — ghi nhận, chưa trừ |
| Nhà bán lẻ gom hàng trước (forward-buying) | Giả định sell-out ≈ sell-in trong chu kỳ |
| Dự phóng chỉ dùng run-rate | Đơn giản, giải thích được, đủ cho quyết định giữa chừng |
| Khuyến mãi chồng lấn | **Gắn cờ `OVERLAP` thay vì phân bổ** — không đoán bừa |

---

## §9 · Chất lượng dữ liệu — bẫy phải xử lý trong `ingest`

| # | Vấn đề | Cách phát hiện | Cách xử lý | ✔ |
|---|---|---|---|---|
| 9.1 | File POS về trễ/thiếu | danh sách file dự kiến (chuỗi, ngày) | loại ngày đó; `COVERAGE_GAP`; **chặn cảnh báo ROI** | ⬜ |
| 9.2 | Dòng trùng | khóa chính (ngày, cửa hàng, SKU) | giữ bản mới nhất theo `ingested_at`; báo số lượng | ⬜ |
| 9.3 | Sản lượng âm (hàng trả lại) | `units < 0` | **giữ lại**; gắn cờ nếu cửa hàng-ngày âm ròng | ⬜ |
| 9.4 | Cửa hàng / SKU lạ | kiểm tra khóa ngoại | cách ly dòng lỗi; liệt kê trong báo cáo DQ | ⬜ |
| 9.5 | Khuyến mãi chồng lấn | cùng cửa hàng × SKU trong 2 chương trình đang chạy | `OVERLAP`; **tắt luật ROI cho phần chồng lấn** | ⬜ |
| 9.6 | Ngày chương trình trong master sai | giá thực tế cho thấy chiết khấu bắt đầu sớm/muộn hơn | lấy ngày bắt đầu **thực tế** từ giá; gắn cờ | ⬜ |
| 9.7 | Cả cửa hàng không bán được gì | mọi SKU đều = 0 trong ngày | đóng cửa / mất dữ liệu — **KHÔNG BAO GIỜ** coi là hết hàng | ⬜ |
| 9.8 | Thiếu độ phủ cửa hàng | số cửa hàng có dữ liệu ÷ phạm vi | chỉ số độ phủ; chặn cảnh báo | ⬜ |
| 9.9 | Thiếu lịch sử baseline | < 4 tuần hợp lệ | baseline dự phòng theo cụm; `BASELINE_INSUFFICIENT`; **hạ độ tin cậy** | ⬜ |
| 9.10 | Sổ cái không nhất quán | chương trình lạ, số tiền âm, `UNCOMMITTED` đã quá hạn | từ chối hoặc phân loại lại; có báo cáo | ⬜ |

---

## §10 · Bộ sinh dữ liệu giả lập — spec chi tiết

File đích: `data/fixtures/`. Codex viết `src/midflight/mockdata.py` theo spec này.

```
midflight generate --seed 7
```

| # | Yêu cầu | Trạng thái |
|---|---|---|
| 10.1 | **Tất định**: cùng `--seed` → cùng byte đầu ra | ⬜ |
| 10.2 | **56 ngày tiền-khuyến-mãi sạch** (để baseline có ≥ 8 tuần) | ⬜ |
| 10.3 | 6 chương trình chạy đồng thời trên 3 chuỗi | ⬜ |
| 10.4 | **P-03** (Chuỗi M, 120 cửa hàng): cài sẵn 27 cửa hàng hết hàng **từ ngày 3**, 9 cửa hàng bán nguyên giá | ⬜ |
| 10.5 | **P-05** (Chuỗi H, 40 cửa hàng): chia 20/20 có/không `has_secondary_display` | ⬜ |
| 10.6 | Cài sẵn ít nhất 1 ca **chồng lấn**, 1 ca **thiếu độ phủ**, 1 ca **thiếu baseline** | ⬜ |
| 10.7 | ≥ 10 cửa hàng đối chứng cùng chuỗi **ngoài phạm vi** (cho `trend_d`) | ⬜ |
| 10.8 | Ghi đúng các CSV theo `04-data-requirements.md` | ⬜ |
| 10.9 | **Tiêu chí xong:** `midflight generate --seed 7 && midflight ingest` chỉ báo đúng các vấn đề **cố tình cài** | ⬜ |

---

## ✅ Định nghĩa "xong" cho Data Science

- [ ] `docs/roi-methodology.md` không còn `TODO(DS)` nào
- [ ] `data/fixtures/*.csv` sinh được bằng 1 lệnh, tất định
- [ ] `05-demo-scenario-numbers.md` khớp **tới từng đồng** với Phụ lục B spec
- [ ] Tự tính tay được ROI ngày 7 của P-03 = **0,743x** mà không cần chạy code
- [ ] Giải thích được **vì sao λ phải nhân với (1 + lift)** chứ không dùng baseline trần
- [ ] Giải thích được **vì sao ROI biên < ROI bình quân** trong 30 giây
