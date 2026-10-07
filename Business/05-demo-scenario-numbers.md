# 05 · 🎯 SỐ LIỆU CHUẨN CHO KỊCH BẢN DEMO

> **Đây là hợp đồng giữa Data Science và vai trò A (engine).**
> Golden test `tests/test_evaluate_golden.py` phải tái tạo **chính xác tới từng đồng** các số dưới đây.
>
> 📏 **Quy tắc vàng:** nếu engine ra số khác → **sửa engine, KHÔNG BAO GIỜ sửa số kỳ vọng.**
> (Luật 2 trong `AGENTS.md`. Codex rất hay "sửa" test đỏ bằng cách đổi giá trị kỳ vọng — chặn ngay.)
>
> Nguồn: Phụ lục B của spec. 📊 DS verify lại **bằng script** và đánh dấu ✔ từng dòng.

---

## 0 · Kinh tế đơn vị chung (P-03 và P-05)

Cà phê hòa tan 3-in-1 nhãn A, hộp 18 gói.

| Hạng mục | Giá trị | ✔ DS verify |
|---|---:|---|
| Giá kệ thường `regular_price_vnd` | **60.000 đ** | ⬜ |
| Giá bán cho nhà bán lẻ `net_price_to_retailer_vnd` | **46.000 đ** | ⬜ |
| Giá vốn đơn vị `unit_cogs_vnd` | **22.000 đ** | ⬜ |
| **Biên lợi nhuận đơn vị `unit_margin`** | **24.000 đ** | ⬜ |

---

## 1 · P-03 — Chuỗi M, 120 cửa hàng, 01→21/10 (21 ngày), giảm 20%, đồng tài trợ 50/50

### 1.1 Thiết lập

| Hạng mục | Phép tính | Kết quả | ✔ |
|---|---|---:|---|
| Scan rebate / sản phẩm có chiết khấu | 60.000 × 20% × 50% | **6.000 đ** | ⬜ |
| Baseline | 120 cửa hàng × 3,0 sp/ngày | **360 sp/ngày** | ⬜ |
| Kế hoạch | 360 × 2,2 (lift +120%) | **792 sp/ngày** | ⬜ |
| Phí trưng bày (đã cam kết) | | 36 tr | ⬜ |
| MDF tùy nghi (PG, sampling) | 14 tr/tuần × 3 tuần | 42 tr | ⬜ |

### 1.2 Kế hoạch cả chương trình

| Hạng mục | Phép tính | Kết quả | ✔ |
|---|---|---:|---|
| Sản lượng tăng thêm | 432 × 21 | 9.072 sp | ⬜ |
| iGP kế hoạch | 9.072 × 24.000 | **217,73 tr** | ⬜ |
| Scan rebate kế hoạch | 16.632 sp × 6.000 | 99,79 tr | ⬜ |
| Tổng chi phí kế hoạch | 99,79 + 36 + 42 | 177,79 tr | ⬜ |
| **ROI kế hoạch** | 217,73 ÷ 177,79 | **1,22x** | ⬜ |
| Lãi ròng kế hoạch | | **+39,94 tr** | ⬜ |

### 1.3 🔧 Vấn đề cài sẵn — 3 nhóm cửa hàng

| Nhóm | Số cửa hàng | Hành vi | ✔ |
|---|---:|---|---|
| Bình thường | **84** | bán 6,0 sp/ngày | ⬜ |
| **Hết hàng** | **27** | bán bình thường ngày 1–2, rồi **0 sp từ ngày 3** | ⬜ |
| **Không áp giá KM** | **9** | bán **nguyên giá**, 3,0 sp/ngày (= baseline, không có lift) | ⬜ |

Sản lượng theo ngày:
- **Ngày 1–2:** 111 × 6 + 9 × 3 = **693 sp/ngày**
- **Ngày 3–7:** 84 × 6 + 27 × 0 + 9 × 3 = **531 sp/ngày**

### 1.4 🔴 Lũy kế đến ngày 7 — SỐ CHÍNH CỦA DEMO

