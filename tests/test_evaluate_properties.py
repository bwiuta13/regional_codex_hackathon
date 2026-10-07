"""Test THUỘC TÍNH (Hypothesis) — các bất biến phải đúng với MỌI đầu vào.

Khác golden test (kiểm một kịch bản cụ thể tới từng đồng), test thuộc tính kiểm
những điều phải đúng BẤT KỂ dữ liệu nào. Chúng bắt được lớp lỗi mà ví dụ cụ thể bỏ sót.

Vai trò A sở hữu file này. Spec §4.10.
"""

from __future__ import annotations

import pytest


@pytest.mark.skip(reason="TODO(A-metrics): bỏ skip khi evaluate() đã có")
def test_incremental_always_equals_actual_minus_baseline() -> None:
    """Bất biến: incremental_units == actual_units - baseline_units, với mọi đầu vào."""
    # TODO(A-metrics): dùng hypothesis.given() sinh units/baseline ngẫu nhiên, kể cả ÂM và 0.
    raise NotImplementedError


@pytest.mark.skip(reason="TODO(A-metrics)")
def test_roi_is_invariant_under_currency_rescaling() -> None:
    """Bất biến: nhân MỌI giá trị tiền với k > 0 -> ROI KHÔNG ĐỔI.

    Bắt được lỗi trộn đơn vị (đồng vs nghìn đồng vs triệu) -- lỗi rất dễ xảy ra
    khi vừa có số VND thô vừa có số "tr" trong tài liệu.
    """
    raise NotImplementedError


@pytest.mark.skip(reason="TODO(A-metrics)")
def test_reallocation_never_exceeds_uncommitted_balance_property() -> None:
    """🔒 Bất biến: với MỌI cấu hình sổ cái, amount <= tổng dòng UNCOMMITTED chưa quá hạn.

    Bản thuộc tính của test cùng tên trong test_alert.py. Đây là ràng buộc an toàn
    quan trọng nhất của sản phẩm -- kiểm cả hai cách.
    """
    raise NotImplementedError


@pytest.mark.skip(reason="TODO(A-metrics)")
def test_snapshot_hash_is_stable_for_identical_inputs() -> None:
    """Bất biến: cùng đầu vào + cùng code -> cùng content_hash, chạy bao nhiêu lần cũng vậy.

    Bắt được nguồn bất định ẩn: thứ tự dict, timestamp lọt vào nội dung, set không sắp xếp,
    float không ổn định.
    """
    raise NotImplementedError


@pytest.mark.skip(reason="TODO(A-metrics)")
def test_trade_spend_components_sum_to_total() -> None:
    """Bất biến: variable + fixed + discretionary == trade_spend, chính xác (số nguyên VND)."""
    # TODO(A-metrics): test này bắt lỗi làm tròn giữa chừng. Tiền là int -> không được sai 1 đồng.
    raise NotImplementedError
