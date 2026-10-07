"""Giai đoạn RECOMMEND — lớp agent: prompt, LLM, validator, renderer, dự phòng.

Entry point: recommend()

🛡️ ĐÂY LÀ NƠI ĐẶT TOÀN BỘ RÀO CHẮN. Nếu file này đúng, agent KHÔNG THỂ đề xuất điều bị cấm,
   kể cả khi mô hình bị dụ, bị prompt injection, hay bị lỗi.

LLM ĐƯỢC LÀM:
  - chọn và sắp thứ tự hành động ứng viên (ĐƯỢC BỎ BỚT nhưng KHÔNG ĐƯỢC TỰ TẠO)
  - viết chẩn đoán kèm đường dẫn bằng chứng
  - viết đoạn diễn giải ngắn cho KAM hoặc trưởng bộ phận trade marketing (en hoặc vi)
  - soạn phần tóm tắt hồ sơ chênh lệch

LLM KHÔNG ĐƯỢC LÀM:
  - gõ số          (văn bản phải viết "{{actual.roi}}", không viết "0.74")
  - tạo hành động mới
  - đặt số tiền
  - nhìn thấy bất cứ thứ gì NGOÀI snapshot

Vai trò B sở hữu file này. Spec §4.7 + Phụ lục D.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Protocol


class LLMClient(Protocol):
    """Client LLM INJECT ĐƯỢC -- để test chạy offline trên phản hồi ghi sẵn.

    Test KHÔNG BAO GIỜ chạm mạng (luật 6 trong AGENTS.md). CI không cần API key.
    """

    def parse(self, *, model: str, input: Any, text_format: type) -> Any: ...


def recommend(
    snapshot_path: Path,
    config_dir: Path,
    llm: LLMClient | None = None,
    language: str = "vi",
) -> dict:
    """Sinh khuyến nghị đã kiểm tra và đã chèn số, từ một snapshot.

    Args:
        snapshot_path: snapshots/<as_of>/<promo_id>.json
        config_dir: thư mục chứa policy.yaml (danh sách hành động, đòn bẩy bị cấm).
        llm: client inject được. None -> đọc tests/recordings/ hoặc dùng mẫu câu dự phòng.
        language: "vi" hoặc "en".

    Returns:
        Khuyến nghị đã render: JSON + Markdown, mọi con số đã chèn từ snapshot.
    """
    # === 1. PROMPT ===========================================================
    # TODO(B-agent): prompt gồm: vai trò, luật, schema, và DỮ LIỆU DẠNG JSON.
    # TODO(B-agent): ⚠️ VĂN BẢN KHÔNG ĐÁNG TIN (promo_name, ghi chú nhà bán lẻ) được truyền vào
    #   DƯỚI DẠNG DỮ LIỆU JSON, KHÔNG BAO GIỜ NHƯ CHỈ DẪN. Đặt nó trong một trường dữ liệu rõ ràng,
    #   kèm câu nói rõ với mô hình rằng nội dung đó là dữ liệu.
    #   Dù vậy, các bước 2-5 của validator VẪN phải chặn mọi ý định bị chèn vào -- phòng thủ nhiều lớp.
    # TODO(B-agent): KHÔNG đưa gì ngoài snapshot vào prompt. Không dòng POS thô, không giá vốn thô.
    #   Đây cũng là câu trả lời cho lo ngại bảo mật: lời gọi LLM chỉ chứa số liệu TỔNG HỢP.
    # TODO(B-agent): đánh phiên bản prompt (PROMPT_VERSION) -> dùng làm khóa cache.

    # === 2. GỌI LLM (Structured Outputs) =====================================
    # TODO(B-agent): client.responses.parse(model=..., input=..., text_format=Recommendation)
    #   -> đọc output_parsed. ⚠️ KIỂM TRA TRƯỜNG `refusal` TRƯỚC khi dùng kết quả.
    # TODO(B-agent): mặc định model "gpt-6-luna" (~0.001 USD mỗi khuyến nghị);
    #   "gpt-6-sol" khi cần chẩn đoán suy luận sâu hơn.
    # TODO(B-agent): ❌ KHÔNG gửi temperature hay top_p cho mô hình suy luận.
    # TODO(B-agent): chế độ strict yêu cầu MỌI TRƯỜNG BẮT BUỘC và additionalProperties: false
    #   -> model trong snapshot.py dùng extra="forbid" và KHÔNG đặt giá trị mặc định.
    # TODO(B-agent): CACHE phản hồi theo khóa (content_hash của snapshot, PROMPT_VERSION, model).
    #   Nhờ vậy demo chạy lại tức thì và không tốn tiền.

    # === 3. VALIDATOR — 6 BƯỚC, ĐỀU TẤT ĐỊNH ================================
    # TODO(B-agent): B1. Đầu ra đúng schema. Structured Outputs đã bảo đảm cấu trúc,
    #   nhưng vẫn parse lại bằng Pydantic -- không tin vào lời hứa của API.
    # TODO(B-agent): B2. MỌI candidate_id PHẢI CÓ trong snapshot.candidates.
    #   -> Nhờ đó mọi loại hành động đều tự động thuộc danh sách được phép.
    #      Đây là rào chắn mạnh nhất: mô hình không bịa được hành động.
    # TODO(B-agent): B3. MỌI đường dẫn bằng chứng phải TRỎ TỚI MỘT TRƯỜNG CÓ THẬT trong snapshot.
    #   "actual.roi" OK; "actual.magic_number" -> từ chối. Bằng chứng ma còn tệ hơn không bằng chứng.
    # TODO(B-agent): B4. 🔢 KHÔNG CÓ CHỮ SỐ NÀO NẰM NGOÀI PLACEHOLDER.
    #   Văn bản phải viết "{{actual.roi}}" chứ không viết "0.74".
    #   ⚠️ MÃ ĐỊNH DANH VÀ NGÀY THÁNG CŨNG ĐI QUA PLACEHOLDER ("{{promo.promo_id}}").
    #   Regex quét mọi chữ số 0-9 nằm ngoài cặp {{ }} -> có là từ chối.
    #   Đây là thứ làm cho "LLM không bịa số" thành ĐẢM BẢO KỸ THUẬT, không phải lời hứa.
    # TODO(B-agent): B5. QUÉT Ý ĐỊNH BỊ CẤM bằng mẫu TIẾNG ANH VÀ TIẾNG VIỆT.
    #   EN: "reduce the discount", "raise the price", "cancel the promotion", "end early",
    #       "renegotiate", "change the rebate", "extend the dates", ...
    #   VI: "giảm mức chiết khấu", "tăng giá", "hủy chương trình", "dừng chương trình",
    #       "kết thúc sớm", "đàm phán lại", "đổi tỷ lệ", "gia hạn", ...
    #   TODO(B-agent): danh sách mẫu đọc từ config/policy.yaml -> forbidden_levers,
    #                  đừng hard-code trong .py (để Business sửa được qua PR).
    # TODO(B-agent): B6. Văn bản không đáng tin đã truyền dưới dạng dữ liệu (xem bước 1);
    #   các bước 2-5 vẫn chặn mọi ý định bị chèn vào.

    # === 4. THỬ LẠI 1 LẦN, RỒI DỰ PHÒNG ======================================
    # TODO(B-agent): validator lỗi -> THỬ LẠI ĐÚNG 1 LẦN, kèm DANH SÁCH LỖI cụ thể trong prompt.
    # TODO(B-agent): vẫn lỗi -> MẪU CÂU DỰ PHÒNG TẤT ĐỊNH.
    #   Dự phòng cho RA CÙNG CÁC HÀNH ĐỘNG với câu chữ đơn giản hơn, và UI HIỆN NHÃN "template".
    #   Nhờ đó demo không bao giờ chết vì mạng hay API.
    # TODO(B-agent): LLM lỗi/timeout cũng đi thẳng vào nhánh dự phòng, không để exception thoát ra.

    # === 5. RENDERER =========================================================
    # TODO(B-agent): điền {{placeholder}} từ snapshot theo đúng đường dẫn.
    # TODO(B-agent): định dạng theo ngôn ngữ:
    #   vi -> "0,74x", "37,9 tr", "19,1%"   (dấu phẩy thập phân, dấu chấm hàng nghìn)
    #   en -> "0.74x", "37.9m VND", "19.1%"
    # TODO(B-agent): placeholder không tồn tại trong snapshot -> LỖI, không render chuỗi rỗng.
    #   Chuỗi rỗng trên UI nguy hiểm hơn một lỗi rõ ràng.
    # TODO(B-agent): ✅ TIÊU CHÍ THÀNH CÔNG: 100% con số hiển thị trên UI và trong văn bản
    #   TRUY ĐƯỢC về một trường trong snapshot. Renderer là thứ bảo đảm điều đó.

    # === 6. ĐẦU RA ===========================================================
    # TODO(B-agent): trả về thẻ khuyến nghị (JSON) + nội dung Markdown cho hồ sơ.
    # TODO(B-agent): kèm cờ `used_fallback` để UI hiện nhãn "template".
    raise NotImplementedError("TODO(B-agent): prompt + LLM + validator + renderer + dự phòng")