| Chỉ số | Kế hoạch | Thực tế | Chênh lệch | ✔ |
|---|---:|---:|---:|---|
| Sản lượng bán | 5.544 | **4.041** | −27,1% | ⬜ |
| Baseline | | **2.520** | | ⬜ |
| Sản lượng tăng thêm | | **1.521** | | ⬜ |
| Lift so với baseline | +120% | **+60,4%** | | ⬜ |
| **iGP** | 72,58 tr | **36,50 tr** | −49,7% | ⬜ |
| Sản lượng có chiết khấu | | 3.852 | | ⬜ |
| Scan rebate | | 23,11 tr | | ⬜ |
| Trưng bày phân bổ (36 × 7/21) | | 12,00 tr | | ⬜ |
| MDF ghi nhận (2 tr/ngày × 7) | | 14,00 tr | | ⬜ |
| **Tổng chi phí trade** | 59,26 tr | **49,11 tr** | | ⬜ |
| **🎯 ROI** | **1,22x** | **0,743x** | **−39,3%** | ⬜ |
| Chiết khấu thực tế cấp chuỗi | 20,0% | **19,06%** | *trông bình thường* ⚠️ | ⬜ |
| Số cửa hàng nghi hết hàng | 0 | **27 (22,5%)** | | ⬜ |
| Số cửa hàng không áp giá KM | 0 | **9 (7,5%)** | | ⬜ |

Chiết khấu thực tế: `1 − 196,24 tr ÷ 242,46 tr = 19,06%`

> ⚠️ **Đây là cú twist của cả bài demo.** Chiết khấu cấp chuỗi 19,06% so với kế hoạch 20% trông
> hoàn toàn bình thường → **mọi báo cáo tổng hợp sẽ bỏ sót vấn đề**. Chỉ ở **cấp cửa hàng**
> mới thấy 27 cửa hàng không bán được gì từ ngày 3 và 9 cửa hàng vẫn bán nguyên giá.

### 1.5 ROI các ngày trước (golden test phải khớp cả 4 mốc)

| Ngày chốt | ROI | Chênh lệch vs kế hoạch | ✔ |
|---|---:|---:|---|
| Ngày 3 | **0,907x** | −26,0% | ⬜ |
| Ngày 4 | **0,837x** | −31,6% | ⬜ |
| Ngày 5 | **0,794x** | −35,2% | ⬜ |
| **Ngày 7** | **0,743x** | **−39,3%** | ⬜ |

### 1.6 Dự phóng cuối kỳ — 3 kịch bản

| Kịch bản | Phép tính | ROI | Lãi/lỗ ròng | ✔ |
|---|---|---:|---:|---|
| **Kế hoạch** | | 1,22x | **+39,9 tr** | ⬜ |
| **Giữ nguyên hiện trạng** (ngày 8–21 ở mức 531/ngày) | 11.475 sp, tăng thêm 3.915 → iGP 93,96 tr; chi phí 65,45 + 36 + 42 = 143,45 tr | **0,655x** | **−49,49 tr** | ⬜ |
| **Khắc phục từ ngày 9** (cả 120 cửa hàng bán 6,0/ngày, tuân thủ giá) | iGP 152,93 tr; chi phí 160,30 tr | **0,954x** | **−7,37 tr** | ⬜ |

**Cải thiện nhờ khắc phục = +42,12 tr**, tách ra:

| Nguồn | Phép tính | Giá trị | ✔ |
|---|---|---:|---|
| Xử lý **hết hàng** | 2.106 sp × (24.000 − 6.000) | **+37,91 tr** | ⬜ |
| Xử lý **tuân thủ giá** | | **+4,21 tr** | ⬜ |

### 1.7 Kiểm định hết hàng (Poisson)

| Bước | Phép tính | Kết quả | ✔ |
|---|---|---:|---|
| λ mỗi ngày | 3,0 × (1 + min(100%, 120%)) | **6,0 sp/ngày** | ⬜ |
| k = 2 ngày không bán được | e^(−12) | **6,1 × 10⁻⁶** < 0,001 → ✅ **gắn cờ** (tính đến ngày 4) | ⬜ |
| Đối chiếu: nếu bỏ qua lift (λ = 3,0) | e^(−6) | 2,5 × 10⁻³ > 0,001 → ❌ chưa gắn cờ, cần 3 ngày | ⬜ |

