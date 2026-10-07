# 📚 docs/ — tài liệu nguồn

> **Con người sở hữu thư mục này. Codex chỉ ĐỌC.**
>
> Đây là nơi chứa "sự thật" mà code phải khớp theo. Khi code và tài liệu lệch nhau,
> **tài liệu đúng và code sai** — trừ khi có người quyết định đổi tài liệu trước.

| File | Nội dung | Chủ sở hữu | Code nào đọc nó |
|---|---|---|---|
| [`roi-methodology.md`](roi-methodology.md) | 🔴 **CÔNG THỨC** — baseline, lift, iGP, chi phí, ROI, dự phóng, hết hàng, giá trị biên | Vai trò A + 📊 DS | `evaluate.py`, `alert.py` |
| [`data-dictionary.md`](data-dictionary.md) | Từ điển dữ liệu: bảng, cột, kiểu, ràng buộc | Vai trò D + 📊 DS | `ingest.py`, `schema.sql`, `mockdata.py` |
| [`codex/`](codex/) | `AGENTS.draft.md`, prompt mẫu, `CODEX_LOG.md` | Vai trò D | — |
| [`superpowers/specs/`](superpowers/specs/) | Đặc tả thiết kế gốc (1441 dòng) | Cả nhóm | — |

## 🔒 Luật đổi công thức

> **Một thay đổi công thức = 3 thứ trong CÙNG MỘT pull request:**
>
> 1. `docs/roi-methodology.md` — định nghĩa mới
> 2. `tests/test_evaluate_golden.py` — giá trị kỳ vọng mới (**con người tính, không phải Codex**)
> 3. `snapshot.py` — tăng `schema_version`
>
> ❌ **KHÔNG BAO GIỜ sửa giá trị kỳ vọng trong golden test chỉ để test pass.** Hỏi người.
> Đây là cái bẫy số 1 khi để agent tự chạy: Codex rất hay "sửa" test đỏ bằng cách đổi số kỳ vọng.

## 🤖 Kiểm tra lệch tự động

Codex không chỉ viết code — nó còn **kiểm tra** code có còn khớp phương pháp không:

```bash
make drift
# codex exec --output-schema .codex/drift.schema.json -o drift.json \
#   "Compare docs/roi-methodology.md with src/midflight/evaluate.py and src/midflight/alert.py.
#    List every formula or threshold that differs, with file and line."
```

CI **báo lỗi** nếu `drift.json` liệt kê bất kỳ điểm lệch nào.
Đây là cách cho giám khảo thấy Codex *kiểm tra* sản phẩm, chứ không chỉ gõ code.
