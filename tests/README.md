# ✅ tests/

> ⚠️ Khung rỗng — Codex sinh nội dung trong ngày thi.
> **Ngoại lệ quan trọng:** giá trị kỳ vọng của golden test **do CON NGƯỜI sở hữu**.

## 🔒 Hai luật không bao giờ phá

1. **Golden test viết TRƯỚC, Codex làm cho pass.**
   ❌ **KHÔNG BAO GIỜ sửa giá trị kỳ vọng để test xanh.** Test đỏ = engine sai, không phải test sai.
   Nếu thật sự cần đổi số kỳ vọng → **hỏi người**, và phải đi kèm thay đổi `docs/roi-methodology.md`
   trong **cùng một PR**.

2. **Test đi qua ĐIỂM VÀO của giai đoạn** (`ingest`, `evaluate`, `alert`, `recommend`, CLI).
   🚫 **Không tách hàm chỉ để test gọi được.** Logic không test được qua caller thì **không tách** —
   test qua caller, hoặc nói rõ với nhóm là phần đó không có unit test.

## Các lớp kiểm thử

| File | Lớp | Nội dung | Vai trò |
|---|---|---|---|
| `test_ingest.py` | Ingest | Lỗi schema & kiểu; toàn vẹn tham chiếu; dòng trùng; **chồng lấn thời gian; thiếu độ phủ; thiếu baseline** | D |
| `test_evaluate_golden.py` | 🔴 **Golden** | Ví dụ P-03/P-05 làm fixture. Khớp **tới từng đồng** tại ngày **3, 4, 5, 7** + dự phóng + giá trị ứng viên | A |
| `test_evaluate_properties.py` | Thuộc tính | Hypothesis: `incremental = actual − baseline`; ROI bất biến khi đổi đơn vị tiền; phân bổ lại **không bao giờ** vượt số dư chưa cam kết; **hash snapshot ổn định** | A |
| `test_alert.py` | Alert | Biên của ngưỡng; chặn theo độ phủ & số ngày; logic ngày liên tiếp | A |
| `test_recommend_guardrails.py` | 🛡️ **Rào chắn** | ≥ 30 ca red-team. Đầu ra cuối ⊆ hành động được phép, **0 ý định bị cấm** | B |
| `test_e2e.py` | Đầu-cuối | `make demo` offline sinh ra snapshot, khuyến nghị, hồ sơ; smoke test dashboard bằng `AppTest` | C/D |

## 🌐 Test KHÔNG BAO GIỜ chạm mạng

Gọi LLM đi qua **client inject được**; test dùng `tests/recordings/`.
→ CI không cần API key, chạy nhanh, và không tốn tiền.

```python
recommend(snapshot_path, config_dir, llm=RecordedClient("tests/recordings/..."))
```

## ✅ Tiêu chí thành công của demo (spec §4.12)

- Vấn đề cài sẵn ở P-03 được gắn cờ **trước hoặc đúng ngày 5/21**
- **100% con số** trên UI và trong văn bản truy được về trường trong snapshot
- **0 khuyến nghị bị cấm** trên toàn bộ bộ red-team
- Toàn bộ pipeline chạy **dưới 60 giây** trên dữ liệu giả lập, mọi test xanh

```bash
uv run pytest -q
uv run pytest tests/test_evaluate_golden.py -v      # trước tiên và quan trọng nhất
uv run pytest tests/test_recommend_guardrails.py -v # rào chắn
```

> 🚨 **Nếu chậm tiến độ, thứ tự cắt:** (1) khoảng bootstrap, (2) PDF hồ sơ, (3) thanh trượt thời gian,
> (4) văn bản tiếng Việt. **KHÔNG BAO GIỜ cắt golden test hay test rào chắn.**
