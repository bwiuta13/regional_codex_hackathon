"""CLI Typer — mỗi lệnh là MỘT GIAI ĐOẠN của pipeline.

ĐÂY LÀ BỀ MẶT CÔNG KHAI CỦA HỆ THỐNG. Test gọi qua các điểm vào này (hoặc qua hàm giai đoạn),
KHÔNG gọi vào hàm phụ trợ nội bộ -- xem luật 5 trong AGENTS.md.

    midflight generate --seed 7
    midflight ingest
    midflight evaluate --as-of 2026-10-07
    midflight alert
    midflight recommend
    midflight dossier
    midflight dashboard

Vai trò D sở hữu file này.
"""

from __future__ import annotations

import typer

app = typer.Typer(
    name="midflight",
    help="AI agent giám sát ROI khuyến mãi thương mại khi chương trình đang chạy.",
    no_args_is_help=True,
)


# TODO(D-data): mỗi lệnh dưới đây CHỈ LÀ VỎ MỎNG gọi hàm giai đoạn tương ứng rồi in kết quả.
#   Không đặt logic nghiệp vụ trong cli.py.
# TODO(D-data): mọi lệnh nhận --data-dir, --db, --config-dir, --snapshots-dir với giá trị mặc định
#   hợp lý, để `make demo` chạy được mà không cần truyền tham số.
# TODO(D-data): in tiến độ ngắn gọn ra stdout -> demo nhìn thấy pipeline đang chạy.


@app.command()
def generate(seed: int = 7) -> None:
    """Sinh dữ liệu giả lập có seed (6 chương trình, 3 chuỗi, 56 ngày tiền-khuyến-mãi)."""
    # TODO(D-data): gọi mockdata.generate(seed, out_dir)
    raise NotImplementedError("TODO(D-data)")


@app.command()
def ingest() -> None:
    """Đọc, kiểm tra và nạp CSV vào DuckDB; in báo cáo chất lượng dữ liệu."""
    # TODO(D-data): gọi ingest.ingest(data_dir, db_path), in báo cáo DQ
    # TODO(D-data): thoát với mã khác 0 khi có lỗi NGHIÊM TRỌNG (schema sai, file thiếu hoàn toàn).
    #   Vấn đề về chất lượng (độ phủ thấp, baseline thiếu) KHÔNG làm fail -- chúng là tín hiệu
    #   hợp lệ, được xử lý bằng cách chặn cảnh báo.
    raise NotImplementedError("TODO(D-data)")


@app.command()
def evaluate(as_of: str) -> None:
    """Tính chỉ số cho mọi chương trình đang chạy tại ngày chốt."""
    # TODO(A-metrics): gọi evaluate.evaluate(as_of, db_path)
    raise NotImplementedError("TODO(A-metrics)")


@app.command()
def alert(as_of: str) -> None:
    """Chạy luật, sinh hành động ứng viên, niêm phong snapshot bất biến."""
    # TODO(A-metrics): gọi alert.alert(as_of, metrics, config_dir, snapshots_dir)
    raise NotImplementedError("TODO(A-metrics)")


@app.command()
def recommend(as_of: str, promo_id: str | None = None, language: str = "vi") -> None:
    """Sinh khuyến nghị đã kiểm tra từ snapshot (dùng bản ghi nếu không có OPENAI_API_KEY)."""
    # TODO(B-agent): gọi recommend.recommend(snapshot_path, config_dir, llm, language)
    # TODO(B-agent): không có OPENAI_API_KEY -> dùng tests/recordings/ rồi tới mẫu câu dự phòng.
    #   Demo PHẢI chạy được offline.
    raise NotImplementedError("TODO(B-agent)")


@app.command()
def dossier(as_of: str, promo_id: str) -> None:
    """Xuất hồ sơ chênh lệch dạng Markdown."""
    # TODO(D-data): gọi dossier.render_dossier(...)
    raise NotImplementedError("TODO(D-data)")


@app.command()
def dashboard() -> None:
    """Mở dashboard Streamlit."""
    # TODO(C-ui): chạy `streamlit run src/midflight/dashboard.py`
    raise NotImplementedError("TODO(C-ui)")


if __name__ == "__main__":
    app()