---

## 2 · P-05 — Chuỗi H, 40 cửa hàng, giảm 15%, 50/50 (chương trình NHẬN phân bổ)

| Hạng mục | Phép tính | Kết quả | ✔ |
|---|---|---:|---|
| Scan rebate / sản phẩm | 60.000 × 15% × 50% | **4.500 đ** | ⬜ |
| Baseline | 40 × 10 | **400 sp/ngày** | ⬜ |
| Kế hoạch (lift +80%) | 400 × 1,8 | **720 sp/ngày** | ⬜ |
| iGP kế hoạch | | 161,28 tr | ⬜ |
| Chi phí kế hoạch | trưng bày 40 tr + MDF 21 tr + rebate | 129,04 tr | ⬜ |
| **ROI kế hoạch** | | **1,25x** | ⬜ |

### 2.1 🔧 Thực tế — chia 20/20 (nhóm so sánh trong chương trình)

| Nhóm | Số cửa hàng | `has_secondary_display` | Bán | ✔ |
|---|---:|---|---:|---|
| Có trưng bày phụ | **20** | `true` | **30 sp/ngày** | ⬜ |
| Không có | **20** | `false` | **20 sp/ngày** | ⬜ |
| **Tổng** | 40 | | **1.000 sp/ngày (+150%)** | ⬜ |

| Lũy kế đến ngày 7 | Giá trị | ✔ |
|---|---:|---|
| iGP | **100,80 tr** | ⬜ |
| Chi phí | **51,83 tr** | ⬜ |
| **ROI** | **1,945x** (cao hơn kế hoạch **+55,6%**) | ⬜ |

> ⭐ Việc chia 20/20 **không phải ngẫu nhiên**. Nó tạo nhóm so sánh để đo **giá trị BIÊN** của
> đòn bẩy trưng bày phụ — thay vì suy ra từ ROI bình quân 1,945x (vốn sẽ thổi phồng kết quả).

---

## 3 · 💰 Quyết định phân bổ lại — MDF tuần 3

**Khoản tiền:** 14 tr · `UNCOMMITTED` · `commit_deadline = 12/10` · entry `L-0342` · haircut 0,70

| Phương án | Phép tính | Giá trị ròng | Độ tin cậy | ✔ |
|---|---|---:|---|---|
| **Giữ ở P-03** | 14 tr × 0,954 × 0,70 = 9,35 tr iGP − 14 tr | **−4,65 tr** | 🔴 **thấp** — mọi cửa hàng P-03 đều có PG nên **không có nhóm so sánh** | ⬜ |
| **Hoãn chi** | | **0** | — | ⬜ |
| **Chuyển sang trưng bày P-05** | xem dưới | **+5,11 tr** | 🟡 **trung bình** — đo được | ⬜ |

**Chi tiết phương án chuyển (within-promo split):**

| Bước | Phép tính | Kết quả | ✔ |
|---|---|---:|---|
| Hiệu ứng trưng bày | 30 − 20 | **10 sp/cửa hàng/ngày** | ⬜ |
| Đóng góp mỗi cửa hàng-ngày | 10 × (24.000 − 4.500) | **195.000 đ** | ⬜ |
| Tổng trước haircut | 20 cửa hàng × 7 ngày × 195.000 | **27,30 tr** | ⬜ |
| Sau haircut 0,70 | 27,30 × 0,70 | **19,11 tr** | ⬜ |
| Trừ chi phí | 19,11 − 14 | **+5,11 tr** | ⬜ |
| **Phân bổ lại thay vì giữ** | 5,11 − (−4,65) | **+9,76 tr** | ⬜ |
| **⚖️ Haircut hòa vốn** (so với hoãn) | 14 ÷ 27,30 | **0,513** | ⬜ |

**Trần số tiền:** `min(bên cho 14 tr, dư địa bên nhận 14 tr, 30% × 61 tr = 18,3 tr)` = **14 tr** ✔

> ⚖️ **Haircut hòa vốn 0,513 nghĩa là:** phân bổ lại tốt hơn hoãn chi **miễn là hiệu ứng thật
> đạt ít nhất 51,3%** hiệu ứng đo được. Con số này **được công bố kèm khuyến nghị** để người duyệt
> tự phán đoán — không bắt họ tin mù vào haircut 0,70.

