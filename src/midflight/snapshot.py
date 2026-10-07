"""HỢP ĐỒNG DỮ LIỆU — PromotionSnapshot và Recommendation.

🔴 FILE QUAN TRỌNG NHẤT CỦA REPO. Phải xong TRƯỚC 10:45 ngày thi, vì mọi phần khác phụ thuộc vào nó.

PromotionSnapshot là ĐIỂM BÀN GIAO DUY NHẤT VÀ BẤT BIẾN giữa lõi tất định và mọi thành phần
còn lại (agent, dashboard, hồ sơ). Nhờ nó, những gì người dùng THẤY và những gì agent NÓI
không thể lệch nhau.

Quy tắc:
  - Snapshot CHỈ ĐƯỢC GHI THÊM. Chạy lại với cùng đầu vào + cùng code -> cùng content_hash.
    Đầu vào thay đổi sinh snapshot MỚI, không bao giờ ghi đè snapshot cũ.
  - Dashboard chỉ ĐỌC snapshot, không bao giờ tự tính lại chỉ số.
  - Thanh trượt "du hành thời gian" trong demo chỉ đơn giản là nạp các snapshot cũ hơn.

Lưu tại: snapshots/<as_of>/<promo_id>.json

Vai trò B sở hữu file này. Spec §4.6 và Phụ lục D.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict

# Phiên bản schema. TĂNG khi đổi cấu trúc hoặc đổi công thức tính bất kỳ trường nào.
# Luật 2 trong AGENTS.md: đổi công thức = methodology doc + golden test + schema_version, CÙNG 1 PR.
SCHEMA_VERSION = "1.0"

# Danh sách hành động ĐÓNG. Nguồn sự thật là config/policy.yaml.
# TODO(B-agent): đọc từ config/policy.yaml khi khởi tạo thay vì khai báo lại ở đây,
#                rồi assert hai bên khớp nhau -> lệch là lỗi cấu hình, phải fail sớm.
ActionType = Literal[
    "REALLOCATE_UNCOMMITTED_FUNDS",
    "ESCALATE_STOCKOUT",
    "ESCALATE_PRICE_COMPLIANCE",
    "DEFER_DISCRETIONARY_SPEND",
    "PREPARE_VARIANCE_DOSSIER",
    "MONITOR",
]

ExceptionCode = Literal[
    "ROI_BEHIND_PLAN",
    "LOW_LIFT",
    "STOCKOUT_SUSPECTED",
    "DISCOUNT_NOT_APPLIED",
    "SPEND_OVERRUN",
    "COVERAGE_GAP",
    "BASELINE_INSUFFICIENT",
    "OVERLAP",
    "OUTPERFORMING",
]


# ---------------------------------------------------------------------------
# PromotionSnapshot — engine ghi, mọi thành phần khác đọc
# ---------------------------------------------------------------------------
# TODO(B-agent): mọi model dưới đây dùng model_config = ConfigDict(frozen=True, extra="forbid").
#   frozen=True       -> bất biến, không ai sửa được snapshot sau khi tạo
#   extra="forbid"    -> bắt lỗi sớm khi engine ghi thừa trường
# TODO(B-agent): TIỀN LÀ int VND. Không dùng float cho bất kỳ trường *_vnd nào.
#   Tỷ lệ (roi, lift, discount_pct, share) dùng float.


class Promo(BaseModel):
    """Thông tin gốc của chương trình. Xem docs/data-dictionary.md -> promotions."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    # TODO(B-agent): promo_id, retailer, brand, start, end, elapsed_days, remaining_days,
    #                discount_pct, mfr_funding_share, fund_pool_id
    # TODO(B-agent): KHÔNG đưa promo_name vào đây nếu không cần. Nếu cần (để hiển thị), nhớ rằng
    #                đây là VĂN BẢN KHÔNG ĐÁNG TIN -> truyền tới LLM dưới dạng JSON data,
    #                không bao giờ như chỉ dẫn. Validator vẫn chặn ý định bị chèn vào.


class Plan(BaseModel):
    """Đường kế hoạch lũy kế đến as_of. Dùng CÙNG công thức với thực tế (roi-methodology §5)."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    # TODO(A-metrics): lift, roi, units_to_date, igp_to_date_vnd, spend_to_date_vnd


class Actual(BaseModel):
    """Thực tế lũy kế đến as_of. Toàn bộ do evaluate() tính."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    # TODO(A-metrics): units, baseline_units, incremental_units, lift, igp_vnd,
    #                  variable_spend_vnd, fixed_spend_recognized_vnd,
    #                  discretionary_spend_recognized_vnd, trade_spend_vnd,
    #                  roi, roi_gap, realized_discount_rate
    # TODO(A-metrics): tách RIÊNG 3 loại chi phí (variable/fixed/discretionary) chứ không chỉ tổng.
    #                  Dashboard cần chúng để vẽ biểu đồ thác nước sổ cái.


class Projection(BaseModel):
    """Dự phóng đến cuối chương trình. roi-methodology §7."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    # TODO(A-metrics): method (vd "trailing_3d_run_rate"), roi, net_vnd
    # TODO(A-metrics): TÊN PHƯƠNG PHÁP BẮT BUỘC ghi vào snapshot -> người đọc biết con số đến từ đâu.
    # TODO(A-metrics): band P10-P90 (bootstrap) nếu còn thời gian. Đây là MỤC CẮT ĐẦU TIÊN.


class DataQuality(BaseModel):
    """Chỉ số chất lượng dữ liệu. Quyết định cảnh báo nào bị CHẶN."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    # TODO(D-data): store_coverage, baseline_fallback_share, overlaps
    # TODO(D-data): store_coverage < config.min_store_coverage -> CHẶN cảnh báo ROI.
    #               Dữ liệu sớm chắp vá dễ tạo báo động giả, và báo động giả làm mất lòng tin
    #               NHANH HƠN việc bỏ sót.


