"""🔴 GOLDEN TEST — giá trị kỳ vọng do CON NGƯỜI sở hữu.

⚠️⚠️ KHÔNG BAO GIỜ SỬA CÁC CON SỐ TRONG FILE NÀY ĐỂ TEST PASS. ⚠️⚠️
Test đỏ nghĩa là ENGINE SAI, không phải test sai. Nếu thật sự cần đổi số kỳ vọng:
  1. hỏi người,
  2. sửa docs/roi-methodology.md,
  3. tăng SCHEMA_VERSION trong snapshot.py,
  tất cả trong CÙNG MỘT PR. (Luật 2 trong AGENTS.md)

Nguồn số liệu: Business/05-demo-scenario-numbers.md (= Phụ lục B của spec).
📊 Data Science phải verify từng con số BẰNG SCRIPT trước ngày thi.

Vai trò A sở hữu file này.
"""

from __future__ import annotations

import pytest

# ---------------------------------------------------------------------------
# Kinh tế đơn vị (Business/05 §0)
# ---------------------------------------------------------------------------
REGULAR_PRICE_VND = 60_000
NET_PRICE_TO_RETAILER_VND = 46_000
UNIT_COGS_VND = 22_000
UNIT_MARGIN_VND = 24_000  # = 46_000 - 22_000

# ---------------------------------------------------------------------------
# P-03 — Chuỗi M, 120 cửa hàng, 2026-10-01 -> 2026-10-21, giảm 20%, 50/50
# ---------------------------------------------------------------------------
P03_SCAN_REBATE_PER_UNIT_VND = 6_000  # 60_000 * 20% * 50%
P03_BASELINE_UNITS_PER_DAY = 360  # 120 cửa hàng * 3.0
P03_PLANNED_UNITS_PER_DAY = 792  # 360 * 2.2

# 🔴 Lũy kế đến NGÀY 7 — số chính của demo
P03_DAY7 = {
    "units": 4_041,
    "baseline_units": 2_520,
    "incremental_units": 1_521,
    "lift": 0.6036,
    "igp_vnd": 36_504_000,
    "variable_spend_vnd": 23_112_000,
    "fixed_spend_recognized_vnd": 12_000_000,  # 36tr * 7/21
    "discretionary_spend_recognized_vnd": 14_000_000,  # 2tr/ngày * 7
    "trade_spend_vnd": 49_112_000,
    "roi": 0.7433,
    "roi_gap": -0.393,
    "realized_discount_rate": 0.1906,  # ⚠️ trông bình thường -> cú twist của demo
    "stockout_stores": 27,
    "price_noncompliant_stores": 9,
}

# Kế hoạch lũy kế đến ngày 7
P03_DAY7_PLAN = {
    "units_to_date": 5_544,
    "roi": 1.2246,
    "igp_to_date_vnd": 72_576_000,
    "spend_to_date_vnd": 59_264_000,
}

# ROI ở các ngày chốt sớm hơn — engine phải khớp CẢ BỐN mốc
P03_ROI_BY_AS_OF = {
    "2026-10-03": (0.907, -0.260),  # (roi, roi_gap)
    "2026-10-04": (0.837, -0.316),
    "2026-10-05": (0.794, -0.352),
    "2026-10-07": (0.7433, -0.393),
}

# Dự phóng cuối kỳ
P03_PROJECTION_STATUS_QUO = {"method": "trailing_3d_run_rate", "roi": 0.6550, "net_vnd": -49_488_000}
P03_PROJECTION_IF_FIXED_FROM_DAY9 = {"roi": 0.954, "net_vnd": -7_370_000}
P03_FIX_UPLIFT_VND = 42_120_000  # = hết hàng 37_908_000 + tuân thủ giá 4_212_000

# Hành động ứng viên
P03_CANDIDATES = {
    "C1": {"type": "ESCALATE_STOCKOUT", "stores": 27, "value_at_stake_vnd": 37_908_000},
    "C2": {"type": "ESCALATE_PRICE_COMPLIANCE", "stores": 9, "value_at_stake_vnd": 4_212_000},
    "C3": {
        "type": "REALLOCATE_UNCOMMITTED_FUNDS",
        "from": "P-03",
        "to": "P-05",
        "amount_vnd": 14_000_000,
        "indicative_net_vnd": 9_760_457,
        "breakeven_haircut": 0.513,
        "marginal_method": "within_promo_split:secondary_display",
        "confidence": "medium",
    },
    "C4": {"type": "PREPARE_VARIANCE_DOSSIER"},
}

