-- ============================================================
--  LTM 開発用ダミーデータ投入（強化版）
-- ============================================================
-- --------------------------
-- persons
-- --------------------------
INSERT IGNORE INTO persons (
    id,
    name,
    fee_category,
    ext1,
    ext2,
    token,
    is_deleted
  )
VALUES (1, '田中花子', 'normal', NULL, NULL, NULL, 0),
  (2, '田中太郎', 'normal', NULL, NULL, NULL, 0),
  (3, '佐藤大輔', 'trainee', NULL, NULL, NULL, 0),
  (4, '山本愛子', 'visitor', NULL, NULL, NULL, 0),
  (5, '鈴木誠', 'normal', NULL, NULL, NULL, 0),
  (6, '高橋美咲', 'normal', NULL, NULL, NULL, 0),
  (7, '加藤亮介', 'trainee', NULL, NULL, NULL, 0);
-- 合計 7 名（normal 4 / trainee 2 / visitor 1）
-- --------------------------
-- meals
-- --------------------------
INSERT IGNORE INTO meals (
    id,
    name,
    category,
    initial_stock,
    ext1,
    ext2,
    is_deleted
  )
VALUES (1, '生姜焼き弁当', 'メイン', NULL, NULL, NULL, 0),
  (2, 'ハンバーグ弁当', 'メイン', NULL, NULL, NULL, 0),
  (3, '唐揚げ弁当', 'メイン', NULL, NULL, NULL, 0),
  (4, '焼き魚弁当', 'メイン', NULL, NULL, NULL, 0);
-- 合計 4 メニュー
-- --------------------------
-- meal_logs（今日の日付 CURDATE()）
-- 同じメニューを複数人が選ぶケースも含める
-- --------------------------
INSERT IGNORE INTO meal_logs (
    id,
    person_id,
    meal_id,
    log_day,
    ext1,
    ext2,
    is_deleted
  )
VALUES -- ◎ 生姜焼き弁当（重複選択テスト）
  (1, 1, 1, CURDATE(), NULL, NULL, 0),
  -- 田中花子
  (2, 2, 1, CURDATE(), NULL, NULL, 0),
  -- 田中太郎
  -- ◎ ハンバーグ弁当
  (3, 3, 2, CURDATE(), NULL, NULL, 0),
  -- 佐藤大輔（trainee）
  -- ◎ 唐揚げ弁当
  (4, 4, 3, CURDATE(), NULL, NULL, 0),
  -- 山本愛子（visitor）
  (5, 5, 3, CURDATE(), NULL, NULL, 0),
  -- 鈴木誠
  -- ◎ 焼き魚弁当（1人）
  (6, 6, 4, CURDATE(), NULL, NULL, 0);
-- 高橋美咲
-- ※ 加藤亮介（person_id = 7）は今日の選択なし
--   → 「未回答者リスト today_unanswered」テスト用
-- --------------------------
-- supplies（必要なら後で）
-- --------------------------
-- INSERT IGNORE INTO supplies (...);