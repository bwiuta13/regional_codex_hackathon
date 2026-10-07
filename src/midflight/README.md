# 🐍 src/midflight/ — code

> ⚠️ **MỌI FILE Ở ĐÂY LÀ KHUNG RỖNG.** Chỉ có docstring, chữ ký hàm và `TODO(...)`.
> Thân hàm đều `raise NotImplementedError`. Codex sinh implementation **trong ngày thi**.

## Kiến trúc: mỗi giai đoạn 1 file, mỗi file 1 entry point

```
                      ┌─────────────────────────────────────────┐
  CSV ──▶ ingest ──▶  │  DuckDB  │──▶ evaluate ──▶ alert ──▶  snapshots/<as_of>/<promo>.json
                      └─────────────────────────────────────────┘          │  🔒 BẤT BIẾN
                                                                            │
                                            ┌───────────────────────────────┤
                                            ▼                               ▼
                                     recommend (LLM)                   dashboard
                                            │                               ▲
                                            └──── validator ────────────────┘
                                                      │
                                                      ▼
                                                   dossier
```

| File | Entry point | Trách nhiệm | Vai trò |
|---|---|---|---|
| `snapshot.py` | *(models)* | 🔴 **HỢP ĐỒNG** Pydantic — mọi giai đoạn dùng chung | B |
| `mockdata.py` | `generate()` | Bộ sinh kịch bản có seed | D |
| `ingest.py` | `ingest()` | Đọc · kiểm tra · nạp DuckDB · báo cáo DQ | D |
| `schema.sql` | — | DDL cho DuckDB | A |
| `evaluate.py` | `evaluate()` | baseline · lift · iGP · chiết khấu · chi phí · ROI · dự phóng | A |
| `alert.py` | `alert()` | luật · chặn · hành động ứng viên · **niêm phong snapshot** | A + D |
| `recommend.py` | `recommend()` | prompt · LLM · validator · renderer · dự phòng | B |
| `dossier.py` | `render_dossier()` | Hồ sơ chênh lệch (Jinja2 → Markdown) | D |
| `dashboard.py` | `main()` | Streamlit — **CHỈ ĐỌC snapshot** | C |
| `cli.py` | `app` | Typer — mỗi giai đoạn 1 lệnh | D |

## 🔒 Luật bắt buộc

1. **Mỗi giai đoạn đọc đầu ra ĐÃ LƯU của giai đoạn trước.** Không gọi chéo trực tiếp.
2. **Mỗi file có ĐÚNG MỘT hàm công khai.** Test đi qua entry point, không gọi hàm nội bộ.
3. 🚫 **Không tách hàm chỉ dùng 1 lần.** Không tách hàm chỉ để test gọi được.
   Thà một hàm dài mà review được còn hơn 10 mảnh rời rạc không ai theo nổi trong 7 giờ.
4. **Dashboard KHÔNG BAO GIỜ tính lại chỉ số** — chỉ đọc snapshot và khuyến nghị.
   Đó là cách đảm bảo UI và agent không thể nói lệch nhau.
5. **Snapshot chỉ được ghi thêm.** Cùng đầu vào + cùng code → cùng `content_hash`.
6. **Tiền là số nguyên VND.** Không float cho tiền ở bất kỳ đâu.
7. **Mọi ngưỡng đọc từ `config/*.yaml`.** Không hard-code một con số nào trong `.py`.

## Xem việc của mình

```bash
grep -rn "TODO(A-metrics)" src tests     # vai trò A
grep -rn "TODO(B-agent)"   src tests     # vai trò B
grep -rn "TODO(C-ui)"      src tests     # vai trò C
grep -rn "TODO(D-data)"    src tests     # vai trò D
```
