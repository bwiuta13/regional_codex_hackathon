"""Test ĐẦU-CUỐI — `make demo` chạy offline và sinh ra đủ sản phẩm.

🌐 CHẠY OFFLINE. Không cần OPENAI_API_KEY.

Vai trò C + D sở hữu file này. Spec §4.10, §4.12.
"""

from __future__ import annotations

import pytest


@pytest.mark.skip(reason="TODO(D-data): bỏ skip khi pipeline đã chạy được")
def test_full_pipeline_offline_produces_snapshot_recommendation_and_dossier() -> None:
    """generate -> ingest -> evaluate -> alert -> recommend -> dossier, hoàn toàn offline."""
    # TODO(D-data): chạy tuần tự qua các ĐIỂM VÀO CLI (không gọi hàm nội bộ).
    # TODO(D-data): assert có file snapshots/2026-10-07/P-03.json
    # TODO(D-data): assert khuyến nghị được sinh (dù qua bản ghi hay mẫu câu dự phòng)
    # TODO(D-data): assert hồ sơ chênh lệch Markdown được sinh
    raise NotImplementedError


@pytest.mark.skip(reason="TODO(D-data)")
def test_pipeline_runs_under_60_seconds() -> None:
    """✅ Tiêu chí thành công (spec §4.12): toàn bộ pipeline < 60 giây trên dữ liệu giả lập."""
    raise NotImplementedError


@pytest.mark.skip(reason="TODO(A-metrics)")
def test_p03_is_flagged_on_or_before_day_5_of_21() -> None:
    """✅ TIÊU CHÍ THÀNH CÔNG QUAN TRỌNG NHẤT CỦA DEMO.

    Vấn đề cài sẵn ở P-03 phải được gắn cờ TRƯỚC HOẶC ĐÚNG ngày 5/21
    -> còn ít nhất 16 ngày để hành động.

    Nếu test này đỏ thì cả bài pitch mất luận điểm chính ("bắt được giữa chừng").
    """
    # TODO(A-metrics): chạy alert cho as_of 2026-10-03, -04, -05.
    #   assert DISCOUNT_NOT_APPLIED có từ 2026-10-03 (phát sáng 04/10)
    #   assert STOCKOUT_SUSPECTED có từ 2026-10-04 (phát sáng 05/10)
    raise NotImplementedError


@pytest.mark.skip(reason="TODO(C-ui)")
def test_dashboard_smoke_with_apptest() -> None:
    """Smoke test dashboard bằng streamlit.testing AppTest trên snapshot fixture."""
    # TODO(C-ui): dùng tests/fixtures/snapshot_P-03_2026-10-07.json
    raise NotImplementedError


@pytest.mark.skip(reason="TODO(C-ui)")
def test_every_number_on_screen_traces_to_a_snapshot_field() -> None:
    """✅ Tiêu chí thành công: 100% con số hiển thị truy được về một trường trong snapshot."""
    # TODO(C-ui): thu thập mọi chuỗi số render ra, assert mỗi chuỗi khớp một giá trị đã định dạng
    #   từ snapshot. Dashboard KHÔNG BAO GIỜ được tự tính lại chỉ số.
    raise NotImplementedError
