# 06 · ❓ CÂU HỎI MỞ — cần người quyết trước ngày thi

> 🔴 **CHẶN** = không giải quyết thì ngày thi sẽ mất thời gian tranh luận hoặc làm sai.
> 🟡 **Nên có** = ảnh hưởng chất lượng pitch. 🟢 **Tốt nếu có** = cải thiện nhỏ.
>
> Cách dùng: điền cột **Trả lời**, đổi trạng thái → `✅ <ngày> <tên người quyết>`.

---

## A · Câu hỏi về cuộc thi

| # | Mức | Câu hỏi | Vì sao quan trọng | Hỏi ai | Trả lời |
|---|---|---|---|---|---|
| **Q1** | 🔴 | File **`AGENTS.md` soạn sẵn** có bị coi là "pre-built code" không? Còn repo scaffold (file `.py` rỗng chỉ có TODO) thì sao? | Luật: *"All building must take place on the day"*. Nếu bị coi là vi phạm → **mất tư cách** | **Ban tổ chức** | ⬜ CHƯA HỎI<br>🛡️ *Cách an toàn hiện tại: gõ lại `AGENTS.md` trong 30 phút đầu; file `.py` để rỗng hoàn toàn, Codex sinh trong ngày* |
| Q7 | 🟡 | Model Codex nào còn khả dụng vào 31/10? (GPT-5.5 **ngừng trên Codex từ 14/10/2026**) | Kế hoạch dùng Sol cho engine, Luna cho khung. Hết hạn mức giữa chiều là rủi ro thật | Trang model OpenAI, **kiểm lại T−1 tuần** | ⬜ |
| Q8 | 🟡 | Nhóm có **3 hay 4** người? | Nếu 3, việc của vai trò D chia cho A và C (§6.5 spec) | Nội bộ nhóm | ⬜ |
| Q9 | 🟢 | Có được cấp **GPT-6 Astra** không? | Dành cho các lỗi khó nhất | Ban tổ chức | ⬜ |

---

## B · Câu hỏi nghiệp vụ & pháp lý

| # | Mức | Câu hỏi | Vì sao quan trọng | Hỏi ai | Trả lời |
|---|---|---|---|---|---|
| **Q2** | 🔴 | Pitch được dùng **số liệu kinh tế khuyến mãi thật đã ẩn danh** (lift, biên lợi nhuận) không, hay giữ hoàn toàn dữ liệu tổng hợp/hư cấu? | Số thật làm câu chuyện thuyết phục hơn nhiều, nhưng **giá vốn là dữ liệu mật** | 👔 Business + Pháp chế | ⬜ |
| **Q3** | 🔴 | **Pháp chế đã duyệt danh sách hành động bị cấm chưa?** | Toàn bộ định vị sản phẩm dựa vào việc nói đúng luật khuyến mại VN. Nói sai trước giám khảo = mất uy tín | Pháp chế | ⬜ |
| **Q5** | 🔴 | Việc **TĂNG mức giảm giữa chừng** có bị coi là "thay đổi chương trình đã thông báo" (bị cấm) không? | Spec ghi rõ **chưa có quy định rõ** → agent **không đề xuất**, nhưng giám khảo có thể hỏi | Pháp chế | ⬜<br>*Lập trường hiện tại: không đề xuất, và nói rõ là vùng xám* |
| Q10 | 🟡 | Công ty có đang **phân loại trạng thái cam kết** trên sổ cái chi phí trade không? | Nếu **chưa** → đây chính là insight để pitch: "chúng tôi thêm một cột và biến dashboard thành quyết định" | 👔 Business / Tài chính | ⬜ |
| Q11 | 🟡 | Công ty có ghi nhận **cửa hàng nào có trưng bày phụ / có PG** không? Nằm ở hệ thống nào? | Không có → mất nhóm so sánh → mất lập luận ROI biên (xuống độ tin cậy "thấp") | 👔 Business / KAM | ⬜ |
| Q12 | 🟡 | `commit_deadline` thực tế sớm hơn ngày dịch vụ bao lâu? | Quyết định cảnh báo phải phát ra **sớm cỡ nào** mới còn kịp hành động | 👔 Business | ⬜ |

---

## C · Câu hỏi về dữ liệu

| # | Mức | Câu hỏi | Vì sao quan trọng | Hỏi ai | Trả lời |
|---|---|---|---|---|---|
| **Q4** | 🟡 | Nhóm có biết **chuỗi thật nào đang chia sẻ POS theo ngày**, và ở mức chi tiết nào (mã hàng × cửa hàng)? | Ảnh hưởng cách kể câu chuyện **"vì sao là bây giờ"** với giám khảo | 👔 Business / KAM | ⬜<br>*Spec: chưa tìm thấy bằng chứng công khai tại WinCommerce, BHX, Co.op, Central Retail* |
| Q13 | 🟡 | Chuỗi có gửi **cả `net_sales` và `regular_price`** không? | Không có cả hai → **mất tính năng phát hiện không tuân thủ giá** (một trong 4 hành động chính) | KAM | ⬜ |
| Q14 | 🟡 | Dữ liệu về theo **ngày** hay **tuần**? Độ trễ bao lâu? | Theo tuần → phải hạ cấp mềm, mất độ nhạy. Spec giả định D+1 lúc 06:00 | KAM | ⬜ |
| Q15 | 🔴 | Có **điều khoản bảo mật** nào cấm đưa dữ liệu (kể cả tổng hợp) qua LLM bên thứ ba không? | Lời gọi LLM chỉ chứa số liệu tổng hợp trong snapshot, nhưng vẫn ra khỏi mạng công ty | Pháp chế / An ninh thông tin | ⬜ |
| Q16 | 🟢 | Danh sách **ngày lễ loại trừ theo âm lịch** 2026–2027 lấy ở đâu? | Baseline cần loại ngày lễ; Tết căn theo âm lịch | 📊 DS | ⬜ |

