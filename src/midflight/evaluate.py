"""Giai đoạn EVALUATE — engine tính chỉ số (tất định).

Entry point: evaluate()

🔴 ĐÂY LÀ NƠI MỌI CON SỐ ĐƯỢC SINH RA. Không một con số nào trong sản phẩm đến từ LLM.

PHẢI khớp chính xác docs/roi-methodology.md §1-§7. Khi lệch nhau: TÀI LIỆU ĐÚNG, CODE SAI.
`make drift` dùng Codex kiểm tra điều này và CI báo lỗi nếu có lệch.

Vai trò A sở hữu file này.
Golden test: tests/test_evaluate_golden.py — giá trị kỳ vọng do CON NGƯỜI sở hữu,
KHÔNG BAO GIỜ sửa chúng để test pass.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path


def evaluate(as_of: date, db_path: Path) -> list[dict]:
    """Tính toàn bộ chỉ số cho mọi chương trình đang chạy, tính đến ngày chốt.

    Args:
        as_of: ngày chốt. Dữ liệu POS tính đến hết ngày này (pos_lag_days = 1).
        db_path: file DuckDB (đầu ra của ingest()).

    Returns:
        Một dict chỉ số cho mỗi chương trình -- đầu vào cho alert().
    """
    # ⚠️ Mọi phép gộp viết bằng DuckDB SQL, MỘT CTE CHO MỘT KHÁI NIỆM, đặt tên đúng như
    #    trong docs/roi-methodology.md. SQL review được; vòng lặp Python thì không.
    # ⚠️ TIỀN LÀ SỐ NGUYÊN VND trong mọi phép tính. Làm tròn ở bước cuối, không làm tròn giữa chừng.

    # === §1 BASELINE =========================================================
    # TODO(A-metrics): NGÀY SẠCH = SKU không khuyến mãi
    #   AND không nằm trong `post_promo_exclusion_days` (14) ngày sau một đợt khuyến mãi
    #   AND ngoài khung ngày lễ (Tết căn theo ÂM LỊCH)
    #   AND không phải ngày nghi hết hàng
    #   rồi CẮT `trim_share` (2.5%) số ngày cao nhất và thấp nhất.
    # TODO(A-metrics): w(k) = chỉ số thứ-trong-tuần, ước lượng ở cấp CỬA HÀNG x NGÀNH HÀNG
    #   (không phải cấp SKU -- cấp SKU quá nhiễu). Cần >= min_clean_weeks (8) tuần ngày sạch.
    # TODO(A-metrics): L[s,k] = trung bình của (units_d / w(dow_d)) trên 28-56 ngày sạch gần nhất.
    # TODO(A-metrics): baseline_d = L[s,k] * w(dow_d) * trend_d
    # TODO(A-metrics): trend_d = Σ thực tế đối chứng / Σ baseline đối chứng, KẸP trong [0.8, 1.2].
    #   Đối chứng = cùng chuỗi, NGOÀI phạm vi chương trình, >= min_control_stores (10).
    #   Không đủ -> trend = 1.0. Phần kẹp quan trọng: không để nhóm đối chứng kéo lệch baseline.
    # TODO(A-metrics): DỰ PHÒNG khi không có lịch sử dùng được -> tốc độ bán trung vị của SKU
    #   trong cụm (chuỗi x định dạng x vùng) * chỉ số quy mô cửa hàng.
    #   Gắn cờ BASELINE_FALLBACK, hoặc MISSING_BASELINE và LOẠI KHỎI tính toán.
    # TODO(A-metrics): ghi lại baseline_fallback_share -> vào DataQuality của snapshot.

    # === §2 SẢN LƯỢNG ========================================================
    # TODO(A-metrics): incremental_units = actual_units - baseline_units
    # TODO(A-metrics): lift = actual_units / baseline_units - 1

    # === §3 LỢI NHUẬN GỘP TĂNG THÊM ==========================================
    # TODO(A-metrics): unit_margin = net_price_to_retailer - unit_COGS   (lấy từ sku_master)
    # TODO(A-metrics): iGP = incremental_units * unit_margin
    #   Giả định đã ghi rõ: sản lượng bán ra tăng thêm chuyển 1:1 thành sản lượng giao hàng
    #   trong chu kỳ. LOẠI TRỪ việc nhà bán lẻ gom hàng trước (forward-buying).

    # === §4 CHI PHÍ TRADE GHI NHẬN LŨY KẾ ====================================
    # TODO(A-metrics): variable = discounted_units * regular_shelf_price * discount_pct
    #                             * mfr_funding_share
    #   ⚠️ CHỈ phần chiết khấu DO NHÀ SẢN XUẤT TÀI TRỢ. Phần nhà bán lẻ thuộc P&L của họ.
    # TODO(A-metrics): một cửa hàng-ngày chỉ tính là CÓ CHIẾT KHẤU khi chiết khấu thực tế
    #   >= 50% kế hoạch. Ngược lại -> gắn cờ không tuân thủ và KHÔNG PHÁT SINH scan rebate.
    #   (Nhà bán lẻ không giảm giá thì cũng không quét rebate.)
    # TODO(A-metrics): fixed = Σ khoản trọn gói (DISPLAY_FEE, feature, tờ rơi)
    #                          * TỶ LỆ SẢN LƯỢNG KẾ HOẠCH LŨY KẾ
    #   ⚠️ KHÔNG phải tỷ lệ thời gian đã qua -- chúng chỉ bằng nhau khi kế hoạch đều theo ngày.
    # TODO(A-metrics): ❌ LOẠI LISTING_FEE khỏi ROI chương trình -- nó mua ĐỘ PHỦ PHÂN PHỐI,
    #   không mua sự kiện. Theo dõi riêng. Đây là lỗi kinh điển của phân tích hậu kiểm.
    # TODO(A-metrics): discretionary = Σ các dòng MDF ghi nhận theo KỲ DỊCH VỤ
    #                                  (period_start..period_end), phân bổ đều.
    # TODO(A-metrics): trade_spend = variable + fixed + discretionary
    # TODO(A-metrics): tính SONG SONG "GÓC NHÌN CAM KẾT" ghi nhận TOÀN BỘ khoản trọn gói
    #   ngay từ ngày 1. Dự phóng cuối kỳ LUÔN dùng toàn bộ số tiền, không dùng phần đã phân bổ.

    # === §5 ROI ==============================================================
    # TODO(A-metrics): ROI = iGP / trade_spend  ;  net = iGP - trade_spend
    # TODO(A-metrics): ROI_gap = ROI_to_date / plan_ROI_to_date - 1
    # TODO(A-metrics): ⚠️ ĐƯỜNG KẾ HOẠCH LŨY KẾ DÙNG CÙNG CÔNG THỨC trên sản lượng kế hoạch
    #   theo ngày. Không được dùng công thức khác cho kế hoạch và thực tế -- nếu không
    #   ROI_gap sẽ vô nghĩa.
    # TODO(A-metrics): chia cho 0 -> trade_spend = 0 thì ROI là None, KHÔNG phải inf.
    #   Hạ độ tin cậy và không phát cảnh báo ROI.

    # === §6 CHIẾT KHẤU THỰC TẾ & TUÂN THỦ GIÁ ================================
    # TODO(A-metrics): realized_discount = 1 - Σ net_sales / Σ (units * regular_shelf_price)
    # TODO(A-metrics): trạng thái cửa hàng (gộp ngày cho tới khi >= min_pooled_units = 5 sp):
    #     NOT_APPLIED  thực tế < max(5%, 50% * kế hoạch)
    #     PARTIAL      thực tế < kế hoạch - 2 điểm %
    #     OK           trong ±2 điểm % quanh kế hoạch
    #     STACKED      thực tế > kế hoạch + 2 điểm %   <- có bên đang giảm thêm: AI tài trợ?
    # TODO(A-metrics): tính ở CẢ 3 CẤP: chuỗi, cửa hàng, ngày.
    #   ⚠️ CÚ TWIST CỦA DEMO: chiết khấu cấp chuỗi 19.06% trông bình thường so với kế hoạch 20%,
    #   nên mọi báo cáo tổng hợp BỎ SÓT vấn đề. Chỉ cấp CỬA HÀNG mới lộ ra.
    #   Nếu chỉ tính cấp chuỗi thì mất luôn tính năng.
    # TODO(A-metrics): giá kệ thường đối chiếu với GIÁ PHỔ BIẾN NHẤT (mode) trong các ngày sạch.
    # TODO(A-metrics): NGÀY BẮT ĐẦU THỰC TẾ của chương trình xác định từ GIÁ THỰC TẾ, không
    #   từ start_date. Nhà bán lẻ đôi khi bắt đầu sớm/muộn một tuần -> gắn cờ khi lệch.

    # === §7 DỰ PHÓNG CUỐI KỲ =================================================
    # TODO(A-metrics): lift_recent = min(lift lũy kế, lift của projection_window_days (3) ngày
    #   gần nhất), với lift ĐÃ HIỆU CHỈNH THỨ-TRONG-TUẦN.
    #   Lấy min bắt được CẢ hiện tượng khuyến mãi "hụt hơi" (lift đạt đỉnh tuần đầu)
    #   LẪN các cú gãy như một làn sóng hết hàng.
    # TODO(A-metrics): projected_units = lũy kế + Σ baseline_d(ngày còn lại) * (1 + lift_recent)
    # TODO(A-metrics): projected_spend = sản lượng có chiết khấu dự phóng * rebate
    #                                    + TOÀN BỘ khoản trọn gói + chi phí tùy nghi còn lại
    # TODO(A-metrics): ⚠️ GHI TÊN PHƯƠNG PHÁP vào kết quả: "trailing_3d_run_rate".
    #   Người đọc phải biết con số đến từ đâu.
    # TODO(A-metrics): band P10-P90 từ bootstrap_resamples (500) lần lấy mẫu THEO CỬA HÀNG.
    #   ⬇️ ĐÂY LÀ MỤC CẮT ĐẦU TIÊN nếu thiếu thời gian. Bỏ band thì ROI_BEHIND_PLAN "xác nhận"
    #   chỉ dựa vào chênh lệch kéo dài, vẫn chạy được.

    # === KIỂM TRA CUỐI ========================================================
    # TODO(A-metrics): golden test phải khớp TỚI TỪNG ĐỒNG tại ngày 3, 4, 5, 7.
    #   P-03 ngày 7: units 4041, baseline 2520, iGP 36_504_000, spend 49_112_000, ROI 0.7433,
    #                realized_discount 0.1906
    #   Xem Business/05-demo-scenario-numbers.md.
    raise NotImplementedError("TODO(A-metrics): triển khai theo docs/roi-methodology.md §1-§7")
