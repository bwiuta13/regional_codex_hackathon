# 01 · Bối cảnh nghiệp vụ (bản tóm tắt 10 phút)

> Dành cho cả nhóm. Đọc file này thay vì đọc hết 1441 dòng spec.
> Nguồn gốc: `docs/superpowers/specs/2026-09-27-midflight-trade-promo-agent-design.vi.md` §2, §3.

---

## 1. Bài toán, bằng chứng

| Sự thật | Con số | Nguồn |
|---|---|---|
| Chi phí trade trên doanh thu gộp của FMCG | **20–30%** (dòng chi lớn thứ 2 sau giá vốn) | Deloitte 2025 [H] |
| Chương trình khuyến mãi **không hòa vốn** | **59%** (7 thị trường phương Tây); Mỹ **71%** | Nielsen 2015 [H] |
| Biết kết quả sau khi chương trình kết thúc | **30–45 ngày** | §2.2 spec |
| Doanh nghiệp giám sát tự động **khi đang chạy** | **chỉ ~10%** | POI 2023 [H] |
| Doanh nghiệp FMCG **chưa áp dụng GenAI** | **62%** | POI 2026 [H] |

**Vì sao khuyến mãi lỗ?** Lãi ròng của nhà sản xuất:

```
net = I × (m − d)  −  B × d  −  F
      ────────────    ───────    ───
      lời từ phần     TIỀN       phí
      bán thêm        CHIẾT KHẤU cố định
                      TRẢ CHO HÀNG
                      VỐN DĨ VẪN BÁN ĐƯỢC   ← thường chính nó làm lỗ
```
`I` = sản lượng tăng thêm · `B` = sản lượng baseline · `m` = biên lợi nhuận đơn vị ·
`d` = phần chiết khấu nhà sản xuất tài trợ/sản phẩm · `F` = phí cố định.

Phần "tăng" còn nhỏ hơn vẻ ngoài: trung bình chia gần đều **1/3 chuyển đổi thương hiệu,
1/3 mua trước, 1/3 mở rộng ngành hàng** (van Heerde & cs. 2004 [H]). Kantar ước **~40% lift là "ảo"** [M].

---

## 2. 🔑 Nhận định cốt lõi — toàn bộ sản phẩm xoay quanh câu này

Giữa chừng một chương trình, **chỉ còn 2 thứ công ty kiểm soát được**:

| | Có sửa được giữa chừng? | Vì sao |
|---|---|---|
| Chiết khấu trợ giá cho doanh số nền, mua trước, ăn mòn doanh số | ❌ **KHÔNG** | Giá & điều khoản đã cam kết → bài học cho kỳ đàm phán sau |
| **Hết hàng** | ✅ **CÓ** | Bổ sung hàng, sửa đơn đặt hàng |
| **Giá khuyến mãi không được áp tại kệ/POS** | ✅ **CÓ** | Buộc thực thi đúng điều khoản ĐÃ thỏa thuận |
| **Tiền tùy nghi chưa cam kết** | ✅ **CÓ** | Chưa hứa với ai → chuyển đi hoặc hoãn |

→ **Phần khắc phục được = thực thi + tiền chưa cam kết.**
Danh sách hành động của MidFlight được thiết kế đúng quanh phần đó, không hơn.

Bằng chứng cho phần "có sửa được":
- Hàng **đang khuyến mãi hết hàng nhiều gần gấp đôi** hàng thường; **70–75% ca hết hàng do vận hành
  tại cửa hàng** (đặt hàng, châm hàng) — Gruen & cs. 2002 [H].
- **65% bản ghi tồn kho tại cửa hàng không chính xác** → không thể tin tồn kho hệ thống,
  phải suy ra hết hàng từ POS — DeHoratius & Raman 2008 [H].
- Nhà sản xuất thường **không nhận được mức chuyển giao chiết khấu đầy đủ** tới người mua — Nijs & cs. 2010 [H].

---

## 3. ⚖️ Ràng buộc pháp lý Việt Nam — lý do agent bị khóa tay

> 👔 **Business phải thuộc phần này.** Giám khảo gần như chắc chắn sẽ hỏi
> *"sao agent không đề xuất giảm giá sâu hơn / dừng chương trình?"*

