# 💬 Prompt mẫu cho Codex

Khuôn chuẩn theo hướng dẫn của OpenAI: **Goal / Context / Constraints / Done when**.
Nhắc file bằng `@`. Lập kế hoạch trước khi việc còn mơ hồ. Yêu cầu viết test.
**Giữ mỗi task trong khoảng 1 giờ làm việc.**

> Prompt viết bằng **tiếng Anh** để Codex hiểu chính xác nhất.

---

## Vai trò A — Engine chỉ số

```text
Goal: implement the evaluate stage.
Context: @docs/roi-methodology.md sections 1-7, @src/midflight/snapshot.py,
         @tests/test_evaluate_golden.py.
Constraints: aggregations in DuckDB SQL; public surface is evaluate(as_of) and the CLI command only;
         money as integer VND; do not modify expected values in the golden test.
Done when: uv run pytest tests/test_evaluate_golden.py passes and ruff is clean.
```

## Vai trò A — Luật cảnh báo + hành động ứng viên

```text
Goal: implement the alert stage: rules, suppression, candidate actions, snapshot sealing.
Context: @docs/roi-methodology.md sections 8-9, @config/thresholds.yaml, @config/policy.yaml,
         @src/midflight/snapshot.py, @tests/test_alert.py.
Constraints: every threshold is READ FROM config/thresholds.yaml - never hard-code a number;
         suppression must block ROI alerts when store coverage < min_store_coverage;
         reallocation candidates must respect config/policy.yaml reallocation rules;
         snapshots are append-only, never overwrite.
Done when: uv run pytest tests/test_alert.py passes and snapshot content hash is stable across reruns.
```

## Vai trò B — Rào chắn agent

```text
Goal: make recommend() reject unsafe or ungrounded LLM output.
Context: @src/midflight/recommend.py, @config/policy.yaml,
         @tests/test_recommend_guardrails.py, spec Appendix D.
Constraints: validator checks candidate ids, evidence paths, no digits outside {{placeholders}},
         EN/VI forbidden-intent patterns; one retry, then template fallback; no network in tests.
Done when: all 30 red-team cases pass offline and the fallback path is covered.
```

## Vai trò D — Dữ liệu giả lập

```text
Goal: seeded generator for the six-promotion scenario in spec section 3.5
      (P-03: stockouts from day 3 in 27 stores, 9 stores without the promo price;
       P-05: secondary-display split 20/20).
Constraints: deterministic with --seed; 56-day clean pre-period;
         writes the CSVs in docs/data-dictionary.md.
Done when: midflight generate --seed 7 && midflight ingest reports only the intentionally
         injected issues.
```

## Vai trò C — Dashboard

```text
Goal: build the promotion detail screen.
Context: @src/midflight/dashboard.py, @src/midflight/snapshot.py,
         a fixture snapshot at @tests/fixtures/snapshot_P-03_2026-10-07.json.
Constraints: the dashboard READS the snapshot only - it must NEVER recompute a metric;
         store grid coloured by issue (stockout / price / normal);
         include the "What we are not changing" box.
Done when: streamlit AppTest smoke test passes and every number on screen traces to a snapshot field.
```

---

## 🤖 Kiểm tra lệch phương pháp — Codex làm NGƯỜI KIỂM

```bash
codex exec --output-schema .codex/drift.schema.json -o drift.json \
  "Compare docs/roi-methodology.md with src/midflight/evaluate.py and src/midflight/alert.py. \
   List every formula or threshold that differs, with file and line."
```

CI **báo lỗi** nếu `drift.json` liệt kê bất kỳ điểm lệch nào.
→ Đây là cách cho giám khảo thấy Codex **kiểm tra** sản phẩm, chứ không chỉ viết code.

## Review cục bộ trước khi merge

```bash
codex review --uncommitted      # trước commit
codex review --base main        # trước khi merge luồng việc
```