---

## D · Câu hỏi về sản phẩm & pitch

| # | Mức | Câu hỏi | Vì sao quan trọng | Hỏi ai | Trả lời |
|---|---|---|---|---|---|
| **Q6** | 🟡 | Dùng thương hiệu **GreenNode/VNG** trên tài liệu pitch, hay thương hiệu trung lập của nhóm? | Ảnh hưởng slide, màu sắc, cách giới thiệu nhóm | Nội bộ nhóm + quản lý | ⬜ |
| Q17 | 🟡 | Tên sản phẩm cuối cùng — giữ **"MidFlight"** hay đổi? | "MidFlight" chỉ là tên tạm (§8 spec) | Nội bộ nhóm | ⬜ |
| Q18 | 🟡 | Ngôn ngữ UI khi demo: **tiếng Việt, tiếng Anh, hay cả hai**? | Giám khảo có thể là người nước ngoài. Agent hỗ trợ cả hai (`language: Literal["en","vi"]`) nhưng demo nên chọn một | Nội bộ nhóm | ⬜ |
| Q19 | 🟢 | Tên 3 chuỗi hư cấu: giữ "Chuỗi H / M / C" hay đặt tên dễ nhớ hơn? | Ảnh hưởng độ mượt khi kể chuyện | 👔 Business | ⬜ |

---

## E · Giả định đang áp dụng (xác nhận hoặc chỉnh)

Những điều này spec đã **giả định sẵn**. Nếu không ai phản đối trước T−1 tuần, coi như đã chốt.

| # | Giả định | Trạng thái |
|---|---|---|
| E1 | Bối cảnh demo là **kênh hiện đại tại Việt Nam**, câu chuyện mở rộng được ra Đông Nam Á | ⬜ Xác nhận |
| E2 | LLM dùng **OpenAI** (vì là hackathon Codex), với Structured Outputs | ⬜ Xác nhận |
| E3 | Stack **Python + DuckDB + Streamlit**. Chỉ đổi sang FastAPI + Next.js nếu nhóm có người chuyên front-end | ⬜ Xác nhận |
| E4 | Nhóm 3–4 người, **7 giờ** build | ⬜ Xác nhận |
| E5 | Phân bổ lại **chỉ trong cùng nguồn quỹ** (nhãn × kênh × quý). Chuyển giữa các nguồn quỹ **ngoài phạm vi** | ⬜ Xác nhận |
| E6 | **"MidFlight" chỉ là tên tạm** | ⬜ Xác nhận |
| E7 | MVP chỉ hỗ trợ cơ chế `PCT_OFF` (mua X tặng Y, combo... làm sau) | ⬜ Xác nhận |
| E8 | Mọi hành động **cần con người duyệt** — không tự động thực thi | ⬜ Xác nhận |

---

## F · Những nhận định KHÔNG kiểm chứng được (đừng nói chắc khi pitch)

Spec đã ghi rõ các điểm này. Giữ nguyên sự trung thực đó khi trả lời giám khảo.

| Nhận định hay bị trích | Cách MidFlight xử lý |
|---|---|
| "72% chương trình tại Mỹ lỗ" (thường gán cho McKinsey) | ❌ Không dùng. Thay bằng **số gốc Nielsen: Mỹ 71%, 2015** [H] |
| Tần suất & độ trễ chỉ số bán lẻ NielsenIQ **tại Việt Nam** | Dùng mô hình chung "kỳ 4 tuần + 2–3 tuần" và **ghi rõ là mô hình chung** |
| Cổng dữ liệu POS cho nhà cung cấp tại WinCommerce / BHX / Co.op / Central Retail | **Chưa tìm thấy bằng chứng công khai** — nói thẳng |
| Thời điểm chốt giá chuẩn cho tờ rơi kênh hiện đại VN | Chưa tìm thấy |
| Tỷ lệ hòa vốn khuyến mãi **tại Việt Nam / Đông Nam Á** | **Chưa có benchmark công bố.** Số phương Tây chỉ mang tính định hướng — **không khẳng định một tỷ lệ cho VN** |

> 🎤 **Mẹo pitch:** chủ động nói ra giới hạn trước khi bị hỏi. Với tiêu chí chấm *"chiều sâu tư duy"*,
> một nhóm biết rõ mình **không** biết gì sẽ ghi điểm cao hơn một nhóm nói chắc mọi thứ.
