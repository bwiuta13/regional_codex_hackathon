# MidFlight — AI Agent giám sát ROI khuyến mãi thương mại khi chương trình đang chạy

> Repo của nhóm cho **Sea x OpenAI Codex Hackathon – Vietnam** (31/10/2026, 10:00–17:00, 7 giờ code).
>
> Đặc tả thiết kế đầy đủ: [`docs/superpowers/specs/2026-09-27-midflight-trade-promo-agent-design.vi.md`](docs/superpowers/specs/2026-09-27-midflight-trade-promo-agent-design.vi.md)
> (bản tiếng Anh: [`...-design.md`](docs/superpowers/specs/2026-09-27-midflight-trade-promo-agent-design.md))

---

## ⚠️ Đọc trước khi chạm vào repo

Luật hackathon: **"All building must take place on the day"** — không nộp code dựng sẵn.

Vì vậy **toàn bộ file `.py` trong repo này là KHUNG RỖNG**: chỉ có docstring, chữ ký hàm,
và comment `TODO(...)`. Mọi thân hàm đều `raise NotImplementedError`. Không có logic nghiệp vụ nào
được viết trước ngày thi.

| Loại file | Trạng thái | Ngày thi làm gì |
|---|---|---|
| `docs/**`, `Business/**` | ✅ Tài liệu — được phép mang theo | Đọc, không cần gõ lại |
| `config/*.yaml` | ✅ Tham số nghiệp vụ (là tài liệu) | Đọc lại, chốt số với Business |
| `src/**/*.py`, `tests/**/*.py` | ⚠️ Khung + TODO, chưa có logic | **Codex sinh implementation từ TODO trong ngày** |
| `docs/codex/AGENTS.draft.md` | ⚠️ Bản nháp | **Gõ lại thành `AGENTS.md` ở thư mục gốc lúc 10:00–10:30** |

> ❓ Còn một câu hỏi mở cho ban tổ chức: `AGENTS.md` soạn sẵn có bị coi là "pre-built" không?
> Xem [`Business/06-open-questions.md`](Business/06-open-questions.md). Cách an toàn: gõ lại trong 30 phút đầu.

---

## MidFlight làm gì

Mỗi sáng, lấy dữ liệu POS của ngày hôm trước + sổ cái chi phí trade, rồi trả lời 3 câu hỏi
**khi chương trình vẫn còn đang chạy**:

1. **Chương trình này có hoàn vốn không?** → ROI lũy kế vs kế hoạch + dự phóng cuối kỳ.
2. **Nếu không, vì sao?** → tách nguyên nhân *cấu trúc* (chiết khấu trợ giá cho doanh số nền)
   khỏi nguyên nhân *thực thi có thể khắc phục* (hết hàng, không áp giá khuyến mãi, thiếu dữ liệu).
3. **Còn làm được gì?** → chỉ đề xuất trong **danh sách đóng** các đòn bẩy công ty còn kiểm soát.
   **Không bao giờ** đụng tới giá, mức chiết khấu, hay ngày chạy đã cam kết (luật Việt Nam, §2.5 spec).

**Pitch 1 câu:** hôm nay tín hiệu đáng tin đầu tiên về một chương trình thất bại chỉ đến sau khi nó
kết thúc 30–45 ngày. MidFlight đưa tín hiệu đó từ **ngày 4–5 của chương trình 21 ngày**.

---

## Bản đồ repo

