# 👔 Business — chuẩn bị nghiệp vụ & dữ liệu trước ngày thi

Folder này **không chứa code**. Đây là nơi bạn **Business** và bạn **Data Science** nhận việc.

Mục tiêu: đến 10:00 ngày 31/10/2026, nhóm kỹ thuật **không phải hỏi một câu nghiệp vụ nào nữa**.
Mọi con số, định nghĩa, ngưỡng và file dữ liệu đã chốt sẵn. 7 giờ chỉ dùng để code.

---

## Vì sao cần folder này

MidFlight là **Deep Domain AI**: giá trị nằm ở chỗ nó mã hóa đúng cách trade marketing thật sự vận hành
(tiền đã cam kết vs chưa cam kết, phương pháp phân tích hậu kiểm, luật khuyến mại Việt Nam).
Nếu nghiệp vụ sai thì code chạy đúng vẫn ra kết quả vô nghĩa — và giám khảo sẽ hỏi đúng chỗ đó.

Ba thứ **chỉ con người quyết được, Codex không được tự chọn**:

1. **Định nghĩa chỉ số** (baseline là gì, ROI tính thế nào) → `docs/roi-methodology.md`
2. **Ngưỡng cảnh báo** (bao nhiêu % thì báo động) → `config/thresholds.yaml`
3. **Danh sách hành động được phép / bị cấm** → `config/policy.yaml`

Đây cũng chính là điều nhóm cam kết trong bài dự thi và sẽ nói với giám khảo ở phần pitch:
*"Những gì chúng tôi KHÔNG giao cho Codex."*

---

## Đọc theo thứ tự

| # | File | Dành cho | Thời gian đọc |
|---|---|---|---|
| 1 | [`01-business-context.md`](01-business-context.md) | **Cả nhóm** — nghiệp vụ tóm tắt | 10 phút |
| 2 | [`02-task-business.md`](02-task-business.md) | 👔 **Business** — checklist phải chốt | 15 phút |
| 3 | [`03-task-data-science.md`](03-task-data-science.md) | 📊 **Data Science** — checklist phải dựng | 20 phút |
| 4 | [`04-data-requirements.md`](04-data-requirements.md) | 👔 + 📊 — hợp đồng dữ liệu chi tiết | 20 phút |
| 5 | [`05-demo-scenario-numbers.md`](05-demo-scenario-numbers.md) | 📊 + vai trò A — số chuẩn cho golden test | 15 phút |
| 6 | [`06-open-questions.md`](06-open-questions.md) | **Cả nhóm** — câu hỏi chặn, cần người quyết | 5 phút |
| — | [`templates/`](templates/) | 📊 — CSV mẫu có header để điền | — |

---

## Ranh giới trách nhiệm

```
👔 BUSINESS                          📊 DATA SCIENCE                    🐍 ENGINEERING (ngày thi)
─────────────────                   ──────────────────                  ──────────────────────
Định nghĩa nghiệp vụ         ──▶    Chuyển thành công thức      ──▶    Codex viết code theo
"Thế nào là hết hàng?"              λ, Poisson, ngưỡng 0.001            docs/roi-methodology.md

Kinh tế đơn vị               ──▶    Sinh dữ liệu giả lập         ──▶    ingest() nạp vào DuckDB
giá kệ / giá bán / giá vốn          6 chương trình × 3 chuỗi

Đòn bẩy được phép / cấm      ──▶    Tính giá trị từng đòn bẩy    ──▶    alert() sinh ứng viên
(ràng buộc PHÁP LÝ)                 value_at_stake_vnd                  recommend() xếp hạng

Ngưỡng cảnh báo              ──▶    Kiểm tra tỷ lệ báo động giả  ──▶    config/thresholds.yaml
"−20% thì báo?"                     trên dữ liệu giả lập
```

**Quy tắc:** Business **không** sửa file `.py`. Data Science **không** tự đổi ngưỡng mà Business đã chốt.
Mọi thay đổi `config/*.yaml` đi qua pull request có review (đó là lý do nó nằm trong git, không phải trong code).

---

## Mốc thời gian đề xuất

| Khi nào | Ai | Việc | Đầu ra |
|---|---|---|---|
| **T−3 tuần** | 👔 | Chốt kinh tế đơn vị + điều khoản thương mại | §1, §2 của `02-task-business.md` |
| **T−3 tuần** | 👔 | Rà soát danh sách hành động được phép/cấm với pháp chế | `config/policy.yaml` được ký |
| **T−2 tuần** | 📊 | Dựng bộ sinh dữ liệu giả lập, verify ra đúng số Phụ lục B | `data/fixtures/*.csv` |
| **T−2 tuần** | 👔 + 📊 | Chốt ngưỡng cảnh báo, đo tỷ lệ báo động giả | `config/thresholds.yaml` |
| **T−1 tuần** | 📊 | Tính tay toàn bộ golden numbers cho ngày 3/4/5/7 | `05-demo-scenario-numbers.md` điền đủ |
| **T−1 tuần** | 👔 | Viết 30+ ca red-team (câu "dụ" agent đổi giá) | `tests/fixtures/redteam_cases.yaml` |
| **T−1 tuần** | Cả nhóm | Kiểm tra lại model Codex còn khả dụng (GPT-5.5 ngừng 14/10) | `06-open-questions.md` |
| **T−1 ngày** | Cả nhóm | Dry-run: đọc lại spec, phân công, chuẩn bị máy | — |
| **Ngày thi 10:00** | Cả nhóm | Gõ `AGENTS.md`, đẩy `config/` + `docs/` lên repo mới | — |

> ⏱️ **Nhắc:** chỉ có **7 giờ** để code. Mỗi câu hỏi nghiệp vụ chưa chốt trước đó sẽ tốn
> 15–30 phút tranh luận giữa buổi — tương đương mất 1 tính năng.

---

## Định nghĩa "xong" cho folder này

Trước ngày thi, folder này phải đạt:

- [ ] Mọi ô `⬜ CHƯA CHỐT` trong `02-task-business.md` và `03-task-data-science.md` đã thành `✅`
- [ ] `Business/templates/*.csv` đã được điền đủ và copy sang `data/fixtures/`
- [ ] `05-demo-scenario-numbers.md` khớp **tới từng đồng** với Phụ lục B của spec
- [ ] `06-open-questions.md` không còn câu hỏi nào gắn nhãn 🔴 CHẶN
- [ ] Bạn Business có thể giải thích miệng trong 60 giây: *vì sao agent không được giảm giá giữa chừng*
