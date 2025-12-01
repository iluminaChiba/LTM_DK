-- ============================================
--  persons: 利用者 / 体験者 / 見学者
-- ============================================
CREATE TABLE persons (
  id INT AUTO_INCREMENT PRIMARY KEY,
  person_name VARCHAR(255) NOT NULL,
  furigana VARCHAR(255) NOT NULL,
  -- URLログイン用のトークン
  token CHAR(64) UNIQUE,
  -- 利用者区分
  -- visitor: 見学者（無料、1〜数日）
  -- trainee: 体験者（無料、数日〜数週間）
  -- normal : 通常利用者（294円負担）
  fee_category ENUM('visitor', 'trainee', 'normal') DEFAULT 'normal',
  is_present BOOLEAN DEFAULT FALSE,
  ext1 VARCHAR(255) DEFAULT NULL,
  ext2 VARCHAR(255) DEFAULT NULL,
  is_deleted BOOLEAN DEFAULT FALSE,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_persons_furigana(furigana)
);
-- ============================================
--  meals: 食事メニュー
-- ============================================
CREATE TABLE meals (
  meal_id INT NOT NULL PRIMARY KEY,
  meal_name VARCHAR(255) NOT NULL,
  furigana VARCHAR(255) NOT NULL,
  side1 VARCHAR(255) DEFAULT NULL,
  side2 VARCHAR(255) DEFAULT NULL,
  side3 VARCHAR(255) DEFAULT NULL,
  kcal DECIMAL(6, 1) DEFAULT NULL,
  protein DECIMAL(6, 1) DEFAULT NULL,
  fat DECIMAL(6, 1) DEFAULT NULL,
  carb DECIMAL(6, 1) DEFAULT NULL,
  salt DECIMAL(6, 1) DEFAULT NULL,
  ext1 VARCHAR(255) DEFAULT NULL,
  ext2 VARCHAR(255) DEFAULT NULL,
  is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_meals_furigana(furigana)
);
-- ============================================
--  allergies: アレルギー情報
-- ============================================
CREATE TABLE allergies (
  meal_id INT NOT NULL,
  egg TINYINT(1) NOT NULL DEFAULT 0,
  milk TINYINT(1) NOT NULL DEFAULT 0,
  wheat TINYINT(1) NOT NULL DEFAULT 0,
  soba TINYINT(1) NOT NULL DEFAULT 0,
  peanut TINYINT(1) NOT NULL DEFAULT 0,
  shrimp TINYINT(1) NOT NULL DEFAULT 0,
  crab TINYINT(1) NOT NULL DEFAULT 0,
  walnut TINYINT(1) NOT NULL DEFAULT 0,
  abalone TINYINT(1) NOT NULL DEFAULT 0,
  squid TINYINT(1) NOT NULL DEFAULT 0,
  salmon_roe TINYINT(1) NOT NULL DEFAULT 0,
  salmon TINYINT(1) NOT NULL DEFAULT 0,
  mackerel TINYINT(1) NOT NULL DEFAULT 0,
  seafood TINYINT(1) NOT NULL DEFAULT 0,
  beef TINYINT(1) NOT NULL DEFAULT 0,
  chicken TINYINT(1) NOT NULL DEFAULT 0,
  pork TINYINT(1) NOT NULL DEFAULT 0,
  orange TINYINT(1) NOT NULL DEFAULT 0,
  kiwi TINYINT(1) NOT NULL DEFAULT 0,
  apple TINYINT(1) NOT NULL DEFAULT 0,
  peach TINYINT(1) NOT NULL DEFAULT 0,
  banana TINYINT(1) NOT NULL DEFAULT 0,
  soy TINYINT(1) NOT NULL DEFAULT 0,
  cashew TINYINT(1) NOT NULL DEFAULT 0,
  almond TINYINT(1) NOT NULL DEFAULT 0,
  macadamia TINYINT(1) NOT NULL DEFAULT 0,
  yam TINYINT(1) NOT NULL DEFAULT 0,
  sesame TINYINT(1) NOT NULL DEFAULT 0,
  gelatin TINYINT(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (meal_id),
  CONSTRAINT fk_allergies_meal FOREIGN KEY (meal_id) REFERENCES meals(meal_id) ON DELETE CASCADE
);
-- ============================================
--  pending_box: 食パック発注の仮登録テーブル
-- ============================================
CREATE TABLE pending_box (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  meal_id VARCHAR(10) NOT NULL,
  meal_name VARCHAR(255) NULL,
  qty INT UNSIGNED NOT NULL,
  arrival_date DATE NOT NULL,
  applicable_date DATE NOT NULL,
  source_filename VARCHAR(255) NULL,
  excel_row INT UNSIGNED NOT NULL,
  status ENUM('pending', 'applied') NOT NULL DEFAULT 'pending',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_pending_meal_id (meal_id)
);
-- ============================================
--  supplies: 入庫履歴（将来拡張用）
-- ============================================
CREATE TABLE supplies (
  id INT AUTO_INCREMENT PRIMARY KEY,
  meal_id INT NOT NULL,
  quantity INT NOT NULL,
  supplied_at DATE NOT NULL,
  ext1 VARCHAR(255) DEFAULT NULL,
  ext2 VARCHAR(255) DEFAULT NULL,
  is_deleted BOOLEAN DEFAULT FALSE,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (meal_id) REFERENCES meals(meal_id)
);
-- ============================================
--  meal_logs: 食事選択／提供ログ
-- ============================================
CREATE TABLE meal_logs (
  id INT AUTO_INCREMENT PRIMARY KEY,
  person_id INT NOT NULL,
  meal_id INT NOT NULL,
  log_day DATE NOT NULL,
  ext1 VARCHAR(255) DEFAULT NULL,
  ext2 VARCHAR(255) DEFAULT NULL,
  is_deleted BOOLEAN DEFAULT FALSE,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  -- 同じ人が同じ日に複数登録されないようにする
  UNIQUE(person_id, log_day),
  FOREIGN KEY (person_id) REFERENCES persons(id),
  FOREIGN KEY (meal_id) REFERENCES meals(meal_id)
);
-- ============================================
--  weekly_menus: 週間メニュー設定
-- ============================================
CREATE TABLE weekly_menus (
  id INT AUTO_INCREMENT PRIMARY KEY,
  week_start DATE NOT NULL,
  meal_id INT NOT NULL,
  ext1 VARCHAR(255) DEFAULT NULL,
  ext2 VARCHAR(255) DEFAULT NULL,
  is_deleted BOOLEAN DEFAULT FALSE,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE(week_start, meal_id),
  FOREIGN KEY (meal_id) REFERENCES meals(meal_id)
);