"""Test giai đoạn ALERT — biên ngưỡng, điều kiện chặn, logic ngày liên tiếp.

🎯 Việc CHẶN cảnh báo quan trọng ngang với việc phát cảnh báo:
   báo động giả làm mất lòng tin NHANH HƠN việc bỏ sót.

Vai trò A sở hữu file này. Ngưỡng: config/thresholds.yaml.
"""

from __future__ import annotations

import pytest


@pytest.mark.skip(reason="TODO(A-metrics): bỏ skip khi alert() đã có")
def test_thresholds_are_read_from_config_not_hardcoded() -> None:
    """Đổi config/thresholds.yaml phải LÀM ĐỔI hành vi -> chứng minh không hard-code."""
    # TODO(A-metrics): chạy alert() với 2 bản config khác nhau, assert kết quả khác nhau.
    #   Test này bảo vệ quyền sở hữu của Trade Marketing với các ngưỡng.
    raise NotImplementedError


@pytest.mark.skip(reason="TODO(A-metrics)")
def test_roi_alert_blocked_when_coverage_below_threshold() -> None:
    """Độ phủ < 80% -> KHÔNG phát ROI_BEHIND_PLAN, dù chênh lệch rất lớn."""
    raise NotImplementedError


@pytest.mark.skip(reason="TODO(A-metrics)")
def test_roi_alert_early_vs_confirmed_severity() -> None:
    """Ngày 3-6 -> mức Trung bình (SỚM). Ngày >= 7 -> mức Cao (XÁC NHẬN).

    Chỉ mức XÁC NHẬN mới mở khóa REALLOCATE_UNCOMMITTED_FUNDS -- chuyển tiền phải chờ
    đủ một chu kỳ thứ-trong-tuần.
    """
    raise NotImplementedError


@pytest.mark.skip(reason="TODO(A-metrics)")
def test_roi_alert_requires_consecutive_evaluations() -> None:
    """1 lần vượt ngưỡng chưa đủ; cần consecutive_evaluations (2) lần liên tiếp."""
    raise NotImplementedError


@pytest.mark.skip(reason="TODO(A-metrics)")
def test_low_sales_is_low_lift_not_stockout() -> None:
    """Doanh số thấp NHƯNG KHÁC 0 -> LOW_LIFT, KHÔNG phải STOCKOUT_SUSPECTED.

    Bằng chứng công bố: các kiểm định "thấp bất thường nhưng khác 0" phần lớn là báo động giả.
    """
    raise NotImplementedError


@pytest.mark.skip(reason="TODO(A-metrics)")
def test_reallocation_never_exceeds_uncommitted_balance() -> None:
    """🔒 Số tiền chuyển KHÔNG BAO GIỜ vượt tổng dòng UNCOMMITTED chưa quá hạn.

    Vi phạm điều này = agent đề xuất chuyển tiền đã hứa với đối tác = mất uy tín sản phẩm.
    """
    raise NotImplementedError


@pytest.mark.skip(reason="TODO(A-metrics)")
def test_reallocation_blocked_across_fund_pools() -> None:
    """same_fund_pool_only = true -> không bao giờ chuyển ngang nhãn hàng / ngang kênh."""
    raise NotImplementedError


@pytest.mark.skip(reason="TODO(A-metrics)")
def test_snapshot_is_append_only_and_hash_is_stable() -> None:
    """Chạy lại cùng đầu vào + cùng code -> CÙNG content_hash; KHÔNG ghi đè file cũ."""
    raise NotImplementedError


@pytest.mark.skip(reason="TODO(A-metrics)")
def test_monitor_is_emitted_when_evidence_is_thin() -> None:
    """Dữ liệu sớm/thiếu -> ứng viên MONITOR. 'Chủ động không hành động' là kết quả HỢP LỆ."""
    raise NotImplementedError
