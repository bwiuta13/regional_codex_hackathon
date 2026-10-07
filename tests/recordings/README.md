# 📼 tests/recordings/

Phản hồi LLM **ghi sẵn**, để test chạy **hoàn toàn offline**.

> 🌐 **Luật 6 trong AGENTS.md: test KHÔNG BAO GIỜ chạm mạng.**
> CI không cần API key, chạy nhanh, không tốn tiền, và không phụ thuộc mạng hội trường.

## Khóa cache

`(content_hash của snapshot, PROMPT_VERSION, model)`

Đổi prompt hoặc đổi model → khóa đổi → cần ghi lại. Snapshot không đổi thì bản ghi vẫn dùng được.

## Ghi bản ghi mới

```bash
# Cần OPENAI_API_KEY. Chỉ chạy khi CỐ Ý muốn cập nhật bản ghi.
uv run pytest tests/test_recommend_guardrails.py --live
```

## Nên ghi những gì

| Loại | Vì sao cần |
|---|---|
| ✅ Đầu ra **hợp lệ** cho P-03 ngày 7 | Đường đi chính của demo |
| ❌ Đầu ra **gõ số** thẳng (`0.74`) | Chứng minh validator bước 4 chặn được |
| ❌ `candidate_id` **không tồn tại** | Chứng minh bước 2 chặn được |
| ❌ Đường dẫn **bằng chứng sai** | Chứng minh bước 3 chặn được |
| ❌ Ý định bị cấm **tiếng Anh** | Chứng minh bước 5 chặn được |
| ❌ Ý định bị cấm **tiếng Việt** | ⚠️ Bắt buộc — chỉ quét EN là lọt |
| ❌ Mô hình **nghe theo prompt injection** | Chứng minh phòng thủ nhiều lớp vẫn chặn |

> 🎯 Các bản ghi "xấu" quan trọng **ngang** bản ghi tốt — chúng mới là thứ chứng minh rào chắn hoạt động.