class ExceptionItem(BaseModel):
    """Một cảnh báo đã kích hoạt. roi-methodology + config/thresholds.yaml."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    # TODO(A-metrics): code (ExceptionCode), severity, first_as_of, confirmed_as_of, stores
    # TODO(A-metrics): first_as_of giúp kể câu chuyện "phát hiện từ ngày 4" trong demo -> đừng bỏ.


class FundLine(BaseModel):
    """Một dòng sổ cái CHƯA CAM KẾT — khoản tiền agent được phép đề xuất chuyển."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    # TODO(A-metrics): entry_id, type (spend_type), amount_vnd, commit_deadline
    # TODO(A-metrics): CHỈ đưa vào đây dòng có commitment == UNCOMMITTED và chưa quá commit_deadline.
    #                  Dòng RETAILER_COMMITTED / INTERNAL_COMMITTED tuyệt đối không được lọt vào,
    #                  nếu không agent sẽ đề xuất chuyển tiền đã hứa với đối tác.


class Funds(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    # TODO(A-metrics): uncommitted_vnd, lines: list[FundLine]


class Candidate(BaseModel):
    """Hành động ứng viên ĐÃ TÍNH SẴN SỐ TIỀN, do engine sinh ra TRƯỚC khi gọi LLM.

    LLM chỉ được CHỌN và XẾP ƯU TIÊN trong danh sách này -- được bỏ bớt nhưng KHÔNG ĐƯỢC TỰ TẠO.
    Đây là rào chắn số 1: nếu LLM không thể tạo hành động mới thì nó không thể đề xuất
    điều gì nằm ngoài chính sách.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    # TODO(A-metrics): candidate_id, type (ActionType), stores, value_at_stake_vnd
    # TODO(A-metrics): riêng REALLOCATE thêm: from_promo, to_promo, amount_vnd,
    #                  indicative_net_vnd, breakeven_haircut, marginal_method, confidence
    # TODO(A-metrics): breakeven_haircut PHẢI công bố kèm khuyến nghị -> người duyệt tự phán đoán,
    #                  không bắt họ tin mù vào haircut 0.70.
    # TODO(A-metrics): confidence = "medium" khi đo được bằng within_promo_split,
    #                               "low"    khi phải dùng dự phòng average_roi.


class PromotionSnapshot(BaseModel):
    """Trạng thái BẤT BIẾN của một chương trình tại một ngày chốt.

    File: snapshots/<as_of_date>/<promo_id>.json
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    # TODO(B-agent): snapshot_id  (dạng "P-03@2026-10-07#9f2c1e7a")
    # TODO(B-agent): schema_version, metric_version (git SHA của code tính chỉ số)
    # TODO(B-agent): as_of_date, promo, plan, actual, projection, data_quality,
    #                exceptions, funds, candidates, content_hash
    # TODO(B-agent): content_hash = sha256 của nội dung đã chuẩn hóa (bỏ chính trường content_hash).
    #                Hash phải ỔN ĐỊNH: cùng đầu vào + cùng code -> cùng hash.
    #                Test thuộc tính (Hypothesis) kiểm điều này.
    # TODO(B-agent): metric_version lấy từ git rev-parse HEAD khi niêm phong snapshot.
    #                Nhờ nó, khi một con số trông lạ, ta truy được code nào đã tính ra nó.


# ---------------------------------------------------------------------------
# Recommendation — schema LLM phải trả về (Structured Outputs, strict mode)
# ---------------------------------------------------------------------------
# ⚠️ Chế độ strict của OpenAI yêu cầu MỌI TRƯỜNG ĐỀU BẮT BUỘC và additionalProperties: false.
#    -> extra="forbid" và KHÔNG ĐẶT GIÁ TRỊ MẶC ĐỊNH cho bất kỳ trường nào dưới đây.


class Finding(BaseModel):
    """Một phát hiện chẩn đoán do LLM viết."""

    model_config = ConfigDict(extra="forbid")

    # TODO(B-agent): text: str      -- CHỈ dùng placeholder "{{actual.roi}}", CẤM chữ số.
    #                                  Kể cả mã định danh và ngày tháng cũng đi qua placeholder
    #                                  ("{{promo.promo_id}}"). Renderer chèn giá trị đã định dạng.
    # TODO(B-agent): evidence: list[str]  -- đường dẫn TRONG snapshot, vd "actual.roi", "exceptions[3]"


class ActionPick(BaseModel):
    """Một hành động LLM chọn từ snapshot.candidates."""

    model_config = ConfigDict(extra="forbid")

    # TODO(B-agent): candidate_id (PHẢI tồn tại trong snapshot.candidates), priority (1 = làm trước),
    #                rationale (chỉ placeholder), evidence


class Recommendation(BaseModel):
    """Đầu ra của lớp agent. Validator kiểm tra trước khi render."""

    model_config = ConfigDict(extra="forbid")

    # TODO(B-agent): snapshot_id, language: Literal["en","vi"], headline,
    #                diagnosis: list[Finding], actions: list[ActionPick],
    #                not_changing: list[str], confidence: Literal["high","medium","low"],
    #                caveats: list[str]
    # TODO(B-agent): not_changing = các đòn bẩy ĐÃ CAM KẾT được CHỦ ĐỘNG giữ nguyên.
    #                Nó hiện thành ô "Những gì chúng tôi sẽ KHÔNG thay đổi" trên UI.
    #                Đây không phải trang trí -- đó là điểm bán hàng.
