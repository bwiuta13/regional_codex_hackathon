# TODO(D-data): hoàn thiện trong ngày thi. Mục tiêu: `make demo` chạy OFFLINE bằng một lệnh.
.PHONY: demo test lint drift clean help

help:
	@echo "make demo   - chạy toàn bộ pipeline rồi mở dashboard (offline được)"
	@echo "make test   - uv run pytest -q"
	@echo "make lint   - ruff check + format"
	@echo "make drift  - Codex kiểm tra code có còn khớp docs/roi-methodology.md không"

# Pipeline đầy đủ. recommend() gọi LLM thật nếu có OPENAI_API_KEY,
# ngược lại dùng tests/recordings/ rồi tới mẫu câu dự phòng -> DEMO KHÔNG BAO GIỜ CHẾT VÌ MẠNG.
demo:
	uv sync
	uv run midflight generate --seed 7
	uv run midflight ingest
	uv run midflight evaluate --as-of 2026-10-07
	uv run midflight alert --as-of 2026-10-07
	uv run midflight recommend --as-of 2026-10-07
	uv run streamlit run src/midflight/dashboard.py

test:
	uv run pytest -q

lint:
	uv run ruff check . && uv run ruff format .

# Codex làm NGƯỜI KIỂM: so khớp tài liệu phương pháp với code.
# CI báo lỗi nếu drift.json liệt kê bất kỳ điểm lệch nào.
drift:
	codex exec --output-schema .codex/drift.schema.json -o drift.json \
	  "Compare docs/roi-methodology.md with src/midflight/evaluate.py and src/midflight/alert.py. \
	   List every formula or threshold that differs, with file and line."

clean:
	rm -rf data/*.csv data/*.duckdb data/dq_report.json drift.json