| Văn bản | Nội dung | Hệ quả cho MidFlight |
|---|---|---|
| **Luật Thương mại 2005, Điều 96** | Thương nhân phải **thực hiện đúng chương trình khuyến mại đã thông báo** và cam kết với khách hàng | Không đổi mức giảm giữa chừng |
| **NĐ 81/2018, Điều 22** | **Không được chấm dứt chương trình trước thời hạn**, trừ 3 trường hợp: (1) bất khả kháng, (2) **hàng khuyến mại đã hết**, (3) cơ quan nhà nước yêu cầu | Không rút ngắn / hủy chương trình |
| **NĐ 128/2024** (từ 01/12/2024) | Khuyến mại giảm giá **không còn phải thông báo** Sở Công Thương | Ràng buộc **không** nằm ở thủ tục — nằm ở nghĩa vụ thực hiện đúng công bố + hợp đồng nhà bán lẻ |
| **TT 39/2025/TT-BCT** | Mức giảm tối đa 50% (100% trong chương trình khuyến mại tập trung, kể cả Tết) | Trần mức giảm |
| **NĐ 239/2026** (26/06/2026) | **Bỏ giới hạn 120 ngày/năm** cho khuyến mại giảm giá một sản phẩm | Lịch khuyến mãi dày hơn → càng nhiều chương trình đồng thời cần theo dõi |

⚠️ **Điểm xoắn đáng chú ý:** hết hàng quan trọng gấp đôi. "Hàng khuyến mại đã hết" là một trong số ít
căn cứ pháp lý để **kết thúc chương trình sớm**. Một làn sóng hết hàng có thể cắt ngắn chính chương trình
mà nhà sản xuất đã trả tiền.

---

## 4. Danh sách hành động — bản chốt (`config/policy.yaml`)

### ✅ ĐƯỢC PHÉP (danh sách đóng — agent không được tự tạo hành động mới)

| Hành động | Nghĩa là gì | Vì sao an toàn |
|---|---|---|
| `REALLOCATE_UNCOMMITTED_FUNDS` | Chuyển tiền tùy nghi **chưa cam kết** (MDF, trưng bày, PG/sampling) từ chương trình kém sang chương trình tốt hơn, **trong cùng một nguồn quỹ** | Tiền nội bộ, chưa hứa với ai. Cần quản lý duyệt |
| `ESCALATE_STOCKOUT` | Gửi danh sách cửa hàng hết hàng + giá trị bị đe dọa cho KAM & chuỗi cung ứng | Sửa lỗi thực thi, không đổi điều khoản |
| `ESCALATE_PRICE_COMPLIANCE` | Chỉ ra cửa hàng mà giá khuyến mãi không đến tay người mua | Thực thi đúng điều khoản ĐÃ thỏa thuận |
| `DEFER_DISCRETIONARY_SPEND` | Hoãn khoản chi tùy nghi chưa cam kết khi không có nơi dùng tốt hơn | Ngừng "ném tiền theo tiền" |
| `PREPARE_VARIANCE_DOSSIER` | Soạn hồ sơ bằng chứng cho kỳ review / gia hạn / đàm phán sau | Dùng dữ liệu đúng thời điểm |
| `MONITOR` | **Chủ động không hành động** khi chưa đủ bằng chứng | Tránh phản ứng quá mức với dữ liệu sớm còn nhiễu |

### ❌ BỊ CẤM khi chương trình đang chạy

| Bị cấm | Lý do |
|---|---|
| Đổi giá kệ hoặc mức chiết khấu | Đã in trên tờ rơi, niêm yết tại kệ. Luật: phải thực hiện đúng chương trình đã thông báo |
| Đổi tỷ lệ scan rebate / tỷ lệ đồng tài trợ | Đã ký với nhà bán lẻ |
| Rút ngắn, hủy, dời ngày chương trình | Đã cam kết với nhà bán lẻ và người mua; NĐ 81/2018 Điều 22 |
| Đàm phán lại điều khoản giữa chừng | Thuộc kỳ đàm phán sau — đó là lúc hồ sơ chênh lệch phát huy tác dụng |

> 💡 Trên UI có hẳn một ô **"Những gì chúng tôi sẽ KHÔNG thay đổi"**. Đó không phải trang trí —
> đó là điểm bán hàng. Nó cho người dùng (và giám khảo) thấy agent biết giới hạn của nó.

---

## 5. Người dùng — ai mở MidFlight mỗi sáng