---

## 4 · 🏆 Tác động danh mục

| Nguồn | Giá trị | ✔ |
|---|---:|---|
| Khắc phục hết hàng + tuân thủ giá ở P-03 | +42,12 tr | ⬜ |
| Tránh được khoản lỗ khi giữ tiền ở P-03 | +4,65 tr | ⬜ |
| Lợi ích ròng của trưng bày P-05 | +5,11 tr | ⬜ |
| **🎯 TỔNG so với giữ nguyên hiện trạng** | **+51,88 tr** | ⬜ |

**Và tất cả đạt được mà KHÔNG thay đổi:** mức giảm 20% trên giá kệ · tỷ lệ đồng tài trợ 50/50 ·
ngày chạy chương trình. ← câu chốt của pitch.

---

## 5 · ⏱️ Dòng thời gian cảnh báo (mỗi cảnh báo phát sáng hôm sau ngày dữ liệu)

| Sáng ngày | Dữ liệu tính đến | Cảnh báo | Bằng chứng | ✔ |
|---|---|---|---|---|
| **4/10** (ngày 4) | ngày 1–3 | `DISCOUNT_NOT_APPLIED` — 9 cửa hàng | chiết khấu thực tế 0% vs kế hoạch 20% | ⬜ |
| **5/10** (ngày 5) | ngày 1–4 | `STOCKOUT_SUSPECTED` — 27 cửa hàng<br>`ROI_BEHIND_PLAN` (sớm)<br>`LOW_LIFT` | 2 ngày liên tiếp không bán được, λ=6,0 → P ≈ 6×10⁻⁶<br>ROI 0,84x vs 1,22x (−31,6%)<br>lift +70% vs +120% | ⬜ |
| **8/10** (ngày 8) | ngày 1–7 | `ROI_BEHIND_PLAN` **xác nhận** (mức Cao) → kéo theo phân bổ lại | đã qua đủ 1 chu kỳ thứ-trong-tuần, chênh lệch vẫn kéo dài (−39,3%).<br>⏰ Kịp **trước hạn 12/10** của MDF tuần 3 | ⬜ |

> ✅ **Tiêu chí thành công của demo (§4.12 spec):** vấn đề cài sẵn ở P-03 phải được gắn cờ
> **trước hoặc đúng ngày 5/21** — tức còn ít nhất **16 ngày** để hành động.

---

## 6 · Các con số khác phải khớp

| Hạng mục | Giá trị | Dùng ở đâu | ✔ |
|---|---:|---|---|
| Cửa hàng-ngày hết hàng | **135** | hồ sơ chênh lệch | ⬜ |
| Cửa hàng-ngày không tuân thủ giá | **63** | hồ sơ + đối soát scan rebate | ⬜ |
| Phí trưng bày cần chứng minh thực thi | 36 tr | hồ sơ chênh lệch | ⬜ |
| `value_at_stake` của `ESCALATE_STOCKOUT` | **37.908.000 đ** | snapshot `candidates[C1]` | ⬜ |
| `value_at_stake` của `ESCALATE_PRICE_COMPLIANCE` | **4.212.000 đ** | snapshot `candidates[C2]` | ⬜ |
| `indicative_net_vnd` của `REALLOCATE` | **9.760.457 đ** | snapshot `candidates[C3]` | ⬜ |
| `breakeven_haircut` | **0,513** | snapshot `candidates[C3]` | ⬜ |

---

## 7 · ✅ Định nghĩa "xong" cho file này

- [ ] 📊 DS đã tick ✔ **toàn bộ** ô ở trên bằng script tự tính (không tin số chép tay)
- [ ] Script verify được commit ở `tests/fixtures/` để tái chạy
- [ ] Bộ sinh dữ liệu `--seed 7` cho ra **đúng** các số này
- [ ] Vai trò A đã chuyển bảng 1.4, 1.5, 1.6 thành `tests/test_evaluate_golden.py`
- [ ] 👔 Business xác nhận các con số này **nghe hợp lý với thực tế ngành**
