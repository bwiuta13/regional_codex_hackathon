# 🤖 docs/codex/ — dùng Codex có chủ đích

> **"Mức độ tận dụng Codex hiệu quả" là 1 trong 4 tiêu chí chấm.**
> Vì vậy việc dùng Codex phải **có chủ đích và NHÌN THẤY ĐƯỢC** — không phải "có dùng autocomplete".

| File | Nội dung | Khi nào dùng |
|---|---|---|
| [`AGENTS.draft.md`](AGENTS.draft.md) | ⚠️ Bản nháp của `AGENTS.md` | **Gõ lại thành `/AGENTS.md` lúc 10:00–10:30 ngày thi** |
| [`prompts.md`](prompts.md) | Prompt mẫu theo khuôn Goal/Context/Constraints/Done when | Trong suốt ngày thi |
| [`CODEX_LOG.md`](CODEX_LOG.md) | Nhật ký mỗi task Codex | Ghi **ngay sau mỗi task**, không để cuối ngày |

## 4 nguyên tắc

1. **Con người sở hữu định nghĩa, Codex viết code.** Công thức, ngưỡng và chính sách hành động lấy từ
   spec và do người review. Codex triển khai, **không bao giờ âm thầm thay đổi**.
2. **Test là hợp đồng.** Golden test dựa trên `Business/05-demo-scenario-numbers.md` được viết **trước**,
   Codex lặp lại cho tới khi pass. **Giá trị kỳ vọng do con người sở hữu.**
3. **Song song, cô lập, có review.** Mỗi chat Codex = 1 kết quả hoàn chỉnh, chạy trong **git worktree riêng**.
   Quyền sở hữu file **không chồng lấn**. Mọi PR qua `@codex review`.
4. **Codex vừa xây vừa kiểm.** Ngoài viết code, `codex exec` chạy **kiểm tra lệch** xem code
   có còn khớp `docs/roi-methodology.md` không → `make drift`.

## Công cụ & cách dùng

| Công cụ | MidFlight dùng thế nào |
|---|---|
| **Codex CLI** | Công cụ chính, mỗi người 1 worktree. `/plan` mở luồng việc · `/goal` kèm "xong khi" · `/diff` + `/review` trước mỗi commit |
| **Codex trong ChatGPT desktop app** | Chạy 2–3 chat song song/người mà không đụng file của nhau (worktree tích hợp) |
| **Extension IDE** | Sửa trực tiếp dashboard và SQL |
| **Codex cloud** | Việc độc lập: fixture red-team, từ điển dữ liệu, **best-of-N** cho 3 phương án bố cục dashboard (`codex cloud exec --attempts`) |
| **`@codex review` trên GitHub** | Tự động review mọi PR theo `## Code Review Rules` trong AGENTS.md |
| **`codex exec`** | Kiểm tra lệch phương pháp, chạy trong CI và trước demo (`--output-schema`, `-o`) |
| **Skills** | `.agents/skills/metric-change/SKILL.md` — ép đúng trình tự: tài liệu → golden test → code → phiên bản schema |

**Mô hình:** Sol mức Medium cho engine và rào chắn · Luna cho code khung, fixture, tài liệu ·
Astra (nếu được cấp) cho lỗi khó nhất.
⚠️ Danh sách mô hình thay đổi nhanh — **GPT-5.5 ngừng trên Codex từ 14/10/2026**. Kiểm lại T−1 tuần.

## ⚠️ Bẫy cần tránh

| Bẫy | Cách phòng |
|---|---|
| Hai chat Codex cùng sửa một file | Bảng sở hữu file (README gốc); mỗi chat 1 worktree |
| **Codex "sửa" golden test đang đỏ bằng cách đổi giá trị kỳ vọng** | Luật 2 trong AGENTS.md + luật review. **Con người sở hữu giá trị golden** |
| Task cloud lỗi khi cài thư viện | Internet mặc định **tắt** trong pha agent → cài mọi thứ trong setup script của môi trường |
| Mô hình ngừng hỗ trợ | Dùng Sol hoặc Luna; kiểm lại 1 tuần trước sự kiện |
| Hết hạn mức giữa chiều | Luna cho code khung; chỉ dùng Sol/Astra ở chỗ cần suy luận |
| UI ôm đồm quá mức | 3 màn hình, có giới hạn thời gian; thứ tự cắt giảm có sẵn |
| **"Code dựng sẵn"** | Chỉ mang theo tài liệu; hỏi ban tổ chức về AGENTS.md (`Business/06-open-questions.md` Q1) |

## 📊 Cho giám khảo thấy gì

- **`CODEX_LOG.md`**: mỗi task 1 dòng — công cụ, prompt, kết quả, **phần con người đã sửa hoặc bác bỏ**
- **Lịch sử PR**: mỗi luồng việc vào main qua PR có luồng `@codex review`
- **Rào chắn**: dành 15 giây trong pitch cho luật AGENTS.md + bước kiểm tra lệch
- **Con số**: số task Codex đã chạy · tỷ lệ dòng code viết cùng Codex · số test được sinh · số lần dùng cloud best-of-N
- **Những gì KHÔNG giao cho Codex**: định nghĩa chỉ số, ngưỡng, chính sách, giá trị golden ← nói rõ điều này
