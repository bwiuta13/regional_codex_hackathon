"""Test giai đoạn INGEST — chất lượng dữ liệu và hạ cấp mềm.

Nguyên tắc: dữ liệu ở Việt Nam về KHÔNG ĐỒNG ĐỀU -> hệ thống không bao giờ được sập,
mà phải GẮN CỜ và CHẶN CẢNH BÁO.

Vai trò D sở hữu file này. Bảng xử lý lỗi: docs/data-dictionary.md.
"""

from __future__ import annotations

import pytest


@pytest.mark.skip(reason="TODO(D-data): bỏ skip khi ingest() đã có")
def test_rejects_bad_schema_and_types() -> None:
    """File sai schema/kiểu -> TỪ CHỐI FILE, ghi vào báo cáo DQ."""
    raise NotImplementedError


@pytest.mark.skip(reason="TODO(D-data)")
def test_quarantines_rows_with_broken_foreign_keys() -> None:
    """store_id/sku_id lạ -> CÁCH LY dòng, liệt kê trong DQ. KHÔNG bỏ im lặng."""
    raise NotImplementedError


@pytest.mark.skip(reason="TODO(D-data)")
def test_deduplicates_by_latest_ingested_at() -> None:
    """Dòng trùng theo (date, store_id, sku_id) -> giữ bản mới nhất, BÁO SỐ LƯỢNG."""
    raise NotImplementedError


@pytest.mark.skip(reason="TODO(D-data)")
def test_keeps_negative_units_as_returns() -> None:
    """units < 0 là hàng trả lại HỢP LỆ -> GIỮ LẠI. Lọc bỏ sẽ làm sai iGP."""
    raise NotImplementedError


@pytest.mark.skip(reason="TODO(D-data)")
def test_whole_store_zero_day_is_not_a_stockout() -> None:
    """⚠️ Cả cửa hàng không bán được gì -> đóng cửa/mất dữ liệu, KHÔNG BAO GIỜ là hết hàng.

    Đây là nguồn báo động giả lớn nhất nếu làm sai.
    """
    raise NotImplementedError


# --- 3 trường hợp bài dự thi đã nêu rõ -------------------------------------
@pytest.mark.skip(reason="TODO(D-data)")
def test_flags_time_overlapping_promotions() -> None:
    """Cùng store x sku trong 2 chương trình ACTIVE -> OVERLAP, TẮT luật ROI phần chồng lấn.

    GẮN CỜ THAY VÌ PHÂN BỔ -- không đoán bừa quy kết.
    """
    raise NotImplementedError


@pytest.mark.skip(reason="TODO(D-data)")
def test_flags_missing_store_coverage() -> None:
    """Độ phủ < 80% -> COVERAGE_GAP và CHẶN cảnh báo ROI.

    ⚠️ Mẫu số phải LOẠI cửa hàng chưa mở / đã đóng (open_date, close_date).
    """
    raise NotImplementedError


@pytest.mark.skip(reason="TODO(D-data)")
def test_flags_missing_baseline_observations() -> None:
    """< 4 tuần ngày sạch -> baseline dự phòng theo cụm, BASELINE_INSUFFICIENT, HẠ ĐỘ TIN CẬY."""
    raise NotImplementedError


@pytest.mark.skip(reason="TODO(D-data)")
def test_detects_actual_start_date_from_prices() -> None:
    """Nhà bán lẻ bắt đầu lệch 1 tuần -> lấy ngày bắt đầu THỰC TẾ từ giá, gắn cờ."""
    raise NotImplementedError


@pytest.mark.skip(reason="TODO(D-data)")
def test_rejects_inconsistent_ledger_rows() -> None:
    """promo_id lạ, amount âm, UNCOMMITTED đã QUÁ commit_deadline -> từ chối/phân loại lại."""
    raise NotImplementedError
