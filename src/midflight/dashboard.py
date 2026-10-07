"""Dashboard Streamlit.

Entry point: main()  (chạy qua `streamlit run src/midflight/dashboard.py`)

🔴 LUẬT SỐ 1: DASHBOARD CHỈ ĐỌC SNAPSHOT VÀ KHUYẾN NGHỊ. KHÔNG BAO GIỜ TỰ TÍNH LẠI CHỈ SỐ.
   Đó là cách đảm bảo những gì người dùng THẤY và những gì agent NÓI không thể lệch nhau.
   Thấy mình sắp viết một phép tính ở đây -> nó thuộc về evaluate.py.

Vai trò C sở hữu file này. Spec §4.8.
"""

from __future__ import annotations


def main() -> None:
    """Chạy ứng dụng Streamlit."""
    # === MÀN 1: DANH MỤC =====================================================
    # TODO(C-ui): ô KPI: số chương trình đang chạy · chi phí lũy kế · ROI danh mục vs kế hoạch
    #             · số cảnh báo mở · QUỸ CHƯA CAM KẾT (con số này là điểm nhấn: "tiền còn cứu được")
    # TODO(C-ui): bảng chương trình: nhãn trạng thái, ROI lũy kế vs kế hoạch, ROI dự phóng, sparkline
    # TODO(C-ui): ⏱️ THANH TRƯỢT NGÀY CHỐT để phát lại -- chỉ đơn giản là NẠP SNAPSHOT CŨ HƠN
    #             từ snapshots/<as_of>/. Không tính lại gì cả.
    #             (Đây là MỤC CẮT THỨ BA nếu thiếu thời gian.)

    # === MÀN 2: CHI TIẾT CHƯƠNG TRÌNH ========================================
    # TODO(C-ui): đường lũy kế KẾ HOẠCH vs THỰC TẾ (sản lượng, iGP, chi phí, ROI) kèm dự phóng.
    #             Chúng phải TÁCH NHAU RÕ TỪ NGÀY 3 -- đó là khoảnh khắc của demo.
    # TODO(C-ui): 🔥 LƯỚI CỬA HÀNG tô màu theo vấn đề (hết hàng / sai giá / bình thường).
    #             ⚠️ ĐÂY LÀ MÀN HÌNH QUAN TRỌNG NHẤT CỦA CẢ DEMO: chiết khấu cấp chuỗi 19,1%
    #             trông bình thường, nhưng lưới cửa hàng cho thấy 27 cửa hàng đỏ và 9 cửa hàng vàng.
    #             Nó chứng minh vì sao báo cáo tổng hợp bỏ sót vấn đề.
    # TODO(C-ui): biểu đồ THÁC NƯỚC SỔ CÁI: đã cam kết · đã đặt lịch · CHƯA CAM KẾT · đã trả.
    #             Phần "chưa cam kết" chính là thứ agent được phép đụng tới.

    # === MÀN 3: CẢNH BÁO & KHUYẾN NGHỊ =======================================
    # TODO(C-ui): hàng đợi cảnh báo sắp theo MỨC ĐỘ.
    # TODO(C-ui): thẻ khuyến nghị: hành động theo thứ tự ưu tiên + CHIP BẰNG CHỨNG liên kết
    #             tới chỉ số tương ứng (bấm vào số -> nhảy tới nguồn của nó).
    # TODO(C-ui): 🛡️ Ô "NHỮNG GÌ CHÚNG TÔI SẼ KHÔNG THAY ĐỔI" -- hiển thị
    #             recommendation.not_changing. ĐÂY KHÔNG PHẢI TRANG TRÍ, ĐÓ LÀ ĐIỂM BÁN HÀNG.
    #             Nó cho người dùng và giám khảo thấy agent biết giới hạn của nó.
    # TODO(C-ui): nút DUYỆT / TỪ CHỐI / HOÃN với LÝ DO BẮT BUỘC -> ghi nhật ký kiểm toán.
    #             Không có lý do -> không cho submit. Nhật ký này vào hồ sơ chênh lệch.
    # TODO(C-ui): hiện nhãn "template" khi recommendation dùng mẫu câu dự phòng (trung thực
    #             với người dùng về việc LLM có chạy hay không).

    # === MÀN 4: HỒ SƠ ========================================================
    # TODO(C-ui): xem trước và xuất hồ sơ chênh lệch (Markdown, PDF nếu còn thời gian).

    # === CHUNG ===============================================================
    # TODO(C-ui): ⚠️ MỌI CON SỐ TRÊN MÀN HÌNH PHẢI TRUY ĐƯỢC VỀ MỘT TRƯỜNG TRONG SNAPSHOT.
    #             Đó là tiêu chí thành công của demo (spec §4.12).
    # TODO(C-ui): hiện chỉ số ĐỘ PHỦ và cảnh báo BASELINE_INSUFFICIENT rõ ràng -- người dùng
    #             phải biết khi nào con số kém tin cậy.
    # TODO(C-ui): smoke test bằng streamlit.testing AppTest -> tests/.
    raise NotImplementedError("TODO(C-ui): dựng 4 màn hình theo spec §4.8")


if __name__ == "__main__":
    main()
