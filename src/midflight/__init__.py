"""MidFlight — AI agent giám sát ROI khuyến mãi thương mại khi chương trình đang chạy.

Pipeline: generate -> ingest -> evaluate -> alert -> recommend -> dashboard

Nguyên tắc nền: SỐ LIỆU DO CODE TÍNH, KHÔNG DO LLM TẠO RA.
LLM chỉ chọn trong các hành động engine đã tính sẵn và giải thích chúng bằng placeholder.

Xem docs/roi-methodology.md (công thức) và config/policy.yaml (hành động được phép).
"""

__version__ = "0.1.0"
