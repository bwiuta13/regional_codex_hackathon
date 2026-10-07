"""Giai đoạn ALERT — luật cảnh báo, điều kiện chặn, hành động ứng viên, niêm phong snapshot.

Entry point: alert()

Chạy luật trên chỉ số, CHẶN luật khi dữ liệu kém, sinh HÀNH ĐỘNG ỨNG VIÊN ĐÃ TÍNH SẴN SỐ TIỀN,
rồi niêm phong PromotionSnapshot bất biến.

🔴 Hành động ứng viên được sinh TẤT ĐỊNH, TRƯỚC KHI gọi LLM. Đây là rào chắn số 1:
   LLM chỉ được CHỌN trong danh sách này, không được tự tạo -> không thể đề xuất điều ngoài chính sách.

Vai trò A + D sở hữu file này.
Mọi ngưỡng ĐỌC TỪ config/thresholds.yaml và config/policy.yaml -- KHÔNG hard-code số nào ở đây.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path


def alert(as_of: date, metrics: list[dict], config_dir: Path, out_dir: Path) -> list[Path]:
    """Chạy luật, sinh ứng viên, ghi snapshot bất biến cho từng chương trình.

    Args:
        as_of: ngày chốt.
        metrics: đầu ra của evaluate().
        config_dir: thư mục chứa thresholds.yaml và policy.yaml.
        out_dir: thư mục snapshots/.

    Returns:
        Đường dẫn các file snapshot đã ghi: snapshots/<as_of>/<promo_id>.json
    """
    # === LUẬT CẢNH BÁO (spec §4.5, ngưỡng ở config/thresholds.yaml) ==========
    # ⚠️ ĐỌC ngưỡng từ YAML. Hard-code một con số ở đây là vi phạm luật review.
    #
    # ROI_BEHIND_PLAN      gap <= max_relative_gap (-0.20) trong consecutive_evaluations (2) lần
    #                      liên tiếp. Trung bình (SỚM) từ ngày 3; CAO (XÁC NHẬN) từ ngày 7 khi
    #                      cận trên khoảng dự phóng cũng dưới kế hoạch (nếu có tính band).
    #                      CHẶN khi độ phủ < 80%.
    # LOW_LIFT             lift <= 60% lift kế hoạch. CHẶN khi đã chạy < 3 ngày.
    # STOCKOUT_SUSPECTED   luật Poisson (§8 dưới) theo cửa hàng x SKU.
    #                      Mức Cao nếu >= 10% số cửa hàng trong phạm vi.
    #                      CHẶN khi cửa hàng không mở hoặc dữ liệu không về.
    # DISCOUNT_NOT_APPLIED trạng thái cửa hàng NOT_APPLIED trong >= 3 ngày.
    #                      CHẶN khi gộp chưa đủ >= 5 sản phẩm.
    # SPEND_OVERRUN        chi phí lũy kế > 115% kế hoạch lũy kế.
    # COVERAGE_GAP         số cửa hàng có dữ liệu < 80% phạm vi. Thông tin; CHẶN cảnh báo ROI.
    # BASELINE_INSUFFICIENT > 20% phạm vi dùng baseline dự phòng. Thông tin; HẠ ĐỘ TIN CẬY.
    # OVERLAP              cửa hàng x SKU nằm trong 2 chương trình đang chạy.
    #                      Thông tin; TẮT cảnh báo ROI cho phần chồng lấn.
    # OUTPERFORMING        gap >= +20%. Thông tin; ĐÁNH DẤU ỨNG VIÊN NHẬN phân bổ.
    #
    # TODO(A-metrics): triển khai 9 luật trên, mỗi luật kèm điều kiện chặn của nó.
    # TODO(A-metrics): ghi first_as_of cho mỗi cảnh báo (lần đầu kích hoạt) và confirmed_as_of.
    #   Cần cho câu chuyện demo "phát hiện từ ngày 4" -- đừng bỏ.
    #
    # 🎯 VIỆC CHẶN CẢNH BÁO RẤT QUAN TRỌNG, KHÔNG PHẢI TÙY CHỌN:
    #   Dữ liệu sớm, chắp vá dễ tạo báo động giả, và báo động giả làm mất lòng tin người dùng
    #   NHANH HƠN cả việc bỏ sót.
    #   - Cảnh báo THỰC THI (hết hàng, sai giá): phát NGAY khi bằng chứng rõ về thống kê,
    #     vì xử lý chúng tốn ít chi phí.
    #   - Cảnh báo dẫn tới CHUYỂN TIỀN: phải chờ ĐỦ MỘT CHU KỲ THỨ-TRONG-TUẦN (7 ngày)
    #     và chênh lệch vẫn kéo dài.

    # === §8 NGHI HẾT HÀNG CHỈ TỪ POS =========================================
    # TODO(A-metrics): λ_d = baseline_d * (1 + min(lift quan sát ở cửa hàng BÌNH THƯỜNG cùng cụm,
    #                                              lift kế hoạch))
    #   ⚠️ PHẢI nhân với (1 + lift), không dùng baseline trần. Hàng đang khuyến mãi lẽ ra bán
    #   NHANH HƠN, nên "không bán được gì" là bất thường hơn nhiều.
    #   Với λ=3.0 (bỏ lift): k=2 -> e^-6 = 2.5e-3 -> CHƯA gắn cờ.
    #   Với λ=6.0 (có lift): k=2 -> e^-12 = 6.1e-6 -> GẮN CỜ.  <- đúng theo demo
    # TODO(A-metrics): gắn cờ khi CẢ BA điều kiện:
    #   (1) k >= min_zero_days (2) ngày liên tiếp không bán được
    #   (2) VÀ cửa hàng VẪN CÓ doanh số các SKU KHÁC trong những ngày đó (đang mở, dữ liệu vẫn về)
    #   (3) VÀ P = exp(-Σ λ_d) < max_probability (0.001)
    #   ⚠️ Thiếu điều kiện (2) -> cửa hàng đóng cửa sẽ bị báo hết hàng -> báo động giả hàng loạt.
    # TODO(A-metrics): sản lượng mất ≈ Σ λ_d trên các ngày bị gắn cờ.
    # TODO(A-metrics): LOẠI các ngày bị gắn cờ khỏi baseline về sau (nếu không baseline sẽ tụt dần).
    # TODO(A-metrics): ❌ KHÔNG triển khai kiểm định "doanh số thấp bất thường nhưng khác 0".
    #   Bằng chứng công bố: các kiểm định đó phần lớn là báo động giả.
    #   -> Doanh số thấp coi là LOW_LIFT, KHÔNG phải hết hàng.

    # === HÀNH ĐỘNG ỨNG VIÊN (tất định, trước LLM) ============================
    # TODO(A-metrics): ESCALATE_STOCKOUT -> danh sách cửa hàng + value_at_stake_vnd
    #   = sản lượng mất * (unit_margin - rebate). Demo: 2106 sp * (24000-6000) = 37_908_000 đ
    # TODO(A-metrics): ESCALATE_PRICE_COMPLIANCE -> cửa hàng NOT_APPLIED + value_at_stake_vnd.
    #   Demo: 4_212_000 đ. Kèm số CỬA HÀNG-NGÀY không tuân thủ (63) để ĐỐI SOÁT SCAN REBATE.
    # TODO(A-metrics): PREPARE_VARIANCE_DOSSIER -> luôn là ứng viên khi có bất kỳ cảnh báo nào.
    # TODO(A-metrics): MONITOR -> ứng viên khi bằng chứng chưa đủ. ⚠️ MONITOR LÀ HÀNH ĐỘNG HỢP LỆ,
    #   không phải "không làm gì". Nó giữ agent khỏi phản ứng quá mức với dữ liệu sớm còn nhiễu.

    # === §9 LOGIC PHÂN BỔ LẠI (config/policy.yaml -> reallocation) ===========
    # TODO(A-metrics): điều kiện kích hoạt: đã chạy >= min_elapsed_days (7)
    #   VÀ ROI_BEHIND_PLAN đã được XÁC NHẬN (không phải cảnh báo sớm).
    # TODO(A-metrics): BÊN CHO: có lỗi thực thi HOẶC ROI dự phóng < 0.90 * kế hoạch;
    #   có dòng sổ cái UNCOMMITTED CHƯA QUÁ commit_deadline.
    #   ⚠️ Chỉ commitment == UNCOMMITTED. Dòng RETAILER_COMMITTED / INTERNAL_COMMITTED
    #   tuyệt đối không được đụng -- đó là tiền đã hứa với đối tác.
    # TODO(A-metrics): BÊN NHẬN: CÙNG fund_pool_id (same_fund_pool_only = true);
    #   ROI dự phóng > 1.10 * kế hoạch; KHÔNG có cờ thực thi; còn >= 7 ngày;
    #   dư địa = chi phí của đòn bẩy CÒN THIẾU (vd trưng bày phụ ở các cửa hàng chưa có).
    # TODO(A-metrics): amount = min(phần chưa cam kết của bên cho,
    #                               dư địa bên nhận,
    #                               max_share_of_recipient_lump_sum_budget (0.30)
    #                                 * ngân sách trọn gói kế hoạch của bên nhận)
    #   Demo: min(14tr, 14tr, 30% x 61tr = 18.3tr) = 14tr
    #
    # TODO(A-metrics): GIÁ TRỊ BIÊN -- ƯU TIÊN đo NGAY TRONG chương trình nhận:
    #     uplift = lift(cửa hàng CÓ đòn bẩy) - lift(cửa hàng KHÔNG có)     [sp/cửa hàng/ngày]
    #     value  = uplift * số cửa hàng-ngày được tài trợ * (unit_margin - rebate)
    #              * marginal_haircut - amount
    #   Demo: (30-20) * 20 cửa hàng * 7 ngày * (24000-4500) = 27.3tr
    #         * 0.70 = 19.11tr - 14tr = +5.11tr      -> confidence = "medium"
    # TODO(A-metrics): DỰ PHÒNG khi KHÔNG có nhóm so sánh:
    #     value = amount * ROI dự phóng * haircut - amount   -> confidence = "low"
    #   Demo (giữ tiền ở P-03): 14tr * 0.954 * 0.70 = 9.35tr - 14tr = -4.65tr
    # TODO(A-metrics): so sánh 3 phương án {giữ ở bên cho, hoãn, phân bổ lại}, chọn tốt nhất.
    #   Demo: phân bổ lại (+5.11tr) > hoãn (0) > giữ (-4.65tr)
    # TODO(A-metrics): ⚖️ CÔNG BỐ breakeven_haircut = amount / tổng trước haircut.
    #   Demo: 14 / 27.3 = 0.513. Con số này đi KÈM khuyến nghị để người duyệt tự phán đoán --
    #   không bắt họ tin mù vào haircut 0.70.
    #
    # 📉 VÌ SAO CẦN TOÀN BỘ LOGIC NÀY: ROI BIÊN < ROI BÌNH QUÂN. Đồng tiền bỏ thêm mua được
    #   ít hơn những đồng đã có (bão hòa, trưng bày đã trả tiền, tồn kho/kệ có hạn), cộng thêm
    #   "lời nguyền của người tối ưu". Dùng ROI bình quân 1.945x của P-05 sẽ thổi phồng kết quả.

    # === NIÊM PHONG SNAPSHOT =================================================
    # TODO(A-metrics): dựng PromotionSnapshot từ metrics + exceptions + funds + candidates.
    # TODO(A-metrics): metric_version = `git rev-parse HEAD` của code tính chỉ số.
    # TODO(A-metrics): content_hash = sha256 nội dung đã chuẩn hóa (bỏ chính trường content_hash).
    # TODO(A-metrics): ghi snapshots/<as_of>/<promo_id>.json
    # TODO(A-metrics): 🔒 CHỈ GHI THÊM. File đã tồn tại -> KHÔNG ghi đè.
    #   Nếu nội dung khác nhau thì đó là lỗi (cùng đầu vào phải cho cùng hash) -> báo lỗi rõ ràng.
    #   "Du hành thời gian" trong demo chỉ là nạp snapshot của ngày chốt cũ hơn.
    raise NotImplementedError("TODO(A-metrics): luật + ứng viên + niêm phong snapshot")
