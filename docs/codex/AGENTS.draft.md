# ⚠️ BẢN NHÁP — gõ lại thành `/AGENTS.md` lúc 10:00 ngày thi

> **File này KHÔNG phải `AGENTS.md`.** Nó là bản nháp để **gõ lại** vào thư mục gốc repo trong
> 30 phút đầu ngày thi, nhằm tuân thủ luật *"All building must take place on the day"*.
>
> ❓ Xem `Business/06-open-questions.md` **Q1** — cần hỏi ban tổ chức xem `AGENTS.md`
> soạn sẵn có bị coi là "pre-built" không. Cách an toàn: gõ lại.
>
> 📝 Giữ nguyên **tiếng Anh** vì đây là file Codex đọc.

---

```markdown
# AGENTS.md — MidFlight
In-flight trade promotion ROI agent. Pipeline: ingest → evaluate → alert → recommend → dashboard.
Specs: docs/roi-methodology.md (formulas), docs/data-dictionary.md, config/*.yaml.

## Golden rules
1. Numbers come from code. No LLM computes or invents a metric. Code must match docs/roi-methodology.md.
2. A formula change = methodology doc + tests/test_evaluate_golden.py + snapshot schema_version, in one PR.
   Never edit expected values in golden tests to make a test pass; ask a human.
3. The agent may only use actions listed in config/policy.yaml. Never add a code path that changes
   price, discount depth, scan-rebate rate, promotion dates or retailer terms.
4. Snapshots under snapshots/ are immutable. Never overwrite one.
5. Do not extract a function that is used in only one place, and never split a function just so a test
   can call it. Test through the stage entry points (ingest, evaluate, alert, recommend, CLI).
6. Tests never touch the network. LLM calls go through the injectable client; tests use tests/recordings/.

## Commands
- Setup: `uv sync` · Tests: `uv run pytest -q` · Lint: `uv run ruff check . && uv run ruff format .`
- Demo (offline): `make demo`

## Conventions
Python 3.12, type hints, Pydantic v2 frozen models for contracts. Money = integer VND.
Metric SQL in DuckDB, one CTE per concept, named as in the methodology doc.

## Done when
`uv run pytest -q` passes, ruff is clean and `make demo` runs offline.

## Code Review Rules
- Flag any metric change without matching methodology and golden-test changes.
- Flag any new action type, or any text path that could suggest changing committed pricing or terms.
- Flag digits typed into LLM narrative templates (numbers must be placeholders).
```

---

## Ghi chú về luật 5

Luật 5 mang **quy ước code của nhóm**: không tách hàm chỉ dùng một lần, không tách hàm chỉ để test gọi được.

Nhờ đó Codex **không băm nhỏ các module giai đoạn** thành những mảnh khó review trong 7 giờ.
Mỗi file giai đoạn (`ingest.py`, `evaluate.py`, `alert.py`, `recommend.py`) có **đúng một entry point công khai**,
và test đi qua entry point đó.
