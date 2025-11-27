-- ============================================
--  persons: 利用者 / 体験者 / 見学者
-- ============================================
CREATE TABLE persons (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  -- URLログイン用のトークン
  token CHAR(64) UNIQUE,
  -- 利用者区分
  -- visitor: 見学者（無料、1〜数日）
  -- trainee: 体験者（無料、数日〜数週間）
  -- normal : 通常利用者（294円負担）
  fee_category ENUM('visitor', 'trainee', 'normal') DEFAULT 'normal',
  ext1 VARCHAR(255) DEFAULT NULL,
  ext2 VARCHAR(255) DEFAULT NULL,
  is_deleted BOOLEAN DEFAULT FALSE,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
-- ============================================
--  meals: メニュー（開始在庫モデル）
-- ============================================
CREATE TABLE meals (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  category VARCHAR(100) DEFAULT NULL,
  vendor_item_id VARCHAR(20) DEFAULT NULL,
  -- 朝時点の在庫数
  initial_stock INT DEFAULT NULL,
  ext1 VARCHAR(255) DEFAULT NULL,
  ext2 VARCHAR(255) DEFAULT NULL,
  is_deleted BOOLEAN DEFAULT FALSE,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
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
  FOREIGN KEY (meal_id) REFERENCES meals(id)
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
  FOREIGN KEY (meal_id) REFERENCES meals(id)
);
-- ============================================
--  weekly_menus: 週間メニュー設定
-- ============================================
CREATE TABLE weekly_menus (
  id INT AUTO_INCREMENT PRIMARY KEY,
  start_date DATE NOT NULL,
  end_date DATE NOT NULL,
  meal_id INT NOT NULL,
  ext1 VARCHAR(255) DEFAULT NULL,
  ext2 VARCHAR(255) DEFAULT NULL,
  is_deleted BOOLEAN DEFAULT FALSE,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (meal_id) REFERENCES meals(id)
);