| Chân dung | Công việc | Nỗi đau hiện nay | MidFlight cho họ |
|---|---|---|---|
| **Trưởng bộ phận trade marketing** (nhãn × kênh) | Phân bổ ngân sách trade giữa các chương trình | Biết kết quả 30–45 ngày sau khi tiền đã tiêu | ROI danh mục hằng ngày vs kế hoạch; đề xuất phân bổ lại trong cùng nguồn quỹ |
| **KAM** (một chuỗi) | Bảo đảm chương trình được thực thi tại chuỗi | Biết hết hàng, sai giá muộn, qua báo cáo thị trường | Danh sách cửa hàng + giá trị bị đe dọa, **ngay trong tuần** |
| **Chuyên viên RGM / Tài chính** | Phân tích hậu kiểm, trích trước chi phí | Đối soát thủ công POS × xuất hàng × chi phí | Snapshot hằng ngày bất biến; hồ sơ chênh lệch tự động |
| **Giám đốc kinh doanh** | Đàm phán năm & quý | Thiếu bằng chứng khi gia hạn | Bộ bằng chứng: cửa hàng-ngày hết hàng, không tuân thủ giá, thực thi trưng bày |

---

## 6. Bối cảnh kênh hiện đại Việt Nam (dùng cho pitch)

- Toàn quốc: kênh truyền thống ~**85%** giá trị FMCG, kênh hiện đại ~**15%** (NielsenIQ 2026) [M].
  Thành thị: kênh hiện đại đã **35–40%** doanh số bán lẻ (Kantar qua ACBS 2026) [M].
- Quy mô chuỗi: WinCommerce **5.141** điểm · Bách Hóa Xanh **3.612** · Saigon Co.op **>800** ·
  Central Retail **>300** · AEON **182 CVS + 40 siêu thị + 16 GMS**.
- **Điều khoản thương mại:** tổng gói chi phí vào kênh hiện đại tới **38–40% giá trị hợp đồng**;
  chiết khấu **25–40%**; đợt giảm giá **15–30% trong 10–30 ngày, 1–3 lần/năm** mỗi chuỗi [M].
- ⏰ **Vì sao bây giờ:** từ **01/06/2025**, NĐ 70/2025 bắt buộc hóa đơn điện tử khởi tạo từ máy tính tiền
  cho hộ/doanh nghiệp bán lẻ doanh thu ≥ 1 tỷ đ/năm → **dữ liệu POS số hóa theo từng mặt hàng
  giờ đã có trên diện rộng** [H].

⚠️ **Trung thực khi pitch:** chưa có bằng chứng công khai về cổng dữ liệu POS cho nhà cung cấp tại
WinCommerce, Bách Hóa Xanh, Co.op hay Central Retail. Vì vậy MidFlight thiết kế để làm việc với
**bất kỳ nguồn nào chuỗi cung cấp** (file xuất từ cổng, EDI, file KAM gửi) và **hạ cấp mềm** khi thiếu dữ liệu.
Đừng nói quá chỗ này — giám khảo có thể biết rõ.

---

## 7. 6 nguyên tắc thiết kế rút ra từ nghiên cứu

| # | Nguyên tắc | Thể hiện ở đâu trong code |
|---|---|---|
| 1 | Khoản lỗ nằm ở doanh số được trợ giá **và** lỗi thực thi → đo cả hai, **tách riêng** | `evaluate.py` |
| 2 | Giữa chừng chỉ thực thi + tiền chưa cam kết còn kiểm soát được | `policy.yaml`, trường `commitment` trong sổ cái |
| 3 | Dữ liệu sớm còn nhiễu, **báo động giả giết chết lòng tin** → điều kiện chặn, luật ngày liên tiếp, `MONITOR` là hành động hợp lệ | `alert.py`, `thresholds.yaml` |
| 4 | **ROI bình quân phóng đại** hiệu quả của đồng tiền bỏ thêm → đo lợi ích **biên** của đúng đòn bẩy sẽ mua | `alert.py` logic phân bổ lại |
| 5 | **LLM không được tính KPI** → engine tất định + placeholder + validator | `recommend.py` |
| 6 | Dữ liệu ở Việt Nam về không đồng đều → chỉ số độ phủ, adapter riêng, hạ cấp mềm | `ingest.py`, `COVERAGE_GAP` |
