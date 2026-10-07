"""Giai đoạn INGEST — đọc, kiểm tra, nạp DuckDB.

Entry point: ingest()

Đọc CSV, kiểm tra kiểu dữ liệu và toàn vẹn tham chiếu, viết báo cáo chất lượng dữ liệu (DQ),
rồi nạp vào DuckDB.

Nguyên tắc: DỮ LIỆU Ở VIỆT NAM VỀ KHÔNG ĐỒNG ĐỀU -> hạ cấp mềm, không bao giờ sập.
Thiếu dữ liệu thì GẮN CỜ và CHẶN CẢNH BÁO, chứ không đoán bừa.

Vai trò D sở hữu file này. Bảng xử lý lỗi: docs/data-dictionary.md + spec §4.9.
"""

from __future__ import annotations

from pathlib import Path


def ingest(data_dir: Path, db_path: Path) -> dict:
    """Nạp toàn bộ CSV vào DuckDB và trả về báo cáo chất lượng dữ liệu.

    Args:
        data_dir: thư mục chứa CSV (đầu ra của generate()).
        db_path: file DuckDB đích.

    Returns:
        Báo cáo DQ: số dòng đã nạp, số dòng bị cách ly, cờ đã bật, độ phủ theo chương trình.
        Báo cáo này được ghi ra file để người đọc được, không chỉ trả về.
    """
    # TODO(D-data): chạy src/midflight/schema.sql để tạo bảng trước khi nạp.

    # --- Kiểm tra bắt buộc (docs/data-dictionary.md, mục cuối) ---------------
    # TODO(D-data): kiểm tra SCHEMA + KIỂU DỮ LIỆU từng file -> sai thì TỪ CHỐI FILE, ghi DQ.
    # TODO(D-data): TOÀN VẸN THAM CHIẾU: store_id/sku_id/promo_id phải tồn tại ở bảng master.
    #   Dòng lỗi -> CÁCH LY (quarantine), KHÔNG bỏ im lặng. Liệt kê trong báo cáo DQ.
    # TODO(D-data): DÒNG TRÙNG theo khóa (date, store_id, sku_id)
    #   -> giữ bản ingested_at MỚI NHẤT, báo số lượng đã khử.
    # TODO(D-data): units < 0 là HÀNG TRẢ LẠI HỢP LỆ -> GIỮ LẠI.
    #   Chỉ gắn cờ khi cửa hàng-ngày ÂM RÒNG. Đừng lọc bỏ, sẽ sai iGP.
    # TODO(D-data): CẢ CỬA HÀNG không bán được gì trong ngày (mọi SKU = 0)
    #   -> coi là ĐÓNG CỬA hoặc MẤT DỮ LIỆU. ⚠️ KHÔNG BAO GIỜ coi là hết hàng.
    #   Đây là nguồn báo động giả lớn nhất nếu làm sai.
    # TODO(D-data): FILE POS TRỄ/THIẾU -> đối chiếu danh sách file dự kiến (chuỗi, ngày).
    #   Loại ngày đó; bật COVERAGE_GAP; CHẶN cảnh báo ROI.
    # TODO(D-data): ĐỘ PHỦ = số cửa hàng CÓ DỮ LIỆU / số cửa hàng trong promotion_scope.
    #   ⚠️ Mẫu số phải LOẠI cửa hàng chưa mở (open_date > ngày) và đã đóng (close_date <= ngày),
    #   nếu không COVERAGE_GAP sẽ báo sai.
    # TODO(D-data): CHỒNG LẤN: cùng store x sku nằm trong 2 chương trình ACTIVE
    #   -> cờ OVERLAP, tắt luật ROI cho phần chồng lấn. GẮN CỜ THAY VÌ PHÂN BỔ -- không đoán bừa.
    # TODO(D-data): NGÀY CHƯƠNG TRÌNH TRONG MASTER SAI: nếu giá thực tế cho thấy chiết khấu
    #   bắt đầu sớm/muộn hơn start_date -> lấy NGÀY BẮT ĐẦU THỰC TẾ từ giá, gắn cờ.
    #   Nhà bán lẻ thường bắt đầu lệch một tuần.
    # TODO(D-data): SỔ CÁI không nhất quán: promo_id lạ, amount_vnd âm,
    #   dòng UNCOMMITTED đã QUÁ commit_deadline -> từ chối hoặc phân loại lại, có báo cáo.
    # TODO(D-data): THIẾU LỊCH SỬ BASELINE (< 4 tuần hợp lệ) -> đánh dấu để evaluate() dùng
    #   baseline dự phòng theo cụm, bật BASELINE_INSUFFICIENT, HẠ ĐỘ TIN CẬY.

    # TODO(D-data): ghi báo cáo DQ ra file (data/dq_report.json hoặc .md) để người đọc được,
    #   và dashboard hiển thị được. Báo cáo chỉ trả về trong RAM thì không ai nhìn thấy.
    raise NotImplementedError("TODO(D-data): đọc, kiểm tra, nạp theo docs/data-dictionary.md")