```
.
├── Business/              👔 Task cho bạn Business + bạn Data Science (ĐỌC ĐẦU TIÊN)
│   ├── 01-business-context.md       nghiệp vụ tóm tắt, không cần đọc hết 1441 dòng spec
│   ├── 02-task-business.md          checklist Business phải chốt gì, hạn nào
│   ├── 03-task-data-science.md      checklist DS phải dựng gì, verify bằng cách nào
│   ├── 04-data-requirements.md      hợp đồng dữ liệu: bảng, cột, nguồn, ai cung cấp
│   ├── 05-demo-scenario-numbers.md  số liệu chuẩn cho kịch bản demo P-03 / P-05
│   ├── 06-open-questions.md         câu hỏi chặn, cần người quyết
│   └── templates/                   CSV mẫu có header để điền
│
├── config/                ⚙️ Tham số do Trade Marketing SỞ HỮU (đổi qua PR có review)
│   ├── thresholds.yaml              ngưỡng cảnh báo
│   └── policy.yaml                  danh sách hành động đóng + luật phân bổ lại
│
├── docs/                  📚 Tài liệu nguồn — con người sở hữu, Codex chỉ đọc
│   ├── roi-methodology.md           CÔNG THỨC (nguồn sự thật cho evaluate.py)
│   ├── data-dictionary.md           từ điển dữ liệu
│   ├── codex/                       AGENTS.draft.md, prompt mẫu, CODEX_LOG.md
│   └── superpowers/specs/           đặc tả thiết kế gốc
│
├── src/midflight/         🐍 Code — mỗi giai đoạn 1 file, mỗi file 1 entry point
│   ├── cli.py                       lệnh Typer = các giai đoạn pipeline
│   ├── mockdata.py   →  generate()  bộ sinh dữ liệu có seed
│   ├── ingest.py     →  ingest()    đọc · kiểm tra · nạp DuckDB
│   ├── schema.sql                   DDL
│   ├── evaluate.py   →  evaluate()  baseline · lift · iGP · chi phí · ROI · dự phóng
│   ├── alert.py      →  alert()     luật · chặn · hành động ứng viên · niêm phong snapshot
│   ├── snapshot.py                  HỢP ĐỒNG Pydantic (mọi giai đoạn dùng chung)
│   ├── recommend.py  →  recommend() prompt · LLM · validator · renderer · dự phòng
│   ├── dossier.py    →  render_dossier()
│   └── dashboard.py                 Streamlit
│
├── data/                  📥 CSV sinh ra (git-ignored) + data/fixtures (commit)
├── snapshots/             🔒 Đầu ra BẤT BIẾN theo ngày chốt — không bao giờ ghi đè
└── tests/                 ✅ Golden test + test rào chắn (viết TRƯỚC, Codex làm cho pass)
```

---

## Pipeline

```
generate → ingest → evaluate → alert → recommend → dashboard
                                  ↓
                        snapshots/<as_of>/<promo>.json   ← điểm bàn giao DUY NHẤT, bất biến
```

Mỗi giai đoạn đọc **đầu ra đã lưu** của giai đoạn trước và có **đúng một lệnh CLI** làm điểm vào.
Dashboard và agent cùng đọc một snapshot, nên những gì người dùng thấy và agent nói **không thể lệch nhau**.

## Chạy (sau khi implement xong trong ngày thi)

```bash
make demo        # uv sync → generate → ingest → evaluate → alert → recommend → dashboard
make test        # uv run pytest -q
make lint        # uv run ruff check . && uv run ruff format .
make drift       # Codex kiểm tra code có còn khớp docs/roi-methodology.md không
```

## Luật vàng của nhóm (chi tiết ở `docs/codex/AGENTS.draft.md`)

1. **Số liệu do code tính.** LLM không bao giờ tính hay gõ một con số nào.
2. **Đổi công thức = sửa `docs/roi-methodology.md` + golden test + `schema_version`, trong cùng 1 PR.**
   Không bao giờ sửa giá trị kỳ vọng trong golden test để test pass — hỏi người.
3. **Agent chỉ dùng hành động có trong `config/policy.yaml`.** Không bao giờ thêm nhánh code
   đổi giá, mức chiết khấu, tỷ lệ scan rebate, ngày chạy hay điều khoản nhà bán lẻ.
4. **Snapshot bất biến.** Không bao giờ ghi đè.
5. **Không tách hàm chỉ dùng 1 lần, và không bao giờ tách hàm chỉ để test gọi được.**
   Test đi qua điểm vào của giai đoạn (`ingest`, `evaluate`, `alert`, `recommend`, CLI).
6. **Test không bao giờ chạm mạng.** Gọi LLM đi qua client inject được; test dùng `tests/recordings/`.

## Phân công (§6.5 spec)

| Vai trò | Sở hữu file | Tag TODO để grep |
|---|---|---|
| **A** — Dữ liệu & chỉ số | `evaluate.py`, `schema.sql`, `test_evaluate_golden.py`, `docs/roi-methodology.md` | `TODO(A-metrics)` |
| **B** — Agent & rào chắn | `snapshot.py`, `recommend.py`, `test_recommend_guardrails.py`, `tests/recordings/` | `TODO(B-agent)` |
| **C** — Dashboard & demo | `dashboard.py`, `dossier.py`, kịch bản demo | `TODO(C-ui)` |
| **D** — Dữ liệu, tích hợp & pitch | `mockdata.py`, `ingest.py`, `alert.py` (cùng A), `Makefile`, CI, `CODEX_LOG.md` | `TODO(D-data)` |

```bash
grep -rn "TODO(A-metrics)" src tests    # xem hết việc của vai trò A
grep -rn "TODO(" src tests config | wc -l
```
