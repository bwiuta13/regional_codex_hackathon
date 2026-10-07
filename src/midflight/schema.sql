-- =============================================================================
-- src/midflight/schema.sql — DDL cho DuckDB
-- -----------------------------------------------------------------------------
-- PHẢI khớp docs/data-dictionary.md. Lệch nhau -> ingest() sẽ bắt được khi kiểm tra kiểu.
--
-- Quy ước: tiền = BIGINT, SỐ NGUYÊN VND. Không dùng DOUBLE cho tiền ở bất kỳ đâu.
--          Tỷ lệ (discount_pct, lift, roi, share) dùng DOUBLE.
--
-- Vai trò A sở hữu file này.
-- =============================================================================

-- TODO(A-metrics): bảng pos_daily
--   date DATE, retailer_id TEXT, store_id TEXT, sku_id TEXT,
--   units INTEGER,                 -- CÓ THỂ ÂM (hàng trả lại) -> không đặt CHECK >= 0
--   net_sales_vnd BIGINT,
--   regular_price_vnd BIGINT,
--   on_hand_units INTEGER,         -- NULL được; KHÔNG ĐÁNG TIN, không dùng để phát hiện hết hàng
--   source_file TEXT, ingested_at TIMESTAMP
--   -- khóa logic: (date, store_id, sku_id). DuckDB không bắt buộc PK, nhưng ingest() phải khử trùng lặp.

-- TODO(A-metrics): bảng promotions
--   promo_id TEXT PRIMARY KEY, retailer_id TEXT, brand TEXT,
--   promo_name TEXT,               -- ⚠️ VĂN BẢN KHÔNG ĐÁNG TIN (prompt injection surface)
--   mechanic TEXT,                 -- MVP: chỉ 'PCT_OFF'
--   discount_pct DOUBLE, mfr_funding_share DOUBLE,
--   start_date DATE, end_date DATE,     -- TÍNH CẢ HAI ĐẦU (inclusive)
--   planned_lift DOUBLE, target_roi DOUBLE,
--   fund_pool_id TEXT, status TEXT

-- TODO(A-metrics): bảng promotion_scope
--   promo_id TEXT, store_id TEXT, sku_id TEXT,
--   has_secondary_display BOOLEAN,  -- ⭐ cờ đòn bẩy -> nhóm so sánh TRONG chương trình
--   has_pg BOOLEAN                  -- ⭐ cờ đòn bẩy
--   -- Đây là MẪU SỐ để tính độ phủ.

-- TODO(A-metrics): bảng trade_spend_ledger
--   entry_id TEXT PRIMARY KEY, promo_id TEXT, fund_pool_id TEXT,
--   spend_type TEXT,    -- SCAN_REBATE | DISPLAY_FEE | LISTING_FEE | MDF_PG | MDF_SAMPLING
--                       -- | MDF_SECONDARY_DISPLAY | MDF_OTHER
--   commitment TEXT,    -- 🔑 RETAILER_COMMITTED | INTERNAL_COMMITTED | UNCOMMITTED
--   status TEXT,        -- PLANNED | ACCRUED | PAID
--   amount_vnd BIGINT,
--   period_start DATE, period_end DATE,
--   commit_deadline DATE,   -- NULL được; BẮT BUỘC với UNCOMMITTED
--   counterparty TEXT

-- TODO(A-metrics): bảng sku_master
--   sku_id TEXT PRIMARY KEY, brand TEXT, category TEXT, pack TEXT,
--   regular_price_vnd BIGINT, net_price_to_retailer_vnd BIGINT, unit_cogs_vnd BIGINT
--   -- 🔒 unit_cogs_vnd là DỮ LIỆU MẬT. Nếu không công bố được, thay bằng unit_margin_vnd.

-- TODO(A-metrics): bảng store_master
--   store_id TEXT PRIMARY KEY, retailer_id TEXT, format TEXT, region TEXT,
--   open_date DATE, close_date DATE
--   -- ⚠️ open_date/close_date dùng để LOẠI cửa hàng khỏi mẫu số độ phủ.

-- TODO(D-data): bảng dq_quarantine — dòng bị cách ly khi ingest
--   source_table TEXT, raw_line TEXT, reason TEXT, ingested_at TIMESTAMP
--   -- Cách ly chứ không bỏ im lặng: người dùng phải thấy được mình mất gì.

-- TODO(A-metrics): các VIEW/CTE trung gian đặt tên ĐÚNG NHƯ trong docs/roi-methodology.md
--   (clean_days, dow_index, base_level, baseline_daily, incremental, igp,
--    variable_spend, fixed_spend, discretionary_spend, roi_to_date, ...)
--   Một CTE cho một khái niệm -> review được, và make drift so khớp được với tài liệu.
