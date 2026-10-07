# 📥 data/ — dữ liệu đầu vào

| Thư mục | Nội dung | Git |
|---|---|---|
| `data/*.csv` | CSV sinh bởi `midflight generate --seed 7` | ❌ **git-ignored** |
| `data/fixtures/` | Tập dữ liệu nhỏ, cố định, cho test | ✅ **commit** |
| `data/midflight.duckdb` | DB sinh bởi `midflight ingest` | ❌ git-ignored |
| `data/dq_report.json` | Báo cáo chất lượng dữ liệu | ❌ git-ignored |

## Vì sao git-ignore

Dữ liệu sinh ra **tất định theo seed** — commit nó chỉ làm repo nặng. Cần dựng lại:

```bash
midflight generate --seed 7
midflight ingest
```

## Đặc tả

- Cột và kiểu: [`docs/data-dictionary.md`](../docs/data-dictionary.md)
- Nghiệp vụ & nguồn: [`Business/04-data-requirements.md`](../Business/04-data-requirements.md)
- Kịch bản cần sinh: [`Business/03-task-data-science.md`](../Business/03-task-data-science.md) §10

> ⚠️ **Tiêu chí xong của bộ sinh:** `midflight generate --seed 7 && midflight ingest`
> báo cáo DQ **chỉ liệt kê đúng các vấn đề cố tình cài** — không có vấn đề lạ.
