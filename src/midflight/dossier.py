"""Giai đoạn DOSSIER — hồ sơ chênh lệch cho kỳ đàm phán sau.

Entry point: render_dossier()

Đây là hành động PREPARE_VARIANCE_DOSSIER biến thành sản phẩm thật:
bộ bằng chứng mang vào kỳ review / gia hạn / đàm phán với chuỗi.

⚖️ Vì sao nó quan trọng về mặt nghiệp vụ: các nguyên nhân CẤU TRÚC (chiết khấu trợ giá cho
doanh số nền) KHÔNG sửa được giữa chừng -- chúng là bài học cho KỲ ĐÀM PHÁN SAU.
Hồ sơ này là cách duy nhất biến một chương trình lỗ thành đòn bẩy đàm phán.

Vai trò D sở hữu file này (vai trò C nếu cần bản PDF).
"""

from __future__ import annotations

from pathlib import Path


def render_dossier(snapshot_path: Path, decisions_path: Path, out_path: Path) -> Path:
    """Sinh hồ sơ chênh lệch dạng Markdown từ snapshot + nhật ký quyết định.

    Args:
        snapshot_path: snapshot của ngày chốt.
        decisions_path: nhật ký duyệt/từ chối/hoãn (kèm lý do).
        out_path: file Markdown đích.
    """
    # TODO(D-data): dùng Jinja2, mẫu ở src/midflight/templates/variance_dossier.md.j2
    # TODO(D-data): nội dung bắt buộc (theo kịch bản demo):
    #   - Tóm tắt chương trình: kế hoạch vs thực tế vs dự phóng
    #   - 135 CỬA HÀNG-NGÀY HẾT HÀNG (danh sách cửa hàng + ngày)
    #   - 63 CỬA HÀNG-NGÀY KHÔNG TUÂN THỦ GIÁ -> phần ĐỐI SOÁT SCAN REBATE
    #     (ta đã trả rebate cho những cửa hàng-ngày không hề giảm giá?)
    #   - Bằng chứng thực thi khoản phí trưng bày 36 tr (có được làm đúng không?)
    #   - Nhật ký quyết định: ai duyệt gì, khi nào, VỚI LÝ DO
    # TODO(D-data): ⚠️ GHI RÕ GIỚI HẠN ĐÃ BIẾT trong hồ sơ (chưa tính ăn mòn doanh số,
    #   hiệu ứng lan tỏa, sụt giảm hậu khuyến mãi, gom hàng trước; dự phóng chỉ dùng run-rate).
    #   Hồ sơ này sẽ được đưa cho ĐỐI TÁC đọc -- nói quá một con số là mất uy tín lâu dài.
    # TODO(D-data): mọi con số lấy TỪ SNAPSHOT, không tính lại ở đây.
    # TODO(C-ui): bản PDF là MỤC CẮT THỨ HAI nếu thiếu thời gian -- giữ bản Markdown.
    raise NotImplementedError("TODO(D-data): render hồ sơ chênh lệch bằng Jinja2")