# ---------------------------------------------------------------------------
# P-05 — Chuỗi H, 40 cửa hàng, giảm 15%, 50/50 (bên NHẬN phân bổ)
# ---------------------------------------------------------------------------
P05_SCAN_REBATE_PER_UNIT_VND = 4_500  # 60_000 * 15% * 50%
P05_DAY7 = {"igp_vnd": 100_800_000, "trade_spend_vnd": 51_830_000, "roi": 1.945}
P05_DISPLAY_UPLIFT_UNITS_PER_STORE_DAY = 10  # 30 (có trưng bày) - 20 (không có)
P05_CONTRIBUTION_PER_STORE_DAY_VND = 195_000  # 10 * (24_000 - 4_500)

# ---------------------------------------------------------------------------
# Kiểm định hết hàng (Poisson)
# ---------------------------------------------------------------------------
STOCKOUT_LAMBDA_PER_DAY = 6.0  # 3.0 * (1 + min(100%, 120%))
STOCKOUT_P_TWO_ZERO_DAYS = 6.1e-6  # exp(-12) < 0.001 -> gắn cờ
STOCKOUT_P_WITHOUT_LIFT = 2.5e-3  # exp(-6)  > 0.001 -> KHÔNG gắn cờ (cần 3 ngày)

# Tác động danh mục
PORTFOLIO_UPLIFT_VS_STATUS_QUO_VND = 51_880_000  # 42.12 + 4.65 + 5.11


@pytest.mark.skip(reason="TODO(A-metrics): bỏ skip khi evaluate() đã có")
def test_p03_metrics_at_day_7() -> None:
    """P-03 tại ngày chốt 2026-10-07 phải khớp P03_DAY7 tới từng đồng."""
    # TODO(A-metrics): gọi evaluate(date(2026,10,7), db_path) qua ĐIỂM VÀO của giai đoạn.
    #   Không gọi hàm phụ trợ nội bộ (luật 5 AGENTS.md).
    # TODO(A-metrics): so sánh CHÍNH XÁC các trường VND (int). Tỷ lệ so sánh với dung sai 1e-4.
    raise NotImplementedError


@pytest.mark.skip(reason="TODO(A-metrics): bỏ skip khi evaluate() đã có")
def test_p03_roi_at_each_as_of() -> None:
    """ROI tại ngày 3, 4, 5, 7 phải khớp P03_ROI_BY_AS_OF."""
    # TODO(A-metrics): lặp qua P03_ROI_BY_AS_OF, chạy evaluate cho từng as_of.
    # TODO(A-metrics): test này bảo vệ câu chuyện demo "phát hiện từ ngày 4" -- nếu nó đỏ,
    #   dòng thời gian cảnh báo sẽ sai và cả kịch bản demo sụp.
    raise NotImplementedError


@pytest.mark.skip(reason="TODO(A-metrics): bỏ skip khi evaluate() đã có")
def test_p03_projection_status_quo() -> None:
    """Dự phóng giữ nguyên hiện trạng: ROI 0.655x, lỗ ròng 49,49 tr."""
    raise NotImplementedError


@pytest.mark.skip(reason="TODO(A-metrics): bỏ skip khi alert() đã có")
def test_p03_candidate_values() -> None:
    """Giá trị ứng viên C1-C4 phải khớp P03_CANDIDATES."""
    # TODO(A-metrics): đặc biệt kiểm breakeven_haircut = 0.513 -- con số này được CÔNG BỐ
    #   cho người duyệt, sai là mất uy tín.
    raise NotImplementedError


@pytest.mark.skip(reason="TODO(A-metrics): bỏ skip khi evaluate() đã có")
def test_p05_within_promo_display_split() -> None:
    """P-05: cửa hàng có trưng bày phụ bán hơn 10 sp/ngày -> cơ sở đo giá trị BIÊN."""
    # TODO(A-metrics): không có test này thì toàn bộ lập luận ROI biên không được bảo vệ.
    raise NotImplementedError


@pytest.mark.skip(reason="TODO(A-metrics): bỏ skip khi alert() đã có")
def test_stockout_poisson_requires_lift_adjustment() -> None:
    """λ phải nhân (1 + lift): với λ=6.0 gắn cờ sau 2 ngày; với λ=3.0 thì KHÔNG."""
    # TODO(A-metrics): test này chặn một lỗi tinh vi -- dùng baseline trần làm λ sẽ khiến
    #   27 cửa hàng chỉ bị phát hiện ở ngày 5 thay vì ngày 4, và demo mất 1 ngày lợi thế.
    raise NotImplementedError
